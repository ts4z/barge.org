barge.org web site
==================

This is an attempt to re-build the BARGE website with a static site generator.
I've chosen Hugo, with the PaperMod theme.

A scrape of barge.org, taken on 23-nov-2024, is in the OLD directory.

TODOs
-----

Forms are broken.

Image galleries are missing.  Images currently live on the CDN.  These need to
be brought over.

Navigation is poor.  We need breadcrumbs to make pages more discoverable.

Some content (old rulebooks) is missing.

How-To
------

To set up, clone this repository, and also get a recent Go version installed.
Install hugo.  Get the submodules (for the theme).

```sh
brew install hugo   # if on mac
go install gohugoio/hugo@latest   # if on debian
git submodule update --init --recursive
```

To run a local server that shows edits:

```sh
hugo serve -D --disableFastRender --renderToMemory
```

To produce a set of files suitable for copying to a web server:

```sh
hugo
```

To copy those files to a web server:

```sh
ssh ssh.some.server.org rm -rf /path/to/destination/\*
scp -v -r public/* ssh.some.server.org:/path/to/destination/
```

(OK, that command is imperfect, but you get the idea.)

All files are supposed to have front matter.  This is bracketed at the top with
dashes, in YAML format.  Some files migrated from the old barge.org are lacking
this.  Feel free to help clean them up.


Guidelines
----------

Help reorganize the site to make it easier to keep up to date.  Put timely
articles (registration open, closed, etc.) in the "news" directory.  As you do,
use "aliases" in the front matter.  [Cool links don't
change.](https://www.w3.org/Provider/Style/URI)

Files may be in HTML or Markdown.  Whenver possible, prefer Markdown to HTML.
Our theme supports raw HTML in line with Markdown.  Use this only as an escape
mechanism, or when migrating pages from HTML to Markdown format piecemeal.

All pages are supposed to have frontmatter headers.  This is missing in some
un-migrated pages, and they don't render well as a result.

Make sure every page has a "title" field and sets "draft: false" in the
frontmatter header.

Avoid TOML, which is permitted in configs and frontmatter.  Write either YAML
or JSON.  Actually, forget I said anything about JSON.
