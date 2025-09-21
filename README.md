barge.org web site
==================

This is the source for the BARGE website.  It utilizes Hugo, with the PaperMod
theme.

A scrape of barge.org, taken on 23-nov-2024, is in the OLD directory.
This was used for the initial content.

Any changes to this repo on the `main` branch will be built (via with GitHub
Actions) and pushed to [www.barge.org](https://www.barge.org/).

How-To
------

### Required reading

Read some tutorial on Markdown.  We're using Goldmark, a variant of
GitHub-Flavored Markdown, but any tutorial will work.

Listen to [Moose Turd Pie](https://www.youtube.com/watch?v=Q1ajLnuw2oo) and
consider the implications.

### You probably want a GitHub account.

You'll need a GitHub account to get write access to the repository or make pull
requests.  If you aren't currently working in software, this process will seem
cumbersome.  If you are working in software, this process will seem cumbersome,
like a familiar, comfortable straitjacket.

### And that's enough to get you to edit Markdown.

If you aren't working on the templating bits or the deployment bits, and you
are just writing articles in Markdown, you might be able to get by with just
making changes on GitHub, which will be automatically deployed.  Editing
Markdown is reasonably safe, and if you make a mistake, we can fix it.

If you are just adding/editing files under content/...,
yeah, you probably don't need to do setup or testing.

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
getting Go, and the Debian build of that is too old, too.

```sh
go install gohugoio/hugo@latest   # if on debian
git submodule update --init --recursive
```

#### Clone this repository

On GitHub, just above and to the right of this text area, go to the Code
dropdown and pick "ssh".  Run that.

#### Test your edits

To run a local server that shows edits:

```sh
hugo serve -D --disableFastRender --renderToMemory
```

#### Deploying the site

This is now automatic.

##### But I really want to do it by hand

To produce a set of files suitable for copying to a web server:

```sh
hugo
```

The files are in the `public` directory and are suitable for copying to a web
server.

To copy those files to a web server:

```sh
ssh ssh.some.server.org rm -rf /path/to/destination/\*
rsync -avzr public/ ssh.some.server.org:/path/to/destination/
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

If you write Markdown (`some_filename.md`), you will not have access to the
full scope of HTML (and this is a feature).  Unlike Markdown in some other
contexts, you *cannot* include HTML in general, and Hugo will *omit* it ... but
you *can* bracket a section like this:

```
    {{< rawhtml }}}
    this<br>
    supports<br>
    any<br>
    markup<br>
    {{< /rawhtml }}}
```

... but please avoid doing this, especially for complex elements.  Do _not_ use
this to modify CSS.

If you write HTML (`some_filename.html`), you are writing only the "body"
portion of the document, not the HEAD.  Hugo will supply the head portion and
will wrap your text in the standard page framework.  This allows using more
HTML features without worrying about how raw HTML will interact with Markdown.
This is not recommended, but you can find some examples where we have done
that.  One of them is the root page, which uses HTML because of bad
interactions with the slideshow gadget and HTML validation.

If all you want to do is add br tags, there is a Hugo shortcode for this.
(These are particularly important for certain trip reports which don't look
right without hard line breaks.)


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

All files may have a "type".  We have a few different types which render
slightly differently (in particular, in-memoriam, the resources page, and the
results pages are all different).  See the Hugo documentation for layouts.

Links should be relative, not absolute.  However, for paginated pages (anything
`.../_index.{md,html}`) links must either be absolute, or made with the
`relref` shortcode.  If this doesn't happen, Hugo will make broken links.
Examples of both can be found throughout the input files.

Guidelines
----------

Help reorganize the site to make it easier to keep up to date.  It is OK to
relocate pages, but as you do,
use "aliases" in the front matter.  [Cool links don't
change.](https://www.w3.org/Provider/Style/URI)  Try to salvage dead
links by pointing them at the most interesting content.  There are many 
old links to barge.org floating around on the web, and it is sad to see them
404.

We don't have a top-level "/news" directory because everything seemend to
fit better somewhere else.  For time-sensitive (and time-expiring) articles,
/blog is a good fit.  For events, note that the event directories will appear
in the blogroll on the root page.  This is based on some Hugo configuration bits.
This works great for some things and is terrible for others.

Files may be in HTML or Markdown.  Whenver possible, prefer Markdown.

Our theme supports raw HTML in line with Markdown.  Use this only as an escape
mechanism, or when migrating pages from HTML to Markdown format piecemeal.

All pages are supposed to have frontmatter headers.  This is the bit between the "---" lines.
Pages will not work quite correctly if this is omitted.

Make sure every page has a "title" field.

Write all frontmatter in YAML.  Avoid JSON unless the YAML version looks bad.
Avoid TOML entirely.

If you find yourself repeating something, or having trouble styling something
in Markdown, make a "shortcode" for it.  See `layouts/_shortcodes`.  This is
currently used for a few different things.  Try to avoid these as they seem
likely to confuse; that said, it is better to use a shortcode than raw HTML.

If you find you need a different layout for a directory, see
`layouts/title-gallery` for an example.

_Don't_ write a lot of custom HTML, or depend on the details of Markdown.  If
you can't do it with the structure of the documents, make new structure with a
shortcode.  If you care about the structure of HTML (rare, but it happens) make
the whole page HTML.

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

Some editors will see things as tables that Hugo won't.  If you do this wrong,
Hugo will mangle your table.  The usual gotcha for me is that Hugo requires a
top heading row on a table, but Emacs doesn't.  Always include this row.

If you need more complicated tables, that's a use for raw HTML.  This happens
on schedule pages which have complicated tables.

To Do
-----

Improve README.md further.

The "tournament" shortcode has a lot of flexibility to allow for transition
from older results.  I'd like to get rid of this.  (Sometimes we say "players",
sometimes we say "entries", sometimes we say "entrants".  We should pick one.)

The tournament shortcode allows multiple levels of h-headings, but some
of the results don't use this (relevant for ToGa).  Fix.

