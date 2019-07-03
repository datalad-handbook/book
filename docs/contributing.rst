.. _contribute:

************
Contributing
************

.. todo::

   Add a section on how to contribute to this
   I'm creating this as a standalone so that we can easily link and reference it


Desired structure of the book
=============================

The book consists of three major parts: Introduction, Basics, and Use Cases,
plus an appendix. Purpose and desired content of these parts are outlined
below.


Introduction
------------

- An introduction to DataLad, and the problems it aims to be a solution for.

- This part is practically free of hands-on content, i.e. no installation
  instructions, no demos. Instead, it is about concepts, analogies, general
  problems.

- In order to avoid too much of a mental split between a reader's desire to
  learn how to actually do things vs. conceptual information, the introduction
  is purposefully kept short and serves as a narrated table of contents with
  plenty of references to other parts of the book.


Basics
------

- This part contains hands-on-style content on skills that are crucial for
  using DataLad productively. Any non-essential information is not in basics,
  but collected in an appendix.

- The order of topics in this part is determined by the order in which they
  become relevant for a novice DataLad user.

- Content should be written in a way that explicitly encourages executing the
  shown commands, up to simple challenges (such as: "find out who the author of
  the first commit in the installed subdataset XY is").


Use Cases
---------

- Topics that do not fit into the introduction or basics parts, but are
  DataLad-centric, go into this part.

- Any chapter is written as a more-or-less self-contained document that makes
  references to introduction and basics, but only few, and more general ones to
  other use cases. This should help with long-term maintenance of the content,
  as the specifics of how to approach a particular use case optimally may
  evolve over time, and cross-references to specific functionality might
  become invalid.

- There is no inherent order in this part, but chapters may be grouped by
  domain, skill-level, or DataLad functionality involved (or combinations of
  those).

- Any content in this part can deviate from the examples and narrative used for
  introduction and basics whenever necessary (e.g. concrete domain specific use
  cases). However, if possible, common example datasets, names, terms should be
  adopted, and the broadest feasible target audience should be assumed. Such
  more generic content should form the early chapters in this part.
