.. _sharelocal1:

Looking without touching
------------------------

Only now, several weeks into the DataLad-101 course does your room
mate realize that he has enrolled in the course as well, but has not
yet attended at all. "Oh man, can you help me catch up?" he asks
you one day. "Sharing just your notes would be really cool for a
start already!"

"Sure thing", you say, and decide that it's probably best if he gets
all of the ``DataLad-101`` course dataset. Sharing datasets was
something you wanted to look into soon, anyway.

This is one exciting aspect of DataLad datasets that has yet been missing
from this course: How does one share a dataset?
In this section, we will cover the simplest way of sharing a dataset:
on a local or shared file system, via an *installation* with a path as
a source.

.. importantnote:: More on public data sharing

   Interested in sharing datasets *publicly*? Read this chapter to get a feel
   for all relevant basic concepts of sharing datasets. Afterwards, head over
   to chapter :ref:`chapter_thirdparty` to find out how to share a dataset
   on third-party infrastructure.

In this scenario multiple people can access the very same files at the
same time, often on the same machine (e.g., a shared workstation, or
a server that people can ":term:`SSH`" into). You might think: "What do I need
DataLad for, if everyone can already access everything?" However,
universal, unrestricted access can easily lead to chaos. DataLad can
help facilitate collaboration without requiring ultimate trust and
reliability of all participants. Essentially, with a shared dataset,
collaborators can see and use your dataset without any danger
of undesired, or uncontrolled modification.

To demonstrate how to share a DataLad dataset on a common file system,
we will pretend that your personal computer
can be accessed by other users. Let's say that
your room mate has access, and you are making sure that there is
a ``DataLad-101`` dataset in a different place on the file system
for him to access and work with.

This is indeed a common real-world use case: Two users on a shared
file system sharing a dataset with each other.
But as we cannot easily simulate a second user in this handbook,
for now, you will have to share your dataset with yourself.
This endeavor serves several purposes: For one, you will experience a very easy
way of sharing a dataset. Secondly, it will show you
how a dataset can be obtained from a path, instead of a URL as shown in section
:ref:`installds`. Thirdly, ``DataLad-101`` is a dataset that can
showcase many different properties of a dataset already, but it will
be an additional learning experience to see how the different parts
of the dataset -- text files, larger files, subdatasets,
:term:`run record`\s -- will appear upon installation when shared.
And lastly, you will likely "share a dataset with yourself" whenever you
will be using a particular dataset of your own creation as input for
one or more projects.

"Awesome!" exclaims your room mate as you take out your laptop to
share the dataset. "You are really saving my ass
here. I'll make up for it when we prepare for the final", he promises.

To install ``DataLad-101`` into a different part
of your file system, navigate out of ``DataLad-101``, and -- for
simplicity -- create a new directory, ``mock_user``, right next to it:

.. runrecord:: _examples/DL-101-116-101
   :language: console
   :workdir: dl-101
   :realcommand: mkdir mock_user
   :notes: (hope this works)
   :cast: 04_collaboration

   $ cd ../
   $ mkdir mock_user

For simplicity, pretend that this is a second user's -- your room mate's --
home directory. Furthermore, let's for now disregard anything about
:term:`permissions`. In a real-world example you likely would not be able to read and write
to a different user's directories, but we will talk about permissions later.

.. index::
   pair: clone; DataLad command
   pair: clone dataset (set location description); with DataLad

After creation, navigate into ``mock_user`` and install the dataset ``DataLad-101``.
To do this, use :dlcmd:`clone`, and provide a path to your original
dataset:

.. runrecord:: _examples/DL-101-116-102
   :language: console
   :workdir: dl-101
   :notes: We pretend to clone the DataLad-101 dataset into a different users home directory. To do this, we use datalad install with a path
   :cast: 04_collaboration


   $ cd mock_user
   $ datalad clone --description "DataLad-101 in mock_user" ../DataLad-101

