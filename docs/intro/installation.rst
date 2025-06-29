.. _install:

Installation and configuration
------------------------------

.. index::
   single: installation; DataLad

Install DataLad
^^^^^^^^^^^^^^^

.. importantnote:: Feedback on installation instructions

   The installation methods presented in this chapter are based on experience
   and have been tested carefully. However, operating systems and other
   software are continuously evolving, and these guides might have become
   outdated. Be sure to check out the online-handbook for up-to-date information.

In general, the DataLad installation requires Python 3 (see the
:find-out-more:`on the difference between Python 2 and 3 <fom-py2v3>` to learn
why this is required), :term:`Git`, and :term:`git-annex`, and for some
functionality `7-Zip <https://7-zip.org>`_.  The instructions below detail how
to install the core DataLad tool and its dependencies on common operating
systems. Various :term:`DataLad extension`\s can be installed separately, if desired.

.. index::
   pair: determine version; with Python
.. find-out-more:: Python 2, Python 3, what's the difference?
   :name: fom-py2v3
   :float: tbp

   DataLad requires Python 3.8, or a more recent version, to be installed on
   your system. The easiest way to verify that this is the case is to open a
   terminal and type :shcmd:`python` to start a Python session:

   .. code-block:: console

     $ python
     Python 3.9.1+ (default, Jan 20 2021, 14:49:22)
     [GCC 10.2.1 20210110] on linux
     Type "help", "copyright", "credits" or "license" for more information.
     >>>

   If this fails, or reports a Python version with a leading ``2``, such as
   ``Python 2.7.18``, try starting :shcmd:`python3`, which some systems use
   to disambiguate between Python 2 and Python 3. If this fails, too, you need
   to obtain a recent release of Python 3. On Windows, attempting to run
   commands that are not installed might cause a Windows Store window to pop
   up. If this happens, Python may not yet be installed. Please check the
   `Windows 10 and 11`_ installation instructions, and *do not* install Python via the
   Windows Store.

   Python 2 is an outdated, in technical terms "deprecated", version of Python.
   Although it still exist as the default Python version on many systems, it is
   no longer maintained since 2020, and thus, most software has dropped support
   for Python 2.  If you only run Python 2 on your system, most Python
   software, including DataLad, will be incompatible, and hence unusable,
   resulting in errors during installation and execution.

   But does that mean that you should uninstall Python 2?  **No**!  Keep it
   installed, especially if you are using Linux or macOS.  Python 2 existed for
   20 years and numerous software has been written for it.  It is quite likely
   that some basic operating system components or legacy software on your
   computer is depending on it, and uninstalling a preinstalled Python 2 from
   your system will likely render it unusable.  Install Python 3, and have both
   versions coexist peacefully.

The following sections provide targeted installation instructions for a set of
common scenarios, operating systems, or platforms.

.. image:: ../artwork/src/install.svg
   :align: center
   :width: 50%
   :alt: Cartoon of a person sitting on the floor in front of a laptop

.. index::
   pair: install DataLad; on Windows

