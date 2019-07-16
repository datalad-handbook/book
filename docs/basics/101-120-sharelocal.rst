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


.. todo::

   TODO: back in old directory, updates notes with

   cat << EOT >> notes.txt
   The command git annex whereis PATH lists the repositories that have
   file content.
   EOT
