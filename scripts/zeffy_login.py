#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright>=1.45",
# ]
# ///
"""
Interactive Zeffy login.  Opens a Chromium window; you log in by hand
(including 2FA, if any), then come back to the terminal and press Enter.
We capture the resulting session cookies to scripts/cookies.json.

First-time setup (one shot):
    cd scripts
    uv run --with playwright playwright install chromium

Then:
    uv run scripts/zeffy_login.py
"""

import asyncio
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

LOGIN_URL = "https://www.zeffy.com/en-US/login"
CONFIRM_URL_FRAGMENT = "/o/"   # any logged-in admin page lives under /en-US/o/...
COOKIES_PATH = Path(__file__).with_name("cookies.json")


async def main() -> int:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(LOGIN_URL)

        print()
        print("A Chromium window has opened.  Log in to Zeffy in that window.")
        print("When you can see the Zeffy admin (campaigns, etc.), come back here.")
        print()
        input("Press Enter once you are logged in... ")

        cookies = await context.cookies()
        zeffy_cookies = [c for c in cookies if "zeffy.com" in c.get("domain", "")]
        if not zeffy_cookies:
            print("ERROR: no zeffy.com cookies captured — did the login complete?",
                  file=sys.stderr)
            await browser.close()
            return 1

        COOKIES_PATH.write_text(json.dumps(zeffy_cookies, indent=2))
        COOKIES_PATH.chmod(0o600)
        print(f"Saved {len(zeffy_cookies)} cookie(s) to {COOKIES_PATH}.")
        await browser.close()
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
