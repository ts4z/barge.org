barge.org web site
==================

This is an attempt to re-build the BARGE website with a static site generator.
I've chosen Hugo, with the PaperMod theme.

A scrape of barge.org, taken on 23-nov-2024, is in the OLD directory.

TODOs
-----
Image galleries are missing.  Images currently live on the CDN.  These need to
be brought over.

A lot of files that could be statically hosted (images and rulebooks) still
live on the old server.

How-To
------

### You probably want a GitHub account.

You'll need a GitHub account to get write access to the repository or make pull
requests.  If you aren't currently working in software, this process will seem
cumbersome.  If you are working in software, this process will seem cumbersome,
like a familiar, comfortable straitjacket.

### And that's enough to get you to edit Markdown.

If you aren't working on the templating bits or the deployment bits, and you
are just writing articles in Markdown, you might be able to get by with just
making changes on GitHub and redeploying.  Editing Markdown is reasonably safe.

If this is you, _and_ you are just adding/editing files under content/...,
yeah, you probably don't need to do setup or testing.

(Nobody is in this category yet because we have not yet made it so the site
auto-deploys.  Soon, though.)

### Installation, Testing, and Deploying

#### You'll need a system with git and hugo installed.

https://gohugo.io/installation/linux/ might help.  We aren't using any of the
fancypants deployment features so the "extended" edition is fine.

##### Mac

If you're on a Mac, you can get git and hugo via homebrew.

```
brew install git hugo
```

##### Linux

If you're on Debian Linux, you'll need hugo.  The Debian build of hugo is too
old, so you'll need to get it and build it with Go.  Of course this means
getting Go, too.

```sh
go install gohugoio/hugo@latest   # if on debian
git submodule update --init --recursive
```

#### Clone this repository

On GitHub, just above and to the right of this text area, go to the Code
dropdown and pick "ssh".

#### Test your edits

To run a local server that shows edits:

```sh
hugo serve -D --disableFastRender --renderToMemory
```

#### Deploying the site

To produce a set of files suitable for copying to a web server:

```sh
hugo
```

The files are in the `public` directory and are suitable for putting on a web
server.

To copy those files to a web server:

```sh
ssh ssh.some.server.org rm -rf /path/to/destination/\*
rsync -r public/ ssh.some.server.org:/path/to/destination/
```

(OK, that command is imperfect, but you get the idea.)

Hugo is a static site generator.  Its output is fully static content.
We do expect links to be relative to the current site, so it does need to be in the
domain it's aware of, and at the correct level of the hierarchy.

But no databases, user management, cookies.  Just web pages.  Like it's 1994
again.  But with @#&#^*! CSS.

File Format
-----------

Hugo supports a few file formats.  Let's stick to Markdown and HTML.

All files are supposed to have front matter.  This is bracketed at the top with
dashes, in YAML format.  This works best if it includes the document title,
the document date (`YYYY-MM-DD` format), and maybe a summary field.

If you write Markdown, it is naturally restricted to a reasonable subset.  You
*cannot* include HTML in general, and Hugo will *omit* it ... but you can
bracket a section like this:

```
    {{< rawhtml }}}
    this<br>
    supports<br>
    any<br>
    markup<br>
    {{< /rawhtml }}}
```

If you write HTML, you are writing only the "body" portion of the document.
Hugo will supply the head portion and will wrap your text in the standard page
framework.  This allows using stylesheets, br tags, etc.


How Hugo Works
--------------

Hugo manages CSS and the decoration on the outside of the page (navigation bar,
tags cross-links, etc).  Without getting into the details, try to follow what
other documents in that directory are doing.

Files that are called "_index.md" mean that the page is a literal index of the
other things that are in that directory. This is good for a blog or for the
in-memoriam page.  In general, other pages in that directory will be enumerated
at the bottom of the index page.

Files that are called "index.md" do not show the pages under that subdirectory,
but let you put multiple components in that directory.  I believe this is a "page bundle".

Files that are not indexes are just flat files.  These can't have more
components.

(These files can also be `_index.html` and `index.html` and behave the same
way.)

It is OK to reorganize the site, but please provide aliases so the old links
continue to work.

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

If you find yourself repeating something, or having trouble styling something in Markdown,
make a "shortcode" for it.  See layouts/shortcodes.  Note that this is currently used
only for tournament headlines.

If you find you need a different layout for a directory, see
layouts/title-gallery for an example.

_Don't_ write a lot of custom HTML, or depend on the details of Markdown.  If
you can't do it with the structure of the documents, make new structure with a
shortcode.

### House style 

All results are listed in tables.  All tables are rank, name, amount.  If there is a tie,
we list the rank multiple times prefixed by "tie".

All tournament headers for events except ToGa are done with the "tournament" shortcode.

Gotchas
-------

### Tables

Tables are something of a black magic in Markdown, and not all Markdown
processors handle them the same way.  Here are the rules that I have found
relevant for Hugo:

1.  A table must start with a heading (it can be empty).
2.  A table is divided from its body with a bunch of horizontal lines, like
    this: `|---|---|---|`.  This makes Hugo see it as a table.  You may specify
    left- or right-justification of the rows, like this: `|--:|---|---|` This
    right-justifies all data in the first column, but the other columns will be
    left-justified.
3.  No merging rows or columns is permitted.

Some editors will see things as tables that Hugo won't.

To Do
-----

The "tournament" shortcode has a lot of flexibility to allow for transition
from older results.  I'd like to get rid of this.  (Sometimes we say "players",
sometimes we say "entries", sometimes we say "entrants".  We should pick one.)

The tournament shortcode allows multiple levels of h-headings, but some
of the results don't use this (relevant for ToGa).  Fix.

