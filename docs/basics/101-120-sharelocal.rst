Sharing datasets: Local File systems
------------------------------------

One exciting aspect of DataLad datasets has yet been missing from this
course: How does one share a dataset?

In this section, we will cover the simplest way of sharing a dataset:
on a local or shared filesystem, via an installation with a path as
a source.

A shared file system is a system that lets multiple users access the
same files at the same time. There are multiple different versions
of shared file systems, and likely, you have already used at least one
of them, for example an ``SSH server``.

.. todo::

   elaborate on this once I have a clear definition of what a shared file
   system is in my head and an idea of which types are commonly used.

Using file systems that many users can access makes sharing files
easy. Using DataLad for this sharing makes it even easier, though.

To demonstrate how to share a DataLad dataset on a common file system
in this course, we have to cheat a bit. We will pretend that you
want to install the ``DataLad-101`` dataset in a different place in
your own file system.

This serves two purposes: For one, you will experience a very easy
way of sharing a dataset. Secondly, it will show you the installation
of a dataset from a path (instead of a URL as shown in the section
:ref:`installds`). Thirdly, ``DataLad-101`` is a dataset that can
showcase many different properties of a dataset already, but it will
be an additional learning experience to see how the different parts
of the dataset -- textfiles, larger files, datalad subdataset -- will
appear upon installation when shared.

To install ``DataLad-101`` with datalad install into a different part
of your file system, navigate out of ``DataLad-101``, and -- for
simplicity -- create a new directory, ``mock_user``, right next to it:

.. runrecord:: _examples/DL-101-120-101
   :language: console
   :workdir: dl-101/DataLad-101

   $ cd ../
   $ mkdir mock_user

Afterwards, navigate into ``mock_user`` and install the dataset
``DataLad-101`` by specifying its path as a ``--source``.

.. runrecord:: _examples/DL-101-120-102
   :language: console
   :workdir: dl-101

   $ cd mock_user
   $ datalad install --source ../DataLad-101 --description "DataLad-101 in mock_user"

This will install ``DataLad-101``. Note that we have given this new
dataset a description about its location as well. Note further that we
have not provided a path to ``datalad install``, and hence it installed the
dataset under its original name in the current directory.

Lets see what this dataset looks like. Before running the command,
try to predict what you will see.

.. runrecord:: _examples/DL-101-120-103
   :language: console
   :workdir: dl-101/mock_user

   $ cd DataLad-101
   $ tree

There are a number of interesting things:
For one, the subdataset has a directory name, but apart from this,
the ``longnow`` directory appears empty. Secondly, the PDFs in
``books/`` appear as they did in the original dataset on first sight:
They are symlinks pointing to some location in the object tree.
But try to open them with a PDF viewer of your choice: They can't be
opened. This mimics our experience when installing the ``longnow``
subdataset: Right after installation, the ``.mp3`` files also could
not be opened, because their file content was not yet retrieved.
The textfiles contents, though, are present, and the files can be
opened.

Lets start by examing the PDFs further. Try to get one of the books:

.. runrecord:: _examples/DL-101-120-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad get books/progit.pdf

Opening this file will work, because the content was retrieved from
the original dataset. But how does DataLad know where to look for
that original content?

This information comes from Git-annex. Before getting the next PDF,
lets query Git-Annex where its content is stored:

.. runrecord:: _examples/DL-101-120-105
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ git annex whereis books/TLCL.pdf

Oh, another checksum! That's hard to read -- what is it?
Luckily, there is a human-readable description next to it:
"course on DataLad-101 on my private Laptop".

This is, finally, where we see the description provided in
``datalad create`` in section :ref:`createDS` becomes handy: It is
a human-readable description of where file content is stored.

The message further informs us that there is only one copy
of this file content known to exist.

To retrieve file content of an annexed file, Git-annex will try
to obtain it from the locations it knows to contain this content.
It uses the checksums to identify these locations.

.. todo::

   what is this checksum?

Let's now turn to the fact that the subdataset ``longnow`` does
not contain not only no file content, but also no file meta data
information to explore the contents of the dataset. This is behavior
that we haven't observed until now.

To fix this, you have to run a somewhat unexpected command:

.. runrecord:: _examples/DL-101-120-106
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad install recordings/longnow

Let's what has changed (excerpt):

.. runrecord:: _examples/DL-101-120-107
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :lines: 1-30

   $ tree

Interesting! The file meta data information is now present, and we can
explore the file hierarchy. The file content however, is not present yet.

What has happened here?

When DataLad installs a dataset, it will by default only install the
superdataset, and not the subdatasets. To explicitly install a dataset
*recursively*, that is, all of the subdatasets inside it as well, one
has to specify the ``-r``/``--recursive`` option:

``datalad install --source ../DataLad-101 -r --description "DataLad-101 in mock_user"``

would have installed the ``longnow`` subdataset as well, and the meta
data about file hierarchies would have been available right from the
start.

So why is this behavior disabled by default?
In :ref:`nesting` we learned that datasets can be nested *arbitrarily* deep.
Upon installing a dataset you might not want to also install a few dozen levels of
nested subdatasets right away.

However, the is a middle way: The ``--recursion-limit`` option let's
you specify how many levels of subdatasets should be installed together
with the superdataset.

``datalad install -s ../DataLad-101 --description "DataLad-101 in mock_user" -r --recursion-limit 1``
hence would have installed the subdataset right away.

Let's now however see the ``git annex whereis`` command in more detail.
Within the original ``DataLad-101`` dataset, we retrieved some of the ``.mp3``
files via ``datalad get``, but now others. How will this influence the
output of ``git annex whereis``?

.. runrecord:: _examples/DL-101-120-108
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   # navigate into the subdirectory
   $ cd recordings/longnow
   # file content exists in original DataLad-101 for this file
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

.. runrecord:: _examples/DL-101-120-109
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # but not for this:
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2005_01_15__James_Carse__Religious_War_In_Light_of_the_Infinite_Game.mp3

.. todo::

   at some point explain that and why it does not work like this from outside the subdataset

The file thats content is present in the original DataLad-101 has one more copy available
than the file that is not present.

.. todo::

   elaborate on what web and mih@medusa are.

.. todo::

   TODO: back in old directory, updates notes with

   cat << EOT >> notes.txt
   The command git annex whereis PATH lists the repositories that have
   file content.
   EOT
