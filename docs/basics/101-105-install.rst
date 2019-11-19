.. _installds:

Install datasets
----------------

So far, we have created a ``DataLad-101`` course dataset. We saved some additional readings
into the dataset, and have carefully made and saved notes on the DataLad
commands we discovered. Up to this point, we therefore know the typical, *local*
workflow to create and populate a dataset from scratch.

But we've been told that with DataLad we could very easily get vast amounts of data to our
computer. Rumor has it that this would be only a single command in the terminal!
Therefore, everyone in today's lecture excitedly awaits today's topic: Installing datasets.

"With DataLad, users can *install* existing
DataLad datasets from paths, URLs, or open-data collections." our lecturer begins.
"This makes accessing data fast and easy. A dataset that others could install can be
created by anyone, without a need for additional software. Your own Datasets can be
installed by others, should you want that, for example. Therefore, not only accessing
data becomes fast and easy, but also *sharing*."
"That's so cool!", you think. "Exam preparation will be a piece of cake if all of us
can share our mid-term and final projects easily!"
"But today, let's only focus on how to install a dataset", she continuous.
"Damn it! Can we not have longer lectures?", you think and set alarms to all of the
upcoming lecture dates in your calendar.
There is so much exciting stuff to come, you can not miss a single one.

.. index:: ! datalad command; install

