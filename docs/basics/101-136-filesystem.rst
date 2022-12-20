.. _filesystem:

Miscellaneous file system operations
------------------------------------

With all of the information about symlinks and object trees,
you might be reluctant to perform usual file system managing
operations, such as copying, moving, renaming or deleting
files or directories with annexed content.

If I renamed one of those books, would the symlink that points
to the file content still be correct? What happens if I'd copy
an annexed file?
If I moved the whole ``books/`` directory? What if I moved
all of ``DataLad-101`` into a different place on my computer?
What if renamed the whole superdataset?
And how do I remove a file, or directory, or subdataset?

Therefore, there is an extra tutorial offered by the courses'
TA today, and you attend.
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
history -- be sure to execute these commands as well (and
be sure to be in the correct dataset).

Renaming files
^^^^^^^^^^^^^^

Let's try it. In Unix, renaming a file is exactly the same as
moving a file, and uses the :command:`mv` command.

.. runrecord:: _examples/DL-101-136-101
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: cd books/ && mv TLCL.pdf The_Linux_Command_Line.pdf && ls -lah --time-style=long-iso
   :notes: Let's look into file system operations. What does renaming does to a file that is symlinked?
   :cast: 03_git_annex_basics

   $ cd books/
   $ mv TLCL.pdf The_Linux_Command_Line.pdf
   $ ls -lah

Try to open the renamed file, e.g., with
``evince The_Linux_Command_Line.pdf``.
This works!

But let's see what changed in the dataset with this operation:

.. runrecord:: _examples/DL-101-136-102
   :language: console
   :workdir: dl-101/DataLad-101/books
   :notes: how does datalad see this? (deleted and untracked -- weird!!)
   :cast: 03_git_annex_basics

   $ datalad status

We can see that the old file is marked as ``deleted``, and
simultaneously, an ``untracked`` file appears: the renamed
PDF.

While this might appear messy, a ``datalad save`` will clean
all of this up. Therefore, do not panic if you rename a file,
and see a dirty dataset status with deleted and untracked files
-- ``datalad save`` handles these and other cases really well
under the hood.

.. runrecord:: _examples/DL-101-136-103
   :language: console
   :workdir: dl-101/DataLad-101/books
   :notes: datalad save rectifies the weird status
   :cast: 03_git_annex_basics

   $ datalad save -m "rename the book"

The :command:`datalad save` command will identify that a file was
renamed, and will summarize this nicely in the resulting commit:

.. runrecord:: _examples/DL-101-136-104
   :language: console
   :workdir: dl-101/DataLad-101/books
   :emphasize-lines: 8-11
   :notes: and this is how it looks like in the history
   :cast: 03_git_annex_basics

   $ git log -n 1 -p

Note that :command:`datalad save` commits all modifications when
it's called without a path specification,
so any other changes will be saved in the same commit as the rename.
If there are unsaved modifications you do not want to commit
together with the file name change, you could give both the
new and the deleted file as a path specification to
:command:`datalad save`, even if it feels unintuitive to
save a change that is marked as a deletion in a
:command:`datalad status`::

   datalad save -m "rename file" oldname newname

Alternatively, there is also a way to save the name change
only using Git tools only, outlined in the following hidden
section. If you are a Git user, you will be very familiar with it.

