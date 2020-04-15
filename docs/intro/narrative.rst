How to use the handbook
=======================

For whom this book is written
-----------------------------

The DataLad handbook is not the DataLad documentation, and it is also
not an explanation of the computational magic that happens in the background.
Instead, it is a procedurally oriented, hands-on crash-course that invites
you to fire up your terminal and follow along.

**If you are interested in learning how to use DataLad, this handbook is for you.**

You do not need to be a programmer, computer scientist, or Linux-crank.
If you have never touched your computers shell before, you will be fine.
No knowledge about :term:`Git` or :term:`git-annex` is required or necessary.
Regardless of your background and personal use cases for DataLad, the
handbook will show you the principles of DataLad, and from chapter 1 onwards
you will be using them.

How to read this book
---------------------

First of all: be excited. DataLad can help you to manage your digital data
workflow in various ways, and in this book you will use many of them right
from the start.
There are many topics you can explore, if you wish:
local or collaborative workflows, reproducible analyses, data publishing, and so on.
If anything seems particularly exciting, you can go ahead, read it, *and do it*.
Therefore, **grab your computer, and be ready to use it**.

Every chapter will give you different challenges, starting from basic local
workflows to more advanced commands, and you will see your skills increase
with each. While learning, it will be easy to
**find use cases in your own work for the commands you come across**.

