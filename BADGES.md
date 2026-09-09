# BADGES.md — generating BARGE name badges

How the badge PDF gets made. This formalizes what we've actually been doing; the
process below is what produced the BARGE 2026 badges in July 2026.

**The normal ask is:** Doug says "make the badges," someone runs the command below on
dgrm4, eyeballs the validation report, and the PDF goes to whoever is printing. Doug is
usually not at the machine — assume this is being driven over SSH from somewhere with
bad internet.

---

## The shape of it

```
Zeffy (registration)  →  zeffy_poll.py  →  website guest list (last names stripped)
                     ↘
                       badges.py  →  badges_canonical.csv  +  badges.pdf
```

`zeffy_poll.py` runs on a schedule and keeps the public registration list fresh.
`badges.py` is **manual and on demand** — it re-fetches the same Zeffy export, but keeps
the fields badges need (last name, hometown, nickname) that the public list strips.

Everything lives in `scripts/`. `badges.py` is a `uv` inline-script (PEP 723) — no venv
to activate, `uv` resolves its own dependencies.

---

## Prerequisites on dgrm4

Verified working 2026-09-08:

- `uv` on PATH — `export PATH=/opt/homebrew/bin:$PATH` first if you're on a
  non-interactive SSH shell, which doesn't source `.zshrc`.
- Playwright Chromium, only needed to refresh cookies:
  `~/Library/Caches/ms-playwright/chromium-*` and `chromium_headless_shell-*`.
  Both present. If they ever go missing:
  `uv run --with playwright playwright install chromium` — a big download, so do
  **not** discover this need at sea.
- `scripts/cookies.json` — a live Zeffy session. **This is the thing that expires.**

---

## Making the badges

### 1. Refresh the Zeffy session (only if the fetch fails)

Cookies die quietly. If `badges.py` exits with `Zeffy auth failed`, refresh them:

```bash
cd ~/projects/barge/scripts
uv run zeffy_login_headless.py --email <the BARGE Zeffy account>
# prompts for the password; not echoed, not in shell history
```

This runs headless Chromium and was written specifically for SSH-only sessions, so it
works fine from a ship. It **requires the Zeffy account to use plain email + password** —
no 2FA, no magic link. On failure it screenshots the final page to
`scripts/last_login.png`; look at that before guessing.

Fallback if headless login breaks: log into Zeffy in a browser on your laptop, copy the
request as cURL from devtools, and feed it to `zeffy_cookies_from_curl.py` (no
dependencies). Clunky, but it needs nothing from dgrm4 but a paste.

### 2. Generate

```bash
cd ~/projects/barge/scripts
uv run badges.py --campaign <campaign-uuid> --pdf badges.pdf
```

Writes `badges_canonical.csv` (one row per attendee, ordered by earliest ticket number)
and the 6-up print-ready `badges.pdf`, and prints a validation report to stdout.

The campaign UUID is the Zeffy campaign for the event — the same one the poller is
pointed at. Exactly one campaign is ever active at a time.

### 3. Offline / no-Zeffy run

If Zeffy is flaky, cookies can't be refreshed, or you just want to re-render from the
last known data:

```bash
uv run badges.py --campaign DRYRUN --last-export last_export.xlsx --pdf badges.pdf
```

`--campaign` is still required by the argument parser but is unused in this path, so any
string works. `last_export.xlsx` is whatever the last successful fetch saved — **check
its date**, because it may predate the final registrations.

This is the escape hatch when everything else fails. It was verified working on
2026-09-08 against the Jul 27 export: 150 badges, 25 pages.

---

## Reading the validation report

The report is advisory — nothing blocks. Read it, decide, re-run if needed.

- **`duplicate nickname 'X' on: A, B`** — two people get the same headline. Usually
  harmless at a poker table, but if they'll be at the same table, add an override.
- **`Nickname auto-filled from first name (N)`** — these people left the nickname field
  blank, so their first name is the headline. Normal; the July run had 24.
- **`Missing hometown (N)`** — the hometown line will be blank on the badge. Fine, or
  chase the person.
