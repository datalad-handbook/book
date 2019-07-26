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
what you need. You will find thousands of helpful post or blogs right away.
Even the experts will google which Git command to use, and how to use it, *constantly*.",
he reassures with a wink.

"I have seen everyone is already working relatively confidently with the
``git log`` or ``tig`` -- great! This is the basics of working with the
history, actually looking at it. Whatever tool you are using for it,
you need a way to see what has been done in a dataset."

In order to effectively work with the history, the most important
information associated with a commit is its checksum. This checksum is how
DataLad identifies dataset modifications in the history, and with this
checksum you can communicate with DataLad or :term:`Git` about these
modifications. The ``datalad rerun`` command introduced in section
:ref:`run2` for example takes such a checksum as an argument, and re-executes
the ``datalad run`` or ``datalad rerun`` :term:`run record` associated with
this checksum. Here is an excerpt from the ``DataLad-101`` history to show a
few abbreviated checksums of the 15 most recent commits:

.. runrecord:: _examples/DL-101-135-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ git log -15 --oneline

Using these checksums for miscellaneous history management operations is also
a very fail-save method. An alternative way for example is to
"count" ancestors of the most recent commit using the notation
``HEAD~2``, ``HEAD^2`` or ``HEAD@{2}``, but using the commit checksum
saves you from accidentally miscounting. Just note that whenever you see
a post or blog using the above notation, some commit in the history is
referenced.

"I'll let you people direct this lecture", the guest lecturer proposes.
"You tell me what you would be interested in doing, and I'll show you how it's
done. For the rest of the lecture, call me Google!"

From the back of the lecture hall comes a question you're really glad
someone asked: "It has happened to me that I accidentally did a
:command:`datalad save` and forgot to either specify the commit message,
or forgot to give a path to the command when I wanted to only save
a very specific change. Or sometimes I also just didn't remember that
additional modifications existed in the dataset and saved unaware of
those. I know that it is good practice to only save
those changes together that belong together, so is there a way to
disentangle an accidental :command:`datalad save` again?"

The room nods in agreement -- apparently, others have run into this
premature slip of the ``Enter`` key as well.

"Sure, of course!", the guest lecturer reassures. "This is a great
question, thank you. Before I'll show you I'll just repeat
what each of you probably already knows by heart: Make sure to run
a :command:`datalad status` prior to a :command:`datalad save`. You'll
get reminded of the changes that would be saved. But let me tell you,
I also frequently forget modifications, and I really appreciate
that Git lets me revert such mistakes."

Let's demonstrate a simple example. First, let's create some random
files. Do this right in your dataset.

.. runrecord:: _examples/DL-101-135-102
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT > test.txt
   "hello, world!"
   EOT

   $ cat << EOT > test2.txt
   A penny for your thoughts;
   5 bucks if they're dirty;
   10 if I'm right in the middle of it

   $ cat << EOT > test3.txt
   A woman calls a Swedish doctor and says:
   Doctor, my young son has just swallowed a fountain pen.
   He says: Oh my goodness, I come right over!
   What should I do until you arrive?
   Use a pencil!

This will generate three new files in your dataset. Run a
:command:`datalad status` to verify this:

.. runrecord:: _examples/DL-101-135-103
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

Now, say you only wanted to save one of these files,
but you accidentally :command:`datalad save` everything:

.. runrecord:: _examples/DL-101-135-104
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save

Whooops, there it happened. A :command:`datalad save` without a
commit message and without a path to the file you wanted to save
individually.

.. runrecord:: _examples/DL-101-135-105
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -p -1

As expected all of the modifications present prior to the
command are saved into the most recent commit. The aim of
the next action is to keep all of the files as they are in the
dataset, but just get them out of the history. We'll use the
:command:`git reset` command for this. It essentially undoes
commits. :command:`git reset: comes with many options, but the
relevant one is ``--mixed``. Specifying the command::

   git reset --mixed COMMIT

will undo all commits in your history until the specified
commit (it does not undo the specified commit).
Importantly, the modifications
you made in these commits that are undone will still be present
in your dataset -- just not written to the history.

The COMMIT in the command can either be a SHASUM or a reference
with the HEAD pointer. Let's stay with the SHASUM:

.. runrecord:: _examples/DL-101-135-106
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: echo "git reset --mixed $(git rev-parse HEAD~1)" && git reset --mixed $(git rev-parse HEAD~1)

Let's see what has happened. First, let's check the history:

.. runrecord:: _examples/DL-101-135-107
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -2

As you can see, the commit is not in the history anymore!
Go on to see what :command:`datalad status` reports:

.. runrecord:: _examples/DL-101-135-108
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad status

Nice, the files are present, and yet untracked. Do they contain
the content still? We will read all of them with :command:`cat`:

.. runrecord:: _examples/DL-101-135-109
   :workdir: dl-101/DataLad-101
   :language: console

   $ cat test*


ahhh shit, what about annexed files? They are a symlink afterwards...







This action will not be
recorded in your history.

Let's start really simple, but also really magical: How does one *see*
data as it was at a previous state in history?

"To see a previous state of the data(set), you have to *checkout*
the commit you are interested in."
Let us for example view the contents of ``notes.txt`` back when we
had just started to learn how to use DataLad. Identify the commit
in which we added a note on ``datalad save`` in your own history
(it will not have the same checksum as the example below).

.. runrecord:: _examples/DL-101-135-102
   :language: console
   :workdir: dl-101/DataLad-101

To see the dataset at this state in time, run ``git checkout COMMIT``

.. runrecord:: _examples/DL-101-135
   :language: console
   :workdir: dl-101/DataLad-101

Let's check out the notes at this state
How do you change or add the commit message
of the last commit?"