This will install your dataset ``DataLad-101`` into your room mate's home
directory. Note that we have given this new
dataset a description about its location. Note further that we
have not provided the optional destination path to :dlcmd:`clone`,
and hence it installed the dataset under its original name in the current directory.

Together with your room mate, you go ahead and see what this dataset looks
like. Before running the command, try to predict what you will see.

.. runrecord:: _examples/DL-101-116-103
   :language: console
   :workdir: dl-101/mock_user
   :notes: How do you think does the dataset look like
   :cast: 04_collaboration

   $ cd DataLad-101
   $ tree

There are a number of interesting things, and your room mate is the
first to notice them:

"Hey, can you explain some things to me?", he asks. "This directory
here, "``longnow``", why is it empty?"
True, the subdataset has a directory name but apart from this,
the ``longnow`` directory appears empty.

"Also, why do the PDFs in ``books/`` and the ``.jpg`` files
appear so weird? They have
this cryptic path right next to them, and look, if I try to open
one of them, it fails! Did something go wrong when we installed
the dataset?" he worries.
Indeed, the PDFs and pictures appear just as they did in the original dataset
on first sight: They are symlinks pointing to some location in the
object tree. To reassure your room mate that everything is fine you
quickly explain to him the concept of a symlink and the :term:`object-tree`
of :term:`git-annex`.

.. index::
   pair: clone; DataLad command

"But why does the PDF not open when I try to open it?" he repeats.
True, these files cannot be opened. This mimics our experience when
installing the ``longnow`` subdataset: Right after installation,
the ``.mp3`` files also could not be opened, because their file
content was not yet retrieved. You begin to explain to your room mate
how DataLad retrieves only minimal metadata about which files actually
exist in a dataset upon a :dlcmd:`clone`. "It's really handy",
you tell him. "This way you can decide which book you want to read,
and then retrieve what you need. Everything that is *annexed* is retrieved
on demand. Note though that the text files
contents are present, and the files can be opened -- this is because
these files are stored in :term:`Git`. So you already have my notes,
and you can decide for yourself whether you want to ``get`` the books."

To demonstrate this, you decide to examine the PDFs further.
"Try to get one of the books", you instruct your room mate:

.. runrecord:: _examples/DL-101-116-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: how does it feel to get a file?
   :cast: 04_collaboration

   $ datalad get books/progit.pdf

"Opening this file will work, because the content was retrieved from
the original dataset.", you explain, proud that this worked just as you
thought it would.

Let's now turn to the fact that the subdataset ``longnow`` contains neither
file content nor file metadata information to explore the contents of the 
dataset: there are no subdirectories or any files under ``recordings/longnow/``.
This is behavior that you have not observed until now.

To fix this and obtain file availability metadata,
you have to run a somewhat unexpected command:

.. runrecord:: _examples/DL-101-116-107
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: how do we get the subdataset? currently it looks empty. --> a plain datalad install
   :cast: 04_collaboration

   $ datalad get -n recordings/longnow

Before we look further into :dlcmd:`get` and the
``-n/--no-data`` option, let's first see what has changed after
running the above command (excerpt):

.. runrecord:: _examples/DL-101-116-108
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :lines: 1-20
   :notes: what has changed? --> file metadata information!
   :cast: 04_collaboration

   $ tree

Interesting! The file metadata information is now present, and we can
explore the file hierarchy. The file content, however, is not present yet.

What has happened here?

When DataLad installs a dataset, it will by default only obtain the
superdataset, and not any subdatasets. The superdataset contains the
information that a subdataset exists though -- the subdataset is *registered*
in the superdataset.  This is why the subdataset name exists as a directory.
A subsequent :dlcmd:`get -n path/to/longnow` will install the registered
subdataset again, just as we did in the example above.