As the handbook is to be a practical guide it includes as many hands-on examples
as we can fit into it. Code snippets look like this, and you should
**copy them into your own terminal to try them out**, but you can also
**modify them to fit your custom needs in your own use cases**.
Note how we distinguish ``comments (#)`` from ``commands ($)`` and their output
in the example below (it shows the creation of a DataLad dataset):

.. code-block:: bash

   # this is a comment used for additional explanations. Anything preceded by $ is a command to try.
   # if the line starts with neither # nor $, its the output of a command
   $ datalad create myfirstrepo
   [INFO   ] Creating a new annex repo at /home/adina/DataLad-101
   create(ok): /home/adina/DataLad-101 (dataset)

When copying code snippets into your own terminal, do not copy the leading
``$`` -- this only indicates that the line is a command, and would lead to an
error when executed.

The book is split into different parts. The upcoming chapters
are the *Basics* that intend to show you the core DataLad functionality
and challenge you to use it. If you want to learn how to use DataLad, it is
recommended to start with this part and read it from start to end.
In the part *use cases*, you will find concrete examples of
DataLad applications for general inspiration -- this is the second part of this book.
If you want to get an overview of what is possible with DataLad, this section will
show you in a concise and non-technical manner.
Pick whatever you find interesting and disregard the rest. Afterwards,
you might even consider :ref:`contribute` to this book by sharing your own use case.

Note that many challenges can have straightforward and basic solutions,
but a lot of additional options or improvements are possible.
Sometimes one could get lost in all of the available DataLad functionality,
or in some interesting backgrounds about a command.
For this reason we put all of the basics in plain sight, and those basics
will let you master a given task and get along comfortably.
Having the basics will be your multi-purpose swiss army knife.
But if you want to have the special knowledge for a very peculiar type
of problem set or that extra increase in skill or understanding,
you'll have to do a detour into some of the *hidden* parts of the book:
When there are command options or explanations that go beyond basics and
best practices, we hide them in foldable book sections in order
to not be too distracting for anyone only interested in the basics.
You can decide for yourself whether you want to check them out:

.. findoutmore:: Click here to show/hide further commands

    Sections like this contain content that goes beyond the basics
    necessary to complete a challenge.

Note further that...

.. gitusernote::

   DataLad uses :term:`Git` and :term:`git-annex` underneath the hood. Readers that
   are familiar with these tools can find occasional notes on how a DataLad
   command links to a Git(-annex) command or concept in boxes like this.
   There is, however, absolutely no knowledge of Git or git-annex necessary
   to follow this book. You will, though, encounter Git commands throughout
   the book when there is no better alternative, and executing those commands will
   suffice to follow along.

Apart from core DataLad commands (introduced in the *Basics* part of this book),
DataLad also comes with many extensions and advanced commands not (yet) referenced
in this handbook. The development of many of these features
is ongoing, and this handbook will incorporate all DataLad commands and extensions
*once they are stable* (that is, once the command(-structure) is likely not to
change anymore). If you are looking for a feature but cannot find it in this
handbook, please take a look at the `documentation <http://docs.datalad.org>`_,
`write <http://handbook.datalad.org/en/latest/contributing.html>`_ or
`request <https://github.com/datalad-handbook/book/issues/new>`_
an additional chapter if you believe it is a worthwhile addition, or
`ask a question on Neurostars.org <https://neurostars.org/latest>`_
with a :command:`datalad` tag if you need help.


What you will learn in this book
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This handbook will teach you simple, yet advanced principles of data
management for reproducible, comprehensible, transparent, and
`FAIR <https://www.go-fair.org/fair-principles/>`_ data
projects. It does so with hands-on tool use of DataLad and its
underlying software, blended with clear explanations of relevant
theoretical backgrounds whenever necessary, and by demonstrating
organizational and procedural guidelines and standards for data
related projects on concrete examples.

You will learn how to create, consume, structure, share, publish, and use
*DataLad datasets*: modular, reusable components that can be version-controlled,
linked, and that are able to capture and track full provenance of their
contents, if used correctly.

At the end of the ``Basics`` section, these are some of the main
things you will know how to do, and understand why doing them is useful:

- **Version-control** data objects, regardless of size, keep track of
  and **update** (from) their sources and shared copies, and capture the
  **provenance** of all data objects whether you consume them from any source
  or create them yourself.

- **Build up complete projects** with data as independent, version-controlled,
  provenance-tracked, and linked DataLad dataset(s) that allow **distribution**,
  modular **reuse**, and are **transparent** both in their structure and their
  development to their current and future states.

- **Bind** modular components into complete data analysis projects, and comply
  to procedural and organizational principles that will help to create transparent
  and comprehensible projects to ease **collaboration** and **reproducibility**.

- **Share** complete data objects, version-controlled as a whole, but including
  modular components (such as data) in a way that preserves the history,
  provenance, and linkage of its components.

After having read this handbook, you will find it easy to create, build up, and
share intuitively structured and version-controlled data projects that
fulfill high standards for reproducibility and FAIRness. You are able to
decide for yourself how deep you want to delve into the DataLad world 
based on your individual use cases, and with every section you will learn
more about state-of-the-art data management.

The storyline
^^^^^^^^^^^^^

Most of the sections in the upcoming chapter follow a continuous **narrative**.
This narrative aims to be as domain-agnostic and relatable as possible, but
it also needs to be able to showcase all of the principles and commands
of DataLad. Therefore, together we will build up a DataLad project for the
fictional educational course ``DataLad-101``.

Envision yourself in the last educational course you took or taught.
You have probably created some files with notes you took, a directory
with slides or books for further reading, and a place where you stored
assignments and their solutions. This is what we will be doing as well.
This project will start with creating the necessary directory structures,
populating them by ``installing`` and ``creating`` several
:term:`DataLad subdataset`\s, adding files and changing their content,
and executing simple scripts with input data to create results we can
share and publish with DataLad.

.. figure:: ../artwork/src/student.svg
   :width: 70%

.. findoutmore:: I can not/do not want to code along...

   If you do not want to follow along and only read, there is a showroom dataset
   of the complete DataLad-101 project at
   `github.com/datalad-handbook/DataLad-101 <https://github.com/datalad-handbook/DataLad-101>`_.
   This dataset contains a separate branch for each section that introduced changes
   in the repository. The branches have the names of the sections, e.g.,
   ``sct_create_a_dataset`` marks the repository state at the end of the first section
   in the first chapter. You can checkout a branch with `git checkout <branch-name>`
   to explore how the dataset looks like at the end of a given section.

   Note that this "public" dataset has a number of limitations, but it is useful
   for an overview of the dataset history (and thus the actions performed throughout
   the "course"), a good display of how many and what files will be present in the
   end of the book, and a demonstration of how subdatasets are linked.

Let's get going!
----------------

If you have DataLad installed, you can dive straight into chapter 1, :ref:`createDS`.
For everyone new, there are the sections :ref:`howto` as a minimal tutorial
to using the shell and :ref:`install` to get your DataLad installation set up.
