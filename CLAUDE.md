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

### git

We use `git` for storing the site.  All pushes to main are deployed to production.
Make small, self-contained git commits whenever possible.

When pulling from remote, use `git pull --rebase`, not `git pull`.

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
  Keep text under ~40 characters for mobile.  Try to limit the number of CTAs to one, or at most, two.

### Images and Page Bundles

Content pages use Hugo [Page Bundles](https://gohugo.io/content-management/page-bundles/): images live in the same directory as the `_index.md` or `index.md` that references them. The `cover.image` front matter field names the cover image file relative to the page bundle. The `tournament` shortcode's `image` param also references page-bundle images (processed at 300×300).

Global/static assets (logos, etc.) live in `static/` and are referenced by absolute path.

The static directory also includes:
- "rulebook", which is not maintained by Hugo or this repository
- "atlarge", which is content that has not yet been migrated

### Front Matter Conventions

All pages require `title` and (for regular pages) `date` in YYYY-MM-DD format. 
All pages should have a summary.

Common optional fields:
- `type` — Selects layout (see table above)
- `draft: false` — Controls publishing.  `draft: false` is our default.
- `cover.image` — Cover image filename (page-bundle relative)
- `summary` — Summary shown in list views
- `aliases` — URL aliases for redirects
- `tags` — Tag taxonomy
- `weight` — Controls sort order in directory listings

### No Raw HTML in Markdown

Hugo is configured to disallow raw HTML in Markdown. Use shortcodes instead, but try to stick
to the templates that already exist.

Consult `CHEATSHEET.md` if you want to review Markdown conventions, but this is
mostly for humans.  Our Markdown is standard, although we do use extensions for
footnotes, tables, and definition lists.

### Heading conventions

Our template engine will output an h1 at the top of every page that needs one.
Avoid putting a second h1 (either HTML or Markdown) with a duplicate title, in
the "page content".  Use the frontmatter title and author fields whenever possible.

### UTF-8

All data is stored in UTF-8.  Older imports may be in Windows character sets in
Windows-1252 or ISO-8859-1 or ISO-8859-15.  It is safe to assume invalid UTF-8
sequences are a Windows-1252 character set.  Avoid using the Unicode
replacement character, or at least highlight it as part of a response to
refactoring.

### Tags

Canonical (URL) form of tags should be in lower-case.  A tag may have a page in
the tags directory which will provide a human readable name, such as "Trip
Report" for the tag `tripreport`.

All pages should be tagged with their relevant year and event.

### URLs

Whenever possible, use relative URLs.  Use Hugo helpers, including relref, to
automate the production of URLs.  (Documents may be relocated in time, and
giving good information to Hugo helps detect errors.)

It is an anti-pattern to link back to the root of the site, although it is
common in human-authored code.

## tools

The `frontmatter` utility can be used for reading and writing frontmatter.  If
it is not installed, it can be installed with:
- `go install github.com/marad/frontmatter@latest`
