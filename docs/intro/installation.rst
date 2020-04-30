.. _install:

Installation and configuration
------------------------------

.. note::

  The handbook is written for DataLad version 0.12.
  If you already have DataLad installed but are unsure whether it is the correct
  version, you can get information on your version of DataLad by typing
  ``datalad --version`` into your terminal.

The content in this chapter is largely based on the information given on the
`DataLad website <https://www.datalad.org/get_datalad.html>`_
and the `DataLad documentation <http://docs.datalad.org/en/latest/gettingstarted.html>`_.

Beyond DataLad itself, the installation requires Python, :term:`Git`,
:term:`git-annex`, and potentially Pythons package manager ``pip``.
The instructions below detail how to install
each of these components for different common operating systems. Please
`file an issue <https://github.com/datalad-handbook/book/issues/new>`_
if you encounter problems.

Note that while these installation instructions will provide you with the core
DataLad tool, many
`extensions <http://docs.datalad.org/en/latest/index.html#extension-packages>`_
exist, and they need to be installed separately, if needed.

.. figure:: ../artwork/src/install.svg
   :width: 70%

Installation instructions for the JSC (JURECA and JUDAC)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Read this if you want to use DataLad at the JSC.

Software installation
"""""""""""""""""""""

One common INM-7 use case for DataLad is using DataLad in conjunction with
the ``datalad-containers`` extension on `JUDAC <https://www.fz-juelich.de/ias/jsc/EN/Expertise/Datamanagement/JUDAC/JUDAC_node.html>`_
and `JURECA <https://www.fz-juelich.de/ias/jsc/EN/Expertise/Supercomputers/JURECA/JURECA_node.html>`_.
Due to `inode limitations <https://www.fz-juelich.de/SharedDocs/FAQs/IAS/JSC/EN/JUST/FAQ_01_Data_limitiations.html?nn=1765188>`_,
the installation of all relevant software needs to create as few files as possible.
Else, a default installation on these two systems will exhaust a user's inode
limit completely, preventing the creation of any additional files.
In order to avoid this, the installation needs to proceed in a way that is shared
between JURECA and JUDAC:

#. Once you have a `JuDoor <https://judoor.fz-juelich.de/login>`_ account, log
   into JUDAC::

      $ ssh <user-ID>@judac.fz-juelich.de

#. Download the latest Miniconda installer and install it into the ``shared/``
   directory. While you have separate ``$HOME`` directories on both HPC systems,
   ``shared/`` is a directory that both systems can access::

      $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O shared/Miniconda3-latest-Linux-x86_64.sh
      $ bash shared/Miniconda3-latest-Linux-x86_64.sh -p ~/shared/miniconda3
      # An interactive installer will ask you to read and agree to the
      # license terms, and will ask you to confirm the installation location.
      # reply "yes" when asked whether to perform a conda init

#. Open a new shell. Install all required software via ``conda``::

   $ conda install -c conda-forge datalad datalad-container p7zip

Subsequently, DataLad and all relevant software should be available on JUDAC,
and you should be able to run any DataLad command from the terminal.
This is because the final part of the Miniconda installation should have
adjusted your ``.bashrc`` file such that ``conda`` and all software installed
via ``conda install`` is accessible from the command line.

.. findoutmore:: What's this modification exactly?

   It looks like this:

   .. code-block:: bash

      $ cat .bashrc
      [...]
      #
      # >>> conda initialize >>>
      # !! Contents within this block are managed by 'conda init' !!
      __conda_setup="$('/p/home/jusers/<user-ID>/judac/shared/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
      if [ $? -eq 0 ]; then
          eval "$__conda_setup"
      else
          if [ -f "/p/home/jusers/<user-ID>/judac/shared/miniconda3/etc/profile.d/conda.sh" ]; then
              . "/p/home/jusers/<user-ID>/judac/shared/miniconda3/etc/profile.d/conda.sh"
          else
              export PATH="/p/home/jusers/<user-ID>/judac/shared/miniconda3/bin:$PATH"
          fi
      fi
      unset __conda_setup
      # <<< conda initialize <<<

   It may look a bit messy if you are unfamiliar with bash, but worry not -- it
   simply points your shell to the location of all conda-installed programs so
   that their commands become available to you.

To get everything to work on JURECA as well requires that your ``.bashrc`` file on
JURECA gets the same modifications. This is some extra work, but done in a few
command line calls:

#. Adjust paths in the ``.bashrc`` file to remove ``judac/`` with the stream
   editor `sed <https://www.gnu.org/software/sed/manual/sed.html>`_::

      $ sed -i 's/judac\/shared\/miniconda3\//shared\/miniconda3\//' .bashrc

#. Move the ``.bashrc`` file into ``shared/``, and create a :term:`symlink` in its
   place::

      $ mv .bashrc shared/
      # create a symlink
      $ ln -s shared/.bashrc .bashrc

#. Log out of JUDAC and log into JURECA from your local machine::

      $ ssh <user-ID>@jureca.fz-juelich.de

#. Make sure that your ``.bashrc`` on JURECA does not contain any precious
   content. It should look something like this::

      $ cat .bashrc
      # ******************************************************************************
      # bash environment file in $HOME
      # Please see:
      # http://www.fz-juelich.de/ias/jsc/EN/Expertise/Datamanagement/OnlineStorage/JUST/FAQ/just-FAQ_node.html
      # for more information and possible modifications to this file
      # ******************************************************************************

      # Source global definitions: Copied from CentOS 7 /etc/skel/.bashrc
      if [ -f /etc/bashrc ]; then
              . /etc/bashrc
      fi

   .. findoutmore:: What if it contains other content than this?

      The content in the ``.bashrc`` file above is not precious, because the
      ``.bashrc`` file you placed into shared should already contain them.
      If there is more, e.g., configurations you made yourself, make sure that
      you copy and paste them into the ``.bashrc`` file in ``shared/``.
      Usually, there should be no need to adjust paths.

#. Remove the ``.bashrc`` file and symlink the ``.bashrc`` file in ``shared/`` instead::

   $ rm .bashrc
   $ ln -s shared/.bashrc .bashrc

#. Open a new session on JURECA. You should now have access to the software you just
   installed on JUDAC.

.. findoutmore:: Troubleshooting inode quotas

   The inode limit from the JSC is quite strict. If you receive an e-mail that
   you have exceeded your quota, here is what you can do:

   * Verify that it is inode limitations that you ran into by running
     ``jutil user dataquota -u <user-ID>``. Check the table columns "inode-usage"
     and "inode-<soft|hard>-limit".
   * Check that your installation does not consume more inodes than expected. On JURECA,
     ``cd`` into the ``shared/`` directory and run the ``ncdu`` command. Once
     the command finished scanning, press ``c`` and confirm that your
     ``miniconda3`` directory consumes about 40k inodes.
   * Remove caches and unused packages by running ``conda clean --all`` to reduce
     the inode usage by a few thousand.
   * On JURECA, run ``ncdu`` in your ``$HOME`` directory to check whether there
     are other directories that consume many inodes.

   The installation takes up almost all available inodes, so be aware that you can
   only have a few thousand files in any of the two systems ``$HOME`` directories.


Configurations on JURECA und JUDAC
""""""""""""""""""""""""""""""""""

