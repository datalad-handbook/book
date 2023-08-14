
.. _glossary:

********
Glossary
********

.. glossary::

   absolute path
      The complete path from the root of the file system. Absolute paths always start with ``/``.
      Example: ``/home/user/Pictures/xkcd-webcomics/530.png``. See also :term:`relative path`.

   adjusted branch
      git-annex concept: a special :term:`branch` in a dataset.
      Adjusted branches refer to a different, existing branch that is not adjusted.
      The adjusted branch is called "adjusted/<branchname>(unlocked)" and on an the adjusted branch", all files handled by :term:`git-annex` are not locked --
      They will stay "unlocked" and thus modifiable.
      Instead of referencing data in the :term:`annex` with a :term:`symlink`, unlocked files need to be copies of the data in the annex.
      Adjusted branches primarily exist as the default branch on so-called :term:`crippled filesystem`\s such as Windows.

   annex
      git-annex concept: a different word for :term:`object-tree`.

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
      A Unix :term:`shell` and command language.

   Bitbucket
      Bitbucket is an online platform where one can store and share version
      controlled projects using Git (and thus also DataLad project), similar
      to :term:`GitHub` or :term:`GitLab`. See `bitbucket.org <https://bitbucket.org>`_.

   branch
      Git concept: A lightweight, independent history streak of your dataset. Branches can contain less,
      more, or changed files compared to other branches, and one can :term:`merge` the changes
      a branch contains into another branch.

   checksum
      An alternative term to :term:`shasum`.

   clone
      Git concept: A copy of a :term:`Git` repository. In Git-terminology, all "installed" datasets
      are clones.

   commit
      Git concept: Adding selected changes of a file or dataset to the repository, and thus making these changes
      part of the revision history of the repository. Should always have an informative :term:`commit message`.

   commit message
      Git concept: A concise summary of changes you should attach to a :dlcmd:`save` command. This summary will
      show up in your :term:`DataLad dataset` history.

   compute node
      A compute node is an individual computer, part of a :term:`high-performance computing (HPC)` or :term:`high-throughput computing (HTC)` cluster.

   conda
      A package, dependency, and environment management system for a number of programming languages.
      Find out more at `docs.conda.io <https://docs.conda.io>`_.
      It overlaps with :term:`pip` in functionality, but it is advised to not use both tools simultaneously for package management.

   container recipe
       A text file template that lists all required components of the computational environment that a :term:`software container` should contain.
       It is made by a human user.

   container image
       Container images are *built* from :term:`container recipe` files.
       They are a static filesystem inside a file, populated with the software specified in the recipe, and some initial configuration.

   crippled filesystem
      git-annex concept: A file system that does not allow making symlinks or removing write :term:`permissions` from files. Examples for this are `FAT <https://en.wikipedia.org/wiki/Design_of_the_FAT_file_system>`_ (likely used by your USB sticks) or `NTFS <https://en.wikipedia.org/wiki/NTFS>`_ (used on Windows systems of the last three decades).

   DataLad dataset
      A DataLad dataset is a Git repository that may or may not have a data annex that is used to
      manage data referenced in a dataset. In practice, most DataLad datasets will come with an annex.

   DataLad extension
      Python packages that equip DataLad with specialized commands. The online version of the handbook has an entire chapter that
      gives an overview of available extensions contains demonstrations.

   DataLad Gooey
      A :term:`DataLad extension` that provides DataLad with a graphical user interface. Find out more in its Documentation: `docs.datalad.org/projects/gooey <https://docs.datalad.org/projects/gooey>`_

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
      A common Linux distribution. `More information at www.debian.org <https://www.debian.org/index.en.html>`__.

   debugging
      Finding and resolving problems within a computer program.
      To learn about debugging a failed execution of a DataLad command, take a look at the section :ref:`debug`.

   Docker
       `Docker <https://www.docker.com>`_ is a containerization software that can package software into :term:`software container`\s, similar to :term:`Singularity`.
       Find out more on `Wikipedia <https://en.wikipedia.org/wiki/Docker_(software)>`__.

   Docker-Hub
       `Docker Hub <https://hub.docker.com>`_ is a library for :term:`Docker` :term:`container image`\s.
       Among other things, it hosts and builds Docker container images.
       You can can *pull* :term:`container image`\s built from a publicly shared :term:`container recipe` from it.

   DOI
      A digital object identifier (DOI) is a character string used to permanently identify
      a resource and link to in on the web. A DOI will always refer to the one resource
      it was assigned to, and only that one.

   extractor
      DataLad concept: A metadata extractor of the :term:`DataLad extension` ``datalad-metalad``
      enables DataLad to extract and aggregate special types of metadata.

   environment variable
      A variable made up of a name/value pair. Programs using a given environment variable will use its associated value for their execution.
      You can find out a bit more on environment variable :ref:`in this Findoutmore <fom-envvar>`.

   ephemeral clone
      dataset clones that share the annex with the dataset they were cloned from, without :term:`git-annex` being aware of it.
      On a technical level, this is achieved via symlinks.
      They can be created with the ``--reckless ephemeral`` option of :dlcmd:`clone`.


   force-push
      Git concept; Enforcing a :gitcmd:`push` command with the ``--force``
      option. Find out more in the
      `documentation of git push <https://git-scm.com/docs/git-push#Documentation/git-push.txt---force>`_.

   fork
      Git concept on repository hosting sites (GitHub, GitLab, Gin, ...);
      `A fork is a copy of a repository on a web-based Git repository hosting site <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`__.

   GIN
      A web-based repository store for data management that you can use to host and
      share datasets. Find out more about GIN `at gin.g-node.org <https://gin.g-node.org/G-Node/Info/wiki>`__.

   Git
      A version control system to track changes made to small-sized files over time. You can find out
      more about git in `the (free) GitPro book <https://git-scm.com/book/en/v2>`_
      or `interactive Git tutorials <https://try.github.io>`_ on :term:`GitHub`.

   git-annex
      A distributed file synchronization system, enabling sharing and synchronizing collections
      of large files. It allows managing files with :term:`Git`, without checking the file content into Git.

   git-annex branch
      This :term:`branch` exists in your dataset if the dataset contains
      an :term:`annex`.  The git-annex branch is completely unconnected to any
      other branch in your dataset, and contains different types of log files.
      Its contents are used for git-annex's internal tracking of the dataset
      and its annexed contents.
      The branch is managed by :term:`git-annex`, and you should not tamper with
      it unless you absolutely know what you are doing.

   Git config file
      A file in which :term:`Git` stores configuration option. Such a file usually exists on
      the system, user, and repository (dataset) level.

   GitHub
      GitHub is an online platform where one can store and share version controlled projects
      using Git (and thus also DataLad project). See `GitHub.com <https://github.com>`_.

   Gitk
      A repository browser that displays changes in a repository or a selected set of commits. It
      visualizes a commit graph, information related to each commit, and the files in the trees
      of each revision.

   GitLab
      An online platform to host and share software projects version controlled with :term:`Git`,
      similar to :term:`GitHub`. See `Gitlab.com <https://about.gitlab.com>`_.

   globbing
      A powerful pattern matching function of a shell. Allows to match the names of multiple files
      or directories. The most basic pattern is ``*``, which matches any number of character, such
      that ``ls *.txt`` will list all ``.txt`` files in the current directory.
      You can read about more about Pattern Matching in
      `Bash's Docs <https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Pattern-Matching>`_.

   high-performance computing (HPC)
      Aggregating computing power from a bond of computers in a way that delivers higher performance than a typical desktop computer in order to solve computing tasks that require high computing power or demand a lot of disk space or memory.


   high-throughput computing (HTC)
      A computing environment build from a bond of computers and tuned to deliver large amounts of computational power to allow parallel processing of independent computational jobs. For more information, see `this Wikipedia entry <https://en.wikipedia.org/wiki/High-throughput_computing>`_.

   http
      Hypertext Transfer Protocol; A protocol for file transfer over a network.

   https
      Hypertext Transfer Protocol Secure; A protocol for file transfer over a network.

   logging
      Automatic protocol creation of software processes, for example in order to gain insights into errors. To learn about logging to troubleshoot problems or remove or increase the amount of information printed to your terminal during the execution of a DataLad command, take a look at the section :ref:`logging`.

   log level
      Adjusts the amount of verbosity during :term:`logging`.

   main
      Git concept: For the longest time, ``master`` was the name of the default :term:`branch` in a dataset. More recently, the name ``main`` is used. If you are not sure, you can find out if your default branch is ``main`` or ``master`` by running ``git branch``.

   Makefile
      Makefiles are recipes on how to create a digital object for the build automation tool `Make <https://en.wikipedia.org/wiki/Make_(software)>`_.
      They are used to build programs, but also to manage projects where some files must be automatically updated from others whenever the others change.

   manpage
      Abbreviation of "manual page". For most Unix programs, the command ``man <program-name>`` will open a :term:`pager` with this commands documentation. If you have installed DataLad as a Debian package, ``man`` will allow you to open DataLad manpages in your terminal.

   master
      Git concept: For the longest time, ``master`` was the name of the default :term:`branch` in a dataset. More recently, the name ``main`` is used. If you are not sure, you can find out if your default branch is ``main`` or ``master`` by running ``git branch``.

   merge
      Git concept: to integrate the changes of one :term:`branch`/:term:`sibling`/ ... into
      a different branch.

   merge request
     See :term:`pull request`.

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

   Open Science Framework (OSF)
      An open source software project that facilitates open collaboration in science research.

   pager
      A `terminal paper <https://en.wikipedia.org/wiki/Terminal_pager>`_ is a program to view file contents in the :term:`terminal`. Popular examples are the programs ``less`` and ``more``. Some terminal output can be opened automatically in a pager, for example the output of a :gitcmd:`log` command. You can use the arrow keys to navigate and scroll in the pager, and the letter ``q`` to exit it.

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
      searches the Python package index `PyPi <https://pypi.org>`_ for a
      package and installs it while resolving any potential dependencies.

   pipe
      Unix concept: A mechanism for providing the output of one command (:term:`stdout`) as the input of a next command (:term:`stdin`) in a Unix terminal. The standard syntax are multiple commands, separated by vertical bars (the "pipes", "|"). Read more `on Wikipedia <https://en.wikipedia.org/wiki/Pipeline_(Unix)>`_.

   provenance
      A record that describes entities and processes that were involved in producing or influencing
      a digital resource. It provides a critical foundation for assessing authenticity, enables trust,
      and allows reproducibility.

   publication dependency
      DataLad concept: An existing :term:`sibling` is linked to a new sibling
      so that the existing sibling is always published prior to the new sibling.
      The existing sibling could be a :term:`special remote` to publish file
      contents stored in the dataset :term:`annex` automatically with every
      :dlcmd:`push` to the new sibling. Publication dependencies can be
      set with the option ``publish-depends`` in the commands
      :dlcmd:`siblings`, :dlcmd:`create-sibling`, and
      :dlcmd:`create-sibling-github/gitlab`.


   pull request
      Also known as :term:`merge request`. Contributions to Git repositories/DataLad datasets can be proposed to be :term:`merge`\d into the dataset by "requesting a pull/update" from the dataset maintainer to obtain a proposed change from a dataset clone or sibling. It is implemented as a feature in repository hosting sites such as :term:`GitHub`, :term:`Gin`, or :term:`GitLab`.

   ref
      Git concept. A "Git Reference", typically shortened to "ref", is a text file containing a :term:`commit` :term:`shasum` as a human-readable reference to a specific version of your dataset or Git repository. Thanks to refs, Git users do not need to memorize or type shasums when switching between dataset states, and can use simple names instead: For example, a :term:`branch` such as ``main`` is a ref, and a :term:`tag` is one, too. In both cases, those refs are text files that contain the shasum of the commit at the tip of a branch, or the shasum of the commit you added the tag to. Refs are organized in the directory ``.git/refs`` and Git commands and configurations can use refs to perform updating operations or determine their behavior. More details can be found at `at git-scm.com <https://git-scm.com/book/en/v2/Git-Internals-Git-References>`_

   relative path
      A path related to the present working directory. Relative paths never start with ``/``.
      Example: ``../Pictures/xkcd-webcomics/530.png``. See also :term:`absolute path`.

   remote
      Git-terminology: A repository (and thus also :term:`DataLad dataset`) that a given repository
      tracks. A :term:`sibling` is DataLad's equivalent to a remote.

   Remote Indexed Archive (RIA) store
      A Remote Indexed Archive (RIA) Store is a flexible and scalable dataset storage
      solution, useful for collaborative, back-up, or storage workflows. Read more
      about RIA stores in the section :ref:`riastore`.

   run procedure
      DataLad concept: An executable (such as a script) that can be called with the
      :dlcmd:`run-procedure` command and performs modifications or routine
      tasks in datasets. Procedures can be written by users, or come with DataLad and
      its extensions. Find out more in section :ref:`procedures`

   run record
      A command summary of a :dlcmd:`run` command, generated by DataLad and included
      in the commit message.

   sed
      A Unix stream editor to parse and transform text. Find out more
      `here <https://en.wikipedia.org/wiki/Sed>`__ and in its
      `documentation <https://www.gnu.org/software/sed/manual/sed.html>`_.

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

   shell
      A command line language and programming language. See also :term:`terminal`.

   special remote
      git-annex concept: A protocol that defines the underlying transport of annexed files
      to and from places that are not :term:`Git` repositories (e.g., a cloud service or
      external machines such as HPC systems).

   squash
      Git concept; Squashing is a Git operation which rewrites history by taking
      a range of commits and squash them into a single commit. For more information
      on rewriting Git history, checkout section :ref:`history` and the
      `documentation <https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History>`__.

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
      Services such as :term:`GitHub`, :term:`GitLab`, and :term:`Gin` use SSH keys and the SSH protocol
      to ease access to repositories. This
      `tutorial by GitHub <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_
      is a detailed step-by-step instruction to generate and use SSH keys for authentication.

   SSH server
      An remote or local computer that users can log into using the :term:`SSH` protocol.

   stdin
      Unix concept: One of the three `standard input/output streams <https://en.wikipedia.org/wiki/Standard_streams>`_
      in programming. Standard input (``stdin``) is a stream from which a program
      reads its input data.

   stderr
      Unix concept: One of the three `standard input/output streams <https://en.wikipedia.org/wiki/Standard_streams>`_
      in programming. Standard error (``stderr``) is a stream to which a program
      outputs error messages, independent from standard output.

   stdout
      Unix concept: One of the three `standard input/output streams <https://en.wikipedia.org/wiki/Standard_streams>`_
      in programming. Standard output (``stdout``) is a stream to which a program
      writes its output data.

   symlink
      A symbolic link (also symlink or soft link) is a reference to another file or path in the form
      of a relative path. Windows users are familiar with a similar concept: shortcuts.

   sibling
      DataLad concept: A dataset clone that a given :term:`DataLad dataset` knows about. Changes can be
      retrieved and pushed between a dataset and its sibling. It is the
      equivalent of a :term:`remote` in Git.

   Singularity
      `Singularity <https://sylabs.io/docs>`_ is a containerization software that can package software into :term:`software container`\s.
      It is a useful alternative to :term:`Docker` as it can run on shared computational infrastructure.
      Find out more on `Wikipedia <https://en.wikipedia.org/wiki/Singularity_(software)>`__.

   Singularity-Hub
       `singularity-hub.org <https://singularity-hub.org>`_ was a Singularity container portal.
       Among other things, it hosts Singularity container images.
       You can can *pull* :term:`container image`\s built from it.

   software container
       Computational containers are cut-down virtual machines that allow you to package software libraries and their dependencies in precise versions into a bundle that can be shared with others.
       They are running instances of a :term:`container image`.
       On your own and other's machines, the container constitutes a secluded software environment that contains the exact software environment that you specified but does not effect any software outside of the container.
       Unlike virtual machines, software containers do not have their own operating system and instead use basic services of the underlying operating system of the computer they run on (in a read-only fashion).
       This makes them lightweight and portable.
       By sharing software environments with containers, such as :term:`Docker` or :term:`Singularity` containers, others (and also yourself) have easy access to software without the need to modify the software environment of the machine the container runs on.

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
      option to :dlcmd:`save`.

   the DataLad superdataset ///
      DataLad provides unified access to a large amount of data at an open data
      collection found at `datasets.datalad.org <https://datasets.datalad.org>`_.
      This collection is known as "The DataLad superdataset" and under its shortcut,
      ``///``. You can install the superdataset -- and subsequently query its content via metadata
      search -- by running ``datalad clone ///``.

   tig
      A text-mode interface for git that allows you to easily browse through your commit history.
      It is not part of git and needs to be installed. Find out more `here <https://jonas.github.io/tig>`_.

   terminal
      The terminal (sometimes also called a shell, console, or CLI) is an interactive, text based interface that allows you to access your computer's functionality.
      The most common command-line shells use :term:`bash` or c-shell.
      You can get a short intro to the terminal and useful commands in the section :ref:`howto`.

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
      Here is help: `A vim tutorial <https://www.openvim.com>`_ and
      `how to configure the default editor for git <https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration>`_.

   virtual environment
      A specific Python installation with packages of your choice, kept in a self-contained directory tree, and not interfering with the system-wide installations.
      Virtual environments are an easy solution to create several different Python environments and come in handy if you want to have a cleanly structured software setup and several applications with software requirements that would conflict with each other in a single system: You can have one virtual environment with package A in version X, and a second one with package A in version Y.
      There are several tools that create virtual environments such as the built-in ``venv`` module, the ``virtualenv`` module, or :term:`conda`.
      Virtual environments are light-weight and you can switch between them fast.

   WSL
      The Windows Subsystem for Linux, a compatibility layer for running Linux destributions on recent versions of Windows. Find out more `here <https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux>`__.

   zsh
      A Unix shell.
