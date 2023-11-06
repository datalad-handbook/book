.. index::
   pair: clone; DataLad command
   pair: clone dataset; with DataLad
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

"With DataLad, users can install *clones* of existing DataLad datasets from paths, URLs, or
open-data collections" our lecturer begins.
"This makes accessing data fast and easy. A dataset that others could install can be
created by anyone, without a need for additional software. Your own datasets can be
installed by others, should you want that, for example. Therefore, not only accessing
data becomes fast and easy, but also *sharing*."
"That's so cool!", you think. "Exam preparation will be a piece of cake if all of us
can share our mid-term and final projects easily!"
"But today, let's only focus on how to install a dataset", she continues.
"Damn it! Can we not have longer lectures?", you think and set alarms to all of the
upcoming lecture dates in your calendar.
There is so much exciting stuff to come, you can not miss a single one.

"Psst!" a student from the row behind reaches over. "There are
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
good addition to the large stash of yet-to-read text books we piled up.
Let's get this dataset into our existing ``DataLad-101`` dataset.

To keep the ``DataLad-101`` dataset neat and organized, we first create a new directory,
called recordings.

.. runrecord:: _examples/DL-101-105-101
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: The next challenge is to clone an existing dataset from the web as a subdataset. First, we create a location for this

   # we are in the root of DataLad-101
   $ mkdir recordings


The command that can be used to obtain a dataset is :dlcmd:`clone`,
but we often refer to the process of cloning a Dataset as *installing*.
Let's install the longnow podcasts in this new directory.

