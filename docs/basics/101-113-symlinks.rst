Modifying large content
-----------------------

So far, we mastered quite a number of challenges: Creating and populating a dataset with
large and small files, modifying content and saving the changes to history, installing
datasets, installing subdatasets within datasets, and recording the impact of commands
on a dataset with the run and re-run commands.

We learned that when we modified content in ``notes.txt``, the modified content was
in a textfile, and that this, in conjunction with the initial configuration template
``text2git`` we gave to ``datalad create``, is meaningful: As the textfile is stored in Git and not
Git-annex, no content unlocking is necessary. As we saw within the demonstrations of ``datalad run``,
modifying content of non-textfiles, such as ``.png``\s requires -- in some types of dataset --
the additional step of *unlocking* file content, either by hand with the ``datalad unlock``
command, or within ``datalad run`` using the ``-o``/``--output`` flag.


Symlinks
--------

There is one detail about DataLad datasets that we haven't covered yet. Its both
a crucial aspect to understanding many aspects of a dataset, but it is also a
potential source of confusion.

You might have noticed already that an ``ls -l`` or ``tree`` command in your dataset shows small
arrows and quite cryptic paths following each non-textfile. Maybe your shell also
displays these files in a different color than textfiles when listing
them. We'll take a look together, using the ``books/`` directory as an example:

.. runrecord:: _examples/DL-101-113-101
   :language: console
   :workdir: dl-101/DataLad-101

   # in the root of DataLad-101
   $ cd books
   $ tree

If you don't know what you are looking at,
this looks weird, if not even intimidating -- or worse: it looks wrong or broken.
First of all: no, it is all fine. But lets start with the basics of what is displayed
here to understand it.

The small ``->`` symbol connecting one path (the books name) to another path (the weird
sequence of characters ending in ``.pdf``) is what is called a
*symbolic link* (short: :term:`symlink`) or *softlink*.
It is a term for any file that contains a reference to another file or directory as
a :term:`relative path` or :term:`absolute path` (in DataLad datasets, we will
only see relative paths). If you use Windows, a related concept is that of a
shortcut.

This means that the files that are in the locations in which you saved content
to, and are named as you named your files, are not actually your files: they
just point to the place where the actual file secretly resides.

But where exactly are the files you created or saved then?
The start of the link path is ``../.git``. The section :ref:`createDS` contained
a note that strongly advised that you should not temper with
(or in the worst case, delete) the ``.git``
repository that was created with ``datalad create``. One reason
why you should not do this is because this directory is where all of your file content
is actually stored.

But why is that? We have to talk a bit Git-annex now in order to understand it.
Note, though, that the information below applies to everything that is not an
*adjusted branch* in a Git-annex *v7 repository* (this information does not make
sense yet, but it will be an important reference point later on; currently, we
do not yet have a v7 repository in ``DataLad-101``).

When a file is given to DataLad to track, DataLad gives the file to Git-annex
if it is larger than a configurable size or not of certain specified types
(e.g. textfiles, as with the ``text2git`` configuration template).

Git-annex, in order to version control the data, takes the file content
and moves it under ``.git/annex/objects`` (the so called *object-tree*),
renames the file, and in its place
creates a symlink pointing to the new location. This is often referred to
as a file being *annexed*.

For a demonstration, take the target path of any of the books symlinks and
open it, for example with ``evince <path>`` (here, for technical reasons,
we extract the symlink of TLCL.pdf
with the ``readlink`` Unix command, but you can simply
copy the path printed in ``tree`` or ``ls -l``).

.. code-block:: bash

   $ evince $(readlink -f TLCL.pdf)

Even though the path looks cryptic, it works and opens the file. Whenever you
use a command like ``evince TLCL.pdf``, internally, your shell will follow
the symlink you have just opened.

But why does this symlink-ing happen? The resulting symlinks that look like
your files but only point to the actual content in ``.git/annex/objects`` are
small in size. An ``ls -lah`` reveals that all of these symlinks have roughly the same,
small size:

.. runrecord:: _examples/DL-101-113-102
   :language: console
   :workdir: dl-101/DataLad-101/books

   $ ls -lah

And small file size means that Git can handle those files!
Therefore, instead of large file content, only the symlinks are committed into
git, and the Git repository stays lean while pointing to arbitrarily large files.

.. container:: toggle

   .. container:: header

      **Addition: more about paths, checksums, and object trees**

   But why does the path needs to be so cryptic? Does someone wants to create
   maximal confusion with those? Can't it be ... more *readable*?

   Its not malicious intent that leads to these paths and file names. Its
   checksums. And they are quite readable -- just not for humans, but Git-annex.
   Understanding the next section is completely irrelevant for the
   subsequent sections of the book. But it can help to establish trust in that
   your data is safely stored and tracked, and it can get certainly helpful
   should you be one of those weird persons that always want to understand
   things (those people are great, btw!). Also, certain file management operations
   can be messy: for example, you shouldn't attempt to move a subdirectory
   (more on this in a dedicated section <link>), because it can break symlinks.
   Knowing bits of the basics can make you more confident with your datasets.

   So how do these names come into existence?

   When a file is annexed, Git-annex generates a *key* from the file content
   that it uses it as a name for the file.
   The key is associated with the content of the file (the *value*).
   Therefore, using this key, file content can be (somewhat) identified
   (or rather: it can be identified whether two files have identical contents,
   or whether file content changed).

   The key is generated using *hashes*. A hash is a function that turns an
   input (e.g. a PDF file) into a string of characters with a fixed length.
   In principle, therefore, the hash function simply transforms a content of
   any size into a string with fixed length.

   The important aspect of it is that it
   will generate the same hash for the same file content, but once file content
   changes, the generated hash will also look differently. If two files are
   turned into identical character strings, the content in these files is
   identical.

   This key (or :term:`checksum`) is the last part of the name of the file the
   symlink links to (in which the actual data content
   is stored). The extension (e.g. ``.pdf``) is appended because some
   operating systems need this information. The key is also one of the subdirectories
   names. This two-level structure is implemented because it helps to prevent
   accidental deletions and changes.

   .. runrecord:: _examples/DL-101-113-103
      :language: console
      :workdir: dl-101/DataLad-101/books

      # take a look at the last part of the target path:
      $ ls -lah TLCL.pdf
      # compare it to the checksum (here of type md5sum) of the PDF file and the subdirectory name
      $ md5sum TLCL.pdf

   There are different hash functions available. Depending on which is used,
   the resulting :term:`checksum` has a certain length and structure.
   By default, DataLad uses ``MD5e`` checksums, but should you want to, you can
   change this default to `one of many other types <https://git-annex.branchable.com/backends/>`_.
   The first part of the file name actually states which hash function is used.

   By now we know where almost all file name paths derived from - the last bit is the
   one after the checksum identifier. It is the size of the content in bytes. An annexed
   file in the object tree thus has a file name following this structure:

   ``checksum-identifier - size -- checksum . extension``

   Lastly, there are two more directories on top of the subdirectory that contains the
   hash, consisting of two letters each. These two letters are also derived from the md5sum,
   and in general exist to avoid issues with too many files in one directory.

