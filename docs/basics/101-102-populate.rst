.. _populate:

Populate a dataset
------------------

The first lecture in DataLad-101 referenced some useful literature.
Even if we end up not reading those books at all, let's download
them nevertheless and put them into our dataset. You never know, right?
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
   :notes: The tree command shows us the directory structure in the dataset. Apart from the directory, it's empty.

   $ tree


Arguably, not the most exciting thing to see. So let's put some PDFs inside.
Below is a short list of optional readings. We decide to download them (they
are all free, in total about 15 MB), and save them in ``DataLad-101/books``.

- Additional reading about the command line: `The Linux Command Line <https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download>`_
- An intro to Python: `A byte of Python <https://github.com/swaroopch/byte-of-python/releases/download/v14558db59a326ba99eda0da6c4548c48ccb4cd0f/byte-of-python.pdf>`_

You can either visit the links and save them in ``books/``,
or run the following commands [#f2]_ to download the books right from the terminal.
Note that we line break the command with ``\`` signs. In your own work you can write
commands like this into a single line. If you copy them into your terminal as they
are presented here, make sure to check the :windows-wit:`on peculiarities of its terminals
<ww-no-multiline-commands>`.

.. windows-wit:: Terminals other than Git Bash can't handle multi-line commands
   :name: ww-no-multiline-commands

   In Unix shells, ``\`` can be used to split a command into several lines, for example to aid readability.
   Standard Windows terminals (including the Anaconda prompt) do not support this.
   They instead use the ``^`` character::

     $ wget -q https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download ^
     -O TLCL.pdf

   If you are not using the Git Bash, you will either need to copy multi-line commands into a single line, or use ``^`` (make sure that there is **no space** afterwards) instead of ``\``.

.. runrecord:: _examples/DL-101-102-103
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: We use wget to download a few books from the web. CAVE: longish realcommand!

   $ cd books
   $ wget -q https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download \
     -O TLCL.pdf
   $ wget -q https://homepages.uc.edu/~becktl/byte_of_python.pdf \
     -O byte-of-python.pdf
   # get back into the root of the dataset
   $ cd ../

Some machines will not have :command:`wget` available by default, but any command that can
download a file can work as an alternative. See the :windows-wit:`for the popular alternative
curl <ww-curl-instead-wget>`.

.. windows-wit:: You can use curl instead of wget
   :name: ww-curl-instead-wget

   Many versions of Windows do not ship with the tool ``wget``.
   You can install it, but it may be easier to use the pre-installed ``curl`` command::

      $ cd books
      $ curl -L https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download \
        -o TLCL.pdf
      $ curl -L https://homepages.uc.edu/~becktl/byte_of_python.pdf \
        -o byte-of-python.pdf
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

Interesting; the ``books/`` directory is "untracked". Remember how content
*can* be tracked *if a user wants to*?
Untracked means that DataLad does not know about this directory or its content,
because we have not instructed DataLad to actually track it. This means that DataLad
does not store the downloaded books in its history yet. Let's change this by
*saving* the files to the dataset's history with the :command:`datalad save` command
(:manpage:`datalad-save` manual).

This time, it is your turn to specify a helpful :term:`commit message`
with the ``-m`` option (although the DataLad command is :command:`datalad save`, we talk
about commit messages because :command:`datalad save` ultimately uses the command
:command:`git commit` to do its work):

.. runrecord:: _examples/DL-101-102-106
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: ATM the files are untracked and thus unknown to any version control system. In order to version control the PDFs we need to save them. We attach a meaningful summary of this with the -m option:

   $ datalad save -m "add books on Python and Unix to read later"

If you ever forget to specify a message, or made a typo, not all is lost. A
:find-out-more:`explains how to amend a saved state <fom-amend-save>`.

.. find-out-more:: "Oh no! I forgot the -m option for datalad-save!"
   :name: fom-amend-save
   :float:

   If you forget to specify a commit message with the ``-m`` option, DataLad will write
   ``[DATALAD] Recorded changes`` as a commit message into your history.
   This is not particularly informative.
   You can change the *last* commit message with the Git command
   :command:`git commit --amend`. This will open up your default editor
   and you can edit
   the commit message. Careful -- the default editor might be :term:`vim`!
   The section :ref:`history` will show you many more ways in which you can
   interact with a dataset's history.


As already noted, any files you ``save`` in this dataset, and all modifications
to these files that you ``save``, are tracked in this history.
Importantly, this file tracking works
regardless of the size of the files -- a DataLad dataset could be
your private music or movie collection with single files being many GB in size.
This is one aspect that distinguishes DataLad from many other
version control tools, among them Git.
Large content is tracked in an *annex* that is automatically
created and handled by DataLad. Whether text files or larger files change,
all of these changes can be written to your DataLad dataset's history.

Let's see how the saved content shows up in the history of the dataset with :command:`git log`.
The option ``-n 1`` specifies that we want to take a look at the most recent commit.
In order to get a bit more details, we add the ``-p`` flag. If you end up in a
pager, navigate with up and down arrow keys and leave the log by typing ``q``:

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
human-readable summary of that action. A :find-out-more:`explains what makes
a good message <fom-commit-message-guidance>`.

.. find-out-more:: DOs and DON'Ts for commit messages
   :name: fom-commit-message-guidance
   :float: tbp

    **DOs**

    - Write a *title line* with 72 characters or less (as we did so far)

    - it should be in imperative voice, e.g., "Add notes from lecture 2"

    - Often, a title line is not enough to express your changes and reasoning behind it. In this case, add a body to your commit message by hitting enter twice (before closing the quotation marks), and continue writing a brief summary of the changes after a blank line. This summary should explain "what" has been done and "why", but not "how". Close the quotation marks, and hit enter to save the change with your message.

    **DON'Ts**

    - passive voice is hard to read afterwards

    - extensive formatting (hashes, asterisks, quotes, ...) will most likely make your shell complain

    - it should be obvious: do not say nasty things about other people

.. gitusernote:: There is no staging area in DataLad

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

Regarding your first remark, you're absolutely right!
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
   :cast: 01_dataset_basics
   :notes: It's inconvenient that we saved two books together - we should have saved them as independent modifications of the dataset. To see how single modifications can be saved, let's download another book

   $ cd books
   $ wget -q https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf
   $ cd ../

:command:`datalad status` shows that there is a new untracked file:

.. runrecord:: _examples/DL-101-102-109
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: Check the dataset state with the status command frequently

   $ datalad status

Let's give :command:`datalad save` precisely this file by specifying its path after the commit message:

.. runrecord:: _examples/DL-101-102-110
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: To save a single modification, provide a path to it!

   $ datalad save -m "add reference book about git" books/progit.pdf

Regarding your second remark, you're right that a :command:`datalad save` without a
path specification would write all of the currently untracked files or modifications
to the history. But check the :find-out-more:`on how to tell it otherwise <fom-save-updated-only>`.

.. find-out-more:: How to save already tracked dataset components only?
   :name: fom-save-updated-only
   :float:

   A :command:`datalad save -m "concise message" --updated` (or the shorter
   form of ``--updated``, ``-u``) will only write *modifications* to the
   history, not untracked files. Later, we will also see ``.gitignore`` files
   that let you hide content from version control.  However, it is good
   practice to safely store away modifications or new content.  This improves
   your dataset and workflow, and will be a requirement for executing certain
   commands.

A :command:`datalad status` should now be empty, and our dataset's history should look like this:

.. runrecord:: _examples/DL-101-102-111
   :workdir: dl-101/DataLad-101
   :language: console
   :cast: 01_dataset_basics
   :notes: Let's view the growing history (concise with the --oneline option):

   # lets make the output a bit more concise with the --oneline option
   $ git log --oneline

“Wonderful! I’m getting a hang on this quickly”, you think. “Version controlling
files is not as hard as I thought!”

But downloading and adding content to your dataset “manually” has two
disadvantages: For one, it requires you to download the content and save it.
Compared to a workflow with no DataLad dataset, this is one additional command
you have to perform (`and that additional time adds up, after a while <https://xkcd.com/1205/>`_). But a more
serious disadvantage is that you have no electronic record of the source of the
contents you added. The amount of :term:`provenance`, the time, date, and author
of file, is already quite nice, but we don't know anything about where you downloaded
these files from. If you would want to find out, you would have to *remember*
where you got the content from – and brains are not made for such tasks.

Luckily, DataLad has a command that will solve both of these problems:
The :command:`datalad download-url` command (:manpage:`datalad-download-url` manual).
We will dive deeper into the provenance-related benefits of using it in later chapters, but for now,
we’ll start with best-practice-building. :command:`datalad download-url` can retrieve content
from a URL (following any URL-scheme from https, http, or ftp or s3) and save it
into the dataset together with a human-readable commit message and a hidden,
machine-readable record of the origin of the content. This saves you time,
and captures :term:`provenance` information about the data you add to your dataset.
To experience this, let's add a final book,
`a beginner’s guide to bash <https://tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf>`_,
to the dataset. We provide the command with a URL, a pointer to the dataset the
file should be saved in (``.`` denotes "current directory"), and a commit message.

.. runrecord:: _examples/DL-101-102-112
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: finally, datalad-download-url

   $ datalad download-url \
     http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
     --dataset . \
     -m "add beginners guide on bash" \
     -O books/bash_guide.pdf

Afterwards, a fourth book is inside your ``books/`` directory:

.. runrecord:: _examples/DL-101-102-113
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics

   $ ls books

However, the :command:`datalad status` command does not return any output –
the dataset state is “clean”:

.. runrecord:: _examples/DL-101-102-114
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics

   $ datalad status

This is because :command:`datalad download-url` took care of saving for you:

.. runrecord:: _examples/DL-101-102-115
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log -p -n 1


At this point in time, the biggest advantage may seem to be the time save. However,
soon you will experience how useful it is to have DataLad keep track for you where
file content came from.

To conclude this section, let's take a final look at the history of your dataset at
this point:

.. runrecord:: _examples/DL-101-102-116
   :language: console
   :workdir: dl-101/DataLad-101

   $ git log --oneline

Well done! Your ``DataLad-101`` dataset and its history are slowly growing.

.. only:: adminmode

   Add a tag at the section end.

     .. runrecord:: _examples/DL-101-102-117
        :language: console
        :workdir: dl-101/DataLad-101

        $ git branch sct_populate_a_dataset


.. rubric:: Footnotes

.. [#f1] ``tree`` is a Unix command to list file system content. If it is not yet installed,
   you can get it with your native package manager (e.g.,  ``apt``, ``brew``, or conda).
   For example, if you use OSX, ``brew install tree``  will get you this tool.
   On Windows, if you have the Miniconda-based installation described in :ref:`install`, you can install the ``m2-base`` package (``conda install m2-base``), which contains tree along with many other Unix-like commands.
   Note that this tree works slightly different than its Unix equivalent - it will only display directories, not files, and it doesn't accept common options or flags.
   It will also display *hidden* directories, i.e., those that start with a ``.`` (dot).

.. [#f2] ``wget`` is a Unix command for non-interactively downloading files from the
   web. If it is not yet installed, you can get it with your native package manager (e.g.,
   ``apt`` or ``brew``). For example, if you use OSX, ``brew install wget``
   will get you this tool.

.. [#f3] See :term:`tig`. Once installed, exchange any git log command you
   see here with the single word ``tig``.
