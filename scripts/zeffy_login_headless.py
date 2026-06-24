#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright>=1.45",
# ]
# ///
"""
Headless Zeffy login for SSH-only sessions.

When the host has no graphical display (so the regular Playwright-based
zeffy_login.py can't open its visible browser), this script runs
Chromium fully headless: it loads the login page, fills email and
password, waits for the post-login redirect to the organizer area,
captures session cookies to scripts/cookies.json, and exits.

Usage:
    uv run scripts/zeffy_login_headless.py --email you@example.com

You'll be prompted for the password (not echoed; no shell history).
On failure, the final page is screenshotted to scripts/last_login.png
to help diagnose what went wrong.

REQUIRES that the Zeffy account uses straight email + password
(no second factor, no magic link).
"""

import argparse
import asyncio
import getpass
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright

LOGIN_URL = "https://www.zeffy.com/en-US/login"
COOKIES_PATH = Path(__file__).with_name("cookies.json")
SCREENSHOT_PATH = Path(__file__).with_name("last_login.png")

# After successful login Zeffy lands somewhere under /en-US/o/... — the
# organizer/admin area.  Any URL containing this fragment counts as success.
SUCCESS_URL_FRAGMENT = "/o/"


async def try_fill(page, selectors, value, label) -> bool:
    for sel in selectors:
        try:
            await page.fill(sel, value, timeout=4000)
            print(f"Filled {label} via {sel}")
            return True
        except Exception:
            continue
    return False


async def try_click(page, selectors, label) -> bool:
    for sel in selectors:
        try:
            await page.click(sel, timeout=3000)
            print(f"Clicked {label} via {sel}")
            return True
        except Exception:
            continue
    return False


async def login(email: str, password: str) -> int:
    async with async_playwright() as p:
        # --disable-blink-features=AutomationControlled hides the obvious
        # navigator.webdriver = true marker; mild de-bot-ification.
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()
        print(f"Loading {LOGIN_URL} ...")
        await page.goto(LOGIN_URL, wait_until="networkidle")

        if not await try_fill(
            page,
            ['input[type="email"]', 'input[name="email"]',
             'input[autocomplete="email"]', 'input[id*="email" i]'],
            email, "email",
        ):
            await page.screenshot(path=SCREENSHOT_PATH)
            print(f"Could not find an email input.  Screenshot: "
                  f"{SCREENSHOT_PATH}", file=sys.stderr)
            await browser.close()
            return 1

        # Some flows put password on the same page; others put it after a
        # "Continue" click.  Try same-page first, fall back to two-step.
        password_filled = await try_fill(
            page,
            ['input[type="password"]',
             'input[autocomplete="current-password"]',
             'input[name="password"]'],
            password, "password",
        )
        if not password_filled:
            # Two-step: click Continue, then find the password input.
            await try_click(
                page,
                ['button[type="submit"]',
                 'button:has-text("Continue")',
                 'button:has-text("Next")'],
                "continue",
            )
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            password_filled = await try_fill(
                page,
                ['input[type="password"]',
                 'input[autocomplete="current-password"]'],
                password, "password (step 2)",
            )

        if not password_filled:
            await page.screenshot(path=SCREENSHOT_PATH)
            print(f"Could not find a password input.  Final URL: {page.url}",
                  file=sys.stderr)
            print(f"Screenshot: {SCREENSHOT_PATH}", file=sys.stderr)
            await browser.close()
            return 1

        # Submit and wait for the URL to land on the organizer area.
        if not await try_click(
            page,
            ['button[type="submit"]',
             'button:has-text("Log in")',
             'button:has-text("Sign in")',
             'button:has-text("Login")'],
            "submit",
        ):
            await page.keyboard.press("Enter")

        try:
            await page.wait_for_url(
                lambda url: SUCCESS_URL_FRAGMENT in url,
                timeout=30000,
            )
        except Exception:
            await page.screenshot(path=SCREENSHOT_PATH)
            print(f"Login didn't reach {SUCCESS_URL_FRAGMENT}.  "
                  f"Final URL: {page.url}", file=sys.stderr)
            print(f"Screenshot: {SCREENSHOT_PATH}", file=sys.stderr)
            await browser.close()
            return 1

        print(f"Logged in.  Landed on {page.url}")

        cookies = await context.cookies()
        zeffy_cookies = [c for c in cookies if "zeffy.com" in c.get("domain", "")]
        if not zeffy_cookies:
            print("ERROR: no zeffy.com cookies captured after login.",
                  file=sys.stderr)
            await browser.close()
            return 1

        COOKIES_PATH.write_text(json.dumps(zeffy_cookies, indent=2))
        COOKIES_PATH.chmod(0o600)
        print(f"Saved {len(zeffy_cookies)} cookie(s) to {COOKIES_PATH}.")
        await browser.close()
        return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", required=True,
                    help="Zeffy account email address.")
    args = ap.parse_args()

    password = getpass.getpass("Zeffy password (not echoed): ")
    if not password:
        sys.exit("No password entered; aborting.")

    return asyncio.run(login(args.email, password))


if __name__ == "__main__":
    sys.exit(main())
