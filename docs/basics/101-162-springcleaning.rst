.. _cleanup:

Fixing up too-large datasets
----------------------------

The previous section highlighted problems of too large monorepos and advised
strategies to them prevent them.
This section introduces some strategies to clean and fix up datasets that got out
of hand size-wise. If there are use cases you would want to see discussed here
or propose solutions for, please
`get in touch <https://github.com/datalad-handbook/book/issues/new/>`_.

Getting contents out of Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say you did a :command:`datalad run` with an analysis that put too
many files under version control by Git, and you want to see them gone.
Sticking to the FSL FEAT analysis example from earlier, you may, for example,
want to get rid of every ``tsplot`` directory, as it contains results that are
irrelevant for you.

Note that there is no way to ``drop`` the files as they are in Git instead of
git-annex. Removing
the files with plain filesystem (``rm``, ``git rm``) operation also does not
shrink your dataset. The files are snapshot and even though they don't exist in
the current state of your dataset anymore, they still exist -- and thus clutter
-- your datasets history. In order to *really* get committed files out of Git,
you need to rewrite history. And for this you need heavy machinery:
`git-filter-repo <https://github.com/newren/git-filter-repo>`_ [#f1]_.
It is a powerful and potentially dangerous tool to rewrite Git history.
Treat this tool like a chainsaw. Very helpful for heavy duty tasks, but also
life-threatening. The command
``git-filter-repo <path-specification> --force`` will "filter-out", i.e., remove
all files **but the ones specified** in ``<path-specification>`` from the datasets
history. Before you use it, please make sure to read its help page thoroughly.

.. findoutmore:: Installing git-filter-repo

   ``git-filter-repo`` is not part of Git but needs to be installed separately.
   Its `GitHub repository <https://github.com/newren/git-filter-repo>`_ contains
   more and more detailed instructions, but it is possible to install via :term:`pip`
   (``pip install git-filter-repo``), and available via standard package managers
   for MacOS and some Linux distributions (mostly rpm-based ones).

The general procedure you should follow is the following:

1. :command:`datalad clone` the repository. This is a safeguard to protect your
   dataset should something go wrong. The clone you are creating will be your
   new, cleaned up dataset.
2. :command:`datalad get` all the dataset contents by running ``datalad get .``
   in the clone.
3. ``git-filter-repo`` what you don't want anymore (see below)
4. Run ``git annex unused`` and a subsequent ``git annex dropunused all`` to remove
   stale file contents that are not referenced anymore.
5. Finally, do some aggressive `garbage collection <https://git-scm.com/docs/git-gc>`_
   with ``git gc --aggressive``

In order to get a hang on the ``git-filter-repo`` step, consider a directory
structure similar to this exemplary run-wise FEAT analysis output structure:

.. code-block:: bash

   $ tree
   sub-*/run-*_<task>-<level>.feat
       ├── custom_timing_files
       ├── logs
       ├── reg
       ├── reg_standard
       │   ├── reg
       │   └── stats
       ├── stats
       └── tsplot

Each of such ``sub-*`` directories contains about 3000 files, and the majority of
them are irrelevant textfiles in ``tsplot/``.
In order to remove them for all subjects and runs from the dataset history,
the following command can be used::

   $ git-filter-repo --path-regex '^sub-[0-9]{2}/run-[0-9]{1}*.feat/tsplot/.*$' --invert-paths --force

The ``--path-regex`` and the regex expression ``'^sub-[0-9]{2}/run-[0-9]{1}*.feat/tsplot/.*$'`` [#f2]_
match all file paths inside of the ``tsplot/`` directories of all subjects and
runs.
The option ``--invert-paths`` then *inverts* this path specification, and leads
to only the files in ``tsplot/`` to be filtered out. Note that there are also
non-regex based path specifications possible, for example with the option
``--path-match`` or ``path-glob``, or with a specification placed in a file.
Please see the manual of ``git-filter-repo`` for more information.


.. rubric:: Footnotes

.. [#f1] Wait, what about ``git filter-branch``? Beyond better performance of
         ``git-filter-repo``, Git also discourages the use of ``filter-branch``
         for safety reasons and points to ``git-filter-repo`` as an alternative.
         For more background info, see this
         `thread <https://lore.kernel.org/git/CABPp-BEr8LVM+yWTbi76hAq7Moe1hyp2xqxXfgVV4_teh_9skA@mail.gmail.com/>`_.

.. [#f2] Regular expressions can be a pain to comprehend if you're not used to
         reading them. This one matches paths that start with (``^``) ``sub-``
         followed by exactly two (``{2}``) numbers that can be between 0 and 9
         (``[0-9]``), followed by ``/run-`` with exactly one (``{1}``) digit
         between 0 and 9 (``[0-9]``), followed by zero or more other characters
         (``*``) until ``.feat/tsplot/``, and ending (``$``) with any amount of
         any character (``.*``). Not exactly easy, but effective.
         One way to practice reading regular expressions, if you're interested
         in that, is by playing `regex crossword <https://regexcrossword.com/>`_.
