.. index::
   pair: data file handling; with git-annex
.. _2-002:
.. _symlink:

Data integrity
--------------

So far, we mastered quite a number of challenges:
Creating and populating a dataset with large and small files, modifying content and saving the changes to history, installing datasets, even as subdatasets within datasets, recording the impact of commands on a dataset with the :dlcmd:`run` and :dlcmd:`rerun` commands, and capturing plenty of :term:`provenance` on the way.
We further noticed that when we modified content in ``notes.txt`` or ``list_titles.sh``, the modified content was in a *text file*.
We learned that this precise type of file, in conjunction with the initial configuration template ``text2git`` we gave to :dlcmd:`create`, is meaningful:
As the text file is stored in Git and not git-annex, no content unlocking is necessary.
As we saw within the demonstrations of :dlcmd:`run`, modifying content of non-text files, such as ``.jpg``\s, typically requires the additional step of *unlocking* file content, either by hand with the :dlcmd:`unlock` command, or within :dlcmd:`run` using the ``-o``/``--output`` flag.

There is one detail about DataLad datasets that we have not covered yet.
It is a crucial component to understanding certain aspects of a dataset, but it is also a potential source of confusion that we want to eradicate.

You might have noticed already that an ``ls -l`` or ``tree`` command in your dataset shows small arrows and quite cryptic paths following each non-text file.
Maybe your shell also displays these files in a different color than text files when listing them.
We'll take a look together, using the ``books/`` directory as an example.
Also check the :windows-wit:`on directory appearance <ww-directories>` for comparison:

.. index::
   pair: no symlinks; on Windows
   pair: tree; terminal command
.. windows-wit:: Dataset directories look different on Windows
   :name: ww-directories
   :float: tb

   First of all, the Windows ``tree`` command lists only directories by default, unless you parametrize it with ``/f``.
   And, secondly, even if you list the individual files, you would not see the :term:`symlink`\s shown below.
   Due to insufficient support for symlinks on Windows, git-annex does not use them.
   The :windows-wit:`on git-annex's adjusted mode <ww-adjusted-mode>` has more on that.

.. runrecord:: _examples/DL-101-115-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: We have to talk about symlinks now.
   :cast: 03_git_annex_basics

   $ # in the root of DataLad-101
   $ cd books
   $ tree

If you do not know what you are looking at,
this looks weird, if not worse: intimidating, wrong, or broken.
First of all: no, **it is all fine**. But let's start with the basics of what is displayed
here to understand it.

The small ``->`` symbol connecting one path (the book's name) to another path (the weird
sequence of characters ending in ``.pdf``) is what is called a
*symbolic link*, :term:`symlink` or *softlink* for short.
It is a term for any file that contains a reference to another file or directory as
a :term:`relative path` or :term:`absolute path`.
If you use Windows, you are familiar with a related, although more basic concept: a shortcut. But see the :windows-wit:`on how the actual behavior is there <ww-adjusted-mode>`.

This means that the files that are in the locations in which you saved content
and are named as you named your files (e.g., ``TLCL.pdf``),
do *not actually contain your files' content*:
they just point to the place where the actual file content resides.

This sounds weird, and like an unnecessary complication of things. But we will
get to why this is relevant and useful shortly. First, however,
where exactly are the contents of the files you created or saved?

The start of the link path is ``../.git``. The section :ref:`createDS` contained
a note that strongly advised that you to not tamper with
(or in the worst case, delete) the ``.git``
repository in the root of any dataset. One reason
why you should not do this is because *this* ``.git`` directory is where all of your file content
is actually stored.

But why is that? We have to talk a bit git-annex now in order to understand it.

When a file is saved into a dataset to be tracked,
by default -- that is in a dataset created without any configuration template --
DataLad gives this file to git-annex. Exceptions to this behavior can be
defined based on

#. file size

#. and/or path/pattern, and thus, for example, file extensions,
   or names, or file types (e.g., text files, as with the
   ``text2git`` configuration template).

git-annex, in order to version control the data, takes the file content
and moves it under ``.git/annex/objects`` -- the so called :term:`object-tree`.
It further renames the file into the sequence of characters you can see
in the path, and in its place
creates a symlink with the original file name, pointing to the new location.
This process is often referred to as a file being *annexed*, and the object
tree is also known as the *annex* of a dataset.

.. index::
   pair: elevated storage demand; in adjusted mode
   pair: no symlinks; on Windows
   pair: adjusted mode; on Windows
.. windows-wit:: File content management on Windows (adjusted mode)
   :name: ww-adjusted-mode
   :float: tbp

   .. include:: topic/adjustedmode-nosymlinks.rst

For a demonstration that this file path is not complete gibberish,
take the target path of any of the book's symlinks and
open it, for example with ``evince <path>``, or any other PDF reader in exchange for ``evince``:

.. runrecord:: _examples/DL-101-115-102
   :language: console
   :workdir: dl-101/DataLad-101/books
   :realcommand: echo "evince $(readlink TLCL.pdf)"
   :notes: we can just open the cryptic file path and it works just as any pdf!
   :cast: 03_git_annex_basics


