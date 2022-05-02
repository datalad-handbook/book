.. _teach:

Teaching with the DataLad Handbook
----------------------------------

The handbook is a free and open source educational instrument made available
under a Creative Commons Attribution-ShareAlike (CC-BY-SA) license [#f1]_.
We are happy if the handbook serves as a helpful tool for other trainers, and
try to provide many useful additional teaching-related functions and contents.
Below, you can find them listed:

Use the handbook as a textbook/syllabus
"""""""""""""""""""""""""""""""""""""""

The Basics sections of the handbook is a stand-alone course that you can refer
trainees to. Regardless of background, users should be able to work through this
part of the book on their own. From our own teaching experiences, it is feasible
and useful to work through any individual basics chapter in one go, and assign
them as weekly or bi-weekly readings.

Use slides from the DataLad course
""""""""""""""""""""""""""""""""""

In parallel to the handbook, we are conducting data management workshops with
attendees of every career stage (MSc students up to PIs). The sessions are either
part of a lecture series (with bi-weekly 90 minute sessions) or workshops of different
lengths. Sessions in the lecture series are based on each chapter. Longer workshops
combine several chapters. You can find the slides for the workshops in the
`companion course repository <https://github.com/datalad-handbook/course>`_.
Slides are made using `reveal.js <https://github.com/hakimel/reveal.js/>`_.
They are available as PDFs in ``talks/PDFs/``, or as the source ``html`` files
in ``talks/``.

Enhance talks and workshops with code demos
"""""""""""""""""""""""""""""""""""""""""""

Any number of code snippets in the handbook that are created with the ``runrecord``
directive can be aggregated into a series of commands that can be sequentially
executed as a code demo using the
`cast_live <https://github.com/datalad-handbook/course/blob/master/tools/cast_live>`_
tool provided in the `companion course repository <https://github.com/datalad-handbook/course>`_.
These code demos allow you to remote-control a second terminal that executes
the code snippets upon pressing ``Enter`` and can provide you with simultaneous
speaker notes.

A number of demos exist that accompany the slides for the data management sessions
in ``casts``, but you can also create your own. To find out how to do this,
please consult the section `directives and demos <http://handbook.datalad.org/en/latest/contributing.html#directives-and-demos>`_
in the contributing guide.
To use the tool, download the ``cast_live`` script and the ``cast_bash.rc`` file
that accompanies it (e.g., by simply cloning/installing the
course repository), and provide a path to the demo you want to run::

   $ cast_live casts/01_dataset_basics

For existing code demos, the chapter :ref:`Code from chapters <codecasts>`
contains numbered lists of code snippets to allow your audience to copy-paste what
you execute to follow along.


Use artwork used in the handbook
""""""""""""""""""""""""""""""""

The handbook's `artwork <https://github.com/datalad-handbook/artwork>`_ repository
contains the sources for figures used in the handbook.

Use the handbook as a template for your own teaching material
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

If you want to document a different software tool in a similar way the handbook does
it, please feel free to use the handbook as a template.



.. rubric:: Footnotes

.. [#f1] CC-BY-SA means that you are free to

    - share - copy and redistribute the material in any medium or format
    - adapt - remix, transform, and build upon the material for any purpose, even commercially

    under the following terms:

    #. Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
    #. ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