- **Overflow flags** — nicknames over ~20 chars / display names over ~25 chars are
  flagged as likely to overflow. The renderer auto-shrinks the nickname (44pt down to a
  18pt floor), so a flag is a "go look at it," not a failure.

Hometowns are normalized automatically — `LAS VEGAS`, `Las Vegas Nevada`, `Las Vegas/NV`
all become `Las Vegas, NV`. The cleaner fixes separators and expands state names; it
cannot fix a misspelled city (`Los Angele/ California` → `Los Angele, CA`), which is what
overrides are for.

---

## Overrides

`scripts/badge_overrides.yaml`, keyed by **ticket number**, applied after parsing and
surviving every regeneration:

```yaml
overrides:
  - ticket: 97
    nickname: "(f*ck c*nc*r)"
  - ticket: 92
    hometown: "Los Angeles, CA"
```

Any of `display_name`, `last_name`, `nickname`, `hometown` may be set; absent fields
leave the Zeffy value alone. **Comment every override with why it exists** — the existing
two explain themselves and that convention is worth keeping.

---

## Printing

Stock is **Avery 74459**, 6-up on letter (2 columns × 3 rows). The sheet has a ~1"
tear-off strip at the top, ~1.125" at the bottom, and side borders, so the cells do not
tile edge to edge — the layout constants in `badges.py` were measured against a real
sheet held up to a light source, not taken from the vendor's nominal dimensions.

Each badge is three layers: the `badge_pile.png` chip-pile background filling the cell, a
white rounded card inset on top of it, then text — nickname (big, auto-shrinking), name,
hometown — plus `banquet.png` in the upper right if that attendee bought a banquet ticket.

### Calibrating a new printer

Printer feed slop shifts everything. Before a real run:

```bash
uv run badges.py --calibration calib.pdf
```

Needs no Zeffy data and no network. Print it on plain paper, hold it against an actual
Avery 74459 sheet over a light source, then correct with `--offset-x` / `--offset-y`
(points; positive = right / down) on the real run.

### Reprints

```bash
uv run badges.py --campaign <uuid> --pdf reprint.pdf --only "halvorsen"
```

Case-insensitive substring against display name, nickname, or last name. Searches the
honorary badges too, so Rodney and Vernon can be reprinted. The rest of the sheet is
padded with blank write-your-own badges rather than left as bare background.

### What gets added automatically

- **Two honorary badges** — Rodney Chen and Vernon Donk — appended to every full run.
- **At least 10 blank badges**, padded so the run ends on a full page. The July run came
  out at 150 badges / 25 pages.

---

## Getting the PDF off dgrm4

It's ~5.7MB, which is the awkward size on a ship connection. Options, roughly in order:

1. **Ask Claude to send it** — in a Claude Code session on dgrm4, ask for the file and it
   arrives on whatever device you're reading from. No scp, no bandwidth on your end.
2. **`scp` to yourself or the printer** —
   `scp -P <port> dgr@dgrm4:~/projects/barge/scripts/badges.pdf .`
3. **Email it** to whoever is printing.

Do not commit the PDF to the repo to move it around — `badges.pdf` and
`badges_reprint.pdf` are build artifacts that happen to be checked in; adding 5.7MB
churn per regeneration is not worth it.

---

## Gotchas

- **Non-interactive SSH shells have no brew on PATH.** `export PATH=/opt/homebrew/bin:$PATH`
  first or `uv` is not found.
- **Cookies expire silently.** The only symptom is `Zeffy auth failed` on the next run.
  Refresh before you need the badges urgently, not during.
- **`badges.py`'s module docstring used to be wrong** — it claimed PDF rendering "isn't
  built yet" long after it was. Trust this file and the `--help` output over prose in the
  script.
- **Dedup is exact-match-after-normalizing** (case-insensitive), not fuzzy. Two spellings
  of the same person produce two badges. Fuzzy matching on bad registration input was
  discussed and never built — deliberately deferred, don't re-propose it without a reason.
- **Don't clobber the July artifacts** while testing. Point `--output` and `--pdf` at a
  scratch directory.