Even though the path looks cryptic, it works and opens the file. Whenever you
use a command like ``evince TLCL.pdf``, internally, programs will follow
the same cryptic symlink like the one you have just opened.

But *why* does this symlink-ing happen? Up until now, it still seems like a very
unnecessary, superfluous thing to do, right?

The resulting symlinks that look like
your files but only point to the actual content in ``.git/annex/objects`` are
small in size. An ``ls -lh`` reveals that all of these symlinks have roughly the same,
small size of ~130 Bytes:

.. runrecord:: _examples/DL-101-115-103
   :language: console
   :workdir: dl-101/DataLad-101/books
   :realcommand: ls -lh --time-style=long-iso
   :notes: Symlinks are super small in size, just the amount of characters in the symlink!
   :cast: 03_git_annex_basics

   $ ls -lh

Here you can see the reason why content is symlinked: Small file size means that
*Git can handle those symlinks*!
Therefore, instead of large file content, only the symlinks are committed into
Git, and the Git repository thus stays lean. Simultaneously, still, all
files stored in Git as symlinks can point to arbitrarily large files in the
object tree. Within the object tree, git-annex handles file content tracking,
and is busy creating and maintaining appropriate symlinks so that your data
can be version controlled just as any text file.

This comes with two very important advantages:

One, should you have copies of the
same data in different places of your dataset, the symlinks of these files
point to the same place - in order to understand why this is the case, you
will need to read the :find-out-more:`on how git-annex manages file content <fom-objecttree>`.
Therefore, any amount of copies of a piece of data
is only one single piece of data in your object tree. This, depending on
how much identical file content lies in different parts of your dataset,
can save you much disk space and time.

The second advantage is less intuitive but clear for users familiar with Git.
Compared to copying and deleting huge data files, small symlinks can be written very very fast, for example, when switching dataset versions, or :term:`branch`\es.

.. gitusernote:: Speedy branch switches

   Switching branches fast, even when they track vasts amounts of data, lets you work with data using the same routines as in software development workflows.

This leads to a few conclusions:

The first is that you should not be worried
to see cryptic looking symlinks in your repository -- this is how it should look.
Again, you can read the :find-out-more:`on why these paths look so weird <fom-objecttree>` and what all of this has to do with data integrity, if you want to.
It has additional information that can help to establish trust in that your data are safely stored and tracked, and understanding more about the object tree and knowing bits of the git-annex basics can make you more confident in working with your datasets.

The second is that it should now be clear to you why the ``.git`` directory
should not be deleted or in any way modified by hand. This place is where
your data are stored, and you can trust git-annex to be better able to
work with the paths in the object tree than you or any other human are.

Lastly, understanding that annexed files in your dataset are symlinked
will be helpful to understand how common file system operations such as
moving, renaming, or copying content translate to dataset modifications
in certain situations. Later in this book, the section :ref:`file system`
will take a closer look at that.

.. _objecttree:
.. index::
   pair: key; git-annex concept
.. find-out-more:: Data integrity and annex keys
   :name: fom-objecttree
   :float: tbp

   So how do these cryptic paths and names in the object tree come into existence?
   It's not malicious intent that leads to these paths and file names - its checksums.

   When a file is annexed, git-annex typically generates a *key* (or :term:`annex key`) from the **file content**.
   It uses this key (in part) as a name for the file and as the path
   in the object tree.
   Thus, the key is associated with the content of the file (the *value*),
   and therefore, using this key, file content can be identified.

   Most key types contain a :term:`checksum`. This is a string of a fixed number of characters
   computed from some input, for example the content of a PDF file,
   by a *hash* function.

   This checksum *uniquely* identifies a file's content.
   A hash function will generate the same character sequence for the same file content, and once file content changes, the generated checksum changes, too.
   Basing the file name on its contents thus becomes a way of ensuring data integrity:
   File content cannot be changed without git-annex noticing, because the file's checksum, and thus its key in its symlink, will change.
   Furthermore, if two files have identical checksums, the content in these files is identical.
   Consequently, if two files have the same symlink, and thus link the same file in the object-tree, they are identical in content.
   This can save disk space if a dataset contains many identical files: Copies of the same data only need one instance of that content in the object tree, and all copies will symlink to it.
   If you want to read more about the computer science basics about hash functions check out the `Wikipedia page <https://en.wikipedia.org/wiki/Hash_function>`_.

   .. runrecord:: _examples/DL-101-115-104
      :language: console
      :workdir: dl-101/DataLad-101/books
      :realcommand: ls -lh --time-style=long-iso TLCL.pdf
      :notes: how does the symlink relate to the shasum of the file?
      :cast: 03_git_annex_basics

      $ # take a look at the last part of the target path:
      $ ls -lh TLCL.pdf

   Let's take a closer look at the structure of the symlink.
   The key from the hash function is the last part of the name of the file the symlink links to (in which the actual data content is stored).

   .. index::
      pair: compute checksum; in a terminal
   .. runrecord:: _examples/DL-101-115-105
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: let's look at how the shasum would look like
      :cast: 03_git_annex_basics

      $ # compare it to the checksum (here of type md5sum) of the PDF file and the subdirectory name
      $ md5sum TLCL.pdf

   The extension (e.g., ``.pdf``) is appended, because some programs require it, and would fail when not working directly with the symlink, but the file that it points to.
   Right at the beginning, the symlink starts with two directories just after ``.git/annex/objects/``,
   consisting of two letters each.
   These two letters are derived from the md5sum of the key, and their sole purpose to exist is to avoid issues with too many files in one directory (which is a situation that certain file systems have problems with).
   The next subdirectory in the symlink helps to prevent accidental deletions and changes, as it does not have write :term:`permissions`, so that users cannot modify any of its underlying contents.
   This is the reason that annexed files need to be unlocked prior to modifications, and this information will be helpful to understand some file system management operations such as removing files or datasets. Section :ref:`file system` takes a look at that.

   The next part of the symlink contains the actual checksum.
   There are different :term:`annex key` backends that use different checksums.
   Depending on which is used, the resulting :term:`checksum` has a certain length and structure, and the first part of the symlink actually states which hash function is used.
   By default, DataLad uses the ``MD5E`` git-annex backend (the ``E`` adds file extensions to annex keys), but should you want to, you can change this default to `one of many other types <https://git-annex.branchable.com/backends>`_.
   The reason why MD5E is used is the relatively short length of the underlying MD5 checksums -- which facilitates cross-platform compatibility for sharing datasets also with users on operating systems that have restrictions on total path length, such as Windows.

   The one remaining unidentified bit in the file name is the one after the checksum identifier.
   This part is the size of the content in bytes.
   An annexed file in the object tree thus has a file name following this structure
   (but see `the git-annex documentation on keys <https://git-annex.branchable.com/internals/key_format>`_ for the complete details):

   ``<backend type>-s<size>--<checksum>.<extension>``

   You now know a great deal more about git-annex and the object tree.
   Maybe you are as amazed as we are about some of the ingenuity used behind the scenes.
   Even more mesmerizing things about git-annex can be found in its `documentation <https://git-annex.branchable.com/git-annex>`_.


