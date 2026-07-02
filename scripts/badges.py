#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.32",
#     "openpyxl>=3.1",
#     "PyYAML>=6.0",
#     "reportlab>=4.0",
# ]
# ///
"""
BARGE 2026 badge pipeline — round 1: canonical attendee list.

Fetches the current Zeffy guest list (or reads a saved XLSX), collapses
multi-purchase rows into one row per attendee, keeps the extra fields
badges need (last name, hometown / city+state), and emits:

  1. A canonical CSV to --output (default scripts/badges_canonical.csv)
     — one row per attendee, ordered by their earliest ticket number.
  2. A validation report to stdout — missing nicknames, duplicate
     nicknames across different people, likely overflow risks, and a
     list of attendees missing a hometown value.

Round 2 will consume the same canonical list to render Avery 74459
PDFs, but that's not built yet.

Reuses the Zeffy client from zeffy_poll.py — same cookies, same
Cloudflare-friendly HTTP headers, same XLSX endpoint.  Unlike the
poller this tool keeps "Name For Badge", "Nickname For Badge",
"City/State For Badge", parses a last name off the display name, and
performs a case-insensitive dedup so e.g. "MRSTCAO" and "Mrstcao"
merge into one row.

Usage:
    uv run scripts/badges.py --campaign <UUID>
    uv run scripts/badges.py --campaign <UUID> --last-export scripts/last_export.xlsx
    uv run scripts/badges.py --campaign <UUID> --output /tmp/canonical.csv
"""

import argparse
import csv
import io
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import openpyxl
import yaml
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as pdfcanvas

# Reuse the poller's Zeffy client.  Importing by module works because
# scripts/ is on sys.path when running via `uv run scripts/badges.py`.
from zeffy_poll import (  # noqa: E402
    AuthExpired,
    fetch_xlsx_bytes,
    format_ticket_type_flags,
    load_session,
    parse_ticket_number,
    ticket_type_to_flags,
)


# Rough thresholds for the "will this overflow the badge?" flags.
# Tune once we've actually printed a sheet — for now, err on the
# side of surfacing things worth eyeballing.
NICKNAME_OVERFLOW = 20
DISPLAY_NAME_OVERFLOW = 25


# ---------------------------------------------------------------------------
# Avery 74459 PDF layout constants.
#
# The stock is 6-up on letter (2 cols × 3 rows).  The badge cells don't
# actually tile edge-to-edge — the sheet has:
#   * a ~1" tear-off strip at the top
#   * a ~1.125" tear-off strip at the bottom
#   * ~0.25" of side border on each edge
#   * a small gap between the left and right columns
#
# So the top row sits high, the bottom row sits low, and the two
# columns are pushed away from the page center.  Values below match a
# real Avery 74459 sheet held up against a light source; --offset-x
# and --offset-y let you nudge everything uniformly for printer feed
# slop after inspecting the calibration page.
# ---------------------------------------------------------------------------
PAGE_W = 8.5 * inch
PAGE_H = 11.0 * inch
CELL_W = 3.5 * inch
CELL_H = 2.25 * inch

# Column geometry: each column moved 0.2" outward from page center vs.
# the vendor nominal, so the gap between the two columns is 0.4".
GRID_MARGIN_LEFT = 0.55 * inch       # was 0.75; -0.2" for the outward shift
COLUMN_GAP = 0.4 * inch              # between the two columns

# Row geometry (top edge of each row measured from the top of the page).
# Nominal was a uniform 2.125"/4.375"/6.625"; adjusted so the top row
# tucks up under the 1" top tear-off and the bottom row tucks down
# against the 1.125" bottom tear-off.
ROW_TOP_INCHES = (1.375, 4.375, 7.325)

SAFE_MARGIN = 0.15 * inch       # interior padding inside each cell (text)