Windows 10 and 11
"""""""""""""""""

There are countless ways to install software on Windows. Here we describe *one*
possible approach that should work on any Windows computer, like one that you
may have just bought.

**Python**:
   Windows itself does not ship with Python, it must be installed separately.
   An installation via ``uv`` (described below) can automatically take care of installing it.

**Git**:
    .. index::
       pair: install Git; on Windows
       single: installation; Git

    Windows does not come with Git preinstalled. If you happen to have it installed already,
    please check if you have configured it for command line use. You should be able
    to open the Windows command prompt and run a command like :shcmd:`git --version`.
    It should return a version number and not an error.

    To install Git, visit the `Git website <https://git-scm.com/download/win>`_ and
    download an installer. If in doubt, go with the 64bit installer of the latest
    version. The installer itself provides various customization options. We
    recommend to leave the defaults as they are, in particular the target
    directory, but configure the following settings (they are distributed over
    multiple dialogs):

    - Select *Git from the command line and also from 3rd-party software*
    - *Enable file system caching*
    - *Select Use external OpenSSH*
    - *Enable symbolic links*


**Git-annex**:
    .. index::
       pair: install git-annex; on Windows
       single: installation; git-annex

    One way to deploy git-annex is via `uv <https://docs.astral.sh/uv/getting-started/installation/>`_, which is installed first. Open ``CMD.exe`` and execute

    .. code-block:: bat

       powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

    Afterwards, install git-annex:

    .. code-block:: bat

       uv tool update git-annex

    This will have also taken care of installing Python. You can test your git-annex installation by running ``git annex test`` (2-3 minutes runtime).

    Alternative ways to install git-annex are the `Windows installer <https://git-annex.branchable.com/install/Windows/>`_ of git-annex, or with the Python package `datalad-installer <https://github.com/datalad/datalad-installer/>`_, which can install git-annex via ``datalad-installer git-annex -m datalad/git-annex:release`` in a ``CMD`` with administrator rights. Please take a look at the respective tools for details.

    For `performance improvements <https://git-annex.branchable.com/projects/datalad/bugs-done/Windows__58___substantial_per-file_cost_for___96__add__96__>`_, regardless of which installation method you chose, we recommend to also set the following git-annex configuration:

    .. code-block:: bat

      > git config --global filter.annex.process "git-annex filter-process"

**DataLad**:
    With uv, DataLad can be installed in the same fashion as ``git-annex``.

    .. code-block:: bat

      > uv tool install datalad

   Beyond ``uv``, the standard Python package manager :term:`pip` can install DataLad as well (see :ref:`pipinstall`).

**7-Zip** (optional, but highly recommended):
    .. index::
       pair: install 7-zip; on Windows
       single: installation; 7-Zip

    Download it from the `7-zip website <https://7-zip.org>`_ (64bit
    installer when in doubt), and install it into the default target directory.

There are many other ways to install DataLad on Windows, check for example the
:windows-wit:`on the Windows Subsystem 2 for Linux <ww-wsl2>`.
One attractive alternative approach is Conda_, a completely different approach is to install the :term:`DataLad Gooey`, which is a standalone installation of DataLad's graphical application (see `the DataLad Gooey documentation <https://docs.datalad.org/projects/gooey>`_ for installation instructions).

.. index::
   pair: install DataLad; on WSL2
.. windows-wit:: Install DataLad using the Windows Subsystem 2 for Linux
   :name: ww-wsl2

   With the Windows Subsystem for Linux, you will be able to use a Unix system
   despite being on Windows.  You need to have a recent build of Windows in
   order to get WSL2 -- we do not recommend WSL1.

   You can find out how to install the Windows Subsystem for Linux at
   `docs.microsoft.com <https://learn.microsoft.com/en-us/windows/wsl/install>`_.
   Afterwards, proceed with your installation as described in the installation instructions
   for Linux.

Using DataLad on Windows has a few peculiarities. In general, DataLad can feel a bit
sluggish on non-WSL2 Windows systems. This is due to various file system issues
that also affect the version control system :term:`Git` itself, which DataLad
relies on. The core functionality of DataLad works, and you should be able to
follow most contents covered in this book.  You will notice, however, that some
Unix commands displayed in examples may not work, and that terminal output can
look different from what is displayed in the code examples of the book, and
that some dependencies for additional functionality are not available for
Windows. Dedicated notes,
"``Windows-wit``\s", contain important information, alternative commands, or
warnings, and an overview of useful Windows commands and general information is included in :ref:`howto`.

.. index::
   pair: install DataLad; on Mac
.. _mac:

Mac (incl. M1)
""""""""""""""

Modern Macs come with a compatible Python 3 version installed by default. The
:find-out-more:`on Python versions <fom-py2v3>` has instructions on how to
confirm that.

DataLad is available via OS X's `homebrew <https://brew.sh>`_ package manager.
First, install the homebrew package manager, which requires `Xcode
<https://apps.apple.com/us/app/xcode/id497799835>`_ to be installed from the
Mac App Store.

Next, install datalad and its dependencies:

.. code-block:: console

   $ brew install datalad

Alternatively, you can exclusively use :shcmd:`brew` for DataLad's non-Python
dependencies, and then check the :find-out-more:`on how to install DataLad via
Python's package manager <fom-macosx-pip>`.

.. find-out-more:: Install DataLad via pip on macOS
   :name: fom-macosx-pip
   :float: tbp

   If Git/git-annex are installed already (via brew), DataLad can also be
   installed via Python's package manager ``pip``, which should be installed
   by default on your system:

   .. code-block:: console

     $ python -m pip install datalad

   Some macOS versions may use ``python3`` instead of ``python`` -- use :term:`tab
   completion` to find out which is installed.

   Recent macOS versions may warn after installation that scripts were installed
   into locations that were not on ``PATH``:

   .. code-block:: text

     The script chardetect is installed in
     '/Users/MYUSERNAME/Library/Python/3.11/bin' which is not on PATH.
     Consider adding this directory to PATH or, if you prefer to
     suppress this warning, use --no-warn-script-location.

   To fix this, add these paths to the ``$PATH`` environment variable.
   You can do this for your own user account by adding something like the following
   to the *profile* file of your shell (exchange the user name accordingly):

   .. code-block:: console

      $ export PATH=$PATH:/Users/MYUSERNAME/Library/Python/3.11/bin

   If you use a :term:`bash` shell, this may be ``~/.bashrc`` or
   ``~/.bash_profile``, if you are using a :term:`zsh` shell, it may be
   ``~/.zshrc`` or ``~/.zprofile``. Find out which shell you are using by
   typing ``echo $SHELL`` into your terminal.

   Alternatively, you could configure it *system-wide*, i.e., for all users of
   your computer by adding the path
   ``/Users/MYUSERNAME/Library/Python/3.11/bin`` to the file ``/etc/paths``,
   e.g., with the editor :term:`nano` (requires using ``sudo`` and authenticating
   with your password):

   .. code-block:: console

      $ sudo nano /etc/paths

   The contents of this file could look like this afterwards (the last line was
   added):

   .. code-block:: console

       /usr/local/bin
       /usr/bin
       /bin
       /usr/sbin
       /sbin
       /Users/MYUSERNAME/Library/Python/3.11/bin

.. index::
   pair: install DataLad; on Debian/Ubuntu

Linux: (Neuro)Debian, Ubuntu, and similar systems
"""""""""""""""""""""""""""""""""""""""""""""""""

DataLad is part of the Debian and Ubuntu operating systems. However, the
particular DataLad version included in a release may be a bit older (check the
versions for `Debian <https://packages.debian.org/datalad>`_ and `Ubuntu
<https://packages.ubuntu.com/datalad>`_ to see which ones are available).

For some recent releases of Debian-based operating systems, `NeuroDebian
<https://neuro.debian.net>`_ provides more recent DataLad versions (check the
`availability table <https://neuro.debian.net/pkgs/datalad.html>`_).  In order to
install from NeuroDebian, follow `its installation documentation
<https://neuro.debian.net/install_pkg.html?p=datalad>`_, which only requires
copy-pasting three lines into a terminal.  Also, should you be confused by the
name: enabling this repository will not do any harm if your field is not
neuroscience.

Whichever repository you end up using, the following command installs DataLad
and all of its software dependencies (including :term:`git-annex` and `p7zip <https://p7zip.sourceforge.net>`_):

.. code-block:: console

   $ sudo apt-get install datalad

The command above will also upgrade existing installations to the most recent
available version.

.. index::
   pair: install DataLad; on Redhat/Fedora

Linux: CentOS, Redhat, Fedora, or similar systems
"""""""""""""""""""""""""""""""""""""""""""""""""

For CentOS, Redhat, Fedora, or similar distributions, there is an `RPM package for git-annex <https://git-annex.branchable.com/install/rpm_standalone>`_.  A
suitable version of Python and :term:`Git` should come with the operating
system, although some servers may run fairly old releases.

DataLad itself can be installed via ``pip``:

.. code-block:: console

   $ python -m pip install datalad

Alternatively, DataLad can be installed together with :term:`Git` and
:term:`git-annex` via Conda_.

.. index::
   pair: install DataLad; on HPC
.. _norootinstall:

Linux-machines with no root access (e.g. HPC systems)
"""""""""""""""""""""""""""""""""""""""""""""""""""""

