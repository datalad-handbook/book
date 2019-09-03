.. _contribute:

Contributing
------------

Thanks for being curious about contributing!
We greatly appreciate and welcome contributions to this book, be it in the form
of an `issue <https://github.com/datalad-handbook/book/issues/new>`_ or a pull request!

If you are considering doing a pull request: Great! Every contribution is valuable,
from fixing typos to writing full chapters.
The steps below outline how the book "works". It is recommended to also create an issue
to discuss changes or additions you plan to make in advance.

Software setup
""""""""""""""

Depending on the size of your contribution, you may want to be able to build the book
locally to test and preview your changes. If you are fixing typos, tweak the
language, or rewrite a paragraph or two, this shouldn't be necessary, and you can safely
skip this paragraph and instead take a look into the paragraph
`Easy pull requests <contribute#Easy pull requests>`_.
If you want to be able to build the book locally, though, please follow these instructions:

-  datalad install the repository recursively. This ensures that dependent subdatasets are installed as well

.. code-block:: bash

   datalad install -r https://github.com/datalad-handbook/book.git

- optional, but recommended: Create a virtual environment

.. code-block:: bash

   virtualenv --python=python3 ~/env/handbook
   . ~/env/handbook/bin/activate

- install the requirements and a custom Python helper for the handbook

.. code-block:: bash

   # navigate into the installed dataset
   cd book
   # install required software
   pip install -r requirements.txt
   pip install -e .

- install ``librsvg2-bin`` (a tool to render ``.svgs``) with your package manager

.. code-block:: bash

   sudo apt-get install librsvg2-bin

Once this is configured, you can build the book locally by running ``make``,
and open it in your browser, for example with ``firefox docs/_build/html/index.html``.


Directives
""""""""""

If you are writing larger sections that contain code, ``gitusernote``\s, ``findoutmore``\s,
or other special directives, please make sure that you read this paragraph.

The book is build with a number of custom directives. If applicable, please
use them in the same way they are used throughout the book.



**Code:** For code that runs
inside a dataset such as ``DataLad-101``, working directories exist. The ``DataLad-101``
dataset for example lives in ``docs/build/wdirs/dl-101``. This comes with the advantage
that code is tested immediately -- if the code snippet contains an error, this error will
be written into the book, and thus prevent faulty commands from being published.
Running code in a working directory will furthermore build up on the existing history
of this dataset, which is very useful if some code relies on working with previously
created content or dataset history. Build code snippets that add to these working directories
by using the ``runrecord`` directive. Commands wrapped in these will write the output
of a command into example files. Make sure to name this files according to the following
schema, because they are executed sequentially:
``DL-101-1<nr-of-section>-1<nr-of-example>``, e.g.
``docs/basics/_examples/DL-101-101-101`` for the first example in the first section
of the basics.
Here is how a ``runrecord`` directive can look like:

.. code-block:: rst

   .. runrecord:: _examples/DL-101-101-101   # give the path to the resulting file
      :language: console
      :workdir: dl-101/DataLad-101    # specify a working directory here

      # this is a comment
      $ this line will be executed

Afterwards, the resulting example files need to be committed into Git. To clear existing
examples and working directory history, run ``make clean`` and ``make clean-examples``.

However, for simple code snippets outside of the narrative of ``DataLad-101``,
simple ``code-block::`` directives are sufficient.

**Other custom directives:** Other custom directives are ``gitusernote``
(for additional Git-related information for Git-users), and ``findoutmore``
(foldable sections that contain content that goes beyond the basics). Make use
of them, if applicable to your contribution.


Easy pull requests
^^^^^^^^^^^^^^^^^^

The easiest way to do a pull request is within the web-interface that Github
and `readthedocs <https://readthedocs.org>`_ provide. If you visit the rendered
version of the handbook at `handbook.datalad.org <http://handbook.datalad.org/>`_
and click on the small, floating ``v:latest`` element at the lower
right-hand side, the ``Edit`` option will take you straight to an editor that
lets you make your changes and submit a pull request.

.. figure:: img/contrib.png
   :figwidth: 100%
   :alt: Access the Github interface to submit a pull request right from within
         Readthedocs.

   You can find an easy way to submit a pull request right from within the handbook.

But you of course are also welcome to submit a pull request with whichever
other workflow suites you best.

Desired structure of the book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The book consists of three major parts: Introduction, Basics, and Use Cases,
plus an appendix. Purpose and desired content of these parts are outlined
below. When contributing to one of these sections, please make sure that your
contribution stays in the scope of the respective section.

Introduction
""""""""""""

- An introduction to DataLad, and the problems it aims to be a solution for.

- This part is practically free of hands-on content, i.e. no installation
  instructions, no demos. Instead, it is about concepts, analogies, general
  problems.

- In order to avoid too much of a mental split between a reader's desire to
  learn how to actually do things vs. conceptual information, the introduction
  is purposefully kept short and serves as a narrated table of contents with
  plenty of references to other parts of the book.


Basics
""""""

- This part contains hands-on-style content on skills that are crucial for
  using DataLad productively. Any non-essential information is not in basics,
  but collected in an appendix.

- The order of topics in this part is determined by the order in which they
  become relevant for a novice DataLad user.

- Content should be written in a way that explicitly encourages executing the
  shown commands, up to simple challenges (such as: "find out who the author of
  the first commit in the installed subdataset XY is").


Use Cases
"""""""""

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
