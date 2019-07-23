Miscallaneous file system operations
------------------------------------

With all of the information about symlinks and object trees,
you might be reluctant to perform usual file system managing
operations, such as copying, moving, or renaming a files or
directories with annexed content.

If I renamed one of those books, would the symlink that points
to the file content still be correct? What happens if I'd copy
an annexed file?
If I moved the whole ``books/`` directory? What if I moved
all of ``DataLad-101`` into a different place on my computer?
What if renamed the whole superdataset?
And how do I remove a file, or directory, or subdataset?

Therefore, there is an extra tutorial offered by the courses'
TA today afternoon, and you attend.
There is no better way of learning than doing. Here, in the
safe space of the ``DataLad-101`` course, you can try out all
of the things you would be unsure about or reluctant to try
on the dataset that contains your own, valuable data.

Below you will find common questions about file system
management operations, and each question outlines caveats and
solutions with code examples you can paste into your own terminal.
Because these code snippets will add many commits to your
dataset, we're cleaning up within each segment with
common git operations that manipulate the datasets
history -- be sure to execute these commands as well.

What happens if I rename an annexed file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's try it. In Unix, renaming a file is exactly the same as
moving a file.

.. runrecord:: _examples/DL-101-114-101
   :language: console
   :workdir: dl-101/DataLad-101

   $ cd books/
   $ mv TLCL.pdf The_Linux_Command_Line.pdf
   $ ls -lah

Try to open the renamed file, e.g. with
``evince The_Linux_Command_Line.pdf``.
This works!

But let's see what changed in the dataset with this operation:

.. runrecord:: _examples/DL-101-114-102
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ datalad status

We can see that the old file is marked as ``deleted``, and
simultaneously, an ``untracked`` file appears: the renamed
PDF.

While this might appear messy, a ``datalad save`` will clean
all of this up. Therefore, don't panic if you rename a file,
and see a dirty dataset with deleted and untracked files
-- ``datalad save`` handles these and other cases really well
under the hood.
Note, however, that you can't have any other
modifications in the dataset, because it is a ``datalad save``
with no path specification.

.. runrecord:: _examples/DL-101-114-103
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ datalad save -m "rename the book"

This command will realize that a simple renaming has taken place,
and will summarize this nicely in the resulting commit:

.. runrecord:: _examples/DL-101-114-104
   :language: console
   :workdir: dl-101/DataLad-101/books
   :emphasize-lines: 8-11

   $ git log -1 -p

Thus, if you have a clean dataset, simply renaming files will
be easily saved to the history with a ``datalad save``.

If, however, you have unsaved modifications in your dataset that you
don't (yet) want to save, you can do a detour by using git tools.
Git has built-in commands that provide a solution in two steps.

Lets revert the renaming of the the files files:

.. runrecord:: _examples/DL-101-114-105
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git reset --hard HEAD~1
   $ datalad status

A Git-specific way to rename files is the ``git mv`` command:

.. runrecord:: _examples/DL-101-114-106
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git mv TLCL.pdf The_Linux_Command_Line.pdf

.. runrecord:: _examples/DL-101-114-107
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ datalad status

We can see that the old file is still seen as "deleted", but the "new",
renamed file is "added". A ``git status`` displays the change
in the dataset a bit more accurate:

.. runrecord:: _examples/DL-101-114-108
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git status

A subsequent ``git commit -m "rename book"`` will write the renaming
-- and only the renaming -- to the datasets history.

.. runrecord:: _examples/DL-101-114-109
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git commit -m "rename book"

Let's revert this now, to have a clean history.

.. runrecord:: _examples/DL-101-114-110
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git reset --hard HEAD~1
   $ datalad status


What happens if I move a file from or into a subdirectory?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's move an annexed file from within ``books/`` into the root
of the superdataset:

.. runrecord:: _examples/DL-101-114-120
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ mv TLCL.pdf ../TLCL.pdf
   $ datalad status