.. find-out-more:: Renaming with Git tools

   Git has built-in commands that provide a solution in two steps.

   If you have followed along with the previous :command:`datalad save`, let's revert the renaming of the the files:

   .. runrecord:: _examples/DL-101-136-105
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: We can also rename with git tools. first: reset history
      :cast: 03_git_annex_basics

      $ git reset --hard HEAD~1
      $ datalad status

   Now we're checking out how to rename files and commit this operation
   using only Git:
   A Git-specific way to rename files is the ``git mv`` command:

   .. runrecord:: _examples/DL-101-136-106
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: we use "git mv" instead of "mv" to rename
      :cast: 03_git_annex_basics

      $ git mv TLCL.pdf The_Linux_Command_Line.pdf

   .. runrecord:: _examples/DL-101-136-107
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: how does the modification appear to datalad now?
      :cast: 03_git_annex_basics

      $ datalad status

   We can see that the old file is still seen as "deleted", but the "new",
   renamed file is "added". A ``git status`` displays the change
   in the dataset a bit more accurately:

   .. runrecord:: _examples/DL-101-136-108
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: how does the modification appear to git?
      :cast: 03_git_annex_basics

      $ git status

   Because the :command:`git mv` places the change directly into the
   staging area (the *index*) of Git [#f1]_,
   a subsequent ``git commit -m "rename book"`` will write the renaming
   -- and only the renaming -- to the dataset's history, even if other
   (unstaged) modifications are present.

   .. runrecord:: _examples/DL-101-136-109
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: git mv put the modification to the staging area, we need to commit
      :cast: 03_git_annex_basics

      $ git commit -m "rename book"


To summarize, renaming files is easy and worry-free. Do not be intimidated
by a file marked as deleted -- a :command:`datalad save` will rectify this.
Be mindful of other modifications in your dataset, though, and either supply
appropriate paths to ``datalad save``, or use Git tools to exclusively save
the name change and nothing else.

Let's revert this now, to have a clean history.

.. runrecord:: _examples/DL-101-136-110
   :language: console
   :workdir: dl-101/DataLad-101/books
   :notes: (reverting again for clean history)
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1
   $ datalad status


Moving files from or into subdirectories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's move an annexed file from within ``books/`` into the root
of the superdataset:

.. runrecord:: _examples/DL-101-136-120
   :language: console
   :workdir: dl-101/DataLad-101/books
   :notes: Renaming was easy. How does moving files into different directories look like?
   :cast: 03_git_annex_basics

   $ mv TLCL.pdf ../TLCL.pdf
   $ datalad status

In general, this looks exactly like renaming or moving a file
in the same directory. There is a subtle difference though:
Currently, the symlink of the annexed file is broken. There
are two ways to demonstrate this. One is trying to open the
file -- this will currently fail. The second way is to look
at the symlink:

.. runrecord:: _examples/DL-101-136-121
   :language: console
   :workdir: dl-101/DataLad-101/books
   :realcommand: cd .. && ls -l --time-style=long-iso TLCL.pdf
   :notes: currently the symlink is broken! it points into nowhere
   :cast: 03_git_annex_basics

   $ cd ../
   $ ls -l TLCL.pdf

The first part of the symlink should point into the ``.git/``
directory, but currently, it does not -- the symlink still looks
like ``TLCL.pdf`` would be within ``books/``. Instead of pointing
into ``.git``, it currently points to ``../.git``, which is non-existent,
and even outside of the superdataset. This is why the file
cannot be opened: When any program tries to follow the symlink,
it will not resolve, and an error such as "no file or directory"
will be returned. But do not panic! A :command:`datalad save` will
rectify this as well:

.. runrecord:: _examples/DL-101-136-122
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: datalad save -m "moved book into root" && ls -l --time-style=long-iso TLCL.pdf
   :notes: but a save rectifies it
   :cast: 03_git_annex_basics

   $ datalad save -m "moved book into root"
   $ ls -l TLCL.pdf

After a ``datalad save``, the symlink is fixed again.
Therefore, in general, whenever moving or renaming a file,
especially between directories, a ``datalad save`` is
the best option to turn to.
Therefore, while it might be startling
if you've moved a file and can not open it directly afterwards, everything
will be rectified by :command:`datalad save` as well.

.. find-out-more:: Why a move between directories is actually a content change

   Let's see how this shows up in the dataset history:

   .. runrecord:: _examples/DL-101-136-123
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: moving files across directory levels is a content change because the symlink changes!
      :cast: 03_git_annex_basics

      $ git log -n 1 -p

   As you can see, this action does not show up as a move, but instead
   a deletion and addition of a new file. Why? Because the content
   that is tracked is the actual symlink, and due to the change in
   relative location, the symlink needed to change. Hence, what looks
   and feels like a move on the file system for you is actually a
   move plus a content change for Git.


.. gitusernote:: git annex fix

   A :command:`datalad save` command internally uses a :command:`git commit` to save changes to a dataset.
   :command:`git commit` in turn triggers a :command:`git annex fix`
   command. This git-annex command fixes up links that have become broken
   to again point to annexed content, and is responsible for cleaning up
   what needs to be cleaned up. Thanks, git-annex!

Finally, let's clean up:

.. runrecord:: _examples/DL-101-136-124
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: (reset history)
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1

Moving files across dataset boundaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Generally speaking, moving files across dataset hierarchies is not advised.
While DataLad blurs the dataset boundaries to ease working in nested dataset,
the dataset boundaries do still exist. If you move a file from one subdataset
into another, or up or down a dataset hierarchy, you will move it out of the
version control it was in (i.e., from one ``.git`` directory into a different
one). From the perspective of the first subdataset, the file will be deleted,
and from the perspective of the receiving dataset, the file will be added to
the dataset, but straight out of nowhere, with none of its potential history
from its original dataset attached to it. Before moving a file, consider whether
*copying* it (outlined in the next but one paragraph) might be a more suitable
alternative.

If you are willing to sacrifice [#f2]_ the file's history and move it to a
different dataset, the procedure differs between annexed files, and files
stored in Git.

For files that Git manages, moving and saving is simple: Move the file, and
save the resulting changes in *both* affected datasets (this can be done with
a recursive :command:`save` from a top-level dataset, though).

.. runrecord:: _examples/DL-101-136-125
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: move files across dataset boundaries
   :cast: 03_git_annex_basics

   $ mv notes.txt midterm_project/notes.txt
   $ datalad status -r

.. runrecord:: _examples/DL-101-136-127
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: save recursively
   :cast: 03_git_annex_basics

   $ datalad save -r -m "moved notes.txt from root of top-ds to midterm subds"

Note how the history of ``notes.txt`` does not exist in the subdataset -- it appears
as if the file was generated at once, instead of successively over the course:

.. runrecord:: _examples/DL-101-136-128
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: show history is vanished
   :cast: 03_git_annex_basics

   $ cd midterm_project
   $ git log notes.txt

(Undo-ing this requires ``git reset``\s in *both* datasets)

.. runrecord:: _examples/DL-101-136-129
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :notes: clean-up
   :cast: 03_git_annex_basics

   # in midterm_project
   $ git reset --hard HEAD~

   # in DataLad-101
   $ cd ../
   $ git reset --hard HEAD~

The process is a bit more complex for annexed files. Let's do it wrong, first:
What happens if we move an annexed file in the same way as ``notes.txt``?

.. runrecord:: _examples/DL-101-136-130
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: move an annexed file wrongly
   :cast: 03_git_annex_basics

   $ mv books/TLCL.pdf midterm_project
   $ datalad status -r

.. runrecord:: _examples/DL-101-136-131
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: save - wrong way still
   :cast: 03_git_annex_basics

   $ datalad save -r -m "move annexed file around"

At this point, this does not look that different to the result of moving
``notes.txt``. Note, though, that the deleted and untracked PDFs are symlinks --
and therein lies the problem: What was moved was not the file content (which is
still in the annex of the top-level dataset, ``DataLad-101``), but its symlink that
was stored in Git. After moving the file, the symlink is broken, and git-annex
has no way of finding out where the file content could be:

.. runrecord:: _examples/DL-101-136-132
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: demonstrate broken symlink with git-annex-whereis
   :cast: 03_git_annex_basics

   $ cd midterm_project
   $ git annex whereis TLCL.pdf

Let's rewind, and find out how to do it correctly:

.. runrecord:: _examples/DL-101-136-133
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :notes: undo wrong moving of annex file
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~
   $ cd ../
   $ git reset --hard HEAD~

The crucial step to remember is to get the annexed file out of the annex prior
to moving it. For this, we need to fall back to git-annex commands:

.. runrecord:: _examples/DL-101-136-134
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: unannex file
   :cast: 03_git_annex_basics

   $ git annex unlock books/TLCL.pdf
   $ mv books/TLCL.pdf midterm_project
   $ datalad status -r

Afterwards, a (recursive) :command:`save` commits the removal of the book from
DataLad-101, and adds the file content into the annex of ``midterm_project``:

.. runrecord:: _examples/DL-101-136-135
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: save annex file after moving it to subdataset

   $ datalad save -r -m "move book into midterm_project"

Even though you did split the file's history, at least its content is in the
correct dataset now:

.. runrecord:: _examples/DL-101-136-136
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: show that moving after unannex worked with git annex whereis

   $ cd midterm_project
   $ git annex whereis TLCL.pdf

But more than showing you how it can be done, if necessary, this paragraph
hopefully convinced you that moving files across dataset boundaries is not
convenient. It can be a confusing and potentially "file-content-losing"-dangerous
process, but it also dissociates a file from its provenance that is captured
in its previous dataset, with no machine-readable way to learn about the move
easily. A better alternative may be copying files with the :command:`datalad copy-file`
command introduced in detail in :ref:`copyfile`, and demonstrated in the next
but one paragraph. Let's quickly clean up by moving the file back:

.. runrecord:: _examples/DL-101-136-137
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :notes: move file back

   # in midterm_project
   $ git annex unannex TLCL.pdf

.. runrecord:: _examples/DL-101-136-138
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :notes: move file back

   $ mv TLCL.pdf ../books
   $ cd ../
   $ datalad save -r -m "move book back from midterm_project"


Copying files
^^^^^^^^^^^^^

Let's create a copy of an annexed file, using the Unix
command ``cp`` to copy.

.. runrecord:: _examples/DL-101-136-140
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: renaming and moving was fine, how about copying?
   :cast: 03_git_annex_basics

   $ cp books/TLCL.pdf copyofTLCL.pdf
   $ datalad status

That's expected. The copy shows up as a new, untracked
file. Let's save it:

.. runrecord:: _examples/DL-101-136-141
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: status says there's an untracked file, let's save it
   :cast: 03_git_annex_basics


   $ datalad save -m "add copy of TLCL.pdf"

.. runrecord:: _examples/DL-101-136-142
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: That's it!
   :cast: 03_git_annex_basics

   $ git log -n 1 -p

That's it.

.. find-out-more:: Symlinks!

   If you have read the additional content in the section
   :ref:`symlink`, you know that the same file content
   is only stored once, and copies of the same file point to
   the same location in the object tree.

   Let's check that out:

   .. runrecord:: _examples/DL-101-136-143
      :language: console
      :workdir: dl-101/DataLad-101
      :realcommand: ls -l --time-style=long-iso copyofTLCL.pdf && ls -l --time-style=long-iso books/TLCL.pdf
      :notes: A cool thing is that the two identical files link to the same place in the object tree
      :cast: 03_git_annex_basics

      $ ls -l copyofTLCL.pdf
      $ ls -l books/TLCL.pdf

   Indeed! Apart from their relative location (``.git`` versus
   ``../.git``) their symlink is identical. Thus, even though two
   copies of the book exist in your dataset, your disk needs to
   store it only once.

   In most cases, this is just an interesting fun-fact, but beware
   when dropping content with :command:`datalad drop`
   (:ref:`remove`):
   If you drop the content of one copy of a file, all
   other copies will lose this content as well.

Finally, let's clean up:

.. runrecord:: _examples/DL-101-136-144
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: (reset history)
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1

.. _copyfileFS:

Copying files across dataset boundaries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. importantnote:: copy-file availability

   :command:`datalad copy-file` requires DataLad version ``0.13.0`` or higher.

Instead of moving files across dataset boundaries, *copying* them is an easier
and -- **beginning with DataLad version 0.13.0** -- actually supported method.
The DataLad command that can be used for this is :command:`datalad copy-file`
(:manpage:`datalad-copy-file` manual). This command allows to copy files
(from any dataset or non-dataset location, annexed or not annexed) into a dataset.
If the file is copied from a dataset and is annexed, its availability metadata
is added to the new dataset as well, and there is no need for unannex'ing the
or even retrieving its file contents. Let's see this in action for a file
stored in Git, and a file stored in annex:

.. runrecord:: _examples/DL-101-136-145
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad copy-file notes.txt midterm_project -d midterm_project

.. runrecord:: _examples/DL-101-136-146
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad copy-file books/bash_guide.pdf midterm_project -d midterm_project

Both files have been successfully transferred and saved to the subdataset, and
no unannexing was necessary.
Note, though, that ``notes.txt`` was annexed in the subdataset, as this subdataset
was not configured with the ``text2git`` :term:`run procedure`.

.. runrecord:: _examples/DL-101-136-147
   :language: console
   :workdir: dl-101/DataLad-101

   $ tree midterm_project

The subdataset has two new commits as :command:`datalad copy-file` can take care
of saving changes in the copied-to dataset, and thus the new subdataset state
would need to be saved in the superdataset.

.. runrecord:: _examples/DL-101-136-148
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status -r

Still, just as when we *moved* files across dataset boundaries, the files'
provenance record is lost:

.. runrecord:: _examples/DL-101-136-149
   :language: console
   :workdir: dl-101/DataLad-101

   $ cd midterm_project
   $ git log notes.txt

Nevertheless, copying files with :command:`datalad copy-file` is easier and safer
than moving them with standard Unix commands, especially so for annexed files.
A more detailed introduction to :command:`datalad copy-file` and a concrete
usecase can currently be found in :ref:`copyfile`.

Let's clean up:

.. runrecord:: _examples/DL-101-136-150
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ git reset --hard HEAD~2


Moving/renaming a subdirectory or subdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moving or renaming subdirectories, especially if they are subdatasets,
*can* be a minefield. But in principle, a safe way to proceed is using
the Unix :command:`mv` command to move or rename, and the :command:`datalad save`
to clean up afterwards, just as in the examples above. Make sure to
**not** use ``git mv``, especially for subdatasets.

Let's for example rename the ``books`` directory:

.. runrecord:: _examples/DL-101-136-151
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: renaming and moving subdirectories and subdatasets can be a minefield, but is usually okay: let's change the name of books to readings
   :cast: 03_git_annex_basics

   $ mv books/ readings
   $ datalad status

.. runrecord:: _examples/DL-101-136-152
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: a save rectifies everything
   :cast: 03_git_annex_basics

   $ datalad save -m "renamed directory"

This is easy, and complication free. Moving (as in: changing the location, instead of
the name) the directory would work in the
same fashion, and a :command:`datalad save` would fix broken symlinks afterwards.
Let's quickly clean this up:

.. runrecord:: _examples/DL-101-136-153
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: (quickly clean up)
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1

But let's now try to move the ``longnow`` subdataset into the root of the
superdataset:

.. runrecord:: _examples/DL-101-136-154
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: But what about renaming or moving a subdataset? Let's move longnow into the root of the dataset
   :cast: 03_git_annex_basics

   $ mv recordings/longnow .
   $ datalad status

.. runrecord:: _examples/DL-101-136-155
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: a save will work and rectify things ...
   :cast: 03_git_annex_basics

   $ datalad save -m "moved subdataset"

.. runrecord:: _examples/DL-101-136-156
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 03_git_annex_basics

   $ datalad status

This seems fine, and it has indeed worked.
However, *reverting* a commit like this is tricky, at the moment. This could
lead to trouble if you at a later point try to revert or rebase chunks of your
history including this move. Therefore, if you can, try not to move subdatasets
around. For now we'll clean up in a somewhat "hacky" way: Reverting, and
moving remaining subdataset contents back to their original place by hand
to take care of the unwanted changes the commit reversal introduced.

.. runrecord:: _examples/DL-101-136-157
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: BUT reverting such a commit in the history can be tricky atm:
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1

.. runrecord:: _examples/DL-101-136-158
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: we have to move the remaining subdataset contents back to the original place
   :cast: 03_git_annex_basics

   $ mv -f longnow recordings


The take-home message therefore is that it is best not to move subdatasets,
but very possible to move subdirectories if necessary. In both cases, do not
attempt moving with the :command:`git mv`, but stick with :command:`mv` and
a subsequent :command:`datalad save`.

.. todo::

   Update this when progress has been made towards
   https://github.com/datalad/datalad/issues/3464


Moving/renaming a superdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once created, a DataLad superdataset may not be in an optimal
place on your file system, or have the best name.

After a while, you might think that the dataset would fit much
better into ``/home/user/research_projects/`` than in
``/home/user/Documents/MyFiles/tmp/datalad-test/``. Or maybe at
some point, a long name such as ``My-very-first-DataLad-project-wohoo-I-am-so-excited``
does not look pretty in your terminal prompt anymore, and going for
``finance-2019`` seems more professional.

These will be situations in which you want to rename or move
a superdataset. Will that break anything?

In all standard situations, no, it will be completely fine.
You can use standard Unix commands such as ``mv`` to do it,
and also whichever graphical user interface or explorer you may
use.

Beware of one thing though: If your dataset either is a sibling
or has a sibling with the source being a path, moving or renaming
the dataset will break the linkage between the datasets. This can
be fixed easily though. We can try this in the following hidden
section.

.. find-out-more:: If a renamed/moved dataset is a sibling...

   As section :ref:`config` explains, each
   sibling is registered in ``.git/config`` in a "submodule" section.
   Let's look at how our sibling "roommate" is registered there:

   .. runrecord:: _examples/DL-101-136-160
      :language: console
      :workdir: dl-101/DataLad-101
      :emphasize-lines: 18-19

      $ cat .git/config

   As you can see, its "url" is specified as a relative path. Say your
   room mate's directory is a dataset you would want to move. Let's see
   what happens if we move the dataset such that the path does not point
   to the dataset anymore:

   .. runrecord:: _examples/DL-101-136-161
      :language: console
      :workdir: dl-101/DataLad-101

      # add an intermediate directory
      $ cd ../mock_user
      $ mkdir onemoredir
      # move your room mates dataset into this new directory
      $ mv DataLad-101 onemoredir

   This means that relative to your ``DataLad-101``, your room mates
   dataset is not at ``../mock_user/DataLad-101`` anymore, but in
   ``../mock_user/onemoredir/DataLad-101``. The path specified in
   the configuration file is thus wrong now.

   .. runrecord:: _examples/DL-101-136-162
      :language: console
      :workdir: dl-101/mock_user

      # navigate back into your dataset
      $ cd ../DataLad-101
      # attempt a datalad update
      $ datalad update

   Here we go::

      'fatal: '../mock_user/DataLad-101' does not appear to be a git repository
       fatal: Could not read from remote repository.

   Git seems pretty insistent (given the amount of error messages) that
   it can not seem to find a Git repository at the location the ``.git/config``
   file specified. Luckily, we can provide this information. Edit the file with
   an editor of your choice and fix the path from
   ``url = ../mock_user/DataLad-101`` to
   ``url = ../mock_user/onemoredir/DataLad-101``.

   Below, we are using the stream editor `sed <https://en.wikipedia.org/wiki/Sed>`_
   for this operation.

   .. runrecord:: _examples/DL-101-136-163
      :language: console
      :workdir: dl-101/DataLad-101

      $ sed -i 's/..\/mock_user\/DataLad-101/..\/mock_user\/onemoredir\/DataLad-101/' .git/config

   This is how the file looks now:

   .. runrecord:: _examples/DL-101-136-164
      :language: console
      :workdir: dl-101/DataLad-101

      $ cat .git/config

   Let's try to update now:

   .. runrecord:: _examples/DL-101-136-165
      :workdir: dl-101/DataLad-101
      :language: console

      $ datalad update

   Nice! We fixed it!
   Therefore, if a dataset you move or rename is known to other
   datasets from its path, or identifies siblings with paths,
   make sure to adjust them in the ``.git/config`` file.

   To clean up, we'll redo the move of the dataset and the
   modification in ``.git/config``.

   .. runrecord:: _examples/DL-101-136-166
      :language: console
      :workdir: dl-101/DataLad-101

      $ cd ../mock_user && mv onemoredir/DataLad-101 .
      $ rm -r onemoredir
      $ cd ../DataLad-101 && sed -i 's/..\/mock_user\/onemoredir\/DataLad-101/..\/mock_user\/DataLad-101/' .git/config


Getting contents out of git-annex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Files in your dataset can either be handled by :term:`Git` or :term:`Git-annex`.
Self-made or predefined configurations to ``.gitattributes``, defaults, or the
``--to-git`` option to :command:`datalad save` allow you to control which tool
does what on up to single-file basis. Accidentally though, you may give a file of yours
to git-annex when it was intended to be stored in Git, or you want to get a previously
annexed file into Git.

Consider you intend to share the cropped ``.png`` images you created from the
``longnow`` logos. Would you publish your ``DataLad-101`` dataset so :term:`GitHub`
or :term:`GitLab`, these files would not be available to others, because annexed
dataset contents can not be published to these services.
Even though you could find a third party service of your choice
and publish your dataset *and* the annexed data (see section :ref:`sharethirdparty`),
you're feeling lazy today. And since it
is only two files, and they are quite small, you decide to store them in Git --
this way, the files would be available without configuring an external data
store.

To get contents out of the dataset's annex you need to *unannex* them. This is
done with the git-annex command :command:`git annex unannex`. Let's see how it
works:

.. runrecord:: _examples/DL-101-136-167
   :language: console
   :workdir: dl-101/DataLad-101

   $ git annex unannex recordings/*logo_small.jpg

Your dataset's history records the unannexing of the files.

.. runrecord:: _examples/DL-101-136-168
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -p -n 1

Once files have been unannexed, they are "untracked" again, and you can save them
into Git, either by adding a rule to ``.gitattributes``, or with
:command:`datalad save --to-git`:

.. runrecord:: _examples/DL-101-136-169
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save --to-git -m "save cropped logos to Git" recordings/*jpg


Deleting (annexed) files/directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removing annexed file content from a dataset is possible in two different ways:
Either by removing the file from the current state of the repository
(which Git calls the *worktree*) but keeping the content in the history
of the dataset, or by removing content entirely from a dataset and its
history.

Removing a file, but keeping content in history
"""""""""""""""""""""""""""""""""""""""""""""""

An ``rm <file>`` or ``rm -rf <directory>`` with a subsequent :command:`datalad save`
will remove a file or directory, and save its removal. The file content however will
still be in the history of the dataset, and the file can be brought back to existence
by going back into the history of the dataset or reverting the removal commit:

.. runrecord:: _examples/DL-101-136-170
   :workdir: dl-101/DataLad-101
   :notes: 2 ways to remove a file from dataset: remove the file from the current state of the repository (the *worktree*) but keeping the content in the history, or remove content entirely from a dataset and its history.
   :cast: 03_git_annex_basics

   # download a file
   $ datalad download-url -m "Added flower mosaic from wikimedia" \
     https://upload.wikimedia.org/wikipedia/commons/a/a5/Flower_poster_2.jpg \
     --path flowers.jpg
   $ ls -l flowers.jpg

.. runrecord:: _examples/DL-101-136-171
   :workdir: dl-101/DataLad-101
   :language: console
   :cast: 03_git_annex_basics


   # removal is easy:
   $ rm flowers.jpg

This will lead to a dirty dataset status:

.. runrecord:: _examples/DL-101-136-172
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: the deletion looks like this for datalad
   :cast: 03_git_annex_basics

   $ datalad status

If a removal happened by accident, a ``git checkout -- flowers.jpg`` would undo
the removal at this stage. To stick with the removal and clean up the dataset
state, :command:`datalad save` will suffice:

.. runrecord:: _examples/DL-101-136-173
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: a save will write the deletion of the file to history, but keep the content.
   :cast: 03_git_annex_basics

   $ datalad save -m "removed file again"

This commits the deletion of the file in the dataset's history.
If this commit is reverted, the file comes back to existence:

.. runrecord:: _examples/DL-101-136-174
   :language: console
   :workdir: dl-101/DataLad-101
   :emphasize-lines: 6
   :notes: reverting the last action will bring back the file content:
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~1
   $ ls

In other words, with an :command:`rm` and subsequent :command:`datalad save`,
the symlink is removed, but the content is retained in the history.

.. _remove:

Removing annexed content entirely
"""""""""""""""""""""""""""""""""

.. index:: ! datalad command; drop

The command to remove file content entirely and irreversibly from a repository is
the :command:`datalad drop` command (:manpage:`datalad-drop` manual).
This command will delete the content stored in the annex of the dataset,
and can be very helpful to make a dataset more lean if the file content is
either irrelevant or can be retrieved from other sources easily. Think about a
situation in which a very large result file is computed by default
in some analysis, but is not relevant for any project, and can thus be removed.
Or if only the results of an analysis need to be kept, but the file contents from
its input datasets can be dropped at these input datasets are backed-up else
where. Because the command works on annexed contents, it will drop file *content*
from a dataset, but it will retain the symlink for this file (as this symlink
is stored in Git).

:command:`drop` can take any number of files.
If an entire dataset is specified, all file content in sub-*directories* is
dropped automatically, but for content in sub-*datasets* to be dropped, the
``-r/--recursive`` flag has to be included.
By default, DataLad will not drop any content that does not have at least
one verified remote copy that the content could be retrieved from again.
It is possible to drop the downloaded image, because thanks to
:command:`datalad download-url` its original location in the web is known:

.. runrecord:: _examples/DL-101-136-175
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: to drop content entirely we use datalad drop
   :cast: 03_git_annex_basics

   $ datalad drop flowers.jpg

Currently, the file content is gone, but the symlink still exist. Opening the
remaining symlink will fail, but the content can be obtained easily again with
:command:`datalad get`:

.. runrecord:: _examples/DL-101-136-176
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: this will keep the symlink, but drop the content, making the dataset lean
   :cast: 03_git_annex_basics

   $ datalad get flowers.jpg

If a file has no verified remote copies, DataLad will only drop its
content if the user enforces it.
DataLad versions prior to ``0.16`` need to enforce dropping using the ``--nocheck`` option, while DataLad version ``0.16`` and up need to enforce dropping using the ``--reckless [MODE]`` option, where ``[MODE]`` is either ``modification`` (drop despite unsaved modifications) ``availability`` (drop even though no other copy is known) ``undead`` (only for datasets; would drop a dataset without announcing its death to linked dataset clones) or ``kill`` (no safety checks at all are run).
While the ``--reckless`` parameter sounds more complex, it ensures a safer operation than the previous ``--nocheck`` implementation.
We will demonstrate this by generating a random PDF file:

.. runrecord:: _examples/DL-101-136-177
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: the content could be dropped bc the file was obtained with datalad, and dl knows where to retrieve the file again. If this isn't the case, datalad will complain. Let's try:
   :cast: 03_git_annex_basics

   $ convert xc:none -page Letter a.pdf
   $ datalad save -m "add empty pdf"

DataLad will safeguard dropping content that it can not retrieve again:

.. runrecord:: _examples/DL-101-136-178
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: datalad does not know how to re-obtain the file, so it complains
   :cast: 03_git_annex_basics

   $ datalad drop a.pdf

But with ``--nocheck`` (for ``<0.16``) or ``--reckless availability`` (for ``0.16`` and higher) it will work:

.. runrecord:: _examples/DL-101-136-179
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: the --nocheck/--reckless flag lets us drop content anyway. This content is gone forever now, though!
   :cast: 03_git_annex_basics

   $ datalad drop --reckless availability a.pdf

Note though that this file content is irreversibly gone now, and
even going back in time in the history of the dataset will not bring it
back into existence.

Finally, let's clean up:

.. runrecord:: _examples/DL-101-136-180
   :workdir: dl-101/DataLad-101
   :language: console
   :notes: let's clean up
   :cast: 03_git_annex_basics

   $ git reset --hard HEAD~2

Deleting content stored in Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is much harder to delete dataset content that is stored in Git compared to
content stored in git-annex.
Operations such as ``rm`` or ``git rm`` remove the file from the *worktree*,
but not from its history, and they can be brought back to life just as annexed
contents that were solely ``rm``\'ed. There is also no straightforward
Git equivalent of ``drop``.
To accomplish a complete removal of a file from a dataset, we recommend the external tool
`git-filter-repo <https://github.com/newren/git-filter-repo>`_.
It is a powerful and potentially very dangerous tool to rewrite Git history.

Usually, removing files stored in Git completely
is not a common or recommended operation, as it involves quite aggressive
rewriting of the dataset history. Sometimes, however, sensitive files, for example
private :term:`SSH key`\s or passwords, or too many or too large files are
accidentally saved into Git, and *need* to get out of the dataset history.
The command ``git-filter-repo <path-specification> --force`` will "filter-out",
i.e., remove all files **but the ones specified** in ``<path-specification>``
from the dataset's history. The section :ref:`cleanup` shows an example
invocation. If you want to use it, however, make sure to attempt it in a dataset
clone or with its ``--dry-run`` flag first. It is easy to lose dataset history
and files with this tool.

Uninstalling or deleting subdatasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: ! datalad command; uninstall

Depending on the exact aim, two commands are of relevance for
deleting a DataLad subdataset. The softer (and not so much "deleting" version)
is to uninstall a dataset with the :command:`datalad uninstall`
(:manpage:`datalad-uninstall` manual).
This command can be used to uninstall any number of
*subdatasets*. Note though that only subdatasets can be uninstalled; the command
will error if given a sub-*directory*, a file, or a top-level dataset.

.. runrecord:: _examples/DL-101-136-181
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: To get rid of subdatasets one can either uninstall or remove them. let's clone one to see:
   :cast: 03_git_annex_basics

   # clone a subdataset - the content is irrelevant, so why not a cloud :)
   $ datalad clone -d . \
    https://github.com/datalad-datasets/disneyanimation-cloud.git \
    cloud

To uninstall the dataset, use

.. runrecord:: _examples/DL-101-136-182
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: uninstall uninstalls the dataset, but it is still registered in the superdataset. a dl install will get the dataset again!
   :cast: 03_git_annex_basics

   $ datalad uninstall cloud

Note that the dataset is still known in the dataset, and not completely removed.
A ``datalad get [-n/--no-data] cloud`` would install the dataset again.

.. index:: ! datalad command; remove

In case one wants to fully delete a subdataset from a dataset, the
:command:`datalad remove` command (:manpage:`datalad-remove` manual) is
relevant [#f3]_.
It needs a pointer to the root of the superdataset with the ``-d/--dataset``
flag, a path to the subdataset to be removed, and optionally a commit message
(``-m/--message``) or recursive specification (``-r/--recursive``).
To remove a subdataset, we will install the uninstalled subdataset again, and
subsequently remove it with the :command:`datalad remove` command:

.. runrecord:: _examples/DL-101-136-183
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: to completely remove the dataset, use datalad remove
   :cast: 03_git_annex_basics

   $ datalad get -n cloud

.. runrecord:: _examples/DL-101-136-184
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: to completely remove the dataset, use datalad remove
   :cast: 03_git_annex_basics

   # delete the subdataset
   $ datalad remove -m "remove obsolete subds" -d . cloud

Note that for both commands a pointer to the *current directory* will not work.
``datalad remove .`` or ``datalad uninstall .`` will fail, even if
the command is executed in a subdataset instead of the top-level
superdataset -- you need to execute the command from a higher-level directory.


Deleting a superdataset
^^^^^^^^^^^^^^^^^^^^^^^

If for whatever reason you at one point tried to remove a DataLad dataset,
whether with a GUI or the command line call ``rm -rf <directory>``, you likely
have seen permission denied errors such as

.. code-block::

    rm: cannot remove '<directory>/.git/annex/objects/Mz/M1/MD5E-s422982--2977b5c6ea32de1f98689bc42613aac7.jpg/MD5E-s422982--2977b5c6ea32de1f98689bc42613aac7.jpg': Permission denied
    rm: cannot remove '<directory>/.git/annex/objects/FP/wv/MD5E-s543180--6209797211280fc0a95196b0f781311e.jpg/MD5E-s543180--6209797211280fc0a95196b0f781311e.jpg': Permission denied
    [...]

This error indicates that there is write-protected content within ``.git`` that
cannot not be deleted. What is this write-protected content? It's the file content
stored in the object tree of git-annex. If you want, you can re-read the section on
:ref:`symlink` to find out how git-annex revokes write permission for the user
to protect the file content given to it. To remove a dataset with annexed content
one has to regain write permissions to everything in the dataset. This is done
with the `chmod <https://en.wikipedia.org/wiki/Chmod>`_ command::

    chmod -R u+w <dataset>

This *recursively* (``-R``, i.e., throughout all files and (sub)directories) gives users
(``u``) write permissions (``+w``) for the dataset.

Afterwards, ``rm -rf <dataset>`` will succeed.

However, instead of ``rm -rf``, a faster way to remove a dataset is using
:command:`datalad remove`: Run ``datalad remove <dataset>`` outside of the
superdataset to remove a top-level dataset with all its contents. Likely,
both  ``--recursive`` and ``--nocheck`` (for DataLad versions ``<0.16``) or ``--reckless [availability|undead|kill]`` (for DataLad versions ``0.16`` and higher) flags are necessary
to traverse into subdatasets and to remove content that does not have verified remotes.

Be aware though that both ways to delete a dataset will
irretrievably delete the dataset, it's contents, and it's history.

Summary
^^^^^^^

To sum up, file system management operations are safe and easy.
Even if you are currently confused about one or two operations,
worry not -- the take-home-message is simple: Use ``datalad save``
whenever you move or rename files. Be mindful that a ``datalad status``
can appear unintuitive or that symlinks can break if annexed files are moved,
but all of these problems are solved after a :command:`datalad save` command.
Apart from this command, having a clean dataset status prior to doing anything
is your friend as well. It will make sure that you have a neat and organized
commit history, and no accidental commits of changes unrelated to your file
system management operations. The only operation you should beware of is
moving subdatasets around -- this can be a minefield.
With all of these experiences and tips, you feel confident that you know
how to handle your datasets files and directories well and worry-free.

.. rubric:: Footnotes

.. [#f1] If you want to learn more about the Git-specific concepts of *worktree*,
         *staging area*/*index* or *HEAD*, the upcoming section :ref:`history` will
         talk briefly about them and demonstrate helpful commands.

.. [#f2] Or rather: split -- basically, the file is getting a fresh new start.
         Think of it as some sort of witness-protection program with complete
         disrespect for provenance...

.. [#f3] This is indeed the only case in which :command:`datalad remove` is
         relevant. For all other cases of content deletion a normal ``rm``
         with a subsequent :command:`datalad save` works best.