# Artwork layer paths (relative to repo root).  Every badge is rendered
# as three stacked layers:
#
#   1. badge_pile.png filling the entire cell (the background "chip pile").
#   2. A white rounded rectangle sitting slightly proud of the text safe
#      zone — this is the readable card the text lives on.
#   3. The text, plus banquet.png (upper-right of the white card) if the
#      attendee has a banquet ticket.
REPO_ROOT = Path(__file__).parent.parent
BADGE_PILE_PATH = REPO_ROOT / "assets" / "badge" / "badge_pile.png"
BANQUET_PATH = REPO_ROOT / "assets" / "badge" / "banquet.png"

# White card geometry.  The card is slightly larger than the text safe
# zone in each direction so text has natural padding inside it, and the
# background pile still shows in a thin border around it.
WHITE_MARGIN = 0.08 * inch       # from cell edge to white card edge
WHITE_CORNER_R = 10              # points; corner radius on the card

# Banquet indicator (upper-right of the white card).
BANQUET_W = 0.55 * inch          # aspect-ratio preserved from the source PNG
BANQUET_INSET = 4                # points; distance from the card's top-right

# Base-14 fonts.  Fine for the current dataset (ASCII + a few accented
# Latin characters).  If we ever see names outside Latin-1 we register
# a full-Unicode TTF and swap here.
FONT_NICKNAME = "Helvetica-Bold"
FONT_NAME = "Helvetica"
FONT_HOMETOWN = "Helvetica-Oblique"
FONT_BANQUET = "Helvetica-Bold"

# Nickname auto-shrink bounds.  Start big for "readable across a poker
# table" prominence, floor at what a human across the table can still
# read.  Values in points.
NICKNAME_MAX_PT = 48
NICKNAME_MIN_PT = 18

NAME_PT = 13
HOMETOWN_PT = 11


@dataclass
class Attendee:
    display_name: str
    last_name: str
    nickname: str
    hometown: str
    tickets: list[int] = field(default_factory=list)
    ticket_type: str = ""


def find_col(header: list[str], *candidates: str) -> int | None:
    for cand in candidates:
        for i, h in enumerate(header):
            if cand in h:
                return i
    return None


