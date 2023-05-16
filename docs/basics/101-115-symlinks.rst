.. index:: ! 2-002
.. _2-002:
.. _symlink:

Data integrity
--------------

So far, we mastered quite a number of challenges:
Creating and populating a dataset with large and small files, modifying content and saving the changes to history, installing datasets, even as subdatasets within datasets, recording the impact of commands on a dataset with the run and re-run commands, and capturing plenty of :term:`provenance` on the way.
We further noticed that when we modified content in ``notes.txt`` or ``list_titles.sh``, the modified content was in a *text file*.
We learned that this precise type of file, in conjunction with the initial configuration template ``text2git`` we gave to :command:`datalad create`, is meaningful:
As the text file is stored in Git and not git-annex, no content unlocking is necessary.
As we saw within the demonstrations of :command:`datalad run`, modifying content of non-text files, such as ``.jpg``\s, typically requires the additional step of *unlocking* file content, either by hand with the :command:`datalad unlock` command, or within :command:`datalad run` using the ``-o``/``--output`` flag.

There is one detail about DataLad datasets that we have not covered yet.
It is a crucial component to understanding certain aspects of a dataset, but it is also a potential source of confusion that we want to eradicate.

You might have noticed already that an ``ls -l`` or ``tree`` command in your dataset shows small arrows and quite cryptic paths following each non-text file.
Maybe your shell also displays these files in a different color than text files when listing them.
We'll take a look together, using the ``books/`` directory as an example:

.. windows-wit:: This will look different to you

   First of all, the ``tree`` equivalent provided by :term:`conda`\s ``m2-base`` package doesn't list individual files, only directories.
   And, secondly, even if you list the individual files (e.g., with ``ls -l``), you would not see the :term:`symlink`\s shown below.
   Due to insufficient support of symlinks on Windows, git-annex does not use them.
   Please read on for a basic understanding of how git-annex usually works -- a Windows Wit at the end of this section will then highlight the difference in functionality on Windows.

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

The small ``->`` symbol connecting one path (the book's name) to another path (the weird
sequence of characters ending in ``.pdf``) is what is called a
*symbolic link* (short: :term:`symlink`) or *softlink*.
It is a term for any file that contains a reference to another file or directory as
a :term:`relative path` or :term:`absolute path`.
If you use Windows, you are familiar with a related, although more basic concept: a shortcut.

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

