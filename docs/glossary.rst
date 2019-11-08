
********
Glossary
********


.. glossary::

   absolute path
      The complete path from the root of the file system. Absolute paths always start with ``/``.
      Example: ``/home/user/Pictures/xkcd-webcomics/530.png``. See also :term:`relative path`.

   adjusted branch
      (Git-annex term) TODO

   annex
      Git annex concept: a different word for :term:`object-tree`.

   bash
      A Unix shell and command language.

   branch
      Git concept: A lightweight, independent history streak of your dataset. Branches can contain less,
      more, or changed files compared to other branches, and one can :term:`merge` the changes
      a branch contains into another branch.

   checksum
      TODO

   clone
      Git concept: A copy of a :term:`Git` repository. In Git-terminology, all "installed" datasets
      are clones.

   commit
      Git concept: Adding selected changes of a file or dataset to the repository, and thus making these changes
      part of the revision history of the repository. Should always have an informative :term:`commit message`.

   commit message
      Git concept: A consise summary of changes you should attach to a :command:`datalad save` command. This summary will
      show up in your :term:`Datalad dataset` history.

   DataLad dataset
      A DataLad dataset is a Git repository that may or may not have a data annex that is used to
      manage data referenced in a dataset. In practice, most DataLad datasets will come with an annex.

   DataLad subdataset
      A DataLad dataset contained within a different DataLad dataset (the parent or :term:`DataLad superdataset`).

   DataLad superdataset
      A DataLad dataset that contains one or more levels of other DataLad datasets (:term:`DataLad subdataset`).

   Debian
      A common Linux distribution. `More information here <https://www.debian.org/index.en.html>`__.

   environment variable
      A variable made up of a name/value pair. Programs using a given environment variable
      will use its associated value for their execution.

   Git
      A version control system to track changes made to small-sized files over time. You can find out
      more about git in `this (free) book <https://git-scm.com/book/en/v2>`_
      or `these interactive Git tutorials <https://try.github.io/>`_ on :term:`Github`.

   Git-annex
      A distributed file synchronization system, enabling sharing and synchronizing collections
      of large files. It allows managing files with :term:`Git`, without checking the file content into Git.

   Git config file
      A file in which :term:`Git` stores configuration option. Such a file usually exists on
      the system, user, and repository (dataset) level.

   Github
      GitHub is an online platform where one can store and share version controlled projects
      using Git (and thus also DataLad project).

   Gitk
      A repository browser that displays changes in a repository or a selected set of commits. It
      visualizes a commit graph, information related to each commit, and the files in the trees
      of each revision.

   Github
      An online platform to host and share software projects version controlled with :term:`Git`. See
      https://github.com/.

   globbing
      A powerful pattern matching function of a shell. Allows to match the names of multiple files
      or directories. The most basic pattern is ``*``, which matches any number of character, such
      that ``ls *.txt`` will list all ``.txt`` files in the current directory.
      You can read about more about Pattern Matching in
      `Bash's Docs <https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Pattern-Matching>`_.

   master
      Git concept: The default :term:`branch` in a dataset.

   merge
      Git concept: to integrate the changes of one :term:`branch`/:term:`sibling`/ ... into
      a different branch.

   metadata
      "Data about data": Information about one or more aspects of data used to summarize
      basic information, for example means of create of the data, creator or author, size,
      or purpose of the data. For example, a digital image may include metadata that
      describes how large the picture is, the color depth, the image resolution, when the image
      was created, the shutter speed, and other data.

   nano
      A common text-editor.

   object-tree
      Git-annex concept: The place where :term:`Git-annex` stores available file contents. Files that are annexed get
      a :term:`symlink` added to :term:`Git` that points to the file content. A different word for :term:`annex`.

   provenance
      A record that describes entities and processes that were involved in producinng or influencing
      a digital resource. It provides a critical foundation for assessing authenticity, enables trust,
      and allows reproducibility.

   relative path
      A path related to the present working directory. Relative paths never start with ``/``.
      Example: ``../Pictures/xkcd-webcomics/530.png``. See also :term:`absolute path`.

   remote
      Git-terminology: A repository (and thus also :term:`DataLad dataset`) that a given repository
      tracks.

   run record
      A command summary of a :command:`datalad run` command, generated by DataLad and included
      in the commit message.

   shasum
      A hexadecimal number, 40 digits long, that is produced by a secure hash algorithm, and
      is used by :term:`Git` to identify :term:`commit`\s. A shasum is a type of :term:`checksum`.

   shebang
      The characters ``#!`` at the very top of a script. One can specify the interpreter (i.e., the
      software that executes a script of yours, such as Python) after with it such as in
      ``#! /usr/bin/python``.
      If the script has executable permissions, it is henceforth able to call the interpreter itself.
      Instead of ``python code/myscript.py`` one can just run ``code/myscript`` if ``myscript`` has
      executable permissions and a correctly specified shebang.

   SSH
      Secure shell (SSH) is a network protocol to link one machine (computer),
      the *client*, to a different local or remote machine, the *server*. See also: :term:`SSH server`.

   SSH server
      An remote or local computer that users can log into using the :term:`SSH` protocol.

   symlink
      A symbolic link (also symlink or soft link) is a reference to another file or path in the form
      of a relative path. Windows users are familiar with a similar concept: shortcuts.

   sibling
      DataLad concept: A dataset clone that a given :term:`DataLad dataset` knows about. Changes can be
      retrieved and pushed between a dataset and its sibling.

   submodule
      Git concept: a submodule is a Git repository embedded inside another Git repository. A
      :term:`DataLad subdataset` is known as a submodule in the :term:`Git config file`.

   tab completion
      Also known as command-line completion. A common shell feature in which
      the program automatically fills in partially types commands upon
      pressing the ``TAB`` key.

   the DataLad superdataset ///
      TODO

   tig
      A text-mode interface for git that allows you to easily browse through your commit history.
      It is not part of git and needs to be installed. Find out more `here <https://jonas.github.io/tig/>`_.

   Ubuntu
      A common Linux distribution. `More information here <https://ubuntu.com>`__.

   version control
      Processes and tools to keep track of changes to documents or other collections of information.

   vim
      A text editor, often the default in UNIX operating systems. If you are not used to using it,
      but ended up in it accidentally: press ``ESC`` ``:`` ``q`` ``!`` ``Enter`` to exit without saving.
      Here is help: `A vim tutorial <https://www.openvim.com/>`_ and
      `how to configure the default editor for git <https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration>`_.

