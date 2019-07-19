Miscallaneous file system operations
------------------------------------

With all of the information about symlinks and object trees,
you might be reluctant to perform usual file system managing
operations, such as copying, moving, or renaming a files or
directories.

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

What happens if I rename an annexed file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's try it. In Unix, renaming a file is exactly the same as
moving a file.

.. runrecord:: _examples/DL-101-114-101
   :language: console
   :workdir: dl-101/DataLad-101

   cd books/
   mv TLCL.pdf The_Linux_Command_Line.pdf
   ls -lah

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

In theory, we would need to do a ``datalad save`` at this point
to commit the "deletion" and the "new file". This however, is
suboptimal, and Git has built-in commands that provide a better
solution.

Lets revert the renaming of the the files:

.. runrecord:: _examples/DL-101-114-103
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git reset --hard master       # this restores TLCL.pdf
   $ rm The_Linux_Command_Line.pdf       # this removes the untracked copy

A more convenient way to rename files is the ``git mv`` command:

.. runrecord:: _examples/DL-101-114-104
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git mv TLCL.pdf The_Linux_Command_Line.pdf

.. runrecord:: _examples/DL-101-114-105
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ datalad status

We can see that the old file is still seen as "deleted", but the "new",
renamed file is "added". A ``git status`` displays the change
in the dataset a bit more accurate:

.. runrecord:: _examples/DL-101-114-106
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ git status

.. todo::

   can I mitigate a ``git commit`` here? I believe the best ``datalad save``
   command to save the renaming (without the rest of the dataset state) is
   ``datalad save -m "renamed TLCL to verbose title" The_Linux_Command_Line.pdf TLCL.pdf``,
   but this still requires listing all paths, and tab completion does not seem to work for
   the "deleted" files...

TODO

What happens if I rename a directory or subdataset?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What happens if I move files, directories, or subdatasets?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first question is easy. Because in Unix renaming is the same as moving,
moving works exactly like renaming in the examples with the PDFs described above.
Make sure to use ``git mv`` instead of ``mv``.

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