But why is that? We have to talk a bit git-annex now in order to understand it [#f1]_.

When a file is saved into a dataset to be tracked,
by default -- that is in a dataset created without any configuration template --
DataLad gives this file to git-annex. Exceptions to this behavior can be
defined based on

#. file size

#. and/or path/pattern, and thus for example file extensions,
   or names, or file types (e.g., text files, as with the
   ``text2git`` configuration template).

git-annex, in order to version control the data, takes the file content
and moves it under ``.git/annex/objects`` -- the so called :term:`object-tree`.
It further renames the file into the sequence of characters you can see
in the path, and in its place
creates a symlink with the original file name, pointing to the new location.
This process is often referred to as a file being *annexed*, and the object
tree is also known as the *annex* of a dataset.

.. windows-wit:: What happens on Windows?
   :name: woa_objecttree
   :float:

   Windows has insufficient support for :term:`symlink`\s and revoking write :term:`permissions` on files.
   Therefore, :term:`git-annex` classifies it as a :term:`crippled filesystem` and has to stray from its default behavior.
   While git-annex on Unix-based file operating systems stores data in the annex and creates a symlink in the data's original place, on Windows it moves data into the :term:`annex` and creates a *copy* of the data in its original place.

   **Why is that?**
   Data *needs* to be in the annex for version control and transport logistics -- the annex is able to store all previous versions of the data, and manage the transport to other storage locations if you want to publish your dataset.
   But as the :ref:`Findoutmore in this section <fom-objecttree>` will show, the :term:`annex` is a non-human readable tree structure, and data thus also needs to exist in its original location.
   Thus, it exists in both places: its moved into the annex, and copied back into its original location.
   Once you edit an annexed file, the most recent version of the file is available in its original location, and past versions are stored and readily available in the annex.
   If you reset your dataset to a previous state (as is shown in the section :ref:`history`), the respective version of your data is taken from the annex and copied to replace the newer version, and vice versa.

   **But doesn't a copy mean data duplication?**
   Yes, absolutely!
   And that is a big downside to DataLad and :term:`git-annex` on Windows.
   If you have a dataset with annexed file contents (be that a dataset you created and populated yourself, or one that you cloned and got file contents with ``datalad get`` from), it will take up more space than on a Unix-based system.
   How much more?
   Every file that exists in your file hierarchy exists twice.
   A fresh dataset with one version of each file is thus twice as big as it would be on a Linux computer.
   Any past version of data does not exist in duplication.

   **Step-by-step demonstration**:
   Let's take a concrete example to explain the last point in more detail.
   How much space, do you think, is taken up in your dataset by the resized ``salt_logo_small.jpg`` image?
   As a reminder: It exists in two versions, a 400 by 400 pixel version (about 250Kb in size), and a 450 by 450 pixel version (about 310Kb in size).
   The 400 by 400 pixel version is the most recent one.
   The answer is: about 810Kb (~0.1Mb).
   The most recent 400x400px version exists twice (in the annex and as a copy), and the 450x450px copy exists once in the annex.
   If you would reset your dataset to the state when we created the 450x450px version, this file would instead exist twice.

   **Can I at least get unused or irrelevant data out of the dataset?**
   Yes, either with convenience commands (e.g., ``git annex unused`` followed by ``git annex dropunused``), or by explicitly using ``drop`` on files (or their past versions) that you don't want to keep anymore.
   Alternatively, you can transfer data you don't need but want to preserve to a different storage location.
   Later parts of the handbook will demonstrate each of these alternatives.

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
   :realcommand: ls -lah --time-style=long-iso
   :notes: Symlinks are super small in size, just the amount of characters in the symlink!
   :cast: 03_git_annex_basics

   $ ls -lah

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
point to the same place (in order to understand why this is the case, you
will need to read the hidden section at the end of the page).
Therefore, any amount of copies of a piece of data
is only one single piece of data in your object tree. This, depending on
how much identical file content lies in different parts of your dataset,
can save you much disk space and time.

The second advantage is less intuitive but clear for users familiar with Git.
Small symlinks can be written very very fast when switching :term:`branch`\es, as opposed to copying and deleting huge data files.

.. gitusernote:: Speedy branch switches

   Switching branches fast, even when they track vasts amounts of data, lets you work with data with the same routines as in software development.

This leads to a few conclusions:

The first is that you should not be worried
to see cryptic looking symlinks in your repository -- this is how it should look.
You can read the :ref:`find-out-more on why these paths look so weird <fom-objecttree>` and what all of this has to do with data integrity, if you want to.
It's additional information that can help to establish trust in that your data are safely stored and tracked, and understanding more about the object tree and knowing bits of the git-annex basics can make you more confident in working with your datasets.

The second is that it should now be clear to you why the ``.git`` directory
should not be deleted or in any way modified by hand. This place is where
your data are stored, and you can trust git-annex to be better able to
work with the paths in the object tree than you or any other human are.

Lastly, understanding that annexed files in your dataset are symlinked
will be helpful to understand how common file system operations such as
moving, renaming, or copying content translate to dataset modifications
in certain situations. Later in this book we will have a section on how
to manage the file system in a DataLad dataset (:ref:`filesystem`).


.. find-out-more:: more about paths, checksums, object trees, and data integrity
   :name: fom-objecttree

   So how do these cryptic paths and names in the object tree come into existence?
   Its not malicious intent that leads to these paths and file names - its checksums.

   When a file is annexed, git-annex generates a *key* (or :term:`checksum`) from the **file content**.
   It uses this key (in part) as a name for the file and as the path
   in the object tree.
   Thus, the key is associated with the content of the file (the *value*),
   and therefore, using this key, file content can be identified --
   or rather: Based on the keys, it can be identified whether file content changed,
   and whether two files have identical contents.

   The key is generated using *hashes*. A hash is a function that turns an
   input (e.g., a PDF file) into a string of characters with a fixed length based on its contents.

   Importantly, a hash function will generate the same character sequence for the same file content, and once file content changes, the generated hash changes, too.
   Basing the file name on its contents thus becomes a way of ensuring data integrity:
   File content can not be changed without git-annex noticing, because file's hash, and thus its key in its symlink, will change.
   Furthermore, if two files have identical hashes, the content in these files is identical.
   Consequently, if two files have the same symlink, and thus link the same file in the object-tree, they are identical in content.
   This can save disk space if a dataset contains many identical files: Copies of the same data only need one instance of that content in the object tree, and all copies will symlink to it.
   If you want to read more about the computer science basics about hashes check out the Wikipedia page `here <https://en.wikipedia.org/wiki/Hash_function>`_.

   .. runrecord:: _examples/DL-101-115-104
      :language: console
      :workdir: dl-101/DataLad-101/books
      :realcommand: ls -lah --time-style=long-iso TLCL.pdf
      :notes: how does the symlink relate to the shasum of the file?
      :cast: 03_git_annex_basics

      # take a look at the last part of the target path:
      $ ls -lah TLCL.pdf

   Let's take a closer look at the structure of the symlink.
   The key from the hash function is the last part of the name of the file the symlink links to (in which the actual data content is stored).

   .. runrecord:: _examples/DL-101-115-105
      :language: console
      :workdir: dl-101/DataLad-101/books
      :notes: let's look at how the shasum would look like
      :cast: 03_git_annex_basics

      # compare it to the checksum (here of type md5sum) of the PDF file and the subdirectory name
      $ md5sum TLCL.pdf

   The extension (e.g., ``.pdf``) is appended because some operating systems (*ehem*, Windows) need this information in order to select the right software to open a file.
   Right at the beginning, the symlink starts with two directories just after ``.git/annex/objects/``,
   consisting of two letters each.
   These two letters are derived from the md5sum of the key, and their sole purpose to exist is to avoid issues with too many files in one directory (which is a situation that certain file systems have problems with).
   The next subdirectory in the symlink helps to prevent accidental deletions and changes, as it does not have write :term:`permissions`, so that users cannot modify any of its underlying contents.
   This is the reason that annexed files need to be unlocked prior to modifications, and this information will be helpful to understand some file system management operations such as removing files or datasets (see section :ref:`filesystem`).

   The next part of the symlink contains the actual hash.
   There are different hash functions available.
   Depending on which is used, the resulting :term:`checksum` has a certain length and structure, and the first part of the symlink actually states which hash function is used.
   By default, DataLad uses ``MD5E`` checksums (relatively short and with a file extension), but should you want to, you can change this default to `one of many other types <https://git-annex.branchable.com/backends/>`_.
   The reason why MD5E is used is because of its short length -- thus it is possible to ensure cross-platform compatibility and share datasets also with users on operating systems that have restrictions on total path lengths, such as Windows.

   The one remaining unidentified bit in the file name is the one after the checksum identifier.
   This part is the size of the content in bytes.
   An annexed file in the object tree thus has a file name following this structure:

   ``checksum-identifier - size -- checksum . extension``

   You now know a great deal more about git-annex and the object tree.
   Maybe you are as amazed as we are about some of the ingenuity used behind the scenes.
   Even more mesmerizing things about git-annex can be found in its `documentation <https://git-annex.branchable.com/git-annex/>`_.

Broken symlinks
^^^^^^^^^^^^^^^

.. index:: ! broken symlink, ! symlink (broken)

Whenever a symlink points to a non-existent target, this symlink is called
*broken*, and opening the symlink would not work as it does not resolve. The
section :ref:`filesystem` will give a thorough demonstration of how symlinks can
break, and how one can fix them again. Even though *broken* sounds
troublesome, most types of broken symlinks you will encounter can be fixed,
or are not problematic. At this point, you actually have already seen broken
symlinks: Back in section :ref:`installds` we explored
the file hierarchy in an installed subdataset that contained many annexed
``mp3`` files. Upon the initial :command:`datalad clone`, the annexed files were not present locally.
Instead, their symlinks (stored in Git) existed and allowed to explore which
file's contents could be retrieved. These symlinks point to nothing, though, as
the content isn't yet present locally, and are thus *broken*. This state,
however, is not problematic at all. Once the content is retrieved via
:command:`datalad get`, the symlink is functional again.

Nevertheless, it may be important to know that some tools that you would expect to work in a dataset with not yet retrieved file contents can encounter unintuitive problems.
Some **file managers** (e.g., OSX's Finder) may not display broken symlinks.
In these cases, it will be impossible to browse and explore the file hierarchy of not-yet-retrieved files with the file manager.
You can make sure to always be able to see the file hierarchy in two separate ways:
Upgrade your file manager to display file types in DataLad datasets (e.g., the `git-annex-turtle extension <https://github.com/andrewringler/git-annex-turtle>`_ for Finder).
Alternatively, use the :command:`ls` command in a terminal instead of a file manager GUI.
Other tools may be more more specialized, smaller, or domain-specific, and may fail to correctly work with broken symlinks, or display unhelpful error messages when handling them, or require additional flags to modify their behavior (such as the :ref:`BIDS Validator <bidsvalidator>`, used in the neuroimaging community).
When encountering unexpected behavior or failures, try to keep in mind that a dataset without retrieved content appears to be a pile of broken symlinks to a range of tools, consult a tools documentation with regard to symlinks, and check whether data retrieval fixes persisting problems.


Finally, if you are still in the ``books/`` directory, go back into the root of
the superdataset.

.. runrecord:: _examples/DL-101-115-106
   :workdir: dl-101/DataLad-101/books
   :language: console
   :notes: understanding how symlinks work will help you with everyday file management operations.
   :cast: 03_git_annex_basics

   $ cd ../


.. _wslfiles:

Cross-OS filesharing with symlinks (WSL2 only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Are you using DataLad on the Windows Subsystem for Linux?
If so, please take a look into the Windows Wit below.

.. windows-wit:: Accessing symlinked files from your Windows system

   If you are using WSL2 you have access to a Linux kernel and POSIX filesystem, including symlink support.
   Your DataLad experience has therefore been exactly as it has been for macOS or Linux users.
   But one thing that bears the need for additional information is sharing files in dataset between your Linux and Windows system.

   Its fantastic that files created under Linux can be shared to Windows and used by Windows tools.
   Usually, you should be able to open an explorer and type ``\\wsl$\<distro>\<path>`` in the address bar to navigate to files under Linux, or type ``explorer.exe`` into the WSL2 terminal.
   Some core limitations of Windows can't be overcome, though: Windows usually isn't capable of handling symlinks.
   So while WSL2 can expose your dataset filled with symlinked files to Windows, your Windows tools can fail to open them.
   How can this be fixed?

   Whenever you need to work with files from your datasets under Windows, you should *unlock* with ``datalad unlock``.
   This operation copies the file from the annex back to its original location, and thus removes the symlink (and also returns write :term:`permissions` to the file).
   Alternatively, use `git-annex adjust --unlock <https://git-annex.branchable.com/git-annex-adjust/>`_ to switch to a new dataset :term:`branch` in which all files are unlocked.
   The branch is called ``adjusted/<branchname>(unlocked)`` (e.g., if the original branch name was ``main``, the new, adjusted branch will be called ``adjusted/main(unlocked)``).
   You can switch back to your original branch using ``git checkout <branchname>``.

.. rubric:: Footnotes

.. [#f1] Note, though, that the information below applies to everything that is not an
         *adjusted branch* in a git-annex *v7 repository* -- this information does not make
         sense yet, but it will be an important reference point later on.
         Just for the record: Currently, we do not yet have a v7 repository
         in ``DataLad-101``, and the explanation below applies to our current dataset.