In order to use DataLad, it is highly recommended to configure your Git identity.
While it is not strictly *necessary*, it makes sense to do it in a way that is
shared between the two HPC systems as well.

On any of the two systems, provide your Name and e-mail address to the
:command:`git config` command::

   $ git config --global --add user.name "Bob McBobFace"
   $ git config --global --add user.email bob@example.com

This will create a ``.gitconfig`` file in your ``$HOME`` directory. Just as
done with the ``.bashrc`` file, move this file into the ``shared/`` directory,
and create a symlink in its place::

   $ mv .gitconfig shared/
   $ ln -s shared/.gitconfig .gitconfig
   $ logout
   # log into the other machine
   $ ssh <user-ID>@<jureca|judac>.fz-juelich.de
   # create a symlink to the shared .gitconfig file
   $ ln -s shared/.gitconfig .gitconfig

Afterwards, you are done, and ready to use DataLad on the HPC systems of the
JSC.


Standard installation instructions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Read this, if you want to install DataLad on your own computer, or any system
that is not part of the JSC.

Linux: (Neuro)Debian, Ubuntu, and similar systems
"""""""""""""""""""""""""""""""""""""""""""""""""

For Debian-based operating systems, the most convenient installation method
is to enable the `NeuroDebian <http://neuro.debian.net/>`_ repository.
If you are on a Debian-based system, but do not have the NeuroDebian repository
enabled, you should very much consider enabling it right now. The above hyperlink links
to a very easy instruction, and it only requires copy-pasting three lines of code.
Also, should you be confused by the name:
enabling this repository will not do any harm if your field is not neuroscience.

The following command installs
DataLad and all of its software dependencies (including the git-annex-standalone package):

