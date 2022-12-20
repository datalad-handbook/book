.. _gitignore:

How to hide content from DataLad
--------------------------------

You have progressed quite far in the DataLad-101 course,
and by now, you have gotten a good overview on the basics
and *not-so-basic-anymore*\s of DataLad.
You know how to add, modify, and save files, even completely
reproducibly, and how to share your work with others.

By now, the :command:`datalad save` command is probably
the most often used command in this dataset.
This means that you have seen some of its peculiarities.
The most striking was that it by default
will save the complete datasets status if one does not provide
a path to a file change. This would result in all content
that is either modified or untracked being saved in a single
commit.

In principle, a general recommendation may be to keep your DataLad
dataset clean. This assists a structured way of working and prevents
clutter, and it also nicely records provenance inside your dataset.
If you have content in your dataset that has been untracked for 9 months
it will be hard to remember where this content came from, whether it
is relevant, and if it is relevant, for what. Adding content to your
dataset will thus usually not do harm -- certainly not for your
dataset.
However, there may be valid reasons to keep content out of
DataLad's version control and tracking. Maybe you hide your secret
``my-little-pony-themesongs/`` collection within ``Deathmetal/``
and do not want a record of this in your history or the directory
being shared together with the rest of the dataset. Who knows?
We would not judge in any way.

In principle, you already know a few
tricks on how to be "messy" and have untracked files.
For :command:`datalad save`, you know that precise file paths allow
you to save only those modifications you want to change.
For :command:`datalad run` you know that one
can specify the ``--explicit`` option
to only save those modifications that are specified in the ``--output``
argument.

Beyond these tricks, there are two ways to leave *untracked* content unaffected
by a :command:`datalad save`. One is the ``-u/--updated`` option of
:command:`datalad save`::

   $ datalad save -m "my commit message here" -u/--updated

will only save dataset modifications to previously tracked
paths. If ``my-little-pony-themesongs/`` is not yet tracked,
a ``datalad save -u`` will leave it untouched, and its existence
or content is not written to the history of your dataset.

A second way of hiding content from DataLad is a ``.gitignore``
file. As the name suggests, it is a :term:`Git` related solution,
but it works just as well for DataLad.

A ``.gitignore`` file is a file that specifies which files should
be *ignored* by the version control tool.
To use a ``.gitignore`` file, simply create a file with this
name in the root of your dataset (be mindful: remember the leading ``.``!).
You can use one of `thousands of publicly shared examples <https://github.com/github/gitignore>`_,
or create your own one.