But what about the ``-n`` option for :dlcmd:`get`?
Previously, we used :dlcmd:`get` to get file content. However,
:dlcmd:`get` operates on more than just the level of *files* or *directories*.
Instead, it can also operate on the level of *datasets*. Regardless of whether
it is a single file (such as ``books/TLCL.pdf``) or a registered subdataset
(such as ``recordings/longnow``), :dlcmd:`get` will operate on it to 1) install
it -- if it is a not yet installed subdataset -- and 2) retrieve the contents of any files.
That makes it very easy to get your file content, regardless of
how your dataset may be structured -- it is always the same command, and DataLad
blurs the boundaries between superdatasets and subdatasets.

In the above example, we called :dlcmd:`get` with the option ``-n/--no-data``.
This option prevents that :dlcmd:`get` obtains the data of individual files or
directories, thus limiting its scope to the level of datasets as only a
:dlcmd:`clone` is performed. Without this option, the command would
have retrieved all of the subdatasets contents right away. But with ``-n/--no-data``,
it only installed the subdataset to retrieve the meta data about file availability.

.. index::
   pair: get all dataset content; with DataLad

To explicitly install all potential subdatasets *recursively*, that is,
all of the subdatasets inside it as well, one can give the
``-r``/``--recursive`` option to :dlcmd:`get`:

.. code-block:: console

  $ datalad get -n -r <subds>

This would install the ``subds`` subdataset and all potential further
subdatasets inside of it, and the meta data about file hierarchies would
have been available right away for every subdataset inside of ``subds``. If you
had several subdatasets and would not provide a path to a single dataset,
but, say, the current directory (``.`` as in :dlcmd:`get -n -r .`), it
would clone all registered subdatasets recursively.

So why is a recursive get not the default behavior?
In :ref:`nesting` we learned that datasets can be nested *arbitrarily* deep.
Upon getting the meta data of one dataset you might not want to also install
a few dozen levels of nested subdatasets right away.

However, there is a middle way [#f1]_: The ``--recursion-limit`` option let's
you specify how many levels of subdatasets should be installed together
with the first subdataset:

.. code-block:: console

  $ datalad get -n -r --recursion-limit 1 <subds>


To summarize what you learned in this section, write a note on how to
install a dataset using a path as a source on a common file system.

Write this note in "your own" (the original) ``DataLad-101`` dataset, though!

.. runrecord:: _examples/DL-101-116-109
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: note in original DataLad-101 dataset
   :cast: 04_collaboration

   $ # navigate back into the original dataset
   $ cd ../../DataLad-101
   $ # write the note
   $ cat << EOT >> notes.txt
   A source to install a dataset from can also be a path, for example as
   in "datalad clone ../DataLad-101".

   Just as in creating datasets, you can add a description on the
   location of the new dataset clone with the -D/--description option.

   Note that subdatasets will not be installed by default, but are only
   registered in the superdataset -- you will have to do a
   "datalad get -n PATH/TO/SUBDATASET" to install the subdataset for file
   availability meta data. The -n/--no-data options prevents that file
   contents are also downloaded.

   Note that a recursive "datalad get" would install all further
   registered subdatasets underneath a subdataset, so a safer way to
   proceed is to set a decent --recursion-limit:
   "datalad get -n -r --recursion-limit 2 <subds>"

   EOT

Save this note.

.. runrecord:: _examples/DL-101-116-110
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 04_collaboration

   $ datalad save -m "add note about cloning from paths and recursive datalad get"

.. index::
   pair: clone; DataLad concept
.. gitusernote:: Get a clone

   A dataset that is installed from an existing source, e.g., a path or URL,
   is the DataLad equivalent of a *clone* in Git.


.. only:: adminmode

    Add a tag at the section end.

      .. runrecord:: _examples/DL-101-116-111
         :language: console
         :workdir: dl-101/DataLad-101

         $ git branch sct_looking_without_touching


.. rubric:: Footnotes

.. [#f1] Another alternative to a recursion limit to :dlcmd:`get -n -r` is
         a dataset configuration that specifies subdatasets that should *not* be
         cloned recursively, unless explicitly given to the command with a path. With
         this configuration, a superdataset's maintainer can safeguard users and prevent
         potentially large amounts of subdatasets to be cloned.
         You can learn more about this configuration in the section :ref:`config2`.
