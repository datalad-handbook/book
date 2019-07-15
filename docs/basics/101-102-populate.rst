.. _populate:

Starting from scratch: Populating a dataset
-------------------------------------------

The first lecture in DataLad-101 referenced some useful literature.
Even if we end up not reading those books at all, lets just download
them and put them into our dataset. You never know, right?
Lets first create a directory to save books for additional reading in.

.. runrecord:: _examples/DL-101-102-1
   :language: console
   :workdir: dl-101/DataLad-101

   $ mkdir books

Lets take a look at the current directory structure:

.. runrecord:: _examples/DL-101-102-2
   :language: console
   :workdir: dl-101/DataLad-101

   $ tree


Arguably, not the most exiting thing to see. So lets put some PDFs inside.
Below is a short list optional readings. We decide to download them (they
are all free, in total 16.1 MB), and save them in ``DataLad-101/books``.

- Additional reading about the command line: `The Linux Command Line <https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download>`_
- An intro to Python: `A byte of Python <https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python>`_

You can either visit the links and save them in ``books/``,
or run the following commands to download the books:

.. runrecord:: _examples/DL-101-102-3
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: cd books &&  wget -nv https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf && wget -nv https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python -O byte-of-python.pdf

   $ cd books
   $ wget https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf
   $ wget https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python -O byte-of-python.pdf
   # get back into the root of the dataset
   $ cd ../

Let's see what happened. First of all, in the root of ``DataLad-101``, show the directory
structure with tree:

.. runrecord:: _examples/DL-101-102-4
   :language: console
   :workdir: dl-101/DataLad-101

   $ tree


Now what does DataLad do with this sudden content? One command you will use very
often is ``datalad status``. It reports on the state of dataset content, and
regular status reports should become a habit in the wake of ``DataLad-101``.

.. runrecord:: _examples/DL-101-102-5
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

Interesting, the ``books/`` directory is "untracked". Remember how content
*can* be tracked *if a user wants to*?
Untracked means that DataLad does not know about this directory or its content,
because we haven't ordered DataLad to actually track it. This means, DataLad
does not keep the downloaded books in its history yet. Lets change this by
saving the files to the datasets history with the ``datalad save`` command.
This time, its your turn to specify a helpful :term:`commit message`
with the ``-m`` option:

.. runrecord:: _examples/DL-101-102-6
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add books on Python and Unix to read later"

.. container:: toggle

   .. container:: header

      **Addition: "Oh no! I forgot the -m option!"**

   If you forget to specify a commit message with ``-m``, DataLad will write
   ``[DATALAD] Recorded changes`` as a commit message into your history.
   This is not particularly informative.
   You can change the *last* commit message with the Git command
   ``git commit --amend``. This will open up your default editor
   and you can edit
   the commit message. Careful - the default editor might be :term:`vim`!

Lets see how this shows up in the history of the dataset with ``git log``.
In order to get a bit more details, we add the ``-p`` flag (leave the git log
by typing ``q``, navigate with up and down arrow keys):

.. runrecord:: _examples/DL-101-102-7
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1-20
   :emphasize-lines: 3-4, 6, 8, 12, 16, 20

   $ git log -p

Now this might look a bit cryptic (and honestly, tig [#f1]_ makes it look prettier).
But this tells us the date and time in which a particular author added two PDFs to
the directory ``books/``, and thanks to that commit message we have a nice human-
readable summary of that action.

.. container:: toggle

    .. container:: header

       **Addition: DOs and DON'Ts for commit messages**

    **DOs**

    - Write a *title line* with 72 characters or less (as we did so far)

    - it should be in imperative voice, e.g. "Add notes from lecture 2"

    - Often, a title line is not enough to express your changes and reasoning behind it. In this case, add a body to your commit message by hitting enter twice (before closing the quotation marks), and continue writing a brief summary of the changes after a blank line. This summary should explain "what" has been done and "why", but not "how". Close the quotation marks, and hit enter to save the change with your message.

    - here you can find more guidelines: https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53

    **DON'Ts**

    - passive voice is hard to read afterwards

    - extensive formatting (hashes, asterisks, quotes, ...) will most likely make your shell complain

    - it should be obvious: do not say nasty things about other people

.. gitusernote::

   Just as in Git, new files are not tracked from their creation on, but only when
   explicitly given to Git (in Git terms with an initial ``git add``). But different
   from the common Git workflow, DataLad skips the staging area. A ``datalad save``
   combines a ``git add`` and a ``git commit``, and therefore, the commit message
   is specified with ``datalad save``.

Cool, so now you have added some files to your dataset history. But what is a bit
inconvenient is that both books were saved *together*. You begin to wonder: "A Python
book and a Unix book do not have that much in common. I probably should not save them
in the same commit. And ... what happens if I have files I don't want to track? A
``datalad save -m "some commit message"`` would write all of what is currently
in my dataset and untracked or modified into the history!"

And you're absolutely right with that! First, it is good practice to save only those changes
together that belong together. We do not want to squish completely unrelated changes
into the same spot of our history, because it would get very nasty should we want to
revert *some* of the changes without affecting others in this commit.
Second, yes, you should have control about what you have tracked by DataLad.

Luckily, we can point ``datalad save`` to exactly the changes we want it to record.
Lets try this by adding yet another book, a good reference work about git:

.. runrecord:: _examples/DL-101-102-8
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: cd books && wget -nv https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf && cd ../

   $ cd books
   $ wget https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf
   $ cd ../

``datalad status`` shows that there is a new untracked file:

.. runrecord:: _examples/DL-101-102-9
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

Lets ``datalad save`` precisely this file by specifying its path after the commit message:

.. runrecord:: _examples/DL-101-102-10
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add reference book about git" books/progit.pdf

Let's make it a habit to always specify precisely which changes we want to write to history.

A ``datalad status`` should now be empty, and our datasets history should look like this:

.. runrecord:: _examples/DL-101-102-11
   :language: console
   :workdir: dl-101/DataLad-101

   # lets make the output a bit more concise with the --oneline option
   $ git log --oneline


Well done! You're ``DataLad-101`` dataset and it's history are slowly growing.


.. rubric:: Footnotes

.. [#f1] A nice and easy tool we can recommend as an alternative to ``git log`` is :term:`tig`.
         Once installed, exchange any git log command you see here with the single word ``tig``.