.. code-block:: bash

   $ sudo apt-get install datalad

The command above will also upgrade existing installations to the most recent
available version.

Linux: CentOS, Redhat, Fedora, or similar systems
"""""""""""""""""""""""""""""""""""""""""""""""""

For CentOS, Redhat, Fedora, or similar distributions, there is an rpm
git-annex-standalone available
`here <https://git-annex.branchable.com/install/rpm_standalone/>`_.
Subsequently, DataLad can be installed via ``pip``.

Alternatively, DataLad can be installed together with :term:`Git` and
:term:`git-annex` via ``conda`` as outlined in the section below.


Linux-machines with no root access (e.g. HPC systems)
"""""""""""""""""""""""""""""""""""""""""""""""""""""

If you want to install DataLad on a machine you do not have root access to, DataLad
can be installed with `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_.

.. code-block:: bash

  $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  $ bash Miniconda3-latest-Linux-x86_64.sh
  # acknowledge license, keep everything at default
  $ conda install -c conda-forge datalad

This should install :term:`Git`, :term:`git-annex`, and DataLad.
The installer automatically configures the shell to make conda-installed
tools accessible, so no further configuration is necessary.

To update an existing installation with conda, use ``conda update datalad``.

macOS/OSX
"""""""""

A common way to install packages on OS X is via the
`homebrew <https://brew.sh/>`_ package manager.
First, install the homebrew package manager. Note that prior
to the installation, `Xcode <https://apps.apple.com/us/app/xcode/id497799835>`_
needs to be installed from the Mac App Store.
Homebrew then can be installed using the command following the
instructions on their webpage (linked above).

Next, `install git-annex <https://git-annex.branchable.com/install/OSX/>`_. The
easiest way to do this is via ``brew``::

   $ brew install git-annex

Once git-annex is available, DataLad can be installed via Pythons package
manager ``pip`` as described below. ``pip`` should already be installed by
default. Recent macOS versions may have ``pip3`` instead of ``pip`` -- use
:term:`tab completion` to find out which is installed. If it is ``pip3``, run::

   $ pip3 install datalad~=0.12

instead of the code snippets in the section below.

If this results in a ``permission denied`` error, install DataLad into
a user's home directory:

.. code-block:: bash

   $ pip3 install --user datalad~=0.12


