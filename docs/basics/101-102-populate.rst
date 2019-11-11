.. _populate:

Populate a dataset
------------------

The first lecture in DataLad-101 referenced some useful literature.
Even if we end up not reading those books at all, let's just download
them and put them into our dataset. You never know, right?
Let's first create a directory to save books for additional reading in.

.. runrecord:: _examples/DL-101-102-101
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: The dataset is empty, lets put some PDFs inside. First, create a directory to store them in:

   $ mkdir books

Let's take a look at the current directory structure with the tree command [#f1]_:

.. runrecord:: _examples/DL-101-102-102
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: The tree command shows us the directory structure in the dataset. Apart from the directory, its empty.

   $ tree


Arguably, not the most exciting thing to see. So let's put some PDFs inside.
Below is a short list of optional readings. We decide to download them (they
are all free, in total about 15 MB), and save them in ``DataLad-101/books``.

- Additional reading about the command line: `The Linux Command Line <https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download>`_
- An intro to Python: `A byte of Python <https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python>`_

You can either visit the links and save them in ``books/``,
or run the following commands [#f2]_ to download the books right from the terminal:

.. runrecord:: _examples/DL-101-102-103
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: cd books && wget -nv https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf && wget -nv https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python -O byte-of-python.pdf && cd ../
   :cast: 01_dataset_basics
   :notes: We use wget to download a few books from the web. CAVE: longish realcommand!

   $ cd books
   $ wget https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf
   $ wget https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python -O byte-of-python.pdf
   # get back into the root of the dataset
   $ cd ../

Let's see what happened. First of all, in the root of ``DataLad-101``, show the directory
structure with tree:

.. runrecord:: _examples/DL-101-102-104
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: Here they are:

   $ tree

.. index:: ! datalad command; status

Now what does DataLad do with this new content? One command you will use very
often is :command:`datalad status` (:manpage:`datalad-status` manual).
It reports on the state of dataset content, and
regular status reports should become a habit in the wake of ``DataLad-101``.

.. runrecord:: _examples/DL-101-102-105
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: What has happened to our dataset now with this new content? We can use datalad status to find out:

   $ datalad status

.. index:: ! datalad command; save

Interesting, the ``books/`` directory is "untracked". Remember how content
*can* be tracked *if a user wants to*?
Untracked means that DataLad does not know about this directory or its content,
because we have not instructed DataLad to actually track it. This means, DataLad
does not keep the downloaded books in its history yet. Let's change this by
saving the files to the dataset's history with the :command:`datalad save` command
(:manpage:`datalad-save` manual).

This time, its your turn to specify a helpful :term:`commit message`
with the ``-m`` option:

.. runrecord:: _examples/DL-101-102-106
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: ATM the files are untracked and thus unknown to any version control system. In order to version control the PDFs we need to save them. We attach a meaningful summary of this with the -m option:

   $ datalad save -m "add books on Python and Unix to read later"

.. findoutmore:: "Oh no! I forgot the -m option!"

   If you forget to specify a commit message with ``-m``, DataLad will write
   ``[DATALAD] Recorded changes`` as a commit message into your history.
   This is not particularly informative.
   You can change the *last* commit message with the Git command
   :command:`git commit --amend`. This will open up your default editor
   and you can edit
   the commit message. Careful -- the default editor might be :term:`vim`!


As already noted, any files you ``save`` in this dataset, and all modifications
to these files that you ``save``, are tracked in this history.
Importantly, this file tracking works
regardless of the size of the files -- a DataLad dataset could be
your private music or movie collection with single files being many GB in size.
This is one aspect that distinguishes DataLad from many other
version control tools, among them Git.
Large content is tracked in an *annex* that is automatically
created and handled by DataLad. Whether text files or larger files change,
all of these changes can be written to your DataLad datasets history.

Let's see how the saved content shows up in the history of the dataset with :command:`git log`.
``-n 1`` specifies that we want to take a look at the most recent commit.
In order to get a bit more details, we add the ``-p`` flag (if in a pager, leave the git log
by typing ``q``, navigate with up and down arrow keys):

.. runrecord:: _examples/DL-101-102-107
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1-20
   :emphasize-lines: 3-4, 6, 8, 12, 16, 20
   :cast: 01_dataset_basics
   :notes: Save command reports what has been added to the dataset. Now we can see how this action looks like in our dataset's history:

   $ git log -p -n 1

Now this might look a bit cryptic (and honestly, tig [#f3]_ makes it look prettier).
But this tells us the date and time in which a particular author added two PDFs to
the directory ``books/``, and thanks to that commit message we have a nice
human-readable summary of that action.

.. findoutmore:: DOs and DON'Ts for commit messages

    **DOs**

    - Write a *title line* with 72 characters or less (as we did so far)

    - it should be in imperative voice, e.g., "Add notes from lecture 2"

    - Often, a title line is not enough to express your changes and reasoning behind it. In this case, add a body to your commit message by hitting enter twice (before closing the quotation marks), and continue writing a brief summary of the changes after a blank line. This summary should explain "what" has been done and "why", but not "how". Close the quotation marks, and hit enter to save the change with your message.

    - here you can find more guidelines: https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53

    **DON'Ts**

    - passive voice is hard to read afterwards

    - extensive formatting (hashes, asterisks, quotes, ...) will most likely make your shell complain

    - it should be obvious: do not say nasty things about other people

.. gitusernote::

   Just as in Git, new files are not tracked from their creation on, but only when
   explicitly added to Git (in Git terms with an initial :command:`git add`). But different
   from the common Git workflow, DataLad skips the staging area. A :command:`datalad save`
   combines a :command:`git add` and a :command:`git commit`, and therefore, the commit message
   is specified with :command:`datalad save`.

Cool, so now you have added some files to your dataset history. But what is a bit
inconvenient is that both books were saved *together*. You begin to wonder: "A Python
book and a Unix book do not have that much in common. I probably should not save them
in the same commit. And ... what happens if I have files I do not want to track?
:command:`datalad save -m "some commit message"` would save all of what is currently
untracked or modified in the dataset into the history!"

Regarding your first remark, you're absolutely right with that!
It is good practice to save only those changes
together that belong together. We do not want to squish completely unrelated changes
into the same spot of our history, because it would get very nasty should we want to
revert *some* of the changes without affecting others in this commit.

Luckily, we can point :command:`datalad save` to exactly the changes we want it to record.
Let's try this by adding yet another book, a good reference work about git,
`Pro Git <https://git-scm.com/book/en/v2>`_:

.. runrecord:: _examples/DL-101-102-108
   :language: console
   :workdir: dl-101/DataLad-101
   :realcommand: cd books && wget -nv https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf && cd ../
   :cast: 01_dataset_basics
   :notes: Its inconvenient that we saved two books together - we should have saved them as independent modifications of the dataset. To see how single modifications can be saved, let's download another book

   $ cd books
   $ wget https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf
   $ cd ../

:command:`datalad status` shows that there is a new untracked file:

.. runrecord:: _examples/DL-101-102-109
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: Check the dataset state with the status command frequently

   $ datalad status

Let's :command:`datalad save` precisely this file by specifying its path after the commit message:

.. runrecord:: _examples/DL-101-102-110
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: To save a single modification, provide a path to it!

   $ datalad save -m "add reference book about git" books/progit.pdf


.. findoutmore:: Some more on save

   Regarding your second remark, you're right that a :command:`datalad save` without a
   path specification would write all of the currently untracked files or modifications
   to the history.
   There are some ways to mitigate this: A :command:`datalad save -m "concise message" --updated`
   (or the shorter form of ``--updated``, ``-u``) will only write *modifications* to the
   history, not untracked files. Later, we will also see ``.gitignore`` files that let
   you hide content from version control.
   However, it is good practice to safely store away modifications or new content.
   This both improves your dataset and workflow, and will be a requirement for the execution
   of certain commands.

A :command:`datalad status` should now be empty, and our dataset's history should look like this:

.. runrecord:: _examples/DL-101-102-111
   :workdir: dl-101/DataLad-101
   :language: console
   :cast: 01_dataset_basics
   :notes: Let's view the growing history (concise with the --oneline option):

   # lets make the output a bit more concise with the --oneline option
   $ git log --oneline


Well done! Your ``DataLad-101`` dataset and its history are slowly growing.


.. rubric:: Footnotes

.. [#f1] ``tree`` is a Unix command to list file system content. If it is not yet installed,
   you can get it with your native package manager (e.g.,
   ``apt`` or ``brew``). For example, if you use OSX, ``brew install tree``
   will get you this tool.
.. [#f2] ``wget`` is a Unix command for non-interactively downloading files from the
   web. If it is not yet installed, you can get it with your native package manager (e.g.,
   ``apt`` or ``brew``). For example, if you use OSX, ``brew install wget``
   will get you this tool.

.. [#f3] See :term:`tig`. Once installed, exchange any git log command you
   see here with the single word ``tig``.
