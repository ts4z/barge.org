#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Convert a "Copy as cURL" command from a browser's devtools into the
scripts/cookies.json shape the poller expects.

Used to refresh Zeffy auth when interactive Playwright login isn't an
option (e.g. SSH-only access to the host).  In a browser, open devtools'
Network tab, find any authenticated request to api.zeffy.com, right-click
→ Copy → Copy as cURL.  Paste that into a file on this host (e.g.
/tmp/zeffy.curl), then run:

    uv run scripts/zeffy_cookies_from_curl.py /tmp/zeffy.curl

The file gets parsed for either a `-H 'cookie: ...'` (Chrome/Edge form)
or a `-b '...'` argument (Firefox/older form), every cookie is rewritten
to scripts/cookies.json with domain=api.zeffy.com (matching the host the
browser was authenticating against — which is the only host the poller
talks to), and we print a one-line summary.

Delete the source curl file after; it contains your auth secret.
"""

import argparse
import json
import re
import sys
from pathlib import Path

COOKIES_PATH = Path(__file__).with_name("cookies.json")

# Pull a cookie header out of an arbitrary curl command.  Browsers wrap
# header values in either single or double quotes; we accept both and
# don't try to handle escape sequences (none appear in cookie values).
COOKIE_HEADER_RE = re.compile(
    r"""-H\s*['"]cookie:\s*([^'"]+)['"]""",
    re.IGNORECASE,
)
COOKIE_B_RE = re.compile(
    r"""-b\s*['"]([^'"]+)['"]""",
)


def parse_cookie_string(s: str) -> list[dict]:
    """Split a Cookie-header value into [{name, value, domain}] entries."""
    out = []
    for chunk in s.split(";"):
        chunk = chunk.strip()
        if not chunk or "=" not in chunk:
            continue
        name, _, value = chunk.partition("=")
        name = name.strip()
        value = value.strip()
        if not name:
            continue
        out.append({
            "name": name,
            "value": value,
            "domain": "api.zeffy.com",
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("curl_file", type=Path,
                    help="Path to a file containing 'Copy as cURL' output.")
    args = ap.parse_args()

    if not args.curl_file.exists():
        sys.exit(f"No such file: {args.curl_file}")

    raw = args.curl_file.read_text()

    m = COOKIE_HEADER_RE.search(raw)
    if not m:
        m = COOKIE_B_RE.search(raw)
    if not m:
        sys.exit("Couldn't find a -H 'cookie: ...' or -b '...' argument in "
                 f"{args.curl_file}.  Make sure you copied the request as "
                 "cURL, not as fetch or PowerShell.")

    cookies = parse_cookie_string(m.group(1))
    if not cookies:
        sys.exit("Found a cookie argument but couldn't parse any "
                 "name=value pairs from it.")

    COOKIES_PATH.write_text(json.dumps(cookies, indent=2))
    COOKIES_PATH.chmod(0o600)
    names = ", ".join(c["name"] for c in cookies)
    print(f"Wrote {len(cookies)} cookie(s) to {COOKIES_PATH}: {names}")
    print(f"You may now delete {args.curl_file} — it contains the auth secret.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
