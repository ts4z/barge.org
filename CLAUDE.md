# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
# Start local dev server (live reload)
hugo server

# Build for production
hugo

# Build for staging environment
hugo --environment staging

# Build with drafts visible
hugo server --buildDrafts
```

The site builds to `public/`. The staging config in `config/staging/hugo.yaml` overrides the base URL to `https://test.bjrge.org/`.

## Architecture Overview

This is a [Hugo](https://gohugo.io/) static site for BARGE.org, the website for BARGE (Big Annual Rec.Gambling Excursion) and related poker community events. The theme is [PaperMod](https://github.com/adityatelange/hugo-PaperMod), with significant custom layouts extending it.

### Content Sections

- `content/barge/` — BARGE event history (1991–present), one subdirectory per year
- `content/embargo/` — EMBARGO event (fall Las Vegas gathering)
- `content/atlarge/` — ATLARGE event (spring Atlantic City gathering)
- `content/peterbarge/` — Peter Barge event
- `content/blog/` — Blog posts including trip reports
- `content/chips/` — BARGE chip gallery and history
- `content/in-memoriam/` — Memorial pages for community members
- `content/resources/` — Rules, code of conduct, etc.
- `content/inc/` — BARGE, Inc. corporate info

### Custom Page Types (layouts/)

Each page's `type` field in front matter selects the layout:

| Type | Use Case |
|------|----------|
| `event-root` | Top-level event page (e.g., `/barge/`); lists subsections without pagination |
| `sequential-section` | Year pages (e.g., `/barge/2025/`); lists sub-pages with prev/next navigation |
| `directory` | Renders a bullet-point list of child pages, supports `href` override and `moreInfo` |
| `chip-gallery` | Chip set gallery pages with optional `pdf` and `large` front matter params |
| `memoriam` | In-memoriam pages; uses `born`, `died`, `location`, `mainEventChamp` front matter |
| `pointer` | Redirect stub — meta-refresh to `href` front matter param; used to redirect old result URLs |

Default type renders using PaperMod's single/list templates (overridden in `layouts/single.html` and `layouts/list.html`).

### Custom Shortcodes (layouts/_shortcodes/)

- **`tournament`** — The main shortcode for results pages. Creates a heading with anchor, tournament metadata. Key params: `event` (required, becomes anchor), `buyin`, `entries`/`players`/`entrants`/`teams`, `prize-pool`, `date`, `image`, `level`, `parentheticals`, `special-event`, `donated`.
- **`figure`** — PaperMod's figure shortcode, forked to fix W3C validation; supports `class`, `link`, `src`, `caption`, `alt`, `width`, `height`, `align`.
- **`asset-figure`** — Like figure but loads from the `assets/` directory (via `resources.Get`); supports `src`, `width`, `alt`.
- **`br`** — Renders a `<br>` tag. Required since Hugo disallows raw HTML in Markdown; use in poems/haiku.
- **`bbb`** — Blue badge/box for inline callouts.
- **`current-organizers`** — Renders organizer list for an event/year.
- **`autoslideshow`** / **`autoslideshow-js`** — Auto-advancing image slideshow.
- **`subdirs`** — Lists subdirectories.

### Site Configuration (`config/_default/hugo.yaml`)

Key params to update regularly:

- `params.nextEvents` — List of upcoming events shown sitewide in the header. Keep text under ~40 characters for mobile. Uses `link` and `text` (supports `&mdash;` etc.).
- `params.ctas` — Call-to-action boxes (yellow) shown on most pages. Typically used for open registration announcements.

### Images and Page Bundles

Content pages use Hugo [Page Bundles](https://gohugo.io/content-management/page-bundles/): images live in the same directory as the `_index.md` or `index.md` that references them. The `cover.image` front matter field names the cover image file relative to the page bundle. The `tournament` shortcode's `image` param also references page-bundle images (processed at 300×300).

Global/static assets (logos, etc.) live in `static/` and are referenced by absolute path.

### Front Matter Conventions

All pages require `title` and (for regular pages) `date` in YYYY-MM-DD format. Common optional fields:
- `type` — Selects layout (see table above)
- `draft: false` — Must be explicit to publish
- `cover.image` — Cover image filename (page-bundle relative)
- `summary` — Summary shown in list views
- `aliases` — URL aliases for redirects
- `tags` — Tag taxonomy
- `weight` — Controls sort order in directory listings

### No Raw HTML in Markdown

Hugo is configured to disallow raw HTML in Markdown. Use shortcodes instead, but try to stick
to the templates that already exist.

Consult `CHEATSHEET.md` if you want to review Markdown conventions.