Installing an existing dataset is done with the :command:`datalad install` command
(:manpage:`datalad-install`).
The command takes a location of an existing dataset (the *source*), and a path to where you want
the dataset to be installed. The source can be a URL or a path to a local directory,
or an SSH server [#f1]_.

"Psst!" your fellow student from the row behind reaches over. "There are
a bunch of audio recordings of a really cool podcast, and they have been shared in the form
of a DataLad dataset! Shall we try whether we can install that?"

"Perfect! What a great way to learn how to install a dataset. Doing it
now instead of looking at slides for hours is my preferred type of learning anyway",
you think as you fire up your terminal and navigate into your ``DataLad-101`` dataset.

In this demonstration, we're using one of the many openly available datasets that
DataLad provides in a public registry that anyone can access. One of these datasets is a
collection of audio recordings of a great podcast, the longnow seminar series [#f2]_.
It consists of audio recordings about long-term thinking, and while the DataLad-101
course is not a long-term thinking seminar, those recordings are nevertheless a
good addition to the large stash of yet-to-read text books we piled up (and also, we
can wholeheartedly recommend them for their worldly wisdoms and compelling, thoughtful
ideas). Let's install this dataset into our existing ``DataLad-101`` dataset.

To keep the ``DataLad-101`` dataset neat and organized, we first create a new directory,
called recordings.

.. runrecord:: _examples/DL-101-105-101
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: The next challenge is to install an existing dataset from the web as a subdataset. First, we create a location for this

   # we are in the root of DataLad-101
   $ mkdir recordings

Let's install the longnow podcasts in this new directory.
Because we are installing a dataset (the podcasts) within an existing dataset (the ``DataLad-101``
dataset), we supply the ``-d`` (``--dataset``) flag.
This specifies the dataset to perform the operation on. Because we are in the root
of the ``DataLad-101`` dataset, the pointer to the dataset is a ``.`` (which is Unix'
way for saying "current directory"). The dataset to be installed lives on Github, and
we can give its Github URL as a source (``-s``, ``--source``). Note that we line
break these examples with a ``\``. You can copy them as they are presented here into
your terminal, but in your own work you can write commands like this into a single
line.

.. runrecord:: _examples/DL-101-105-102
   :language: console
   :workdir: dl-101/DataLad-101/
   :realcommand: datalad install -d . -s https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow
   :cast: 01_dataset_basics
   :notes: We need to install the dataset as a subdataset. For this, we use the datalad install command with a --dataset option and --source option as well as a path. Else the dataset would not be registered as a subdataset!

   $ datalad install --dataset . \
   --source https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow

   # or, alternatively, using the shorter options:
   $ datalad install -d . \
   -s https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow

This command copied the repository found at the URL https://github.com/datalad-datasets/longnow-podcasts.git
into the existing ``DataLad-101`` dataset, into the directory ``recordings/longnow``.

Note: if we had not specified the path ``recordings/longnow``, the command would have installed the
dataset in the root of the directory and cleverly used the name of the remote repository
"``longnow-podcasts``". Alternatively, you could have also installed the dataset from within
the ``recordings``, or ``books`` directory. Important: If you are installing *within* a dataset,
but execute the command not from the root of this dataset, your ``-d`` option needs to specify
the path to the root of the dataset, and the path needs to start from the directory root. For example,
if you navigate into ``recordings`` the command would be::

  datalad install -d ../ -s https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow

Note that the path did not change, but ``-d .`` changed to ``-d ../``
(the Unix expression for ``parent directory``, i.e.,  "one-directory-up").
Later in this book there is a dedicated section that explains what this ``-d``/``--dataset`` option
does and why it is important, but for now just be mindful of the instruction above.

.. findoutmore:: What if I do not install into an existing dataset?

   If you do not install inside an existing dataset, you only need to omit the ``dataset``
   option. You can try::
  
     datalad install -s https://github.com/datalad-datasets/longnow-podcasts.git

   anywhere outside of your ``Datalad-101`` dataset to install the dataset into a new directory
   called ``longnow-podcasts``.

.. gitusernote::

   The :command:`datalad install` command uses :command:`git clone`.

Here is the repository structure:

.. runrecord:: _examples/DL-101-105-103
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: Let's take a look at the directory structure after the installation

   $ tree -d   # we limit the output to directories

We can see that recordings has one subdirectory, our newly installed ``longnow``
dataset. Within the dataset are two other directories, ``Long_Now__Conversations_at_The_Interval``
and ``Long_Now__Seminars_About_Long_term_Thinking``.
If we navigate into one of them and list its content, we'll see many ``.mp3`` files (here is an
excerpt).


.. runrecord:: _examples/DL-101-105-104
   :language: console
   :workdir: dl-101/DataLad-101/
   :lines: 1-15
   :cast: 01_dataset_basics
   :notes: And now lets look into these seminar series folders: There are hundreds of mp3 files, yet the download only took a few seconds! How can that be?

   $ cd recordings/longnow/Long_Now__Seminars_About_Long_term_Thinking
   $ ls


Dataset content identity and availability information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Surprised you turn to your fellow student and wonder about
how fast the dataset was installed. Should
a download of that many ``.mp3`` files not take much more time?

Here you can see another import feature of DataLad datasets
and the :command:`datalad install` command:

Upon installation of a DataLad dataset, DataLad retrieves only small files
(for example text files or markdown files) and (small) metadata
information about the dataset. It does not, however, download any large files
(yet). The metadata exposes the dataset's file hierarchy
for exploration (note how you are able to list the dataset contents with ``ls``),
and downloading only this metadata speeds up the installation of a DataLad dataset
of many TB in size to a few seconds. Just now, after installation, the dataset is
small in size:

.. runrecord:: _examples/DL-101-105-105
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow/Long_Now__Seminars_About_Long_term_Thinking
   :cast: 01_dataset_basics
   :notes: Upon installation of a DataLad dataset, DataLad retrieves only small files and metadata. Therefore the dataset is tiny in size. The files are non-functional now atm (Try opening one)

   $ cd ../      # in longnow/
   $ du -sh      # Unix command to show size of contents

This is tiny indeed!

If you executed the previous ``ls`` command in your own terminal, you might have seen
the ``.mp3`` files highlighted in a different color than usually.
On your computer, try to open
one of the ``.mp3`` files.

You will notice that you cannot open any of the
audio files. This is not your fault: *None of these files exist on your computer yet*.

Wait, what?

This sounds strange, but it has many advantages. Apart from a fast installation,
it allows you to retrieve precisely the content you need, instead of all the contents
of a dataset. Thus, even if you install a dataset that is many TB in size,
it takes up only few MB of space after installation, and you can retrieve only those
components of the dataset that you need.

Let's see how large the dataset would be in total if all of the files were present.
For this, we supply an additional option to :command:`datalad status`. Make sure to be
(anywhere) inside of the ``longnow`` dataset to execute the following command:

.. runrecord:: _examples/DL-101-105-106
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: But how large would the dataset be if we had all the content?

   $ datalad status --annex

Woah! More than 200 files, totaling more than 15 GB?
You begin to appreciate that DataLad did not
download all of this data right away! That would have taken hours given the crappy
internet connection in the lecture hall, and you aren't even sure whether your
hard drive has much space left...


But you nevertheless are curious on how to actually listen to one of these ``.mp3``\s now.
So how does one actually "get" the files?

.. index:: ! datalad command; get

The command to retrieve file content is :command:`datalad get` (:manpage:`datalad-get` manual).
You can specify one or more
specific files, or ``get`` all of the dataset by specifying :command:`datalad get .` (with ``.``
denoting "current directory").

First, we get one of the recordings in the dataset -- take any one of your choice
(here, its the first).

.. runrecord:: _examples/DL-101-105-107
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: Now let's finally get some content in this dataset. This is done with the datalad get command

   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

Try to open it -- it will now work.

If you would want to get the rest of the missing data, instead of specifying all files individually,
we can use ``.`` to refer to *all* of the dataset like this:

.. code-block:: bash

   $ datalad get .

(However, with a total size of more than 15GB, this might take a while, so do not do that now.
If you did execute the command above, interrupt it by pressing ``CTRL`` + ``C`` -- Do not worry,
this will not break anything)

Isn't that easy?

Let's see how much data is now present locally. For this, :command:`datalad status --annex all`
has a nice summary:

.. runrecord:: _examples/DL-101-105-108
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: Datalad status can also summarize how much of the content is already present locally:

   $ datalad status --annex all

This shows you how much data of the total data is present locally. With one file,
it is only a fraction of the total size.

Let's ``get`` a few more recordings, just because it was so mesmerizing to watch
DataLad's fancy progress bars.

.. runrecord:: _examples/DL-101-105-109
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: Let's get a few more files. Note how already obtained files are not downloaded again:

   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3 \
   Long_Now__Seminars_About_Long_term_Thinking/2003_12_13__Peter_Schwartz__The_Art_Of_The_Really_Long_View.mp3 \
   Long_Now__Seminars_About_Long_term_Thinking/2004_01_10__George_Dyson__There_s_Plenty_of_Room_at_the_Top__Long_term_Thinking_About_Large_scale_Computing.mp3

Note that any data that is already retrieved (the first file) is not downloaded again.
Datalad summarizes the outcome of the execution of ``get`` in the end and informs
that the download of one file was ``notneeded`` and the retrieval of the other files was ``ok``.

You have now experienced how easy it is to obtain shared data with DataLad.
But beyond simply sharing the *data* in the dataset, when sharing or installing
a DataLad dataset, all copies also include the datasets *history*.

For example, we can find out who created the dataset in the first place
(the output shows an excerpt of ``git log --reverse``, which displays the
history from first to most recent commit):

.. runrecord:: _examples/DL-101-105-110
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :emphasize-lines: 3
   :lines: 1-13
   :cast: 01_dataset_basics
   :notes: On Dataset nesting: You have seen the history of DataLad-101. But the subdataset has a standalone history as well! We can find out who created it!


   $ git log --reverse

But that's not all. The seminar series is ongoing, and more recordings can get added
to the original repository shared on Github.
Because an installed dataset knows the dataset it was installed from,
the locally installed dataset can simply be updated, and thus get the new recordings,
should there be some. But we will see examples of this later in this handbook.

Now you can not only create datasets and work with them locally, you can also consume
existing datasets by installing them. Because that's cool, and because you will use this
command frequently, make a note of it into your ``notes.txt``, and :command:`datalad save` the
modification.

.. runrecord:: _examples/DL-101-105-111
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: We can make a note about this:

   # in the root of DataLad-101:
   $ cd ../../
   $ cat << EOT >> notes.txt
   The command 'datalad install [--source] PATH'
   installs a dataset from e.g., a URL or a path.
   If you install a dataset into an existing
   dataset (as a subdataset), remember to specify the
   root of the superdataset with the '-d' option.

   EOT
   $ datalad save -m "Add note on datalad install"


.. note::

  Listing files directly after an installation of a dataset will
  work if done in a terminal with ``ls``.
  However, certain file managers (such as OSX's Finder [#f3]_) may fail to
  display files that are not yet present locally (i.e., before a
  :command:`datalad get` was run). Therefore, be  mindful when exploring
  a dataset hierarchy with a file manager -- it might not show you
  the available but not yet retrieved files. More about why this is will be
  explained in section :ref:`symlink`.

.. rubric:: Footnotes

.. [#f1] Additionally, a source  can also be a pointer to an open-data collection,
         for example :term:`the DataLad superdataset ///` -- more on what this is and how to
         use it later, though.

.. [#f2] The longnow podcasts are lectures and conversations on long-term thinking produced by
         the LongNow foundation. Subscribe to the podcasts at http://longnow.org/seminars/podcast.
         Support the foundation by becoming a member: https://longnow.org/membership. http://longnow.org

.. [#f3] You can also upgrade your file manager to display file types in a
         DataLad datasets (e.g., with the
         `git-annex-turtle extension <https://github.com/andrewringler/git-annex-turtle>`_
         for Finder)
