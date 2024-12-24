
BARGE.org Markdown Cheatsheet
=============================

This is a cheat sheet that provides example Markdown and a little sandbox for
experimentation.

See the bottom for the bit about shortcodes, which are very important for Hugo!

Note that Markdown fundamentally has a trivial mapping into HTML.  We prefer to
write Markdown, because it is easier to write---and harder to get wrong.  (It
is VERY easy to write invalid HTML that _looks_ like it works.)

Feel free to edit this, especially on a branch, and view it in GitHub.

Theory of Operation
-------------------

HTML is hard to read.  Markdown is easy to read.  More people will help maintain
documents if they are easy to read.

(It is possible to generate nice human-readable HTML.  Tools don't, they always
make it look terrible.  See the contents of the OLD directory.  It is harder to
make ugly Markdown, because Markdown doesn't let you hide your sins so easily.)

Titles, headings, and subheadings
---------------------------------

Equal-underlined makes big titles.  Dash-underline makes small titles.

The number of dashes don't have to be the same as the text, but if they are,
isn't it pretty?

### Other titles

Alternatively, a leading `# ` sequence makes a first-level title (equal-line),
and "## " makes a second level (dash-line) title.  I prefer `=` and `-`
underlined titles, but these are fine, too.

Note that you must put the `#` followed by a space.  Otherwise some tools will
think it's a hashtag.

#### Other other titles

The title above is a h4.

##### This is a still smaller title

The title above is h5.

###### Level 6 headings are fun for the very well-organized

Remember, anal-retentive is spelled with a hyphen.

## Italics and bold

Either marked with *asterisks* or _underline_ makes italics.

Anything marked with **two stars** is bold.

And, of course, there is always _**bold italic**_.

## Fixed-width

Backticks generate `fixed width` text.

```
    Triple backticks generate big blocks of fixed-with text
    that respects line breaks, etc.
    
    You can always tell when programmers are designing 
    this kind of thing.
```

# HTML in the Markdown

Hugo does not support raw HTML in Markdown, for reasons.

So, in general, do not use HTML in our Markdown.

You _can_ put HTML in Markdown with the rawhtml shortcode, but please avoid
this.  It is more useful to use a shortcode for semantic markup, and then we
can turn that into the specific HTML we want.

The original Markdown spec assumes one can escape to HTML for anything that
Markdown omits.  Since we do _not_ have that out, we use shortcodes. See below,
especially the one about br.  You'll need it for haiku.

# Quotations

> > > A greater-than in column 0 leads to an indent.

> > More than one quote leads to more than one indent.
> > Naturally, these can span multiple lines,
> > but will be paragrah-breaked in the usual way.

> Just like email from the old days.

Before top-posting.

# Special characters

If you don't want to have bold and italic, you have to "escape" the \* with a
backslash, \\\* \<- like this.

Two hyphens make an endash--like that.  You can also use the HTML entity, which is
&amp;ndash;.

Emashes are very useful---three hyphens, that is, `---`, should do it.  In HTML,
it's &amp;mdash;.

(It's not clear if GitHub renders these correctly, but I believe they're in the spec.)

In general, Unicode characters are well-supported.  Just use them.  (Characters
are encoded in UTF-8, which is pretty standard, and easy to confuse with ASCII
text.)

Another interesting one is that three perioids make an ellipsis...

Some other codes can be typed using HTML entities if you can't remember how to type the Unicode character:

|            | code    | description           |
|------------|:--------|-----------------------|
| &amp;amp;  | &amp;   | ampersand             |
| &amp;9824; | &#9824; | black spade           |
| &amp;9825; | &#9825; | white heart (avoid)   |
| &amp;9826; | &#9826; | white diamond (avoid) |
| &amp;9827; | &#9827; | black spade           |
| &amp;9828; | &#9828; | white spade  (avoid)  |
| &amp;9829; | &#9829; | black (red) heart     |
| &amp;9830; | &#9830; | black (red) diamond   |
| &amp;9831; | &#9831; | white club (avoid)    |

If you find others, extend this list.  A lot of things use the decimal
representation for the Unicode character number; some stuff will use hex.  Both
work fine.  (Ask Tim about the iPod 9829 story in person and why he knows this
number by...heart.)

# Section Dividers

Three dashes in the left column turn into an \<hr\>.

---

# Github-Flavored Markdown features

Github has a common Markdown variant called (get this) Github-flavored
Markdown, or GFM.

We are not using this as a consequence of being hosted on GitHub, it's just a
conveneient standard.

Note that the BARGE rulebook currently uses a different parser that does not
support tables or footnotes.  Ask Tim if he finds this annoying.[^1]

| tables                        | are a common extension     |
|:------------------------------|----------------------------|
| are easy                      |                            |
| this columnis left-justified  | this column is             |
|                               | right-justified            |
| note the colon in the divider |                            |
|                               | Markdown tables are not as |
|                               | general as HTML tables     |


[^1]: He does.

# Shortcodes

Hugo supports "shortcodes".  The details of this are not here.  The
implementations are in layouts/shortcodes/

In general, we use these for semantic marking that gets turned into HTML.

One exception is the "br" shortcode, which puts in a line break.  Without it,
Markdown doesn't represent paragraphs well.

Haiku are needed <br>
Everyone writes poetry <br>
That is very bad. 

This page is _not_ part of the BARGE site, so we render with raw BR tags.
If we put this onto a BARGE page, we would want to change `\<br\>` to `{{\< br \>}}`.
