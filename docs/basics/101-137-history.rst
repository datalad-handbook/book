.. _history:

Back and forth in time
----------------------


Almost everyone inadvertently deleted or overwrote files at some point with
a hasty operation that caused data fatalities or at least troubles to
re-obtain or restore data.
With DataLad, no mistakes are forever: One powerful feature of datasets
is the ability to revert data to a previous state and thus view earlier content or
correct mistakes. As long as the content was version controlled (i.e., tracked),
it is possible to look at previous states of the data, or revert changes --
even years after they happened -- thanks to the underlying version control
system :term:`Git`.

.. figure:: ../artwork/src/versioncontrol.svg
   :width: 70%

To get a glimpse into how to work with the history of a dataset, today's lecture
has an external Git-expert as a guest lecturer.
"I do not have enough time to go through all the details in only
one lecture. But I'll give you the basics, and an idea of what is possible.
Always remember: Just google what you need. You will find thousands of helpful tutorials
or questions on `Stack Overflow <https://stackoverflow.com>`_ right away.
Even experts will *constantly* seek help to find out which Git command to
use, and how to use it.", he reassures with a wink.

The basis of working with the history is to *look at it* with tools such
as :term:`tig`, :term:`gitk`, or simply the :command:`git log` command.
The most important information in an entry (commit) in the history is
the :term:`shasum` (or hash) associated with it.
This hash is how dataset modifications in the history are identified,
and with this hash you can communicate with DataLad or :term:`Git` about these
modifications or version states [#f1]_.
Here is an excerpt from the ``DataLad-101`` history to show a
few abbreviated hashes of the 15 most recent commits [#f2]_:

.. runrecord:: _examples/DL-101-137-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ git log -15 --oneline


"I'll let you people direct this lecture", the guest lecturer proposes.
"You tell me what you would be interested in doing, and I'll show you how it's
done. For the rest of the lecture, call me Google!"

Fixing (empty) commit messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From the back of the lecture hall comes a question you're really glad
someone asked: "It has happened to me that I accidentally did a
:command:`datalad save` and forgot to specify the commit message,
how can I fix this?".
The room nods in agreement -- apparently, others have run into this
premature slip of the ``Enter`` key as well.

Let's demonstrate a simple example. First, let's create some random files.
Do this right in your dataset.

.. runrecord:: _examples/DL-101-137-102
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT > Gitjoke1.txt
   Git knows what you did last summer!
   EOT

   $ cat << EOT > Gitjoke2.txt
   Knock knock. Who's there? Git.
   Git-who?
   Sorry, 'who' is not a git command - did you mean 'show'?
   EOT

   $ cat << EOT > Gitjoke3.txt
   In Soviet Russia, git commits YOU!
   EOT

This will generate three new files in your dataset. Run a
:command:`datalad status` to verify this:

.. runrecord:: _examples/DL-101-137-103
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

And now:

.. runrecord:: _examples/DL-101-137-104
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save

Whooops! A :command:`datalad save` without a
commit message that saved all of the files.

.. runrecord:: _examples/DL-101-137-105
   :language: console
   :workdir: dl-101/DataLad-101
   :emphasize-lines: 6

   $ git log -p -1

As expected, all of the modifications present prior to the
command are saved into the most recent commit, and the commit
message DataLad provides by default, ``[DATALAD] Recorded changes``,
is not very helpful.

Changing the commit message of the most recent commit can be done with
the command :command:`git commit --amend`. Running this command will open
an editor (the default, as configured in Git), and allow you
to change the commit message. Make sure to read the :ref:`find-out-more on changing other than the most recent commit <fom-rebase1>` in case you want to improve the commit message of more commits than only the latest.

Try running the :command:`git commit --amend` command right now and give
the commit a new commit message (you can just delete the one created by
DataLad in the editor)!

.. find-out-more:: Changing the commit messages of not-the-most-recent commits
   :name: fom-rebase1
   :float:

   The :command:`git commit --amend` command will let you
   rewrite the commit message of the most recent commit. If you
   however need to rewrite commit messages of older commits, you
   can do so during a so-called "interactive rebase" [#f4]_. The command
   for this is

   .. code-block:: bash

      $ git rebase -i HEAD~N

   where ``N`` specifies how far back you want to rewrite commits.
   ``git rebase -i HEAD~3`` for example lets you apply changes to the
   any number of commit messages within the last three commits.

   Be aware that an interactive rebase lets you *rewrite* history.
   This can lead to confusion or worse if the history you are rewriting
   is shared with others, e.g., in a collaborative project. Be also aware
   that rewriting history that is *pushed*/*published* (e.g., to GitHub)
   will require a force-push!

   Running this command gives you a list of the N most recent commits
   in your text editor (which may be :term:`vim`!), sorted with
   the most recent commit on the bottom.
   This is how it may look like:

   .. code-block:: bash

      pick 8503f26 Add note on adding siblings
      pick 23f0a52 add note on configurations and git config
      pick c42cba4 add note on DataLad's procedures

      # Rebase b259ce8..c42cba4 onto b259ce8 (3 commands)
      #
      # Commands:
      # p, pick <commit> = use commit
      # r, reword <commit> = use commit, but edit the commit message
      # e, edit <commit> = use commit, but stop for amending
      # s, squash <commit> = use commit, but meld into previous commit
      # f, fixup <commit> = like "squash", but discard this commit's log message
      # x, exec <command> = run command (the rest of the line) using shell
      # b, break = stop here (continue rebase later with 'git rebase --continue')
      # d, drop <commit> = remove commit
      # l, label <label> = label current HEAD with a name

   An interactive rebase allows to apply various modifying actions to any
   number of commits in the list. Below the list are descriptions of these
   different actions. Among them is "reword", which lets you "edit the commit
   message". To apply this action and reword the top-most commit message in this list
   (``8503f26 Add note on adding siblings``, three commits back in the history),
   exchange the word ``pick`` in the beginning of the line with the word
   ``reword`` or simply ``r`` like this::

      r 8503f26 Add note on adding siblings

   If you want to reword more than one commit message, exchange several
   ``pick``\s. Any commit with the word ``pick`` at the beginning of the line will
   be kept as is. Once you are done, save and close the editor. This will
   sequentially open up a new editor for each commit you want to reword. In
   it, you will be able to change the commit message. Save to proceed to
   the next commit message until the rebase is complete.
   But be careful not to delete any lines in the above editor view --
   **An interactive rebase can be dangerous, and if you remove a line, this commit will be lost!** [#f5]_

Untracking accidentally saved contents (tracked in Git)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next question comes from the front:
"It happened that I forgot to give a path to the :command:`datalad save`
command when I wanted to only start tracking a very specific file.
Other times I just didn't remember that
additional, untracked files existed in the dataset and saved unaware of
those. I know that it is good practice to only save
those changes together that belong together, so is there a way to
disentangle an accidental :command:`datalad save` again?"

Let's say instead of saving *all three* previously untracked Git jokes
you intended to save *only one* of those files. What we
want to achieve is to keep all of the files and their contents
in the dataset, but get them out of the history into an
*untracked* state again, and save them *individually* afterwards.

.. importantnote:: Untracking is different for Git versus git-annex!

   Note that this is a case with *text files* (stored in Git)! For
   accidental annexing of files, please make sure to check out
   the next paragraph!

This is a task for the :command:`git reset` command. It essentially allows to
undo commits by resetting the history of a dataset to an earlier version.
:command:`git reset` comes with several *modes* that determine the
exact behavior it, but the relevant one for this aim is ``--mixed`` [#f3]_.
Specifying the command::

   git reset --mixed COMMIT

will preserve all changes made to files since the specified
commit in the dataset but remove them from the dataset's history.
This means all commits *since* ``COMMIT`` (but *not including* ``COMMIT``)
will not be in your history anymore and become "untracked files" or
"unsaved changes" instead. In other words, the modifications
you made in these commits that are "undone" will still be present
in your dataset -- just not written to the history anymore. Let's
try this to get a feel for it.

The COMMIT in the command can either be a hash or a reference
with the HEAD pointer.

.. find-out-more:: Git terminology: branches and HEADs?

   A Git repository (and thus any DataLad dataset) is built up as a tree of
   commits. A *branch* is a named pointer (reference) to a commit, and allows you
   to isolate developments. The default branch is called ``master``. ``HEAD`` is
   a pointer to the branch you are currently on, and thus to the last commit
   in the given branch.

   .. image:: ../artwork/src/git_branch_HEAD.png
      :width: 50%

   Using ``HEAD``, you can identify the most recent commit, or count backwards
   starting from the most recent commit. ``HEAD~1`` is the ancestor of the most
   recent commit, i.e., one commit back (``f30ab`` in the figure above). Apart from
   the notation ``HEAD~N``, there is also ``HEAD^N`` used to count backwards, but
   less frequently used and of importance primarily in the case of *merge*
   commits.
   `This post <https://stackoverflow.com/questions/2221658/whats-the-difference-between-head-and-head-in-git>`__
   explains the details well.

Let's stay with the hash, and reset to the commit prior to saving the Gitjokes.

First, find out the shasum, and afterwards, reset it.

.. runrecord:: _examples/DL-101-137-106
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 3 --oneline

.. runrecord:: _examples/DL-101-137-107
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "$ git reset --mixed $(git rev-parse HEAD~1)" && git reset --mixed $(git rev-parse HEAD~1)

Let's see what has happened. First, let's check the history:

.. runrecord:: _examples/DL-101-137-108
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 2 --oneline

As you can see, the commit in which the jokes were tracked
is not in the history anymore! Go on to see what :command:`datalad status`
reports:

.. runrecord:: _examples/DL-101-137-109
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad status

Nice, the files are present, and untracked again. Do they contain
the content still? We will read all of them with :command:`cat`:

.. runrecord:: _examples/DL-101-137-110
   :workdir: dl-101/DataLad-101
   :language: console

   $ cat Gitjoke*

Great. Now we can go ahead and save only the file we intended
to track:

.. runrecord:: _examples/DL-101-137-111
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad save -m "save my favorite Git joke" Gitjoke2.txt

Finally, let's check how the history looks afterwards:

.. runrecord:: _examples/DL-101-137-112
   :workdir: dl-101/DataLad-101
   :language: console

   $ git log -2

Wow! You have rewritten history [#f4]_ !

Untracking accidentally saved contents (stored in git-annex)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous :command:`git reset` undid the tracking of *text* files.
However, those files are stored in Git, and thus their content
is also stored in Git. Files that are annexed, however, have
their content stored in git-annex, and not the file itself is stored
in the history, but a symlink pointing to the location of the file
content in the dataset's annex. This has consequences for
a :command:`git reset` command: Reverting a save of a file that is
annexed would revert the save of the symlink into Git, but it will
not revert the *annexing* of the file.
Thus, what will be left in the dataset is an untracked symlink.

To undo an accidental save of that annexed a file, the annexed file
has to be "unlocked" first with a :command:`datalad unlock` command.

We will simulate such a situation by creating a PDF file that
gets annexed with an accidental :command:`datalad save`:

.. runrecord:: _examples/DL-101-137-113
   :language: console
   :workdir: dl-101/DataLad-101

   # create an empty pdf file
   $ convert xc:none -page Letter apdffile.pdf
   # accidentally save it
   $ datalad save

This accidental :command:`save` has thus added both text files
stored in Git, but also a PDF file to the history of the dataset.
As an :command:`ls -l` reveals, the PDF file has been annexed and is
thus a :term:`symlink`:

.. runrecord:: _examples/DL-101-137-114
   :language: console
   :realcommand:  ls -l --time-style=long-iso apdffile.pdf
   :workdir: dl-101/DataLad-101

   $ ls -l apdffile.pdf

Prior to resetting, the PDF file has to be unannexed.
To unannex files, i.e., get the contents out of the object tree,
the :command:`datalad unlock` command is relevant:

.. runrecord:: _examples/DL-101-137-115
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad unlock apdffile.pdf

The file is now no longer symlinked:

.. runrecord:: _examples/DL-101-137-116
   :language: console
   :realcommand:  ls -l --time-style=long-iso apdffile.pdf
   :workdir: dl-101/DataLad-101

   $ ls -l apdffile.pdf

Finally, :command:`git reset --mixed` can be used to revert the
accidental :command:`save`. Again, find out the shasum first, and
afterwards, reset it.

.. runrecord:: _examples/DL-101-137-117
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 3 --oneline

.. runrecord:: _examples/DL-101-137-118
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "$ git reset --mixed $(git rev-parse HEAD~1)" && git reset --mixed $(git rev-parse HEAD~1)

To see what has happened, let's check the history:

.. runrecord:: _examples/DL-101-137-119
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 2 --oneline

... and also the status of the dataset:

.. runrecord:: _examples/DL-101-137-120
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

The accidental save has been undone, and the file is present
as untracked content again.
As before, this action has not been recorded in your history.

Viewing previous versions of files and datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next question is truly magical: How does one *see*
data as it was at a previous state in history?

This magic trick can be performed with the :command:`git checkout`.
It is a very heavily used command for various tasks, but among
many it can send you back in time to view the state of a dataset
at the time of a specific commit.

Let's say you want to find out which notes you took in the first
few chapters of the handbook. Find a commit :term:`shasum` in your history
to specify the point in time you want to go back to:

.. runrecord:: _examples/DL-101-137-121
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 20 --oneline

Let's go 15 commits back in time:

.. runrecord:: _examples/DL-101-137-122
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "$ git checkout $(git rev-parse HEAD~15)" && git checkout $(git rev-parse HEAD~15)

How did your ``notes.txt`` file look at this point?

.. runrecord:: _examples/DL-101-137-123
   :language: console
   :workdir: dl-101/DataLad-101

   $ tail notes.txt

Neat, isn't it? By checking out a commit shasum you can explore a previous
state of a datasets history. And this does not only apply to simple text
files, but every type of file in your dataset, regardless of size.
The checkout command however led to something that Git calls a "detached HEAD state".
While this sounds scary, a :command:`git checkout master` will bring you
back into the most recent version of your dataset and get you out of the
"detached HEAD state":

.. runrecord:: _examples/DL-101-137-124
   :language: console
   :workdir: dl-101/DataLad-101

   $ git checkout master


Note one very important thing: The previously untracked files are still
there.

.. runrecord:: _examples/DL-101-137-125
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

The contents of ``notes.txt`` will now be the most recent version again:

.. runrecord:: _examples/DL-101-137-126
   :language: console
   :workdir: dl-101/DataLad-101

   $ tail notes.txt

... Wow! You traveled back and forth in time!
But an even more magical way to see the contents of files in previous
versions is Git's :command:`cat-file` command: Among many other things, it lets
you read a file's contents as of any point in time in the history, without a
prior :command:`git checkout` (note that the output is shortened for brevity and shows only the last few lines of the file):

.. runrecord:: _examples/DL-101-137-127
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1, 48-
   :realcommand: echo "$ git cat-file --textconv $(git rev-parse HEAD~15):notes.txt" && git cat-file --textconv $(git rev-parse HEAD~15):notes.txt

The cat-file command is very versatile, and
`it's documentation <https://git-scm.com/docs/git-cat-file>`_ will list all
of its functionality. To use it to see the contents of a file at a previous
state as done above, this is how the general structure looks like::

   $ git cat-file --textconv SHASUM:<path/to/file>

Undoing latest modifications of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previously, we saw how to remove files from a datasets history that
were accidentally saved and thus tracked for the first time.
How does one undo a *modification* to a tracked file?

Let's modify the saved ``Gitjoke1.txt``:

.. runrecord:: _examples/DL-101-137-128
   :language: console
   :workdir: dl-101/DataLad-101

   $ echo "this is by far my favorite joke!" >> Gitjoke2.txt

.. runrecord:: _examples/DL-101-137-129
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat Gitjoke2.txt

.. runrecord:: _examples/DL-101-137-130
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

.. runrecord:: _examples/DL-101-137-131
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add joke evaluation to joke" Gitjoke2.txt

How could this modification to ``Gitjoke2.txt`` be undone?
With the :command:`git reset` command again. If you want to
"unsave" the modification but keep it in the file, use
:command:`git reset --mixed` as before. However, if you want to
get rid of the modifications entirely, use the option ``--hard``
instead of ``--mixed``:

.. runrecord:: _examples/DL-101-137-132
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -n 2 --oneline

.. runrecord:: _examples/DL-101-137-133
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "$ git reset --hard $(git rev-parse HEAD~1)" && git reset --hard $(git rev-parse HEAD~1)

.. runrecord:: _examples/DL-101-137-134
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat Gitjoke2.txt

The change has been undone completely. This method will work with
files stored in Git and annexed files.

Note that this operation only restores this one file, because the commit that
was undone only contained modifications to this one file. This is a
demonstration of one of the reasons why one should strive for commits to
represent meaningful logical units of change -- if necessary, they can be
undone easily.

Undoing past modifications of files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What :command:`git reset` did was to undo commits from
the most recent version of your dataset. How
would one undo a change that happened a while ago, though,
with important changes being added afterwards that you want
to keep?

Let's save a bad modification to ``Gitjoke2.txt``,
but also a modification to ``notes.txt``:

.. runrecord:: _examples/DL-101-137-140
   :language: console
   :workdir: dl-101/DataLad-101

   $ echo "bad modification" >> Gitjoke2.txt

.. runrecord:: _examples/DL-101-137-141
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "did a bad modification" Gitjoke2.txt

.. runrecord:: _examples/DL-101-137-142
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT >> notes.txt

   Git has many handy tools to go back in forth in time and work with the
   history of datasets. Among many other things you can rewrite commit
   messages, undo changes, or look at previous versions of datasets.
   A superb resource to find out more about this and practice such Git
   operations is this chapter in the Pro-git book:
   https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History
   EOT

.. runrecord:: _examples/DL-101-137-143
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add note on helpful git resource" notes.txt

The objective is to remove the first, "bad" modification, but
keep the more recent modification of ``notes.txt``. A :command:`git reset`
command is not convenient, because resetting would need to reset
the most recent, "good" modification as well.

One way to accomplish it is with an *interactive rebase*, using the
:command:`git rebase -i` command [#f5]_. Experienced Git-users will know
under which situations and how to perform such an interactive rebase.

However, outlining an interactive rebase here in the handbook could lead to
problems for readers without (much) Git experience: An interactive rebase,
even if performed successfully, can lead to many problems if it is applied with
too little experience, for example in any collaborative real-world project.

Instead, we demonstrate a different, less intrusive way to revert one or more
changes at any point in the history of a dataset: the :command:`git revert`
command.
Instead of *rewriting* the history, it will add an additional commit in which
the changes of an unwanted commit are reverted.

The command looks like this:

.. code-block:: bash

   $ git revert SHASUM

where ``SHASUM`` specifies the commit hash of the modification that should
be reverted.

.. find-out-more:: Reverting more than a single commit

   You can also specify a range of commits like this::

      $ git revert OLDER_SHASUM..NEWERSHASUM

   This command will revert all commits starting with the one after
   ``OLDER_SHASUM`` (i.e. **not including** this commit) until and **including**
   the one specified with ``NEWERSHASUM``.
   For each reverted commit, one new commit will be added to the history that
   reverts it. Thus, if you revert a range of three commits, there will be three
   reversal commits. If you however want the reversal of a range of commits
   saved in a single commit, supply the ``--no-commit`` option as in

   .. code-block:: bash

      $ git revert --no-commit OLDER_SHASUM..NEWERSHASUM

   After running this command, run a single ``git commit`` to conclude the
   reversal and save it in a single commit.

Let's see how it looks like:

.. runrecord:: _examples/DL-101-137-144
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "$ git revert $(git rev-parse HEAD~1)" && git revert $(git rev-parse HEAD~1)

This is the state of the file in which we reverted a modification:

.. runrecord:: _examples/DL-101-137-145
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat Gitjoke2.txt

It does not contain the bad modification anymore. And this is what happened in
the history of the dataset:

.. runrecord:: _examples/DL-101-137-146
   :language: console
   :workdir: dl-101/DataLad-101
   :emphasize-lines: 6-8, 20

   $ git log -n 3

The commit that introduced the bad modification is still present, but it
transparently gets undone with the most recent commit. At the same time, the
good modification of ``notes.txt`` was not influenced in any way. The
:command:`git revert` command is thus a transparent and safe way of undoing past
changes. Note though that this command can only be used efficiently if the
commits in your datasets history are meaningful, independent units -- having
several unrelated modifications in a single commit may make an easy solution
with :command:`git revert` impossible and instead require a complex
:command:`checkout`, :command:`revert`, or :command:`rebase` operation.

Finally, let's take a look at the state of the dataset after this operation:

.. runrecord:: _examples/DL-101-137-147
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

As you can see, unsurprisingly, the :command:`git revert` command had no
effects on anything else but the specified commit, and previously untracked
files are still present.

Oh no! I'm in a merge conflict!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When working with the history of a dataset, especially when rewriting
the history with an interactive rebase or when reverting commits, it is
possible to run into so-called *merge conflicts*.
Merge conflicts happen when Git needs assistance in deciding
which changes to keep and which to apply. It will require
you to edit the file the merge conflict is happening in with
a text editor, but such merge conflict are by far not as scary as
they may seem during the first few times of solving merge conflicts.

This section is not a guide on how to solve merge-conflicts, but a broad
overview on the necessary steps, and a pointer to a more comprehensive guide.

- The first thing to do if you end up in a merge conflict is
  to read the instructions Git is giving you -- they are a useful guide.
- Also, it is reassuring to remember that you can always get out of
  a merge conflict by aborting the operation that led to it (e.g.,
  ``git rebase --abort``).
- To actually solve a merge conflict, you will have to edit files: In the
  documents the merge conflict applies to, Git marks the sections it needs
  help with with markers that consists of ``>``, ``<``, and ``=``
  signs and commit shasums or branch names.
  There will be two marked parts, and you have to delete the one you do not
  want to keep, as well as all markers.
- Afterwards, run ``git add <path/to/file>`` and finally a ``git commit``.

An excellent resource on how to deal with merge conflicts is
`this post <https://docs.github.com/en/github/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line>`_.

Summary
^^^^^^^

This guest lecture has given you a glimpse into how to work with the
history of your DataLad datasets.
To conclude this section, let's remove all untracked contents from
the dataset. This can be done with :command:`git clean`: The command
:command:`git clean -f` swipes your dataset clean and removes any untracked
file.
**Careful! This is not revertible, and content lost with this commands can not be recovered!**
If you want to be extra sure, run :command:`git clean -fn` beforehand -- this will
give you a list of the files that would be deleted.

.. runrecord:: _examples/DL-101-137-148
   :language: console
   :workdir: dl-101/DataLad-101

   $ git clean -f

Afterwards, the :command:`datalad status` returns nothing, indicating a
clean dataset state with no untracked files or modifications.

.. runrecord:: _examples/DL-101-137-149
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

Finally, if you want, apply your new knowledge about reverting commits
to remove the ``Gitjoke2.txt`` file.


.. only:: adminmode

   Add a tag at the section end.

     .. runrecord:: _examples/DL-101-137-160
        :language: console
        :workdir: dl-101/DataLad-101

        $ git branch sct_back_and_forth_in_time


.. rubric:: Footnotes

.. [#f1] For example, the :command:`datalad rerun` command introduced in section
         :ref:`run2` takes such a hash as an argument, and re-executes
         the ``datalad run`` or ``datalad rerun`` :term:`run record` associated with
         this hash. Likewise, the :command:`git diff` can work with commit hashes.

.. [#f2] There are other alternatives to reference commits in the history of a dataset,
         for example "counting" ancestors of the most recent commit using the notation
         ``HEAD~2``, ``HEAD^2`` or ``HEAD@{2}``. However, using hashes to reference
         commits is a very fail-save method and saves you from accidentally miscounting.

.. [#f3] The option ``--mixed`` is the default mode for a :command:`git reset`
         command, omitting it (i.e., running just ``git reset``) leads to the
         same behavior. It is explicitly stated in this book to make the mode
         clear, though.

.. [#f4] Note though that rewriting history can be dangerous, and you should
         be aware of what you are doing. For example, rewriting parts of the
         dataset's history that have been published (e.g., to a GitHub repository)
         already or that other people have copies of, is not advised.

.. [#f5] When in need to interactively rebase, please consult further documentation
         and tutorials. It is out of the scope of this handbook to be a complete
         guide on rebasing, and not all interactive rebasing operations are
         complication-free. However, you can always undo mistakes that occur
         during rebasing with the help of the `reflog <https://git-scm.com/docs/git-reflog>`_.