The :dlcmd:`clone` command takes a location of an existing dataset to clone. This *source*
can be a URL or a path to a local directory, or an SSH server [#f1]_. The dataset
to be installed lives on :term:`GitHub`, at
`https://github.com/datalad-datasets/longnow-podcasts.git <https://github.com/datalad-datasets/longnow-podcasts>`_,
and we can give its GitHub URL as the  first positional argument.
Optionally, the command also takes as second positional argument a path to the *destination*,
-- a path to where we want to install the dataset to. In this case it is ``recordings/longnow``.
Because we are installing a dataset (the podcasts) into an existing dataset (the ``DataLad-101``
dataset), we also supply a ``-d/--dataset`` flag to the command.
This specifies the dataset to perform the operation on, and allows us to install
the podcasts as a *subdataset* of ``DataLad-101``. Because we are in the root
of the ``DataLad-101`` dataset, the pointer to the dataset is a ``.`` (which is Unix'
way of saying "current directory").

As before with long commands, we line break the code below with a ``\``. You can
copy it as it is presented here into your terminal, but in your own work you
can write commands like this into a single line.

.. runrecord:: _examples/DL-101-105-102
   :language: console
   :workdir: dl-101/DataLad-101/
   :cast: 01_dataset_basics
   :notes: We need to clone the dataset as a subdataset. For this, we use the datalad clone command with a --dataset option and a path. Else the dataset would not be registered as a subdataset!

   $ datalad clone --dataset . \
    https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow

This command copied the repository found at the URL https://github.com/datalad-datasets/longnow-podcasts
into the existing ``DataLad-101`` dataset, into the directory ``recordings/longnow``.
The optional destination is helpful: If we had not specified the path
``recordings/longnow`` as a destination for the dataset clone, the command would
have installed the dataset into the root of the ``DataLad-101`` dataset, and instead
of ``longnow`` it would have used the name of the remote repository "``longnow-podcasts``".
But the coolest feature of :dlcmd:`clone` is yet invisible: This command
also recorded where this dataset came from, thus capturing its *origin* as
:term:`provenance`. Even though this is not obvious at this point in time, later
chapters in this handbook will demonstrate how useful this information can be.

.. index::
   pair: clone; DataLad concept
.. gitusernote:: Clone internals

   The :dlcmd:`clone` command uses :gitcmd:`clone`.
   A dataset that is installed from an existing source, e.g., a path or URL,
   is the DataLad equivalent of a *clone* in Git.

.. index::
   pair: clone into another dataset; with DataLad
.. find-out-more:: Do I have to install from the root of datasets?

   No. Instead of from the *root* of the ``DataLad-101`` dataset, you could have also
   installed the dataset from within the ``recordings``, or ``books`` directory.
   In the case of installing datasets into existing datasets you however need
   to adjust the paths that are given with the ``-d/--dataset`` option:
   ``-d`` needs to specify the path to the root of the dataset. This is
   important to keep in mind whenever you do not execute the :dlcmd:`clone` command
   from the root of this dataset. Luckily, there is a shortcut: ``-d^`` will always
   point to root of the top-most dataset. For example, if you navigate into ``recordings``,
   the command would be:

   .. code-block:: bash

     datalad clone -d^ https://github.com/datalad-datasets/longnow-podcasts.git longnow

.. find-out-more:: What if I do not install into an existing dataset?

   If you do not install into an existing dataset, you only need to omit the ``-d/--dataset``
   option. You can try:

   .. code-block:: bash
  
     datalad clone https://github.com/datalad-datasets/longnow-podcasts.git

   anywhere outside of your ``DataLad-101`` dataset to install the podcast dataset into a new directory
   called ``longnow-podcasts``. You could even do this inside of an existing dataset.
   However, whenever you install datasets into of other datasets, the ``-d/--dataset``
   option is necessary to not only install the dataset, but also *register* it
   automatically into the higher level *superdataset*. The upcoming section will
   elaborate on this.

Here is the repository structure:

.. index::
   pair: tree; terminal command
   pair: display directory tree; on Windows
.. windows-wit:: use tree

   The Windows version of tree requires different parametrization, so please run ``tree`` instead of ``tree -d``.

.. runrecord:: _examples/DL-101-105-103
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 01_dataset_basics
   :notes: Let's take a look at the directory structure after cloning

   $ tree -d   # we limit the output to directories

We can see that ``recordings`` has one subdirectory, our newly installed ``longnow``
dataset with two subdirectories.
If we navigate into one of them and list its content, we'll see many ``.mp3`` files (here is an excerpt).

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

Surprised, you turn to your fellow student and wonder about
how fast the dataset was installed. Should
a download of that many ``.mp3`` files not take much more time?

Here you can see another import feature of DataLad datasets
and the :dlcmd:`clone` command:
Upon installation of a DataLad dataset, DataLad retrieves only small files
(for example text files or markdown files) and (small) metadata
about the dataset. It does not, however, download any large files
(yet). The metadata exposes the dataset's file hierarchy
for exploration (note how you are able to list the dataset contents with ``ls``),
and downloading only this metadata speeds up the installation of a DataLad dataset
of many TB in size to a few seconds. Just now, after installing, the dataset is
small in size:

.. index::
   pair: show file size; in a terminal
.. runrecord:: _examples/DL-101-105-105
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow/Long_Now__Seminars_About_Long_term_Thinking
   :cast: 01_dataset_basics
   :notes: Upon cloning of a DataLad dataset, DataLad retrieves only small files and metadata. Therefore the dataset is tiny in size. The files are non-functional now atm (Try opening one)

   $ cd ../      # in longnow/
   $ du -sh      # Unix command to show size of contents

This is tiny indeed!

If you executed the previous ``ls`` command in your own terminal, you might have seen
the ``.mp3`` files highlighted in a different color than usually.
On your computer, try to open one of the ``.mp3`` files.
You will notice that you cannot open any of the audio files.
This is not your fault: *None of these files exist on your computer yet*.

Wait, what?

This sounds strange, but it has many advantages. Apart from a fast installation,
it allows you to retrieve precisely the content you need, instead of all the contents
of a dataset. Thus, even if you install a dataset that is many TB in size,
it takes up only few MB of space after the install, and you can retrieve only those
components of the dataset that you need.

Let's see how large the dataset would be in total if all of the files were present.
For this, we supply an additional option to :dlcmd:`status`. Make sure to be
(somewhere) inside of the ``longnow`` dataset to execute the following command:

.. runrecord:: _examples/DL-101-105-106
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: But how large would the dataset be if we had all the content?

   $ datalad status --annex

Woah! More than 200 files, totaling more than 15 GB?
You begin to appreciate that DataLad did not
download all of this data right away! That would have taken hours given the crappy
internet connection in the lecture hall, and you are not even sure whether your
hard drive has much space left...


But you nevertheless are curious on how to actually listen to one of these ``.mp3``\s now.
So how does one actually "get" the files?

.. index::
   pair: get; DataLad command

The command to retrieve file content is :dlcmd:`get`.
You can specify one or more specific files, or ``get`` all of the dataset by
specifying :dlcmd:`get .` at the root directory of the dataset (with ``.`` denoting "current directory").

.. index::
   pair: get file content; with DataLad

First, we get one of the recordings in the dataset -- take any one of your choice
(here, it's the first).

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

However, with a total size of more than 15GB, this might take a while, so do not do that now.
If you did execute the command above, interrupt it by pressing ``CTRL`` + ``C`` -- Do not worry,
this will not break anything.

.. index::
   pair: show dataset size; with DataLad

Isn't that easy?
Let's see how much content is now present locally. For this, :dlcmd:`status --annex all`
has a nice summary:

.. runrecord:: _examples/DL-101-105-108
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: DataLad status can also summarize how much of the content is already present locally:

   $ datalad status --annex all

This shows you how much of the total content is present locally. With one file,
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
DataLad summarizes the outcome of the execution of ``get`` in the end and informs
that the download of one file was ``notneeded`` and the retrieval of the other files was ``ok``.


.. index::
   pair: get; DataLad concept
.. gitusernote:: Get internals

   :dlcmd:`get` uses :gitannexcmd:`get` underneath the hood.

.. index::
   pair: drop file content; with DataLad

Keep whatever you like
^^^^^^^^^^^^^^^^^^^^^^

"Oh shit, oh shit, oh shit..." you hear from right behind you. Your fellow student
apparently downloaded the *full* dataset accidentally. "Is there a way to get rid
of file contents in dataset, too?", they ask. "Yes", the lecturer responds,
"you can remove file contents by using :dlcmd:`drop`. This is
really helpful to save disk space for data you can easily reobtain, for example".

.. index::
   pair: drop; DataLad command

The :dlcmd:`drop` command will remove
file contents completely from your dataset.
You should only use this command to remove contents that you can :dlcmd:`get`
again, or generate again (for example with next chapter's :dlcmd:`datalad run`
command), or that you really do not need anymore.

Let's remove the content of one of the files that we have downloaded, and check
what this does to the total size of the dataset. Here is the current amount of
retrieved data in this dataset:

.. runrecord:: _examples/DL-101-105-110
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow

   $ datalad status --annex all

We drop a single recording's content that we previously downloaded with
:dlcmd:`get` ...

.. runrecord:: _examples/DL-101-105-111
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow

   $ datalad drop Long_Now__Seminars_About_Long_term_Thinking/2004_01_10__George_Dyson__There_s_Plenty_of_Room_at_the_Top__Long_term_Thinking_About_Large_scale_Computing.mp3

... and check the size of the dataset again:

.. runrecord:: _examples/DL-101-105-112
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow

   $ datalad status --annex all

Dropping the file content of one ``mp3`` file saved roughly 40MB of disk space.
Whenever you need the recording again, it is easy to re-retrieve it:

.. runrecord:: _examples/DL-101-105-113
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow

   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2004_01_10__George_Dyson__There_s_Plenty_of_Room_at_the_Top__Long_term_Thinking_About_Large_scale_Computing.mp3

Reobtained!

This was only a quick digression into :dlcmd:`drop`. The main principles
of this command will become clear after chapter
:ref:`chapter_gitannex`, and its precise use is shown in the paragraph on
:ref:`removing file contents <remove>`.
At this point, however, you already know that datasets allow you do
:dlcmd:`drop` file contents flexibly. If you want to, you could have more
podcasts (or other data) on your computer than you have disk space available
by using DataLad datasets -- and that really is a cool feature to have.

Dataset archeology
^^^^^^^^^^^^^^^^^^

You have now experienced how easy it is to (re)obtain shared data with DataLad.
But beyond sharing only the *data* in the dataset, when sharing or installing
a DataLad dataset, all copies also include the dataset's *history*.

.. index::
   pair: log; Git command
   pair: show history (reverse); with Git

For example, we can find out who created the dataset in the first place
(the output shows an excerpt of ``git log --reverse``, which displays the
history from first to most recent commit):

.. runrecord:: _examples/DL-101-105-114
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :emphasize-lines: 3
   :lines: 1-13
   :cast: 01_dataset_basics
   :notes: On Dataset nesting: You have seen the history of DataLad-101. But the subdataset has a standalone history as well! We can find out who created it!


   $ git log --reverse

But that's not all. The seminar series is ongoing, and more recordings can get added
to the original repository shared on GitHub.
Because an installed dataset knows the dataset it was installed from,
your local dataset clone can be updated from its origin, and thus get the new recordings,
should there be some. Later in this handbook, we will see examples of this.

.. index::
   pair: update here-document; in a terminal
   pair: save dataset modification; with DataLad

Now you can not only create datasets and work with them locally, you can also consume
existing datasets by installing them. Because that's cool, and because you will use this
command frequently, make a note of it into your ``notes.txt``, and :dlcmd:`save` the
modification.

.. runrecord:: _examples/DL-101-105-115
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics
   :notes: We can make a note about this:

   # in the root of DataLad-101:
   $ cd ../../
   $ cat << EOT >> notes.txt
   The command 'datalad clone URL/PATH [PATH]' installs a dataset from
   e.g., a URL or a path. If you install a dataset into an existing
   dataset (as a subdataset), remember to specify the root of the
   superdataset with the '-d' option.

   EOT
   $ datalad save -m "Add note on datalad clone"

.. index::
   pair: placeholder files; on Mac
.. importantnote:: Empty files can be confusing

   Listing files directly after the installation of a dataset will
   work if done in a terminal with ``ls``.
   However, certain file managers (such as OSX's Finder [#f3]_) may fail to
   display files that are not yet present locally (i.e., before a
   :dlcmd:`get` was run). Therefore, be  mindful when exploring
   a dataset hierarchy with a file manager -- it might not show you
   the available but not yet retrieved files.
   Consider browsing datasets with the :term:`DataLad Gooey` to be on the safe side.
   More about why this is will be explained in section :ref:`symlink`.


.. only:: adminmode

   Add a tag at the section end.

     .. runrecord:: _examples/DL-101-105-116
        :language: console
        :workdir: dl-101/DataLad-101

        $ git branch sct_install_datasets


.. rubric:: Footnotes

.. [#f1] Additionally, a source  can also be a pointer to an open-data collection,
         for example :term:`the DataLad superdataset ///` -- more on what this is and how to
         use it later, though.

.. [#f2] The longnow podcasts are lectures and conversations on long-term thinking produced by
         the LongNow foundation and we can wholeheartedly recommend them for their worldly
         wisdoms and compelling, thoughtful ideas. Subscribe to the podcasts at https://longnow.org/seminars/podcast.
         Support the foundation by becoming a member: https://longnow.org/join.

.. [#f3] You can also upgrade your file manager to display file types in a
         DataLad datasets (e.g., with the
         `git-annex-turtle extension <https://github.com/andrewringler/git-annex-turtle>`_
         for Finder)