In general, this looks exactly like renaming or moving a file
in the same directory. There is a subtle difference though:
Currently, the symlink of the annexed file is broken. There
are two ways to demonstrate this. One is trying to open the
file -- this will currently fail. The second way is to look
at the symlink:

.. runrecord:: _examples/DL-101-114-121
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ cd ../
   $ ls -l TLCL.pdf

The first part of the symlink should point into the ``.git/``
directory, but currently, it doesn't -- the symlink still looks
like ``TLCL.pdf`` would be within ``books/``. Instead of pointing
into ``.git``, it currently points to ``../.git``, which is non-existent,
and even outside of the superdataset. This is why the file
cannot be opened: When any program tries to resolve the symlink,
it will not resolve, and an error such as "no file or directory"
will be returned.. But don't panic! A ``datalad save`` will
rectify this as well:

.. runrecord:: _examples/DL-101-114-122
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "moved book into root"
   $ ls -l TLCL.pdf

After a ``datalad save``, the symlink is fixed again.
Therefore, in general, whenever moving or renaming a file,
especially between directories, a ``datalad save`` is
the best option to turn to.

.. container:: toggle

   .. container:: header

      **Addition: Why a move between directories is actually a content change**

   Let's see how this shows up in the dataset history:

   .. runrecord:: _examples/DL-101-114-123
      :language: console
      :workdir: dl-101/DataLad-101/books

      $ git log -1 -p

   As you can see, this action does not show up as a move, but instead
   a deletion and addition of a new file. Why? Because the content
   that is tracked is the actual symlink, and due to the change in
   relative location, the symlink needed to change. Hence, what looks
   and feels like a move on the file system for you is actually a
   move plus a content change.

This has given you much background, and you have also seen many
symlinks -- maybe more than you wanted? If you are currently confused,
worry not: The take-home-message is simple: Use ``datalad save``
whenever you move or rename files.

Finally, let's clean up:

.. runrecord:: _examples/DL-101-114-124
   :language: console
   :workdir: dl-101/DataLad-101

   $ git reset --hard HEAD~1


What happens if I copy a file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's create a copy of an annexed file, using the Unix
command ``cp`` to copy.

.. runrecord:: _examples/DL-101-114-130
   :language: console
   :workdir: dl-101/DataLad-101

   $ cp books/TLCL.pdf copyofTLCL.pdf
   $ datalad status

That's expected. The copy shows up as a new, untracked
file. Let's save it:

.. runrecord:: _examples/DL-101-114-131
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add copy of TLCL.pdf"

.. runrecord:: _examples/DL-101-114-132
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -1 -p

That's it.

.. container:: toggle

   .. container:: header

      **Addition: Symlinks!**

   If you have read the additional content in the section
   :ref:`symlinks`, you know that the same file content
   is only stored once, and copies of the same file point to
   the same location in the object tree.

   Let's check that out:

   .. runrecord:: _examples/DL-101-114-133
      :language: console
      :workdir: dl-101/DataLad-101

      $ ls -l copyofTLCL.pdf
      $ ls -l books/TLCL.pdf

   Indeed! Apart from their relative location (``.git`` versus
   ``../.git``) their symlink is identical. Thus, even though two
   copies of the book exist in your dataset, your disk needs to
   store only one.

Finally, let's clean up:

.. runrecord:: _examples/DL-101-114-134
   :language: console
   :workdir: dl-101/DataLad-101

   $ git reset --hard HEAD~1

What happens if I rename a directory or subdataset?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What happens if I move directories, or subdatasets?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: directory (all files in a directory will be renamed)
TODO: subdataset (tricky: change in .gitmodules. Also, I failed trying to
revert a ``git mv`` with ``git reset --hard master``. It did not move
subdataset back into original place, the subds became an untracked directory.

What if I move the superdataset into a different place on my computer?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: I don't think it should be a problem, but not sure whether I'm
missing something

What happens if I copy files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: Copying will create a new file that could be added. Its not symlinked,
I don't yet understand why, but the file is write-protected (why exactly? bc
symlinked content is write protected?), which is
inconveniently difficult to explain (needs digression into permissions)