To specify dataset content to be git-ignored, you can either write
a full file name, e.g. ``playlists/my-little-pony-themesongs/Friendship-is-magic.mp3``
into this file, or paths or patterns that make use of globbing, such as
``playlists/my-little-pony-themesongs/*``. The hidden section at the end of this
page contains some general rules for patterns in ``.gitignore`` files. Afterwards,
you just need to save the file once to your dataset so that it is version controlled.
If you have new content you do not want to track, you can add
new paths or patterns to the file, and save these modifications.

Let's try this with a very basic example: Let's git-ignore all content in
a ``tmp/`` directory in the ``DataLad-101`` dataset:

.. runrecord:: _examples/DL-101-179-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ cat << EOT > .gitignore

   tmp/*
   EOT

.. runrecord:: _examples/DL-101-179-102
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad status

.. runrecord:: _examples/DL-101-179-103
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad save -m "add something to ignore" .gitignore

This ``.gitignore`` file is very minimalistic, but its sufficient to show
how it works. If you now create a ``tmp/`` directory, all of its contents would be
ignored by your datasets version control. Let's do so, and add a file into it
that we do not (yet?) want to save to the dataset's history.

.. runrecord:: _examples/DL-101-179-104
   :workdir: dl-101/DataLad-101
   :language: console

   $ mkdir tmp
   $ echo "this is just noise" > tmp/a_random_ignored_file

.. runrecord:: _examples/DL-101-179-105
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad status

As expected, the file does not show up as untracked -- it is being
ignored! Therefore, a ``.gitignore`` file can give you a space inside of
your dataset to be messy, if you want to be.

.. find-out-more:: Rules for .gitignore files

   Here are some general rules for the patterns you can put into a ``.gitignore``
   file, taken from the book `Pro Git <https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository#_ignoring>`_ :

   - Blank lines or lines starting with ``#`` are ignored
   - Standard :term:`globbing` patterns work. The line

     .. code-block:: bash

        *.[oa]

     lets all files ending in ``.o`` or ``.a`` be ignored. Importantly, these patterns
     will be applied recursively through your dataset, so that a file matching this
     rule will be ignored, even if it is in a subdirectory of your dataset. If you
     want to ignore specific files in the directory your ``.gitignore`` file lies in,
     but not any subdirectories, start the pattern with a forward slash (``/``), as
     in ``/TODO``.
   - To specify directories, you can end patterns with a forward slash (``/``), for
     example ``build/``.
   - You can negate a pattern by starting it with an exclamation point (``!``), such
     as ``!lib.a``. This would track the file ``lib.a``, even if you would be ignoring
     all other files with ``.a`` extension.

   The manpage of ``gitignore`` has an extensive and well explained overview.
   To read it, simply type ``man gitignore`` into your terminal.

   You can have a single ``.gitignore`` file in the root of your dataset,
   and its rules apply recursively to the entire hierarchy of the dataset (but not
   subdatasets!). Alternatively, you can have additional ``.gitignore`` files in
   subdirectories of your dataset. The rules in these nested ``.gitignore`` files only
   apply to the files under the directory where they are located.

.. importantnote:: Implications of git-ignored outputs for re-running

   Note one caveat: If a command creates an output that is git-ignored,
   (e.g. anything inside of ``tmp/`` in our dataset), a subsequent command
   that requires it as an undisclosed input will only succeed if both
   commands a ran in succession. The second command will fail if re-ran on its own,
   however.

.. find-out-more:: Globally ignoring files

   Its not only possible to define files or patterns for files to ignore inside
   of individual datasets, but to also set global specifications to have every
   single dataset you own ignore certain files or file types.

   This can be useful, for example, for unwanted files that your operating system
   or certain software creates, such as `lock files <https://fileinfo.com/extension/lock>`_,
   `.swp files <https://www.networkworld.com/article/2931534/what-are-unix-swap-swp-files.html>`_,
   `.DS_Store files <https://en.wikipedia.org/wiki/.DS_Store>`_,
   `Thumbs.DB <https://en.wikipedia.org/wiki/Windows_thumbnail_cache#Thumbs.db>`_,
   or others.

   To set rules to ignore files for all of your datasets, you need to create a
   *global* ``.gitignore`` file. The only difference between a repository-specific
   and a global ``.gitignore`` file is its location on your file
   system. You can put it either in its default location ``~/.config/git/ignore``
   (you may need to create the ``~/.config/git`` directory first),
   or place it into any other location and point Git to it. If you create a
   file at  ``~/.gitignore_global`` and run

   .. code-block:: bash

      $ git config --global core.excludesfile ~/.gitignore_global

   Git -- and consequently DataLad -- will not bother you about any of the files
   or file types you have specified. The following snippet defines a typical
   collection of ignored files to be defined across different platforms, and should work on Unix-like systems (like MacOS and Linux distributions).

   .. code-block:: bash

     $ touch ~/.gitignore_global
     $ for f in .DS_Store ._.DS_Store '*.swp' Thumbs.db ehthumbs.db; do \
       echo "$f" >> ~/.gitignore_global; done


.. only:: adminmode

   Add a tag at the section end.

   .. runrecord:: _examples/DL-101-179-106
      :language: console
      :workdir: dl-101/DataLad-101

      $ git branch sct_hide_content

   As this is currently the last section in the book, I'll add siblings to the
   published showroom datasets to it here:

   .. runrecord:: _examples/DL-101-179-107
      :language: console
      :workdir: dl-101/DataLad-101

      $ datalad siblings add -d . --name public --url https://github.com/datalad-handbook/DataLad-101.git

   .. runrecord:: _examples/DL-101-179-108
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ datalad siblings add -d . --name public --url https://github.com/datalad-handbook/midterm_project.git

   .. runrecord:: _examples/DL-101-179-109
      :language: console
      :workdir: dl-101/DataLad-101

      $ git config -f .gitmodules --replace-all submodule.midterm_project.url https://github.com/datalad-handbook/midterm_project
      $ datalad save -m "SERVICE COMMIT - IGNORE. This commit only serves to appropriately reference the subdataset in the public showroom dataset"

   This allows to automatically push all section branches (not accidentally synced or adjusted annex branches) with
   git push. Note: requires git push; datalad publish can not handle this atm (see https://github.com/datalad/datalad/issues/4006)

   .. runrecord:: _examples/DL-101-179-110
      :language: console
      :workdir: dl-101/DataLad-101

      $ git config --local remote.public.push 'refs/heads/sct*'
      $ git config --local --add remote.public.push 'refs/heads/master'
