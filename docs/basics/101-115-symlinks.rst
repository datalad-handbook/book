.. _symlink:

Data integrity
--------------

So far, we mastered quite a number of challenges: Creating and populating a dataset with
large and small files, modifying content and saving the changes to history, installing
datasets, installing subdatasets within datasets, and recording the impact of commands
on a dataset with the run and re-run commands.
We further took note that when we modified content in ``notes.txt`` or ``list_files.py``,
the modified content was in a *text file*. We learned that
this precise type of file, in conjunction with the initial configuration template
``text2git`` we gave to :command:`datalad create`, is meaningful: As the textfile is
stored in Git and not Git-annex, no content unlocking is necessary.
As we saw within the demonstrations of :command:`datalad run`,
modifying content of non-text files, such as ``.jpg``\s, requires
-- spoiler: at least in our current type of dataset --
the additional step of *unlocking* file content, either by hand with the :command:`datalad unlock`
command, or within :command:`datalad run` using the ``-o``/``--output`` flag.

There is one detail about DataLad datasets that we have not covered yet. Its both
a crucial aspect to understanding certain aspects of a dataset, but it is also a
potential source of confusion that we want to eradicate.

You might have noticed already that an ``ls -l`` or ``tree`` command in your dataset shows small
arrows and quite cryptic paths following each non-text file. Maybe your shell also
displays these files in a different color than text files when listing
them. We'll take a look together, using the ``books/`` directory as an example:

.. runrecord:: _examples/DL-101-115-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: We have to talk about symlinks now.
   :cast: 03_git_annex_basics

   # in the root of DataLad-101
   $ cd books
   $ tree

If you do not know what you are looking at,
this looks weird, if not worse: intimidating, wrong, or broken.
First of all: no, **it is all fine**. But let's start with the basics of what is displayed
here to understand it.

The small ``->`` symbol connecting one path (the books name) to another path (the weird
sequence of characters ending in ``.pdf``) is what is called a
*symbolic link* (short: :term:`symlink`) or *softlink*.
It is a term for any file that contains a reference to another file or directory as
a :term:`relative path` or :term:`absolute path`.
If you use Windows, you are familiar with a related concept: a shortcut.

This means that the files that are in the locations in which you saved content
to and are named as you named your files (e.g., ``TLCL.pdf``),
do *not actually contain your files' content*:
they just point to the place where the actual file content resides.

This sounds weird, and like an unnecessary complication of things. But we will
get to why this is relevant and useful shortly. First, however,
where exactly are the contents of the files you created or saved?

The start of the link path is ``../.git``. The section :ref:`createDS` contained
a note that strongly advised that you to not temper with
(or in the worst case, delete) the ``.git``
repository in the root of any dataset. One reason
why you should not do this is because *this* ``.git`` directory is where all of your file content
is actually stored.

