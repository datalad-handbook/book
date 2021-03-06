.. _install:

Installation and configuration
------------------------------

.. importantnote:: DataLad version requirement

  The handbook is written for DataLad version 0.12 or higher. The higher the
  version, the better, but it should be at least DataLad 0.12.0.
  If you already have DataLad installed but are unsure whether it is the correct
  version, you can get information on your version of DataLad by typing
  ``datalad --version`` into your terminal.

Install DataLad
^^^^^^^^^^^^^^^

The content in this chapter is largely based on the information given on the
`DataLad website <https://www.datalad.org/get_datalad.html>`_
and the `DataLad documentation <http://docs.datalad.org/en/stable/>`_.
Python installation instructions are largely based on instructions from the `2020 OHBM hackathon <https://ohbm.github.io/hackathon2020/logistics/>`_.

Beyond DataLad itself, the installation requires Python 3, :term:`Git`, and :term:`git-annex`, and may require Python's package manager ``pip`` and `p7zip/7-Zip <https://7-zip.org/>`_.
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

Python 3 (all operating systems)
""""""""""""""""""""""""""""""""

You should make sure that you have Python 3 installed on your system.
The easiest way to do this is to open a terminal and type "python" to open a minimalistic Python session::

   $ python
   Python 3.9.1+ (default, Jan 20 2021, 14:49:22)
   [GCC 10.2.1 20210110] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

If this fails, or reports a Python version with a leading ``2``, such as ``Python 2.7.18``, try typing ``python3`` (which some systems use to disambiguate between Python 2 and Python 3).
If this fails, too, you need to obtain a recent release of Python 3.

If you are on Windows, please note that you should **not** install Python via the Windows store, even if it opens after you typed ``python``, as this version requires additional configurations by hand (in particular of your ``$PATH`` :term:`environment variable`).
Please instead check the Windows section at the end of the section for more convenient alternatives.

.. find-out-more:: Python 2, Python 3, what's the difference?

   Python 2 is an outdated, in technical terms "deprecated", version of Python.
   Although it still exist as the default Python version on many systems, it is no longer maintained since 2020, and thus, most software has dropped support for Python 2.
   If you only run Python 2 on your system, most Python software, including DataLad, will be incompatible, and hence unusable, resulting in errors during installation and execution.

   But does that mean that you should uninstall Python 2?
   **No**.
   Keep it installed, especially if you are using Linux or MacOS.
   Python 2 existed for 20 years and numerous software has been written in it.
   It is quite likely that some basic operating system components or legacy software on your computer is depending on it, and uninstalling a preinstalled Python 2 from your system will likely render it unusable.
   Install Python 3, and have both versions coexist peacefully.

Regardless of your operating system, we recommend installing Python via `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, a minimal Python installer.
To install it from the command line, run

.. code-block:: bash

   $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-<YOUR-OS>-x86_64.sh
   $ bash Miniconda3-latest-<YOUR-OS>-x86_64.sh

In the above call, replace ``<YOUR-OS>`` with an identifier for your operating system, such as "Linux" or "MacOSX" (if you are on Windows, please read the Windows-specific instructions).
During the installation, you will need to accept a license agreement (press Enter to scroll down, and type "yes" and Enter to accept), confirm the installation into the default directory, and you should respond "yes" to the prompt ``“Do you wish the installer to initialize Miniconda3 by running conda init? [yes|no]”``.
Afterwards, you can remove the installation script by running ``rm ./Miniconda3-latest-*-x86_64.sh``.

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
DataLad and all of its software dependencies (including the git-annex-standalone package and `p7zip <http://p7zip.sourceforge.net/>`_):

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

.. _norootinstall:

Linux-machines with no root access (e.g. HPC systems)
"""""""""""""""""""""""""""""""""""""""""""""""""""""

If you want to install DataLad on a machine you do not have root access to, DataLad
can be installed with `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`__.

.. code-block:: bash

  $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  $ bash Miniconda3-latest-Linux-x86_64.sh
  # acknowledge license, keep everything at default
  $ conda install -c conda-forge datalad

This should install :term:`Git`, :term:`git-annex`, `p7zip <http://p7zip.sourceforge.net/>`_ and DataLad.
The installer automatically configures the shell to make conda-installed
tools accessible, so no further configuration is necessary.

To update an existing installation with conda, use ``conda update datalad``.

macOS/OSX
"""""""""

DataLad is available from pip, but also OS X's `homebrew <https://brew.sh/>`_ package manager.
First, install the homebrew package manager. Note that prior
to the installation, `Xcode <https://apps.apple.com/us/app/xcode/id497799835>`_
needs to be installed from the Mac App Store.

Next, install datalad and `git-annex <https://git-annex.branchable.com/install/OSX/>`_.
The easiest way to do this is in one go via ``brew``::

   $ brew install datalad

If git-annex is installed already (via brew), DataLad can also be installed via Pythons package manager ``pip`` (see paragraph on pip), which should already be installed by default on your system.
Recent macOS versions may use ``pip3`` instead of ``pip`` -- use :term:`tab completion` to find out which is installed.

.. find-out-more:: If something is not on PATH...

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

Finally, install the `p7zip <http://p7zip.sourceforge.net/>`_ dependency -- it is available via ``brew`` as well.

Using Python's package manager ``pip``
""""""""""""""""""""""""""""""""""""""

