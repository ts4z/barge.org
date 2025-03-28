---
title: Chip Design Notes
draft: false
author: Tim Showalter
---

(Work in progress)

This is all just my opinion, yet I'm writing this in third person.  It feels
weird but it will survive your edits better. &mdash;ts4z

Color
-----

We[^1] spent a lot of time worrying about chip colors.  A common problem in BARGE chip designs
is that some colors, notably red and orange, or red and pink, can be too close.

[^1] Mostly Patrick.

Patrick's suggestion is to print chips in black & white and make sure they look
different enough to be able to tell them apart in less-than-ideal light.

Ideally, the vendor allows exact matching to Pantone shades.  Unfortunately,
our current vendor does not.  Their colors appear to be broadly pretty good,
just not graphic designer ideal.

Printing Tolerances
-------------------

### Edges

BRPro allows printing all the way to the edge of a chip.  But they are not
exact in their positioning.  BRPro claims their chips do not need a "bleed" at
the chip edges.  This is technically true, but the design will not be
well-aligned to the edge.  A little shifting is inevitable.

Tim ordered a couple dealer buttons from BRPro, intended to have a 1mm border
around a graphic with a hard outer circle edge.  BRPro's tolerances are such
that this was just 0.5mm off.  It stands out.  But if the graphic had a softer
outer edge, these flaws would not be apparent.

A good workaround is to make sure anything very close to the edge does not
track the edge exactly.  On Tim's 2025 chips, the "BARGE XXXV" text is far
enough from the chip edge that it was not a problem.  But the denominations on
the back do not follow the curve, and proofs showed that some of the near-edge
denominations clipped at the edge of the chip.

### Blur of Dye-Sublimation

The dye sub process tends to blur sharp lines slightly.  This is not very
noticeable in photographs.  Thin black lines become slightly thicker.


Text
----

Patrick strongly prefers Arial for text on chips.  It replicates well with the
dye sub process.

Tim insisted on Futura.  He's happy with it, but you might not be.


Make Proofs of BRPro Chips
--------------------------

We learned in 2025 that making proof chips was key.  We identified a number of
problems.  This is particularly important if you haven't printed chips before.

Software
--------

Tim's advice: Pony up and buy Illustrator for a few months.

Tim used Inkscape (which is open source/free software) for some prototypes.  It
had some glitchy habits when printing, but it did help bash out some of the
original ideas.

Patrick gained some experience with another package, but it's not what the
vendor uses, and it lacks some features that Illustrator has.

Sales
-----

We're still figuring this part out.
