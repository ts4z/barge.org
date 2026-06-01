#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.32",
#     "openpyxl>=3.1",
#     "PyYAML>=6.0",
# ]
# ///
"""
One-shot poll of a Zeffy campaign's guest list.

Reads scripts/cookies.json (produced by zeffy_login.py), hits the Zeffy
internal export endpoint for the named campaign, decodes the returned XLSX,
and writes a Hugo data file in the form:

    last_updated: "2026-06-01 17:30 UTC"
    registrations:
      - full_name: ...
        ticket: 1
        nickname: ...

Run zeffy_login.py first to capture cookies.

Usage:
    uv run scripts/zeffy_poll.py --campaign <UUID> --output <PATH>
    uv run scripts/zeffy_poll.py --campaign <UUID> --output <PATH> --dry-run
"""

import argparse
import base64
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
import openpyxl
import yaml

ENDPOINT = "https://api.zeffy.com/_new/trpc/exportGuestList"

SCRIPT_DIR = Path(__file__).parent
COOKIES_PATH = SCRIPT_DIR / "cookies.json"


def build_body(campaign_id: str) -> dict:
    return {
        "occurrenceIds": [],
        "ticketingId": campaign_id,
        "filters": {
            "searchFilter": "",
            "statusFilter": [],
            "rateFilter": [],
            "answerFilter": [],
        },
        "exportParameters": {
            "locale": "EN",
            "timezone": "America/Los_Angeles",
        },
        "exportFileType": "Excel",
        "columnsSelection": {
            "selectedColumns": ["guestName", "buyerName", "ticketNumber",
                                "customQuestions"],
        },
    }


def load_session() -> requests.Session:
    if not COOKIES_PATH.exists():
        sys.exit(f"No cookies at {COOKIES_PATH}.  Run zeffy_login.py first.")
    session = requests.Session()
    for c in json.loads(COOKIES_PATH.read_text()):
        session.cookies.set(c["name"], c["value"], domain=c.get("domain"))
    return session


def fetch_xlsx_bytes(session: requests.Session, campaign_id: str) -> bytes:
    resp = session.post(
        ENDPOINT,
        json=build_body(campaign_id),
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    if resp.status_code in (401, 403):
        sys.exit("Auth failed (HTTP %d).  Re-run zeffy_login.py." % resp.status_code)
    resp.raise_for_status()
    payload = resp.json()
    try:
        b64 = payload["result"]["data"]["data"]["export"]
    except (KeyError, TypeError):
        sys.exit(f"Unexpected response shape: {json.dumps(payload)[:500]}")
    return base64.b64decode(b64)


def parse_ticket_number(s: str) -> int | None:
    # Zeffy returns either bare digits ("13") or "#13 General Admission"
    # depending on the campaign's ticket-type setup.  Take the first run of
    # digits, optionally preceded by '#'.
    m = re.search(r"#?\s*(\d+)", s or "")
    return int(m.group(1)) if m else None


def parse_workbook(xlsx_bytes: bytes, debug: bool = False) -> list[dict]:
    wb = openpyxl.load_workbook(io.BytesIO(xlsx_bytes), read_only=True, data_only=True)
    if debug:
        print(f"  sheets: {wb.sheetnames}")
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if debug:
        print(f"  raw row count: {len(rows)}")
        for i, r in enumerate(rows[:5]):
            print(f"  row[{i}]: {r}")
    if not rows:
        return []

    header = [str(c).strip().lower() if c else "" for c in rows[0]]
    if debug:
        print(f"  header: {header}")

    def find_col(*candidates: str) -> int | None:
        for cand in candidates:
            for i, h in enumerate(header):
                if cand in h:
                    return i
        return None

    # Column-preference order for the displayed name:
    #   "Name For Badge"  — custom question, used by campaigns where one
    #                       buyer can register multiple attendees (BARGE).
    #   "Guest name"      — Zeffy's built-in column (populated when each
    #                       ticket has its own guest profile; e.g. ATLARGE).
    #   "Buyer name"      — last-resort fallback.
    badge_col = find_col("name for badge", "badge name")
    guest_col = find_col("guest")
    buyer_col = find_col("buyer")
    ticket_col = find_col("ticket")
    notes_col = find_col("nickname", "questions", "notes")

    if ticket_col is None or (badge_col is None and guest_col is None
                              and buyer_col is None):
        sys.exit(f"Could not find name/ticket columns in header: {header}")

    def cell(row: tuple, idx: int | None) -> str:
        # openpyxl read-only mode truncates trailing Nones, so a row may be
        # shorter than the header.  Treat missing/None as empty.
        if idx is None or idx >= len(row) or row[idx] is None:
            return ""
        return str(row[idx]).strip()

    out: list[dict] = []
    for r in rows[1:]:
        if not r or all(c is None for c in r):
            continue
        full_name = (cell(r, badge_col) or cell(r, guest_col)
                     or cell(r, buyer_col))
        if not full_name:
            continue
        ticket_num = parse_ticket_number(cell(r, ticket_col))
        nickname = cell(r, notes_col)
        out.append({
            "full_name": full_name,
            "ticket": ticket_num,
            "nickname": nickname,
        })

    out.sort(key=lambda r: (r["ticket"] is None, r["ticket"] or 0))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", required=True,
                    help="Zeffy campaign ID (the formId in the campaign URL).")
    ap.add_argument("--output", required=True, type=Path,
                    help="Path to the Hugo data YAML file to write.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print parsed rows, do not write the data file.")
    args = ap.parse_args()

    session = load_session()
    xlsx_bytes = fetch_xlsx_bytes(session, args.campaign)

    raw_path = SCRIPT_DIR / "last_export.xlsx"
    raw_path.write_bytes(xlsx_bytes)
    print(f"Wrote raw export to {raw_path} ({len(xlsx_bytes)} bytes).")

    rows = parse_workbook(xlsx_bytes, debug=args.dry_run)

    if not rows:
        sys.exit("Parsed 0 rows.  Refusing to clobber data file.  "
                 "Check cookies and campaign id.")

    print(f"Parsed {len(rows)} row(s).")

    if args.dry_run:
        for r in rows:
            print(f"  #{r['ticket']!s:>4}  {r['full_name']!r:<40}  "
                  f"nick={r['nickname']!r}")
        return 0

    payload = {
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "registrations": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)
    )
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