DataLad can be installed via Python's package manager
`pip <https://pip.pypa.io/en/stable/>`_.
``pip`` comes with Python distributions, e.g., the Python distributions
downloaded from `python.org <https://www.python.org>`_. When downloading
Python, make sure to chose a recent Python **3** distribution.

If you have Python and ``pip`` set up,
to automatically install DataLad and most of its software dependencies, type

.. code-block:: bash

   $ pip install datalad

If this results in a ``permission denied`` error, install DataLad into
a user's home directory:

.. code-block:: bash

   $ pip install --user datalad

On some systems, in particular macOS, you may need to call ``pip3`` instead of ``pip``::

   $ pip3 install datalad
   # or, in case of a "permission denied error":
   $ pip3 install --user datalad

``pip`` is not able to install the `7-zip <https://7-zip.org/>`_ dependency.
Please install a flavor of 7-zip that is appropriate for your operating system (such as `p7zip <http://p7zip.sourceforge.net/>`_ for Linux or macOS) if it isn't yet installed.

In addition, it is necessary to have a current version of :term:`git-annex` installed which is also
not set up automatically by using the ``pip`` method.
You can find detailed installation instructions on how to do this
`here <https://git-annex.branchable.com/install/>`__.
For Windows, extract the provided EXE installer into an existing Git
installation directory (e.g. ``C:\\Program Files\Git``). If done
this way, no ``PATH`` variable manipulation is necessary.

An existing installation can be upgraded with ``pip install -U datalad``.

Windows 10
""""""""""

There are two ways to get DataLad on Windows 10: one is within Windows itself,
the other is using WSL2, the Windows Subsystem for Linux, version 2.
With the Windows Subsystem for Linux, you will be able to use a Unix system despite being on Windows.
You need to have a recent build of Windows 10 in order to get WSL2 -- we do not recommend WSL1.
Information on how to install WSL2 can be found at `docs.microsoft.com <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_.
Afterwards, proceed with your installation as described in the installation instructions for Linux.

Note: Using Windows itself comes with some downsides.
We have created a dedicated page, :ref:`ohnowindows` with an explanation and overview.
In general, DataLad can feel a bit sluggish on Windows systems. This is because of
a range of filesystem issues that also affect the version control system :term:`Git` itself,
which DataLad relies on. The core functionality of DataLad works, and you should
be able to follow most contents covered in this book.
You will notice, however, that some Unix commands displayed in examples may not
work, and that terminal output can look different from what is displayed in the
code examples of the book, and that some dependencies for additional functionality are not available for Windows.
If you are a Windows user and want to help improve the handbook for Windows users,
please `get in touch <https://github.com/datalad-handbook/book/issues/new>`_.
Dedicated boxes, "``Windows-Workaround``\s", contain important information, alternative commands, or warnings, and if you are proceeding with a native Windows 10 system you should be close attention to them.

- **Step 1**: Install Git

  - If you haven't installed :term:`Git` yet, please download and install the latest release from `git-scm.com/ <https://git-scm.com/>`_.

  - During installation, you will be asked to "Select Components".
    In order to get a slightly nicer visual experience, tick the box at "Use a TrueType font in all console windows".
    Afterwards, you can open a Git bash, a :term:`terminal` that is nicer than standard Windows terminals.

- **Step 2**: Install Conda

  - Go to https://docs.conda.io/en/latest/miniconda.html and pick the
    latest Python 3 installer. Miniconda is a free, minimal installer for
    conda and will install `conda <https://docs.conda.io/en/latest/>`_,
    Python, depending packages, and a number of useful packages such as
    `pip <https://pip.pypa.io/en/stable/>`_.

  - Using the Git Bash shell for DataLad makes a nicer and more visually appealing experience.
    If you want to be able to do this, make sure that Miniconda is available from within your Git bash.
    One way to achieve this is to `tick "Add Anaconda to my PATH environment variables" during installation <https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-git-bash-conda/>`_.
    You can test if you succeeded by opening a new Git bash and typing ``conda`` -- if this shows you a help message, you're good.
    Alternatively, you can use the ``Anaconda prompt``, a preconfigured terminal shell installed with Miniconda, as a terminal.
    Find it by searching for "Anaconda prompt" in your search bar.
    From now on, any further action must either take place in the ``Anaconda prompt``, or the Git Bash.


- **Step 3**: Install DataLad and its dependencies

  - Enter an Anaconda prompt or your Git bash, and install DataLad and its dependencies by running ``conda install -c conda-forge datalad``
  
- **Step 4**: Install git-annex (temporarily necessary)

  - One of DataLad's core dependencies is :term:`git-annex`.
    For the longest time, git-annex installers for Windows lacked support for `mimeencoding <https://en.wikipedia.org/wiki/MIME>`_.
    Without mimeencoding, a standard DataLad procedure, the ``text2git`` configuration (it will be introduced in the very first section of the Basics), is not functional.
    Therefore, we started to build git-annex with support for mimeencoding ourselves.
    You can find the standalone git-annex installer for Windows with mimeencoding at `http://datasets.datalad.org/datalad/packages/windows/ <http://datasets.datalad.org/datalad/packages/windows/>`_.

- Optional - Install Unix tools

  - Many Unix command-line tools such as ``cp`` are not available by default.
    You can get a good set of tools by installing :term:`conda`\s ``m2-base`` package via ``conda install m2-base`` in an Anaconda prompt.
    **NOTE**: We're currently `investigating whether m2-base may cause problems <https://github.com/ContinuumIO/anaconda-issues/issues/12124>`_ -- use with caution.

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