def parse_extended(xlsx_bytes: bytes) -> list[Attendee]:
    wb = openpyxl.load_workbook(io.BytesIO(xlsx_bytes), read_only=True,
                                data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    header = [str(c).strip().lower() if c else "" for c in rows[0]]

    badge_col = find_col(header, "name for badge", "badge name")
    guest_col = find_col(header, "guest")
    buyer_col = find_col(header, "buyer")
    ticket_col = find_col(header, "ticket number")
    type_col = find_col(header, "ticket type")
    nickname_col = find_col(header, "nickname for badge", "nickname",
                            "questions", "notes")
    city_col = find_col(header, "city/state for badge", "city/state",
                        "hometown", "city")

    if ticket_col is None or (badge_col is None and guest_col is None
                              and buyer_col is None):
        sys.exit(f"Could not find required columns in header: {header}")

    def cell(row: tuple, idx: int | None) -> str:
        if idx is None or idx >= len(row) or row[idx] is None:
            return ""
        return str(row[idx]).strip()

    raw = []
    for r in rows[1:]:
        if not r or all(c is None for c in r):
            continue
        display_name = (cell(r, badge_col) or cell(r, guest_col)
                        or cell(r, buyer_col))
        if not display_name:
            continue
        parts = display_name.split()
        last_name = parts[-1] if len(parts) > 1 else ""
        raw.append({
            "display_name": display_name,
            "last_name": last_name,
            "nickname": cell(r, nickname_col),
            "hometown": cell(r, city_col),
            "ticket": parse_ticket_number(cell(r, ticket_col)),
            "type_flags": ticket_type_to_flags(cell(r, type_col)),
        })

    # Sort by ticket ascending so the earliest row wins for display fields.
    raw.sort(key=lambda r: (r["ticket"] is None, r["ticket"] or 0))

    # Case-insensitive dedup on (display_name, nickname).  Values kept
    # verbatim from the earliest row; later rows contribute additional
    # tickets, a hometown backfill if the earlier row had none, and
    # union'd ticket-type flags.
    by_key: dict[tuple[str, str], Attendee] = {}
    flags_by_key: dict[tuple[str, str], set[str]] = {}
    for r in raw:
        key = (r["display_name"].casefold(), r["nickname"].casefold())
        if key not in by_key:
            by_key[key] = Attendee(
                display_name=r["display_name"],
                last_name=r["last_name"],
                nickname=r["nickname"],
                hometown=r["hometown"],
                tickets=[r["ticket"]] if r["ticket"] is not None else [],
            )
            flags_by_key[key] = set()
        else:
            a = by_key[key]
            if r["ticket"] is not None:
                a.tickets.append(r["ticket"])
            if not a.hometown and r["hometown"]:
                a.hometown = r["hometown"]
        flags_by_key[key] |= r["type_flags"]

    out = []
    for key, a in by_key.items():
        a.ticket_type = format_ticket_type_flags(flags_by_key[key])
        # If the attendee didn't fill in a nickname, fall back to the
        # first token of their display name — better than a blank
        # headline on the badge.
        if not a.nickname:
            first = a.display_name.split()[0] if a.display_name else ""
            a.nickname = first
        out.append(a)
    # Present sorted by earliest ticket for downstream ergonomics.
    out.sort(key=lambda a: min(a.tickets) if a.tickets else 9999)
    return out


def apply_overrides(attendees: list[Attendee], overrides_path: Path) -> int:
    """Apply per-ticket overrides from scripts/badge_overrides.yaml.

    The file is a small hand-maintained list of corrections we want to
    survive regenerations (Zeffy nicknames people misjudged, awkwardly-
    long strings shortened for the badge, etc.).  Format:

        overrides:
          - ticket: 97
            nickname: "(f*ck c*nc*r)"
          - ticket: 42
            hometown: "Portland, OR"

    Fields present in an override replace the value on the matching
    attendee; fields absent leave the Zeffy value untouched.  Returns
    the number of attendees actually modified so the caller can log it.
    """
    if not overrides_path.exists():
        return 0
    doc = yaml.safe_load(overrides_path.read_text()) or {}
    entries = doc.get("overrides") or []
    if not entries:
        return 0

    by_ticket = {t: a for a in attendees for t in a.tickets}
    applied = 0
    for entry in entries:
        ticket = entry.get("ticket")
        target = by_ticket.get(ticket)
        if target is None:
            print(f"  override warning: no attendee with ticket #{ticket}",
                  file=sys.stderr)
            continue
        changed = False
        for field_name in ("display_name", "last_name", "nickname", "hometown"):
            if field_name in entry:
                setattr(target, field_name, entry[field_name])
                changed = True
        if changed:
            applied += 1
    return applied


def validation_report(attendees: list[Attendee]) -> None:
    problems: list[str] = []

    # Note attendees whose nickname was auto-filled from their first
    # name (i.e., they didn't answer the Zeffy question).  Not really a
    # problem — badges will still print — but worth flagging in case
    # Doug wants to reach out.
    autofilled: list[Attendee] = []
    for a in attendees:
        first = a.display_name.split()[0] if a.display_name else ""
        if a.nickname and a.nickname == first:
            autofilled.append(a)

    # Same nickname on two different display_names.
    by_nick: dict[str, list[Attendee]] = defaultdict(list)
    for a in attendees:
        if a.nickname:
            by_nick[a.nickname.casefold()].append(a)
    for group in by_nick.values():
        distinct_names = {a.display_name.casefold() for a in group}
        if len(distinct_names) > 1:
            names = ", ".join(f"'{a.display_name}'" for a in group)
            problems.append(
                f"  duplicate nickname '{group[0].nickname}' on: {names}"
            )

    # Overflow risk.  Thresholds are placeholders until we've printed.
    for a in attendees:
        if len(a.nickname) > NICKNAME_OVERFLOW:
            problems.append(
                f"  long nickname ({len(a.nickname)} chars): "
                f"'{a.nickname}' — {a.display_name}"
            )
        if len(a.display_name) > DISPLAY_NAME_OVERFLOW:
            problems.append(
                f"  long display name ({len(a.display_name)} chars): "
                f"'{a.display_name}'"
            )

    print(f"Validation: {len(problems)} flag(s).")
    for p in problems:
        print(p)

    if autofilled:
        names = ", ".join(a.display_name for a in autofilled)
        print()
        print(f"Nickname auto-filled from first name ({len(autofilled)}): {names}")

    missing_hometown = [a for a in attendees if not a.hometown]
    if missing_hometown:
        names = ", ".join(a.display_name for a in missing_hometown)
        print()
        print(f"Missing hometown ({len(missing_hometown)}): {names}")


# ---------------------------------------------------------------------------
# PDF rendering
# ---------------------------------------------------------------------------

def cell_origin(row: int, col: int,
                offset_x: float = 0.0, offset_y: float = 0.0) -> tuple[float, float]:
    """Bottom-left corner of cell (row, col) in ReportLab points.

    row 0 is the top row, col 0 is the left column.  Column gap and
    per-row top margin come from module-level constants — the rows are
    NOT uniformly spaced (see the block-comment above the constants).
    offset_x / offset_y are applied in the natural sense: positive
    shifts the print right / down.
    """
    x = GRID_MARGIN_LEFT + col * (CELL_W + COLUMN_GAP) + offset_x
    y = PAGE_H - ROW_TOP_INCHES[row] * inch - CELL_H - offset_y
    return x, y


def fit_font_size(text: str, max_width: float, font: str,
                  max_pt: int, min_pt: int) -> int:
    """Largest integer point size at which text fits into max_width.

    If no size in [min_pt, max_pt] fits, returns min_pt — the caller
    should have caught it in the validation report.
    """
    for pt in range(max_pt, min_pt - 1, -1):
        if stringWidth(text, font, pt) <= max_width:
            return pt
    return min_pt


def draw_badge(c: pdfcanvas.Canvas, x0: float, y0: float,
               a: Attendee) -> None:
    """Draw one badge into the cell whose lower-left corner is (x0, y0).

    Layers, drawn bottom to top:

        1. badge_pile.png stretched to fill the whole cell.
        2. White rounded rectangle sitting on top, sized WHITE_MARGIN
           smaller than the cell.
        3. Text on top of the white card:
             * Hometown line ~10pt above the safe-zone bottom
               (skipped cleanly if empty).
             * Display name single-spaced above hometown, or in the
               hometown's slot if hometown is empty.
             * Nickname above that, bold, auto-shrunk from
               NICKNAME_MAX_PT down to NICKNAME_MIN_PT to fit the safe
               zone width.
        4. banquet.png in the upper-right of the white card (only if
           the attendee has a banquet ticket).
    """
    # --- Layer 1: background pile fills the cell ---
    c.drawImage(str(BADGE_PILE_PATH), x0, y0, CELL_W, CELL_H)

    # --- Layer 2: white rounded card ---
    wx = x0 + WHITE_MARGIN
    wy = y0 + WHITE_MARGIN
    ww = CELL_W - 2 * WHITE_MARGIN
    wh = CELL_H - 2 * WHITE_MARGIN
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(wx, wy, ww, wh, WHITE_CORNER_R, stroke=0, fill=1)
    c.setFillColorRGB(0, 0, 0)

    # --- Text sits in the interior safe zone (concentric with the card) ---
    sx = x0 + SAFE_MARGIN
    sy = y0 + SAFE_MARGIN
    sw = CELL_W - 2 * SAFE_MARGIN
    sh = CELL_H - 2 * SAFE_MARGIN

    # --- Bottom lines: hometown + name, tight single-spacing ---
    # Anchor the hometown baseline near the safe-zone bottom.  Name
    # baseline sits (font size × 1.15) above it — snug single spacing.
    home_baseline_y = sy + 10   # points above safe-zone bottom
    name_baseline_y = home_baseline_y + int(HOMETOWN_PT * 1.15) + 2
    if not a.hometown:
        # No hometown to render — let the name occupy the bottom slot
        # instead of leaving an empty line there.
        name_baseline_y = home_baseline_y

    c.setFont(FONT_NAME, NAME_PT)
    c.drawCentredString(sx + sw / 2, name_baseline_y, a.display_name)

    if a.hometown:
        c.setFont(FONT_HOMETOWN, HOMETOWN_PT)
        c.drawCentredString(sx + sw / 2, home_baseline_y, a.hometown)

    # --- Nickname band: everything above the name line, with breathing gap ---
    nickname_band_bottom = name_baseline_y + NAME_PT + 8
    nickname_band_top = sy + sh
    nickname = a.nickname or ""
    if nickname:
        pt = fit_font_size(nickname, sw, FONT_NICKNAME,
                           NICKNAME_MAX_PT, NICKNAME_MIN_PT)
        c.setFont(FONT_NICKNAME, pt)
        # Vertically center in the band.  Rough glyph geometry: baseline
        # sits ~0.28 × pt below the visual center of the glyph.
        band_mid = (nickname_band_top + nickname_band_bottom) / 2
        c.drawCentredString(sx + sw / 2, band_mid - pt * 0.28, nickname)

    # --- Layer 4: banquet indicator (upper-right of the white card) ---
    if "Banquet" in a.ticket_type:
        # preserveAspectRatio + only a width hint lets ReportLab pick
        # the correct height from the source PNG (turkey leg + cocktail).
        c.drawImage(
            str(BANQUET_PATH),
            wx + ww - BANQUET_W - BANQUET_INSET,
            wy + wh - (BANQUET_W * 442 / 772) - BANQUET_INSET,
            BANQUET_W,
            BANQUET_W * 442 / 772,
            mask="auto",
            preserveAspectRatio=True,
        )


def render_badges_pdf(attendees: list[Attendee], out_path: Path,
                      offset_x: float = 0.0, offset_y: float = 0.0) -> int:
    """Write the full-run PDF (6 badges per page).  Returns page count."""
    c = pdfcanvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    page = 1
    for i, a in enumerate(attendees):
        pos_on_page = i % 6
        col = pos_on_page % 2
        row = pos_on_page // 2
        x, y = cell_origin(row, col, offset_x, offset_y)
        draw_badge(c, x, y, a)
        if pos_on_page == 5 and i < len(attendees) - 1:
            c.showPage()
            page += 1
    c.showPage()
    c.save()
    return page


def render_calibration_pdf(out_path: Path,
                           offset_x: float = 0.0,
                           offset_y: float = 0.0) -> None:
    """One-page calibration overlay: cell outlines and center crosshairs.

    Print this on plain paper, then hold it up to a sheet of Avery 74459
    over a light source to see how well the cells align with the die-cuts.
    Nudge --offset-x / --offset-y until it lines up, then use the same
    offsets when generating the real PDF.
    """
    c = pdfcanvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))

    # Instructions in the top margin — outside the grid so they can't
    # affect what you're measuring.
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, PAGE_H - 0.75 * inch,
                 "PRINT AT 100% (\"Actual Size\") — NOT \"Fit to Page\"")
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, PAGE_H - 1.05 * inch,
                 "Hold this sheet against Avery 74459 over a light source.  "
                 "The rectangles below should line up with the die-cuts.")
    c.drawString(0.75 * inch, PAGE_H - 1.25 * inch,
                 f"Offsets in use: x={offset_x:+.2f} pt, y={offset_y:+.2f} pt.")

    c.setLineWidth(0.5)
    c.setStrokeColorRGB(0.35, 0.35, 0.35)
    for row in range(3):
        for col in range(2):
            x, y = cell_origin(row, col, offset_x, offset_y)
            c.rect(x, y, CELL_W, CELL_H)
            cx = x + CELL_W / 2
            cy = y + CELL_H / 2
            arm = 10
            c.line(cx - arm, cy, cx + arm, cy)
            c.line(cx, cy - arm, cx, cy + arm)
            c.setFont("Helvetica", 6)
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.drawString(x + 3, y + 3, f"r{row}c{col}")
            c.setFillColorRGB(0, 0, 0)
    c.save()


