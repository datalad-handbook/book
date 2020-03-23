
********
Glossary
********


.. glossary::

   absolute path
      The complete path from the root of the file system. Absolute paths always start with ``/``.
      Example: ``/home/user/Pictures/xkcd-webcomics/530.png``. See also :term:`relative path`.

   adjusted branch
      (git-annex term) TODO

   annex
      Git annex concept: a different word for :term:`object-tree`.

   annex UUID
       A :term:`UUID` assigned to an annex of each individual :term:`clone` of a dataset repository.
       :term:`git-annex` uses this UUID to track file content availability information.
       The UUID is available under the configuration key ``annex.uuid`` and is stored in the
       configuration file of a local clone (``<dataset root>/.git/config``).
       A single dataset instance (i.e. a local clone) has exactly one annex UUID,
       but other clones of the same dataset each have their own unique annex UUIDs.

   bare Git repositories
       A bare Git repository is a repository that contains the contents of the ``.git``
       directory of regular DataLad datasets or Git repositories, but no worktree
       or checkout. This has advantages: The repository is leaner, it is easier
       for administrators to perform garbage collections, and it is required if you
       want to push to it at all times. You can find out more on what bare repositories are and how to use them
       `here <https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a
       -Server>`__.

   bash
      A Unix shell and command language.

   Bitbucket
      Bitbucket is an online platform where one can store and share version
      controlled projects using Git (and thus also DataLad project), similar
      to :term:`GitHub` or :term:`GitLab`. See `bitbucket.org <https://bitbucket.org.com/>`_.

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
      Git concept: A concise summary of changes you should attach to a :command:`datalad save` command. This summary will
      show up in your :term:`DataLad dataset` history.

   DataLad dataset
      A DataLad dataset is a Git repository that may or may not have a data annex that is used to
      manage data referenced in a dataset. In practice, most DataLad datasets will come with an annex.

   DataLad subdataset
      A DataLad dataset contained within a different DataLad dataset (the parent or :term:`DataLad superdataset`).

   DataLad superdataset
      A DataLad dataset that contains one or more levels of other DataLad datasets (:term:`DataLad subdataset`).

   dataset ID
      A :term:`UUID` that identifies a dataset as a unit -- across its entire history and flavors.
      This ID is stored in a dataset's own configuration file (``<dataset root>/.datalad/config``)
      under the configuration key ``datalad.dataset.id``.
      As this configuration is stored in a file that is part of the Git
      history of a dataset, this ID is identical for all :term:`clone`\s of a dataset and across all
      its versions.

   Debian
      A common Linux distribution. `More information here <https://www.debian.org/index.en.html>`__.

   DOI
      A digital object identifier (DOI) is a character string used to permanently identify
      a resource and link to in on the web. A DOI will always refer to the one resource
      it was assigned to, and only that one.

   environment variable
      A variable made up of a name/value pair. Programs using a given environment variable
      will use its associated value for their execution.

   ephemeral clone
      TODO

   GIN
      A web-based repository store for data management that you can use to host and
      share datasets. Find out more about GIN `here <https://gin.g-node.org/G-Node/Info/wiki>`__.

   Git
      A version control system to track changes made to small-sized files over time. You can find out
      more about git in `this (free) book <https://git-scm.com/book/en/v2>`_
      or `these interactive Git tutorials <https://try.github.io/>`_ on :term:`GitHub`.

   git-annex
      A distributed file synchronization system, enabling sharing and synchronizing collections
      of large files. It allows managing files with :term:`Git`, without checking the file content into Git.

   git-annex branch
      A :term:`branch` in your dataset if it contains an :term:`annex`.  It is
      completely unconnected to any other branches in your dataset, and contains
      different types of log files. The contents of this branch are used for
      git-annex internal tracking of the dataset and its annexed contents.
      It is managed by :term:`git-annex`, and you should not temper with it.

   Git config file
      A file in which :term:`Git` stores configuration option. Such a file usually exists on
      the system, user, and repository (dataset) level.

   GitHub
      GitHub is an online platform where one can store and share version controlled projects
      using Git (and thus also DataLad project). See`GitHub.com <https://github.com/>`_.

   Gitk
      A repository browser that displays changes in a repository or a selected set of commits. It
      visualizes a commit graph, information related to each commit, and the files in the trees
      of each revision.

   GitLab
      An online platform to host and share software projects version controlled with :term:`Git`,
      similar to :term:`GitHub`. See `Gitlab.com <https://about.gitlab.com/>`_.

   globbing
      A powerful pattern matching function of a shell. Allows to match the names of multiple files
      or directories. The most basic pattern is ``*``, which matches any number of character, such
      that ``ls *.txt`` will list all ``.txt`` files in the current directory.
      You can read about more about Pattern Matching in
      `Bash's Docs <https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Pattern-Matching>`_.

   http
      Hypertext Transfer Protocol; A protocol for file transfer over a network.

   https
      Hypertext Transfer Protocol Secure; A protocol for file transfer over a network.

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
      git-annex concept: The place where :term:`git-annex` stores available file contents. Files that are annexed get
      a :term:`symlink` added to :term:`Git` that points to the file content. A different word for :term:`annex`.

   permissions
      Access rights assigned by most file systems that determine whether a user can view (``read permission``),
      change (``write permission``), or execute (``execute permission``) a specific content.

      - ``read permissions`` grant the ability to a file, or the contents (file names) in a directory.
      - ``write permissions`` grant the ability to modify a file. When content is stored in the
        :term:`object-tree` by :term:`git-annex`, your previously granted write permission for this
        content is revoked to prevent accidental modifications.
      - ``execute permissions`` grant the ability to execute a file. Any script that should be an executable
        needs to get such permission.

   pip
      A Python package manager. Short for "Pip installs Python". ``pip install <package name>``
      searches the Python package index `PyPi <https://pypi.org/>`_ for a
      package and installs it while resolving any potential dependencies.

   provenance
      A record that describes entities and processes that were involved in producing or influencing
      a digital resource. It provides a critical foundation for assessing authenticity, enables trust,
      and allows reproducibility.

   publication dependency
      DataLad concept: An existing :term:`sibling` is linked to a new sibling
      so that the existing sibling is always published prior to the new sibling.
      The existing sibling could be a :term:`special remote` to publish file
      contents stored in the dataset :term:`annex` automatically with every
      :command:`datalad push` to the new sibling. Publication dependencies can be
      set with the option ``publish-depends`` in the commands
      :command:`datalad siblings`, :command:`datalad create-sibling`, and
      :command:`datalad create-sibling-github/gitlab`.

   relative path
      A path related to the present working directory. Relative paths never start with ``/``.
      Example: ``../Pictures/xkcd-webcomics/530.png``. See also :term:`absolute path`.

   remote
      Git-terminology: A repository (and thus also :term:`DataLad dataset`) that a given repository
      tracks. A :term:`sibling` is DataLad's equivalent to a remote.

   Remote Indexed Archive (RIA) store
      A Remote Indexed Archive (RIA) Store is a flexible and scalable dataset storage
      solution, useful for collaborative, back-up, or storage workflows. Read more
      about RIA stores in the usecase :ref:`usecase_datastore`.

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
      If the script has executable :term:`permissions`, it is henceforth able to call the interpreter itself.
      Instead of ``python code/myscript.py`` one can just run ``code/myscript`` if ``myscript`` has
      executable :term:`permissions` and a correctly specified shebang.

   special remote
      git-annex concept: A protocol that defines the underlying transport of annexed files
      to and from places that are not :term:`Git` repositories (e.g., a cloud service or
      external machines such as HPC systems).

   SSH
      Secure shell (SSH) is a network protocol to link one machine (computer),
      the *client*, to a different local or remote machine, the *server*. See also: :term:`SSH server`.

   SSH key
      An SSH key is an access credential in the SSH protocol that can be used to login
      from one system to remote servers and services, such as from your private
      computer to an :term:`SSH server`, without supplying your username or password
      at each visit. To use an SSH key for authentication, you need to generate a
      key pair on the system you would like to use to access a remote system or service
      (most likely, your computer).
      The pair consists of a *private* and a *public* key. The public key is shared
      with the remote server, and the private key is used to authenticate your machine
      whenever you want to access the remote server or service.
      Services such as :term:`GitHub`, :term:`GitLab`, and :term:`GIN` use SSH keys and the SSH protocol
      to ease access to repositories. This
      `tutorial by GitHub <https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_
      is a detailed step-by-step instruction to generate and use SSH keys for authentication.

   SSH server
      An remote or local computer that users can log into using the :term:`SSH` protocol.

   symlink
      A symbolic link (also symlink or soft link) is a reference to another file or path in the form
      of a relative path. Windows users are familiar with a similar concept: shortcuts.

   sibling
      DataLad concept: A dataset clone that a given :term:`DataLad dataset` knows about. Changes can be
      retrieved and pushed between a dataset and its sibling. It is the
      equivalent of a :term:`remote` in Git.

   submodule
      Git concept: a submodule is a Git repository embedded inside another Git repository. A
      :term:`DataLad subdataset` is known as a submodule in the :term:`Git config file`.

   tab completion
      Also known as command-line completion. A common shell feature in which
      the program automatically fills in partially types commands upon
      pressing the ``TAB`` key.


   tag
      Git concept: A mark on a commit that can help to identify commits. You can attach
      a tag with a name of your choice to any commit by supplying the ``--version-tag <TAG-NAME>``
      option to :command:`datalad save`.

   the DataLad superdataset ///
      DataLad provides unified access to a large amount of data at an open data
      collection found at `datasets.datalad.org <http://datasets.datalad.org/>`_.
      This collection is known as "The DataLad superdataset" and under its shortcut,
      ``///``. You can install the superdataset -- and subsequently query its content via metadata
      search -- by running ``datalad clone ///``.

   tig
      A text-mode interface for git that allows you to easily browse through your commit history.
      It is not part of git and needs to be installed. Find out more `here <https://jonas.github.io/tig/>`_.

   Ubuntu
      A common Linux distribution. `More information here <https://ubuntu.com>`__.

   UUID
      Universally Unique Identifier. It is a character string used for *unambiguous*,
      identification, formatted according to a specific standard. This
      identification is not only unambiguous and unique on a system, but indeed *universally*
      unique -- no UUID exists twice anywhere *on the planet*.
      Every DataLad dataset has a UUID that identifies a dataset uniquely as a whole across
      its entire history and flavors called :term:`Dataset ID` that looks similar to
      this ``0828ac72-f7c8-11e9-917f-a81e84238a11``. This dataset ID will only exist once,
      identifying only one particular dataset on the planet. Note that this does not
      require all UUIDs to be known in some central database -- the fact that no UUID
      exists twice is achieved by mere probability: The chance of a UUID being duplicated
      is so close to zero that it is negligible.

   version control
      Processes and tools to keep track of changes to documents or other collections of information.

   vim
      A text editor, often the default in UNIX operating systems. If you are not used to using it,
      but ended up in it accidentally: press ``ESC`` ``:`` ``q`` ``!`` ``Enter`` to exit without saving.
      Here is help: `A vim tutorial <https://www.openvim.com/>`_ and
      `how to configure the default editor for git <https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration>`_.

   zsh
      A Unix shell.