.. findoutmore:: If something is not on PATH...

    Recent macOS versions may warn after installation that scripts were installed
    into locations that were not on ``PATH``::

       The script chardetect is installed in '/Users/awagner/Library/Python/3.7/bin' which is not on PATH.
       Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.

    To fix this, add these paths to the ``$PATH`` environment variable.
    You can either do this for your own user (1), or for all users of the computer (2)
    (requires using ``sudo`` and authenticating with your computer's password):

    (1) Add something like (exchange the user name accordingly)

    .. code-block:: bash

       export PATH=$PATH:/Users/awagner/Library/Python/3.7/bin

    to the *profile* file of your shell. If you use a :term:`bash` shell, this may
    be ``~/.bashrc`` or ``~/.bash_profile``, if you are using a :term:`zsh` shell,
    it may be ``~/.zshrc`` or ``~/.zprofile``. Find out which shell you are using by
    typing ``echo $SHELL`` into your terminal.

    (2) Alternatively, configure it *system-wide*, i.e., for all users of your computer
    by adding the the path ``/Users/awagner/Library/Python/3.7/bin`` to the file
    ``/etc/paths``, e.g., with the editor :term:`nano`:

    .. code-block:: bash

       sudo nano /etc/paths

    The contents of this file could look like this afterwards (the last line was
    added):

    .. code-block:: bash

        /usr/local/bin
        /usr/bin
        /bin
        /usr/sbin
        /sbin
        /Users/awagner/Library/Python/3.7/bin


Using Pythons package manager ``pip``
"""""""""""""""""""""""""""""""""""""

DataLad can be installed via Pythons package manager
`pip <https://pip.pypa.io/en/stable/>`_.
``pip`` comes with Python distributions, e.g., the Python distributions
downloaded from `python.org <https://www.python.org>`_. When downloading
Python, make sure to chose a recent Python **3** distribution.

If you have Python and ``pip`` set up,
to automatically install DataLad and its software dependencies, type

.. code-block:: bash

   $ pip install datalad~=0.12

If this results in a ``permission denied`` error, install DataLad into
a user's home directory:

.. code-block:: bash

   $ pip install --user datalad~=0.12

An existing installation can be upgraded with ``pip install -U datalad``.

In addition, it is necessary to have a current version of :term:`git-annex` installed which is
not set up automatically by using the ``pip`` method.
You can find detailed installation instructions on how to do this
`here <https://git-annex.branchable.com/install/>`__.

For Windows, extract the provided EXE installer into an existing Git
installation directory (e.g. ``C:\\Program Files\Git``). If done
this way, no ``PATH`` variable manipulation is necessary.


Windows 10
""""""""""

There are two ways to get DataLad on Windows 10: one is within Windows itself,
the other is using WSL, the Windows Subsystem for Linux. We recommend the
former, but information on how to use the WSL can be found here:

.. container:: toggle

   .. container:: header

      Using the Windows Subsystem for Linux

   You can find out how to install the Windows Subsystem for Linux at
   `ubuntu.com/wsl <https://ubuntu.com/wsl>`_. Afterwards, proceed with your
   installation as described in the installation instructions for Linux.

Note: Using Windows itself comes with some downsides.
In general, DataLad can feel a bit sluggish on Windows systems. This is because of
a range of filesystem issues that also affect the version control system :term:`Git` itself,
which DataLad relies on. The core functionality of DataLad works, and you should
be able to follow the contents covered in this book.
You will notice, however, that some Unix commands displayed in examples may not
work, and that terminal output can look different from what is displayed in the
code examples of the book.
If you are a Windows user and want to help improve the handbook for Windows users,
please `get in touch <https://github.com/datalad-handbook/book/issues/new>`_.

Note: This installation method will get you a working version of
DataLad, but be aware that many Unix commands shown in the book
examples will not work for you, and DataLad-related output might
look different from what we can show in this book. Please
`get in touch <https://github.com/datalad-handbook/book/issues/new>`__
touch if you want to help.

- **Step 1**: Install Conda

  - Go to https://docs.conda.io/en/latest/miniconda.html and pick the
    latest Python 3 installer. Miniconda is a free, minimal installer for
    conda and will install `conda <https://docs.conda.io/en/latest/>`_,
    Python, depending packages, and a number of useful packages such as
    `pip <https://pip.pypa.io/en/stable/>`_.

  - During installation, keep everything on default. In particular, do
    not add anything to ``PATH``.

  - From now on, any further action must take place in the ``Anaconda prompt``,
    a preconfigured terminal shell. Find it by searching for "Anaconda prompt"
    in your search bar.

- **Step 2**: Install Git

  - In the ``Anaconda prompt``, run::

       conda install -c conda-forge git

    Note: Is has to be from ``conda-forge``, the anaconda version does not
    provide the ``cp`` command.

- **Step 3**: Install git-annex

  - Obtain the current git-annex versions installer
    `from here <https://downloads.kitenet.net/git-annex/windows/current/>`_.
    Save the file, and double click the downloaded
    :command:`git-annex-installer.exe` in your Downloads.

  - During installation, you will be prompted to "Choose Install Location".
    **Install it into the miniconda Library directory**, e.g.
    ``C:\Users\me\Miniconda3\Library``.

- **Step 4**: Install DataLad via pip

  - ``pip`` was installed by ``miniconda``. In the ``Anaconda prompt``, run::

       pip install datalad~=0.12

- **Step 5**: Install 7zip

  - `7zip <https://7-zip.de/download.html>`_ is a dependency of DataLad and
    not installed by default on Windows 10. Please make sure to download and
    install it.

.. _installconfig:

Initial configuration
^^^^^^^^^^^^^^^^^^^^^

.. index:: ! Git identity

Initial configurations only concern the setup of a :term:`Git` identity. If you
are a Git-user, you should hence be good to go.

.. figure:: ../artwork/src/gitidentity.svg
   :width: 70%

If you have not used the version control system Git before, you will need to
tell Git some information about you. This needs to be done only once.
In the following example, exchange ``Bob McBobFace`` with your own name, and
``bob@example.com`` with your own email address.

.. code-block:: bash

   # enter your home directory using the ~ shortcut
   % cd ~
   % git config --global --add user.name "Bob McBobFace"
   % git config --global --add user.email bob@example.com

This information is used to track changes in the DataLad projects you will
be working on. Based on this information, changes you make are associated
with your name and email address, and you should use a real email address
and name -- it does not establish a lot of trust nor is it helpful after a few
years if your history, especially in a collaborative project, shows
that changes were made by ``Anonymous`` with the email
``youdontgetmy@email.fu``.
And do not worry, you won't get any emails from Git or DataLad.
