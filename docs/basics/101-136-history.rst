Back and forth in time: Working with history
--------------------------------------------

One powerful feature of a version control system is the ability to revert
data to a previous state and thus view earlier content or correct mistakes.

Everyone of us already inadvertently deleted or overwrote files. In some cases,
it might have been possible to restore the lost content. But surely each of us
is especially cautious with some command in the flavors of ``rm`` (remove files),
``save`` (save files -- maybe you accidentally deleted content), or similar
because of a hasty operation that caused data fatalities in the past.
With DataLad, no mistakes are forever. As long as the content was version
controlled, it is possible to look at previous states of the data, or revert
changes -- even years after they happened.

To get a glimpse into how to work with the history of a dataset, today's lecture
consists entirely of this topic.
But because working with the history of a dataset is entirely
:term:`Git`\-based, we have an external Git-expert as a guest lecturer.

"Good morning! What a wonderful day to learn some Git commands!" he greets
everyone. "I don't have enough time to go through all the details in only
one lecture. But I'll give you the basics. And always remember: Just google
what you need. You will find thousands of helpful post or stackoverflow questions right away.
Even the experts will google which Git command to use, and how to use it, *constantly*.",
he reassures with a wink.

"I have seen everyone is already working relatively confidently with the
``git log`` or ``tig`` -- great! This is the basics of working with the
history, actually looking at it. Whatever tool you are using for it,
you need a way to see what has been done in a dataset."

In order to effectively work with the history, the most important
information associated with a commit is its hash. This hash is how
DataLad identifies dataset modifications in the history, and with this
hash you can communicate with DataLad or :term:`Git` about these
modifications. The ``datalad rerun`` command introduced in section
:ref:`run2` for example takes such a hash as an argument, and re-executes
the ``datalad run`` or ``datalad rerun`` :term:`run record` associated with
this hash. Here is an excerpt from the ``DataLad-101`` history to show a
few abbreviated hashes of the 15 most recent commits:

.. runrecord:: _examples/DL-101-136-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ git log -15 --oneline

Using these hashes for miscellaneous history management operations is also
a very fail-save method. An alternative way for example is to
"count" ancestors of the most recent commit using the notation
``HEAD~2``, ``HEAD^2`` or ``HEAD@{2}``, but using the commit hash
saves you from accidentally miscounting. Just note that whenever you see
a post or blog using the above notation, some commit in the history is
referenced.

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

.. runrecord:: _examples/DL-101-136-102
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

.. runrecord:: _examples/DL-101-136-103
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

And now:

.. runrecord:: _examples/DL-101-136-104
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save

Whooops! A :command:`datalad save` without a
commit message that saved all of the files.

.. runrecord:: _examples/DL-101-136-105
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
to change the commit message. Try running this command and give
that commit a new commit message (you can just delete the one
created by DataLad in the editor).

Fixing accidentally saved contents (tracked in Git)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next question comes from the front:
"It happened that I forgot to give a path to the :command:`datalad save`
command when I wanted to only save a very specific change.
Or sometimes I also just didn't remember that
additional modifications existed in the dataset and saved unaware of
those. I know that it is good practice to only save
those changes together that belong together, so is there a way to
disentangle an accidental :command:`datalad save` again?"

For this let's now say instead of committing all three Git jokes from
before you intended to save only one of those files. What we in this case
want to achieve is to keep all of the files as they are in the
dataset, but just get them out of the history to :command:`datalad save`
only one of the files afterwards.

.. important::

   Note that this is a case with *text files* (stored in Git)! For
   accidental annexing of files, please make sure to check out
   the next paragraph!

We'll use the :command:`git reset` command for this. It essentially allows to
undo commits by resetting the history of a dataset to an earlier version.
:command:`git reset` comes with several *modes* that determine the
exact behavior it, but the relevant one for this aim is ``--mixed`` [#f1]_.
Specifying the command::

   git reset --mixed COMMIT

will preserve all changes made to files until the specified
commit in the dataset, but remove them from the datasets history.
This means the commits *until* ``COMMIT`` (not *including* ``COMMIT``)
will not be in your history anymore, and instead "untracked files" or
"unsaved changes". In other words, the modifications
you made in these commits that are "undone" will still be present
in your dataset -- just not written to the history anymore.

The COMMIT in the command can either be a hash or a reference
with the HEAD pointer. Let's stay with the hash, and reset to the
commit prior to saving the Gitjokes:

.. runrecord:: _examples/DL-101-136-106
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "git reset --mixed $(git rev-parse HEAD~1)" && git reset --mixed $(git rev-parse HEAD~1)

Let's see what has happened. First, let's check the history:

.. runrecord:: _examples/DL-101-136-107
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -2

As you can see, the commit is not in the history anymore!
Go on to see what :command:`datalad status` reports:

.. runrecord:: _examples/DL-101-136-108
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad status

Nice, the files are present, and yet untracked. Do they contain
the content still? We will read all of them with :command:`cat`:

.. runrecord:: _examples/DL-101-136-109
   :workdir: dl-101/DataLad-101
   :language: console

   $ cat Gitjoke*

Great. Now we can go ahead and save only those changes we intended
to save:

.. runrecord:: _examples/DL-101-136-110
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad save -m "save my favourite Git joke" Gitjoke2.txt

Finally, lets check how the history looks afterwards:

.. runrecord:: _examples/DL-101-137-111
   :workdir: dl-101/DataLad-101
   :language: console

   git log -2

It is only the last save that is recorded in the history, not the
previous save that recorded all three files. You have rewritten
history [#f2]_ !

Fixing accidentally saved contents (stored in Git-annex)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous :command:`git reset`

This action will not be recorded in your history.

The next question is really magical: How does one *see*
data as it was at a previous state in history?

"To see a previous state of the data(set), you have to *checkout*
the commit you are interested in."
Let us for example view the contents of ``notes.txt`` back when we
had just started to learn how to use DataLad. Identify the commit
in which we added a note on ``datalad save`` in your own history
(it will not have the same hash as the example below).

.. runrecord:: _examples/DL-101-136-110
   :language: console
   :workdir: dl-101/DataLad-101



To see the dataset at this state in time, run ``git checkout COMMIT``

.. runrecord:: _examples/DL-101-136-110
   :language: console
   :workdir: dl-101/DataLad-101

Let's check out the notes at this state.

Todo: continue...


More content:

* How do you change or add the commit message
  of the last commit or add files to it (Git commit --amend)?

* definitely something about git annex unannex

* .. ??


.. rubric:: Footnotes

.. [#f1] The option ``--mixed`` is the default mode for a :command:`git reset`
         command, omitting it (i.e., running just ``git reset``) leads to the
         same behavior. It is explicitly stated in this book to make the mode
         clear, though.

.. [#f2] Note though that rewriting history can be dangerous, and you should
         be aware of what you are doing. For example, rewriting parts of the
         dataset's history that have been published (e.g., to a Github repository)
         already or that other people have copies of is not advised.