def filter_attendees(attendees: list[Attendee], only: str) -> list[Attendee]:
    """Match on display_name, nickname, or last_name (case-insensitive substring)."""
    needle = only.casefold()
    matches = [
        a for a in attendees
        if needle in a.display_name.casefold()
        or needle in a.nickname.casefold()
        or needle in a.last_name.casefold()
    ]
    return matches


def emit_csv(attendees: list[Attendee], path: Path) -> None:
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ticket", "display_name", "last_name", "nickname",
                    "hometown", "ticket_type", "all_tickets"])
        for a in attendees:
            primary = min(a.tickets) if a.tickets else ""
            w.writerow([
                primary,
                a.display_name,
                a.last_name,
                a.nickname,
                a.hometown,
                a.ticket_type,
                ",".join(str(t) for t in sorted(a.tickets)),
            ])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign",
                    help="Zeffy campaign UUID.  Not needed with --calibration.")
    ap.add_argument(
        "--output", type=Path,
        default=Path(__file__).parent / "badges_canonical.csv",
        help="Where to write the canonical CSV.  Default: scripts/badges_canonical.csv",
    )
    ap.add_argument(
        "--last-export", type=Path,
        help="Skip the Zeffy fetch and read this XLSX file instead.  "
             "Useful when Zeffy is flaky or for offline iteration.",
    )
    ap.add_argument(
        "--overrides", type=Path,
        default=Path(__file__).parent / "badge_overrides.yaml",
        help="Hand-maintained corrections applied after parsing.  "
             "Default: scripts/badge_overrides.yaml (skipped if absent).",
    )
    ap.add_argument(
        "--pdf", type=Path,
        help="Also render a full-run 6-up badge PDF to this path.",
    )
    ap.add_argument(
        "--calibration", type=Path,
        help="Render a calibration-page PDF to this path and exit.  "
             "No Zeffy data is fetched or read.",
    )
    ap.add_argument(
        "--only", type=str,
        help="With --pdf, render only attendees matching this string "
             "(case-insensitive substring against display_name, nickname, "
             "or last_name).  Useful for reprints.",
    )
    ap.add_argument(
        "--offset-x", type=float, default=0.0,
        help="Horizontal offset in points applied to every cell.  "
             "Positive shifts print right.  Tune with --calibration.",
    )
    ap.add_argument(
        "--offset-y", type=float, default=0.0,
        help="Vertical offset in points applied to every cell.  "
             "Positive shifts print down.  Tune with --calibration.",
    )
    args = ap.parse_args()

    # Calibration is a standalone path — no data source needed.
    if args.calibration:
        render_calibration_pdf(args.calibration, args.offset_x, args.offset_y)
        print(f"Wrote calibration page to {args.calibration}.")
        return 0

    if not args.campaign:
        sys.exit("--campaign is required (unless you're only running --calibration).")

    if args.last_export:
        if not args.last_export.exists():
            sys.exit(f"No file at {args.last_export}")
        xlsx_bytes = args.last_export.read_bytes()
        print(f"Read {len(xlsx_bytes)} bytes from {args.last_export}.")
    else:
        session = load_session()
        try:
            xlsx_bytes = fetch_xlsx_bytes(session, args.campaign)
        except AuthExpired as e:
            sys.exit(
                f"Zeffy auth failed ({e}).  Refresh cookies via "
                "scripts/zeffy_login_headless.py."
            )
        print(f"Fetched {len(xlsx_bytes)} bytes from Zeffy.")

    attendees = parse_extended(xlsx_bytes)
    print(f"Parsed {len(attendees)} canonical attendee(s).")

    n_overridden = apply_overrides(attendees, args.overrides)
    if n_overridden:
        print(f"Applied {n_overridden} override(s) from {args.overrides}.")
    print()
    validation_report(attendees)
    print()

    emit_csv(attendees, args.output)
    print(f"Wrote {args.output}.")

    if args.pdf:
        to_render = attendees
        if args.only:
            to_render = filter_attendees(attendees, args.only)
            if not to_render:
                sys.exit(f"--only {args.only!r} matched no attendees.")
            print(f"--only {args.only!r} matched {len(to_render)} attendee(s).")
        pages = render_badges_pdf(to_render, args.pdf,
                                  args.offset_x, args.offset_y)
        print(f"Wrote {args.pdf} ({pages} page(s), {len(to_render)} badges).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