The most convenient user-based installation can be achieved via Conda_.

.. index::
   pair: install DataLad; with Conda
.. _conda:

Conda
"""""

Conda is a software distribution available for all major operating systems, and
its `Miniconda <https://docs.conda.io/miniconda.html>`_ installer
offers a convenient way to bootstrap a DataLad installation. Importantly, it
does not require admin/root access to a system.

`Detailed, platform-specific installation instructions
<https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html>`_ are available
in the Conda documentation. In short: download and run the installer, or, from
the command line, run

.. code-block:: console

   $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-<YOUR-OS>-x86_64.sh
   $ bash Miniconda3-latest-<YOUR-OS>-x86_64.sh

In the above call, replace ``<YOUR-OS>`` with an identifier for your operating
system, such as "Linux" or "MacOSX".  During the installation, you will need to
accept a license agreement (press Enter to scroll down, and type "yes" and
Enter to accept), confirm the installation into the default directory, and you
should respond "yes" to the prompt ``“Do you wish the installer to initialize
Miniconda3 by running conda init? [yes|no]”``.  Afterwards, you can remove the
installation script by running ``rm ./Miniconda3-latest-*-x86_64.sh``.

The installer automatically configures the shell to make conda-installed tools
accessible, so no further configuration is necessary.  Once Conda is installed,
the DataLad package can be installed from the ``conda-forge`` channel:

.. code-block:: console

  $ conda install -c conda-forge datalad

In general, all of DataLad's software dependencies are automatically installed, too.
This makes a conda-based deployment very convenient. A from-scratch DataLad installation
on a HPC system, as a normal user, is done in three lines:

.. code-block:: console

  $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  $ bash Miniconda3-latest-Linux-x86_64.sh
  $ # acknowledge license, keep everything at default
  $ conda install -c conda-forge datalad

In case a dependency is not available from Conda (e.g., there is no git-annex
package for Windows in Conda), please refer to the platform-specific
instructions above.

To update an existing installation with conda, use:

.. code-block:: console

  $ conda update -c conda-forge datalad

The `DataLad installer`_ also supports setting up a Conda environment, in case
a suitable Python version is already available.

.. index::
   pair: install DataLad; with pip
.. _pipinstall:

Using Python's package manager ``pip``
""""""""""""""""""""""""""""""""""""""

As mentioned above, DataLad can be installed via Python's package manager `pip
<https://pip.pypa.io>`_.  ``pip`` comes with any Python distribution
from `python.org <https://www.python.org>`_, and is available as a system-package
in nearly all GNU/Linux distributions.

If you have Python and ``pip`` set up, to automatically install DataLad and
most of its software dependencies, type

.. code-block:: console

   $ python -m pip install datalad

If this results in a ``permission denied`` error, you can install DataLad into
a user's home directory:

.. code-block:: console

   $ python -m pip install --user datalad

On some systems, you may need to call ``python3`` instead of ``python``:

.. code-block:: console

   $ python3 -m pip install datalad
   $ # or, in case of a "permission denied error":
   $ python3 -m pip install --user datalad

An existing installation can be upgraded with ``python -m pip install -U datalad``.

``pip`` is not able to install non-Python software, such as 7-zip or
:term:`git-annex`.  But you can install the `DataLad installer`_ via a ``python -m pip install datalad-installer``. This is a command-line tool that aids installation
of DataLad and its key software dependencies on a range of platforms.


Install datalad-next
^^^^^^^^^^^^^^^^^^^^

``datalad-next`` is a :term:`DataLad extension`, i.e., a separate Python package that equips DataLad with additional functionality.
You can read more about extensions in general in :ref:`extensions_intro`, and more about ``datalad-next`` specifically in :ref:`datalad-next`.

As ``datalad-next`` brings next-generation commands and performance improvements to existing commands, we recommend users to **install** and **configure** it.
It is available via Python package managers such as :term:`pip` and ``uv`` (e.g., ``pip install datalad-next``).

After installation, you need to enable the use of the extension with the following configuration::

   git config --global --add datalad.extensions.load next

.. index:: ! configure user identity; with Git
.. _installconfig:

Initial configuration
^^^^^^^^^^^^^^^^^^^^^

Initial configurations only concern the setup of a :term:`Git` identity. If you
are a Git-user, you should hence be good to go.

.. figure:: ../artwork/src/gitidentity.svg
   :width: 70%

If you have not used the version control system Git before, you will need to
tell Git some information about you. This needs to be done only once.
In the following example, exchange ``Bob McBobFace`` with your own name, and
``bob@example.com`` with your own email address.

.. code-block:: console

   $ # enter your home directory using the ~ shortcut
   $ cd ~
   $ git config --global --add user.name "Bob McBobFace"
   $ git config --global --add user.email bob@example.com

This information is used to track changes in the DataLad projects you will
be working on. Based on this information, changes you make are associated
with your name and email address, and you should use a real email address
and name -- it does not establish a lot of trust nor is it helpful after a few
years if your history, especially in a collaborative project, shows
that changes were made by ``Anonymous`` with the email
``youdontgetmy@email.fu``.
And do not worry, you won't get any emails from Git or DataLad.


.. _DataLad installer: https://github.com/datalad/datalad-installer
