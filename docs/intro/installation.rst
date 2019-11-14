.. _install:

Installation and configuration
------------------------------

.. note::

  The handbook is written for DataLad version 0.12. Currently, the latest version available
  via many package managers is 0.11. Therefore, the most convenient way to obtain a
  suitable version of datalad is to install of the most recent 0.12 release candidate,
  ``datalad~=0.12.0rc6``, via ``pip`` or ``conda``. Until 0.12 is released, please use
  ``pip`` or ``conda``-based methods to install the release candidate.

Install DataLad
^^^^^^^^^^^^^^^

The content in this chapter is largely based on the information given on the
`DataLad website <https://www.datalad.org/get_datalad.html>`_
and the `DataLad documentation <http://docs.datalad.org/en/latest/gettingstarted.html>`_.

Beyond DataLad itself, the installation requires Python, Pythons package manager ``pip``,
:term:`Git`, and :term:`Git-annex`. The instructions below detail how to install
each of these components for different common operating systems. Please
`file an issue <https://github.com/datalad-handbook/book/issues/new>`_
if you encounter problems.

Note that while these installation instructions will provide you with the core
DataLad tool, many
`extensions <http://docs.datalad.org/en/latest/index.html#extension-packages>`_
exist, and they need to be installed separately, if needed.


Linux: (Neuro)Debian, Ubuntu, and similar systems
"""""""""""""""""""""""""""""""""""""""""""""""""

.. note::

   Do not use this method at the current time. This note will be removed
   once DataLad 0.12 has been released.

For Debian-based operating systems, the most convenient installation method
is to enable the `NeuroDebian <http://neuro.debian.net/>`_ repository.
If you are on a Debian-based system, but do not have the NeuroDebian repository
enabled, you should very much consider enabling it right now. The above hyperlink links
to a very easy instruction, and it only requires copy-pasting three lines of code.
Also, should you be confused by the name:
enabling this repository will not do any harm if your field is not neuroscience.

The following command installs
DataLad and all of its software dependencies (including the Git-annex-standalone package):

.. code-block:: bash

   $ sudo apt-get install datalad


Linux-machines with no root access (e.g. HPC systems)
"""""""""""""""""""""""""""""""""""""""""""""""""""""

If you want to install DataLad on a machine you do not have root access to, DataLad
can be installed with `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_.

.. code-block:: bash

  $ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  $ bash Miniconda3-latest-Linux-x86_64.sh
  # acknowledge license, keep everything at default
  $ conda install -c conda-forge datalad
  # upgrade to the latest release candidate to match the requires of the book
  $ conda install -c conda-forge/label/rc datalad

This should install :term:`Git`, :term:`Git-annex`, and DataLad.
The installer automatically configures the shell to make conda-installed
tools accessible, so no further configuration is necessary.

macOS/OSX
"""""""""

A common way to install packages on OS X is via the
`homebrew <https://brew.sh/>`_ package manager.
First, install the homebrew package manager. Note that prior
to the installation, `Xcode <https://apps.apple.com/us/app/xcode/id497799835>`_
needs to be installed from the Mac App Store.
Homebrew then can be installed using the command following the
instructions on their webpage (linked above).

Next, `install Git-annex <https://git-annex.branchable.com/install/OSX/>`_. The
easiest way to do this is via ``brew``::

   $ brew install git-annex

Once Git-annex is available, DataLad can be installed via Pythons package
manager ``pip`` as described below. ``pip`` should already be installed by
default. Recent macOS versions may have ``pip3`` instead of ``pip`` -- use
:term:`tab completion` to find out which is installed. If it is ``pip3``, run::

   $ pip3 install datalad~=0.12.0rc6

instead of the code snippets in the section below.

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

   $ pip install datalad~=0.12.0rc6

If this results in a ``permission denied`` error, install DataLad into
a user's home directory:

.. code-block:: bash

   $ pip install --user datalad~=0.12.0rc6

In addition, it is necessary to have a current version of :term:`Git-annex` installed which is
not set up automatically by using the ``pip`` method.
You can find detailed installation instructions on how to do this
`here <https://git-annex.branchable.com/install/>`__.

For Windows, extract the provided EXE installer into an existing Git
installation directory (e.g. ``C:\\Program Files\Git``). If done
this way, no ``PATH`` variable manipulation is necessary.

