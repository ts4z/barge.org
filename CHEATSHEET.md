
BARGE.org Markdown Cheatsheet
=============================

This is a cheat sheet that provides example Markdown and a little sandbox for
experimentation.

See the bottom for the bit about shortcodes, which are very important for Hugo!

Note that Markdown fundamentally has a trivial mapping into HTML.  We prefer to
write Markdown, because it is easier to write---and harder to get wrong.  (It
is VERY easy to write invalid HTML that _looks_ like it works.)

Feel free to edit this, especially on a branch, and view it in GitHub.

Titles, headings, and subheadings
---------------------------------

Equal-underlined makes big titles.  Dash-underline makes small titles.

The number of dashes don't have to be the same as the text, but if they are,
isn't it pretty?

### Other titles

Alternatively, a leading "# " sequence makes a first-level title (equal-line),
and "## " makes a second level (dash-line) title

#### Other other titles

##### This is a still smaller title

###### This is for the severely OCD

## Italics and bold

Either marked with *asterisks* or _underline_ makes italics.

Anything marked with **two stars** is bold.

Of course, _**bold italic**_ is a thing, I think.

## Fixed-width

Backticks generate `fixed width` text.

```
    Triple backticks generate big blocks of fixed-with text
    that respects line breaks, etc.
    
    You can always tell when programmers are designing 
    this kind of thing.
```

# HTML in the Markdown

(This is like getting peanut butter in the chocolate.)

In general, do not use HTML in Markdown.  Hugo won't tolerate it.

You can put HTML in Markdown with the rawhtml shortcode, but please avoid this.
It is more useful to use a shortcode for semantic markup and then we can turn that
into the specific HTML we want.

This is a small issue.  Markdown is designed to be easier to read than HTML,
but the original Markdown spec assumes one can escape to HTML.  Since we do
_not_ have that out, we use shortcodes. See below, especially the one about br.

# Special characters

If you don't want to have bold and italic, you have to "escape" the \* with a
backslash, \\\* \<- like this.

Emashes are very useful---Markdown has a special syntax for them: \-\-\-

In general, Unicode characters are well-supported.  Just use them.  (Characters
are encoded in UTF-8, which is pretty standard, and easy to confuse with ASCII
text.)

|            | code    | description         |
|------------|:--------|---------------------|
| &amp;amp;  | &amp;   | ampersand           |
| &amp;9828; | &#9830; | white spade         |
| &amp;9829; | &#9829; | black (red) heart   |
| &amp;9830; | &#9830; | black (red) diamond |
| &amp;9831; | &#9831; | black spade         |
| &amp;9832; | &#9832; | white heart         |
| &amp;9832; | &#9833; | white diamond       |
| &amp;9832; | &#9834; | black club          |

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
If we put this onto a BARGE page, we would want to change \<br\> to {{\< br \>}}.