.. raw:: latex

   \vspace{1cm}

.. image:: ../artwork/src/teacher.svg
   :width: 50%
   :align: center

.. index:: ! broken symlink, ! symlink; broken
.. _wslfiles:

Broken symlinks
^^^^^^^^^^^^^^^

Whenever a symlink points to a non-existent target, this symlink is called
*broken* or *dangling*, and opening the symlink would not work as it does not resolve. The
section :ref:`file system` will give a thorough demonstration of how symlinks can
break, and how one can fix them again. Even though *broken* sounds
troublesome, most types of broken symlinks you will encounter can be fixed,
or are not problematic. At this point, you actually have already seen broken
symlinks: Back in section :ref:`installds` we explored
the file hierarchy in an installed subdataset that contained many annexed
``mp3`` files. Upon the initial :dlcmd:`clone`, the annexed files were not present locally.
Instead, their symlinks (stored in Git) existed and allowed to explore which
file's contents could be retrieved. These symlinks point to nothing, though, as
the content isn't yet present locally, and are thus *broken*. This state,
however, is not problematic at all. Once the content is retrieved via
:dlcmd:`get`, the symlink is functional again.

Nevertheless, it may be important to know that some tools that you would expect to work in a dataset with not yet retrieved file contents can encounter unintuitive problems.
Some **file managers** (e.g., OSX's Finder) may not display broken symlinks.
In these cases, it will be impossible to browse and explore the file hierarchy of not-yet-retrieved files with the file manager.
You can make sure to always be able to see the file hierarchy in two separate ways:
Upgrade your file manager to display file types in DataLad datasets (e.g., the `git-annex-turtle extension <https://github.com/andrewringler/git-annex-turtle>`_ for Finder), or use the `DataLad Gooey <https://docs.datalad.org/projects/gooey>`_ to browse datasets.
Alternatively, use the :shcmd:`ls` command in a terminal instead of a file manager GUI.
Other tools may be more more specialized, smaller, or domain-specific, and may fail to correctly work with broken symlinks, or display unhelpful error messages when handling them, or require additional flags to modify their behavior.
When encountering unexpected behavior or failures, try to keep in mind that a dataset without retrieved content appears to be a pile of broken symlinks to a range of tools, consult a tools documentation with regard to symlinks, and check whether data retrieval fixes persisting problems.

A last special case on symlinks exists if you are using DataLad on the Windows Subsystem for Linux. Take a look at the :windows-wit:`on WSL2 symlink access <ww-wsl2-symlinks>`
for that.

.. index::
   pair: access WSL2 symlinked files; on Windows
   single: WSL2; symlink access
   pair: log; Git command
.. windows-wit:: Accessing symlinked files from your Windows system
   :name: ww-wsl2-symlinks
   :float: tbp

   .. include:: topic/wsl2-symlinkaccess.rst


Finally, if you are still in the ``books/`` directory, go back into the root of
the superdataset.

.. runrecord:: _examples/DL-101-115-106
   :workdir: dl-101/DataLad-101/books
   :language: console
   :notes: understanding how symlinks work will help you with everyday file management operations.
   :cast: 03_git_annex_basics

   $ cd ../
