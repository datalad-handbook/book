.. _usertypes:

Tell me what you are and I tell you where to start
--------------------------------------------------

The DataLad Handbook has grown into an extensive document. Depending on your
use case for DataLad, you may not want to read *all* of the content there is.
This section tries to be your guide.

.. figure:: ../artwork/src/user_types.svg

If you can identify with one of the user types listed below, check out the
recommended sections.

**1** Independent but intrigued
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"I don't have a particular use case for DataLad (yet), but I want to know what
it is all about".

Start by reading sections :ref:`executive_summary` to get a high-level overview
about DataLad's functionality, and continue with section :ref:`philo` for
a short introduction to the fundamental principles of the software.
Afterwards, you may want to skim through the different
:ref:`usecases <usecase-intro>` to see whether one catches your attention.
The :ref:`cheat`, finally, can give you concrete command overviews.

**2** Eager to try all of the things!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"I so want to try out *all* of DataLad!"

Awesome, and Welcome! The complete :ref:`basics-intro` part of the book was
written for you. If you read it from start to end, you will become a DataLad
expert. Don't forget to :ref:`install <install>` DataLad first, though.
And if the Basics are not enough, continue right into the :ref:`usecase-intro`
afterwards.

**3** Seeking help
^^^^^^^^^^^^^^^^^^

"I ran into a problem and hoped the book could help".

The section :ref:`help` may give you a good general overview on what to do if
you encountered a problem. If you're dealing with file system operations,
:ref:`filesystem` could be a resource to help you, and for all things configuration,
the chapter :ref:`chapter_config` is your place to go to. If you are confused by
symlinks or "permission denied" error in your dataset, checkout section
:ref:`symlink` for some Basics on :term:`git-annex`. The "Quick search" bar at
the sidebar can also help to navigate to relevant sections, and the
`index <http://handbook.datalad.org/en/latest/genindex.html>`_ at the end of the
book can show you where all commands mentioned in the handbook are introduced.

If you're seeking help with regard to large datasets you might want to take a look at
Use case :ref:`usecase_HCP_dataset`.

.. todo::

   write section on scaling up

If none of this helps, don't hesitate to file an
`issue <https://github.com/datalad/datalad/issues>`_ or post your question
to `Neurostars.org <https://neurostars.org>`_. We are happy to help, and
appreciate bug reports!


**4** The impatient
^^^^^^^^^^^^^^^^^^^

"I need to get going. FAST."

Umm, sure. In principle, you can jump through the Basics and checkout precisely
the sections you need, even though not all things will become clear.
It's best to keep the :ref:`cheat` near by.

You want to know how to set-up and share an analysis
with DataLad? Reading chapters :ref:`chapter_datasets`, :ref:`chapter_gitannex`,
:ref:`chapter_yoda` and chapter :ref:`chapter_thirdparty` should work for you.

You want to use DataLad as a back-up or dataset storage solution? Go to
section :ref:`riastore` and usecase :ref:`usecase_datastore`.


**5** The data publisher
^^^^^^^^^^^^^^^^^^^^^^^^

"I have a large amount of data that I want to publish, and thought DataLad would
be a potential solution."

If you're not yet familiar with DataLad's concept of a dataset, quickly read
through the chapter :ref:`chapter_datasets`, and reading :ref:`chapter_gitannex`
is also a good idea to get the Basics of how large files in datasets are handled.
Afterwards, jump to chapter :ref:`chapter_thirdparty`.
Depending on the amount of data, it may make sense to read about an example
of a large dataset (80TB/15 million files) in the usecase :ref:`usecase_HCP_dataset`,
and about the possibility of a :term:`Remote Indexed Archive (RIA) store` in the
section :ref:`riastore` and the usecase :ref:`usecase_datastore`.


**6** The advanced user
^^^^^^^^^^^^^^^^^^^^^^^

"Don't bore me with all the introductory stuff..."

You already have plenty of DataLad experience and want to learn about advanced
aspects of it? The handbook can show you a few of those!
The section :ref:`procedures` can show you how to write or distribute
run-procedures. The section :ref:`hooks` introduces the hook feature of
DataLad. The section

.. todo::

   write chapter on rclone feature

can show you how to use DataLad's rclone helper for special remotes.
The section :ref:`riastore` introduces the concept of a
:term:`Remote Indexed Archive (RIA) store`. Still not enough?
We're happy to consider your
`feature request <https://github.com/datalad-handbook/book/issues/new>`_ for new
handbook content, but also your pull request with your addition or use case.


**7** Teacher
^^^^^^^^^^^^^

"I came here to teach!"

Awesome! There are instructions in section :ref:`teach`, and the
`companion repository at github.com/datalad-handbook/course <https://github.com/datalad-handbook/course>`_
contains slides, code casts, and tools for teaching.
