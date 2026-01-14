# BARGE.org Codebase Guide for AI Agents

## Project Overview

This is a Hugo static site for BARGE.org (Big August Rec.Gambling Excursion), a poker event organization. The site uses the PaperMod theme and is automatically deployed via GitHub Actions to `www.barge.org` on every push to `main`.

## Architecture

- **Static site generator**: Hugo with PaperMod theme (as git submodule)
- **Content**: Markdown files in `content/` (Goldmark/GFM variant)
- **Layouts**: Custom layouts in `layouts/` override theme defaults
- **Configuration**: `config/_default/hugo.yaml` (plus `config/staging/` for test environment)
- **Deployment**: Automated via `.github/workflows/build-deploy.yml` using rsync to production server
- **Legacy content**: `OLD/` directory contains scraped HTML from 2024-11-23 migration

## Critical Workflows

### Local development and testing
```bash
# Clone with theme submodule
git submodule update --init --recursive

# Run local server (see changes instantly)
hugo serve -D --disableFastRender --renderToMemory

# Build static site (outputs to public/)
hugo
```

### Deployment
- **Automatic**: Push to `main` branch triggers GitHub Actions build and rsync to production
- **No manual deployment needed** unless explicitly required
- Test environment uses `config/staging/` overrides

## Content Conventions

### Front Matter (Required on ALL pages)
```yaml
---
title: Page Title                # REQUIRED
date: 2025-01-15                # REQUIRED (YYYY-MM-DD format)
type: sequential-section        # Optional: custom layout type
draft: false                    # Set true to exclude from production
tags: [barge, 2026]            # Optional
summary: Brief description     # Optional, use if the page is longer than trivial.
---
```

### Directory Structure Semantics
- **`_index.md`**: Creates an auto-listing page (shows child pages below, like blog index or in-memoriam)
- **`index.md`**: Creates a page bundle (can include images/resources, doesn't auto-list children)
- Files without "index" are standalone pages (cannot have sub-resources in directory)

### Links and Aliases
- Use **relative paths** for links: `[text](../other-page/)` 
- For paginated pages (`_index.md`), use absolute paths or `{{< relref "path" >}}` shortcode
- When moving/renaming pages, add `aliases:` to front matter to preserve old URLs (per [Cool URIs don't change](https://www.w3.org/Provider/Style/URI))
- Link to specific lines: `[see config](config/_default/hugo.yaml#L15)`

### Markdown Specifics
- **Line breaks in poetry/haiku**: Use `{{< br >}}` shortcode, NOT raw `<br>` tags
- **Tables**: Must have header row with `|---|---|` separator line; use `:` for alignment (`|--:|` = right-align)
- **Raw HTML**: Avoid except when migrating. Use `{{< rawhtml >}} ... {{< /rawhtml >}}` if absolutely necessary
- **Special chars**: Use HTML entities (`&mdash;`, `&ndash;`) or direct Unicode. Three hyphens `---` = em-dash

## Custom Shortcodes (in `layouts/_shortcodes/`)

Essential shortcodes for content authors:
- `{{< br >}}` - Line break (critical for poems/trip reports)
- `{{< tournament event="Event Name" buyin="$100" entries="50" ... >}}` - Standardized tournament headers with auto-generated anchors
- `{{< figure src="image.jpg" >}}` - Enhanced image with linking
- `{{< subdirs >}}` - List subdirectories (used in event indexes)

See `CHEATSHEET.md` for Markdown examples and `layouts/_shortcodes/tournament.html` for tournament shortcode parameters.

## Custom Layout Types

Set via `type:` in front matter:
- **`sequential-section`**: Event pages (BARGE/EMBARGO year directories) - shows content followed by chronological child pages
- **`memoriam`**: Memorial pages with special styling
- **`title-gallery`**: Gallery-style layouts
- Examples: [content/barge/2024/_index.md](content/barge/2024/_index.md), [content/in-memoriam/](content/in-memoriam/)

## Dynamic Site Elements (via `hugo.yaml`)

Two key parameters control site-wide notifications:

### Next Events Banner
```yaml
params:
  nextEvents:
    - link: "/embargo/2026/"
      text: "EMBARGO @ Resorts World — Jan 29-Feb 1"  # Max ~40 chars (mobile)
```

### Call-to-Action Boxes (Yellow highlight boxes on most pages)
```yaml
params:
  ctas:
    - link: https://barge.regfox.com/embargo-2026
      text: "EMBARGO 2026 Registration is Open"  # Max ~40 chars
```

Update these in [config/_default/hugo.yaml](config/_default/hugo.yaml) for site-wide announcements.

## Styling and Partials

- Custom partials in `layouts/_partials/` extend PaperMod theme (e.g., `ctas.html`, `next-events.html`, `common-header.html`)
- **PaperMod theme override workflow**: Theme lives in `themes/PaperMod/` as git submodule - DO NOT modify files there directly
  - To override theme behavior: copy file from `themes/PaperMod/layouts/` to `layouts/` with same path structure
  - Example: Override `themes/PaperMod/layouts/partials/footer.html` by creating `layouts/partials/footer.html`
  - This pattern accommodates eventual theme replacement or removal
- CSS customizations: `assets/css/` (theme provides base styles)
- Do not write extensive custom HTML - use shortcodes or create new layout types instead

## Common Tasks

### Adding a new event year
1. Create `content/barge/2026/_index.md` (or `embargo/2026/`)
2. Set `type: sequential-section` in front matter
3. Add subdirectories for schedule, results, etc.
4. Update `params.nextEvents` in `hugo.yaml` when active

### Adding memorial pages
1. Create `content/in-memoriam/person_name/index.md` (page bundle for images)
2. Set `type: memoriam` in front matter
3. Index at [content/in-memoriam/_index.md](content/in-memoriam/_index.md) auto-lists all

### Tournament results tables
- Use `{{< tournament >}}` shortcode for headers (creates anchor links)
- Standard format: `| Rank | Name | Amount |`
- For ties: `| tie 1 | Player A | $100 |` (repeat rank with "tie" prefix)

## Gotchas

- **Hugo version**: CI uses 0.152.2 (see `.github/workflows/build-deploy.yml`)
- **Submodules**: Remember `git submodule update --init --recursive` after cloning
- **Table syntax**: Hugo requires header row; different from some Markdown parsers
- **Hidden files**: Backup files like `*.~1~` are in repo but ignored by Hugo
- **Relative links**: Break in paginated (`_index.md`) pages - use absolute or `relref`
- **Draft pages**: Use `hugo serve -D` to preview drafts locally (excluded from production build)

## File Organization Philosophy

- Prefer Markdown over HTML for maintainability
- Keep content in `content/` - never in `layouts/` or `static/`
- Use shortcodes for repeated patterns (not copy-pasted HTML)
- Document structure beats inline styling
- Preserve old URLs with aliases when reorganizing

## Additional Resources

- [CHEATSHEET.md](CHEATSHEET.md) - Markdown examples and syntax reference
- [README.md](README.md) - Full setup and deployment guide
- Hugo shortcodes: `layouts/_shortcodes/*.html`
- Theme documentation: `themes/PaperMod/README.md`