But why is that? We have to talk a bit Git-annex now in order to understand it [#f1]_.

When a file is saved into a dataset to be tracked,
by default -- that is in a dataset created without any configuration template --
DataLad gives this file to Git-annex. Exceptions to this behavior can be
defined based on

#. file size

#. and/or path/pattern, and thus for example file extensions,
   or names, or file types (e.g., text files, as with the
   ``text2git`` configuration template).

Git-annex, in order to version control the data, takes the file content
and moves it under ``.git/annex/objects`` -- the so called :term:`object-tree`.
It further renames the file into the sequence of characters you can see
in the path, and in its place
creates a symlink with the original file name, pointing to the new location.
This process is often referred to as a file being *annexed*, and the object
tree is also known as the *annex* of a dataset.

For a demonstration that this file path is not complete gibberish,
take the target path of any of the book's symlinks and
open it, for example with ``evince <path>`` (Note: exchange ``evince`` with
your standard PDF reader).

.. runrecord:: _examples/DL-101-115-102
   :language: console
   :workdir: dl-101/DataLad-101/books
   :realcommand: echo "evince $(readlink TLCL.pdf)"
   :notes: we can just open the cryptic file path and it works just as any pdf!
   :cast: 03_git_annex_basics


Even though the path looks cryptic, it works and opens the file. Whenever you
use a command like ``evince TLCL.pdf``, internally, your shell will follow
the same cryptic symlink like the one you have just opened.

But *why* does this symlink-ing happen? Up until now, it still seems like a very
unnecessary, superfluous thing to do, right?

The resulting symlinks that look like
your files but only point to the actual content in ``.git/annex/objects`` are
small in size. An ``ls -lah`` reveals that all of these symlinks have roughly the same,
small size of ~130 Bytes:

.. runrecord:: _examples/DL-101-115-103
   :language: console
   :workdir: dl-101/DataLad-101/books
   :notes: Symlinks are super small in size, just the amount of characters in the symlink!
   :cast: 03_git_annex_basics

   $ ls -lah

Here you can see the reason why content is symlinked: Small file size means that
*Git can handle those symlinks*!
Therefore, instead of large file content, only the symlinks are committed into
Git, and the Git repository thus stays lean. Simultaneously, still, all
files stored in Git as symlinks can point to arbitrarily large files in the
object tree. Within the object tree, Git-annex handles file content tracking,
and is busy creating and maintaining appropriate symlinks so that your data
can be version controlled just as any text file.

This comes with a two very important advantages:

One, should you have copies of the
same data in different places of your dataset, the symlinks of these files
point to the same place (in order to understand why this is the case, you
will need to read the hidden section at the end of the page).
Therefore, any amount of copies of a piece of data
is only one single piece of data in your object tree. This, depending on
how much identical file content lies in different parts of your dataset,
can save you much disk space and time.

The second advantage is a

.. gitusernote::

   Small symlinks can be written very very fast when switching branches,
   as opposed to copying and deleting huge data files.

This leads to a few conclusions:

The first is that you should not be worried
to see cryptic looking symlinks in your repository -- this is how it should
look. If you are interested in why these paths look so weird, and what all
of this has to do with data integrity, you can check
out the hidden section below.

The second is that it should now be clear to you why the ``.git`` directory
should not be deleted or in any way modified by hand. This place is where
your data is stored, and you can trust Git-annex to be better able to
work with the paths in the object tree than you or any other human are.

Lastly, understanding that annexed files in your dataset are symlinked
will be helpful to understand how common file system operations such as
moving, renaming, or copying content translate to dataset modifications
in certain situations. Later in this book we will have a section on how
to manage the file system in a datalad dataset (:ref:`filesystem`).


.. findoutmore:: more about paths, checksums, object trees, and data integrity

   But why does the target path to the object tree needs to be so cryptic?
   Does someone want to create
   maximal confusion with this naming? Can't it be ... more *readable*?

   Its not malicious intent that leads to these paths and file names. Its
   checksums. And they are quite readable -- just not for humans, but Git-annex.
   Understanding the next section is completely irrelevant for the
   subsequent sections of the book. But it can help to establish trust in that
   your data is safely stored and tracked, and it can get certainly helpful
   should you be one of those people that always want to understand
   things in depth. Also, certain file management operations
   can be messy -- for example, when you attempt to move a subdirectory
   (more on this in a dedicated section :ref:`filesystem`) it can break symlinks, and
   you need to take appropriate actions to get the dataset back into a clean
   state.
   Understanding more about the object tree can help to understand such
   problems, and knowing bits of the Git-annex basics can make you more
   confident in working with your datasets.

   So how do these paths and names come into existence?

   When a file is annexed, Git-annex generates a *key* from the **file content**.
   It uses this key (in part) as a name for the file and as the path
   in the object tree.
   Thus, the key is associated with the content of the file (the *value*),
   and therefore, using this key, file content can be identified --
   or rather: Based on the keys, it can be identified whether two files
   have identical contents, and whether file content changed.

   The key is generated using *hashes*. A hash is a function that turns an
   input (e.g., a PDF file) into a string of characters with a fixed length.
   In principle, therefore, the hash function simply transforms a content of
   any size into a string with fixed length.

   The important aspect of a hash function is that it
   will generate the same hash for the same file content, but once file content
   changes, the generated hash will also look differently. If two files are
   turned into identical character strings, the content in these files is thus
   identical. Therefore, if two files have the same symlink, and thus
   link the same file in the object-tree, they are identical in content.
   If you have many copies of the same data in your dataset, the object
   tree will contain only one instance of that content, and all copies will
   symlink to it, thus saving disk space. But furthermore,
   the file name also becomes a way of ensuring data integrity. File content
   can not be changed without Git-annex noticing, because the symlink to the
   file content will change. If you want to read more about the
   computer science basics about about hashes check out the Wikipedia
   page `here <https://en.wikipedia.org/wiki/Hash_function>`_.

   This key (or :term:`checksum`) is the last part of the name of the file the
   symlink links to (in which the actual data content
   is stored). The extension (e.g., ``.pdf``) is appended because some
   operating systems (Windows) need this information.
   The key is also one of the subdirectory names in the path. This subdirectory
   adds an important feature to the :term:`object-tree`: It revokes the users
   permissions to modify it.
   This two-level structure is implemented because it helps to prevent
   accidental deletions and changes, and this information will be helpful
   to understand some file system management operations (see section
   :ref:`filesystem`), for
   example deleting a subdataset.

   .. runrecord:: _examples/DL-101-115-104
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: how does the symlink relate to the shasum of the file?
      :cast: 03_git_annex_basics

      # take a look at the last part of the target path:
      $ ls -lah TLCL.pdf

   .. runrecord:: _examples/DL-101-115-105
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: let's look at how the shasum would look like
      :cast: 03_git_annex_basics

      # compare it to the checksum (here of type md5sum) of the PDF file and the subdirectory name
      $ md5sum TLCL.pdf

   There are different hash functions available. Depending on which is used,
   the resulting :term:`checksum` has a certain length and structure.
   By default, DataLad uses ``MD5E`` checksums, but should you want to, you can
   change this default to `one of many other types <https://git-annex.branchable.com/backends/>`_.
   The first part of the file name actually states which hash function is used.
   The reason why MD5E is used is because it is comparatively short -- thus it
   is possible to share your datasets also with users on operating systems that
   have restrictions on total path lengths (Windows). Therefore, refrain from
   changing this default if you are on Windows, or want Windows user to be able
   to use your dataset.


   By now we know where almost all parts of the file name derived from -- the remaining
   unidentified bit in the file name is the
   one after the checksum identifier. This part is the size of the content in bytes. An annexed
   file in the object tree thus has a file name following this structure:

   ``checksum-identifier - size -- checksum . extension``

   As a last puzzle piece to shed some light onto the path in the object tree,
   there are two more directories on top of the subdirectory named after the checksum,
   just after ``.git/annex/objects/``,
   consisting of two letters each. These two letters are also derived from the md5sum
   of the key, and their sole purpose to exist is to avoid issues with too many files
   in one directory (which is a situation that certain file systems have problems with).

   In summary, you now know a great deal about Git-annex and the object tree. Maybe you
   are as amazed as we are about some of the ingenuity used behind the scenes. In any
   case, this section was hopefully insightful, and not confusing. If you are still curious
   about Git-annex, you can check out its
   `documentation <https://git-annex.branchable.com/git-annex/>`_.

Broken symlinks
^^^^^^^^^^^^^^^

Whenever a symlink points to a non-existent target, this symlink is called
*broken*, and opening the symlink would not work as it does not resolve. The
section :ref:`filesystem` will give a thorough demonstration of how symlinks can
break, and how one can fix them again. Even though *broken* sounds
troublesome, most types of broken symlinks you will encounter can be fixed,
or are not problematic. At this point, you actually have already seen broken
symlinks: Back in section :ref:`installds` we explored
the file hierarchy in an installed subdataset that contained many annexed
``mp3`` files. Upon installation, the annexed files were not present locally.
Instead, their symlinks (stored in Git) existed and allowed to explore which
file's contents could be retrieved. These symlinks point to nothing, though, as
the content isn't yet present locally, and are thus *broken*. This state,
however, is not problematic at all. Once the content is retrieved via
:command:`datalad get`, the symlink is functional again.

Nevertheless, it may be important to know that some file managers (e.g., OSX's
Finder) may not display broken symlinks. In these cases, it will be
impossible to browse and explore the file hierarchy of not-yet-retrieved
files with the file manager. You can make sure to always be able to see the
file hierarchy in two seperate ways: Upgrade your file manager to display
file types in a DataLad datasets (e.g., the
`git-annex-turtle extension <https://github.com/andrewringler/git-annex-turtle>`_
for Finder). Alternatively, use the :command:`ls` command in a terminal instead
of a file manager GUI.

Finally, if you are still in the ``books/`` directory, go back into the root of
the superdataset.

.. runrecord:: _examples/DL-101-115-106
   :workdir: dl-101/DataLad-101/books
   :language: console
   :notes: understanding how symlinks work will help you with everyday file management operations.
   :cast: 03_git_annex_basics

   $ cd ../

.. rubric:: Footnotes

.. [#f1] Note, though, that the information below applies to everything that is not an
         *adjusted branch* in a Git-annex *v7 repository* -- this information does not make
         sense yet, but it will be an important reference point later on.
         Just for the record: Currently, we do not yet have a v7 repository
         in ``DataLad-101``, and the explanation below applies to our current dataset.