Windows 10
""""""""""

There are two ways to get DataLad on Windows 10: one is within Windows itself,
the other is using WSL, the Windows Subsystem for Linux.

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

.. container:: toggle

   .. container:: header

      **1) Install within Windows [RECOMMENDED]**

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

   - **Step 3**: Install Git-annex

      - Obtain the current Git-annex versions installer
        `from here <https://downloads.kitenet.net/git-annex/windows/current/>`_.
        Save the file, and double click the downloaded
        :command:`git-annex-installer.exe` in your Downloads.

      - During installation, you will be prompted to "Choose Install Location".
        **Install it into the miniconda Library directory**, e.g.
        ``C:\Users\me\Miniconda3\Library``.

   - **Step 4**: Install DataLad via pip

      - ``pip`` was installed by ``miniconda``. In the ``Anaconda prompt``, run::

           pip install datalad~=0.12.0rc6


.. container:: toggle

   .. container:: header

      **2) Install within WSL**

   .. note::

      Do not use this method at the current time. This note will be removed
      once DataLad 0.12 has been released.

   The Windows Subsystem for Linux (WSL) allows Windows users to have full access
   to a Linux distribution within Windows.
   If you have always used Windows be prepared for some user experience changes when
   using Linux compared to Windows. For one, there will be no graphical user interface
   (GUI). Instead, you will work inside a terminal window. This however
   mirrors the examples and code snippets provided in this handbook exactly.
   Using a proper Linux installation improves the DataLad handbook experience on Windows
   *greatly*. However, it comes with
   the downside of two filesystems that are somewhat separated. Data access to files
   within Linux from within Windows is problematic:
   Note that there will be incompatibilities between the Windows and Linux filesystems.
   Files that are created within the WSL for example can not be modified with
   Windows tools. A great resource to get started and understand the WSL is
   `this guide <https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/>`_.


   **Requirements**:

   WSL can be enabled for **64-bit** versions of **Windows 10** systems running
   **Version 1607** or above. To check whether your computer fulfills these requirements,
   open *Settings* (in the start menu) > *System* > *About*. If your version number is
   less than 1607, you will need to perform a
   `windows update <https://support.microsoft.com/en-us/help/4028685/windows-10-get-the-update>`_
   before installing WSL.

   The instructions below show you how to set up the WSL and configure it to use
   DataLad and its dependencies. They follow the
   `Microsoft Documentation on the Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_.
   If you run into troubles during the installation, please consult the
   `WSL troubleshooting page <https://docs.microsoft.com/en-us/windows/wsl/troubleshooting>`_.


   - **Step 1**: Enable the windows subsystem for Linux

      - Open Windows Power Shell as an Administrator and run

      .. code-block:: bash

         $ Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

      - Afterwards, when prompted in the Power Shell, restart your computer

   - **Step 2**: Install a Debian Linux distribution

      - To do this, visit the Microsoft store, and search for the Debian distro.
        We **strongly** recommend installing :term:`Debian`, even though other
        distributions are available. "Get" the app, and "install" it.

   - **Step 3**: Initialize the distribution

      - Launch the Subsystem either from the Microsoft store or from the Start menu. This
        will start a terminal. Do not worry -- there is a dedicated section (:ref:`howto`)
        on how to work with the terminal if you have not so far.

      - Upon first start, you will be prompted to enter a new UNIX username and password.
        Tip: chose a short name, and no spaces or special characters. The password will
        become necessary when you elevate a process using ``sudo`` -- sudo let's you execute a
        process with rights of another user, such as administrative rights, for examples when
        you need to install software.

      - Right after initial installation, your Linux distribution will be minimally equipped.
        Update your package catalog and upgrade your installed packages by running the command below.
        As with all code examples in this book, make sure to copy commands exactly, including
        capitalization. If this is the first time you use ``sudo``, your system will warn you
        to use it with care. During upgrading installed packages, the terminal will ask
        you to confirm upgrades by pressing ``Enter``.

      .. code-block:: bash

         $ sudo apt update && sudo apt upgrade

   - **Step 4**: Enable NeuroDebian

      - In your terminal, run

      .. code-block:: bash

         $ wget -O- http://neuro.debian.net/lists/stretch.de-md.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list

      - Afterwards, run

      .. code-block:: bash

         $ curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xA5D32F012649A5A9" | sudo apt-key add

      - lastly do another

      .. code-block:: bash

         $ sudo apt-update && sudo apt upgrade

   - **Step 4**: Install datalad and everything it needs

      .. code-block:: bash

         $ sudo apt install datalad


.. container:: toggle

   .. container:: header

      **3) Install within WSL2**

   .. note::

      Do not use this method at the current time. This note will be removed
      once DataLad 0.12 has been released.


   The Windows Subsystem for Linux (WSL) allows Windows users to have full access
   to a Linux distribution within Windows. The Windows Subsystem for Linux 2 (WSL2)
   is the (currently pre-released) update to the WSL.
   If you have always used Windows be prepared for some user experience changes when
   using Linux compared to Windows. For one, there will be no graphical user interface
   (GUI). Instead, you will work inside a terminal window. This however
   mirrors the examples and code snippets provided in this handbook exactly.
   Using a proper Linux installation improves the DataLad handbook experience on Windows
   *greatly*. However, it comes with
   the downside of two filesystems that are somewhat separated. Data access to files
   within Linux from within Windows is problematic:
   Note that there will be incompatibilities between the Windows and Linux filesystems.
   Files that are created within the WSL for example can not be modified with
   Windows tools. A great resource to get started and understand the WSL is
   `this guide <https://github.com/michaeltreat/Windows-Subsystem-For-Linux-Setup-Guide/>`_.

   **Requirements**:

   WSL can be enabled for **64-bit** versions of **Windows 10** systems running
   Windows 10 Insider Preview Build 18917 or higher. You can find out how to enter
   the Windows Insider Program to get access to the prebuilds
   `here <https://insider.windows.com/en-us/>`_.
   To check whether your computer fulfills these requirements,
   open *Settings* (in the start menu) > *System* > *About*. Your version number should be
   at least 1903.
   Furthermore, your computer needs to support
   `Hyper-V Virtualization <https://www.thomasmaurer.ch/2017/08/install-hyper-v-on-windows-10-using-powershell/>`_.

   The instructions below show you how to set up the WSL and configure it to use
   DataLad and its dependencies. They follow the
   `Microsoft Documentation on the Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_.
   If you run into troubles during the installation, please consult the
   `WSL troubleshooting page <https://docs.microsoft.com/en-us/windows/wsl/troubleshooting>`_.



   - **Step 1**: Enable the windows subsystem for Linux.

      - Start the Power Shell as an administrator. Run both commands below,
        only restart after the second one (despite being prompted after the first one already)::

           Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
           Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

   - **Step 2**: Install a Debian Linux distribution

      - To do this, visit the Microsoft store, and search for the Debian distro.
        We **strongly** recommend installing :term:`Debian`, even though other
        distributions are available. "Get" the app, and "install" it.

   - **Step 3**: Initialize the distribution

      - Launch the Subsystem either from the Microsoft store or from the Start menu. This
        will start a terminal. Do not worry -- there is a dedicated section (:ref:`howto`)
        on how to work with the terminal if you haven't so far.

      - Upon first start, you will be prompted to enter a new UNIX username and password.
        Tip: chose a short name, and no spaces or special characters. The password will
        become necessary when you elevate a process using ``sudo`` -- sudo let's you execute a
        process with rights of another user, such as administrative rights, for examples when
        you need to install software.


   - **Step 4**: Configure the WLS

      - Start the Power Shell as an administrator. To set the WSL version to WSL2, run
        ``wsl --set-default-version 2``. Configure the distro to use WSL2 by running
        ``wsl -l -v``. This should give an output like this::

               NAME        STATE               VERSION
           *   Debian       Running            2

   - **Step 5**: Enable NeuroDebian

      - In the terminal of your distribution, run

      .. code-block:: bash

         $ wget -O- http://neuro.debian.net/lists/stretch.de-md.libre | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list

      - Afterwards, run

      .. code-block:: bash

         $ curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xA5D32F012649A5A9" | sudo apt-key add

      - lastly do another

      .. code-block:: bash

         $ sudo apt-update && sudo apt upgrade

   - **Step 6**: Install datalad and everything it needs from Neurodebian

      .. code-block:: bash

         $ sudo apt install datalad

   .. todo::

      - maybe update Step 6 to use ``pip3`` to install DataLad and Git-annex.


Initial configuration
^^^^^^^^^^^^^^^^^^^^^

Initial configurations only concern the setup of a :term:`Git` identity. If you
are a Git-user, you should hence be good to go.
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
