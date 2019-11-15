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
commit. This, by the way, is the reason why a :command:`datalad run`
requires a clean dataset: The :command:`datalad save` that a :command:`datalad run` ends with
internally should only save changes that can be attributed to
the command that was run, and not changes that existed already
but were yet unsaved.

In principle, a general recommendation may be to keep your DataLad
dataset clean. This assists a structured way of working and prevents
clutter, and it also nicely records provenance inside your dataset.
If you have content in your dataset that has been untracked for 9 months
it will be hard to remember where this content came from, whether it
is relevant, and if it is relevant, for what. Adding content to your
dataset will thus usually not do harm -- certainly not for your
dataset.


However, there may be valid reasons to keep content out of
DataLads version control and tracking. Maybe you hide your secret
``my-little-pony-themesongs/`` collection within ``Deathmetal/``
and do not want a record of this in your history or the directory
being shared together with the rest of the dataset. Who knows?
We would not judge in any way. In principle, you already know a few
tricks on how to be "messy" and have untracked files.
For :command:`datalad save`, you know that precise file paths allow
you to save only those modifications you want to change.
For :command:`datalad run` you know that one
can specify the ``--explicit`` option
to only save those modifications that are specified in the ``--output``
argument.

But there are two ways to leave untracked content unaffected
by a :command:`datalad save`. One is an option within :command:`datalad save`
itself::

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
``playlists/my-little-pony-themesongs/*``. Afterwards,
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

.. note::

   Note one caveat: If a command creates an output that is git-ignored,
   (e.g. anything inside of ``tmp/`` in our dataset), a subsequent command
   that requires it as an undisclosed input will only succeed if both
   commands a ran in succession. The second command will fail if re-ran on its own,
   however.
