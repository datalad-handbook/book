.. _install:

Installation and configuration
------------------------------

Install DataLad
^^^^^^^^^^^^^^^

The content in this chapther is largely based on the information given on the
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


OS X
""""

A common way to install packages on OS X is via the
`homebrew <https://brew.sh/>`_ package manager.
First, install the homebrew package manager. Note that prior
to the installation, `Xcode <https://apps.apple.com/us/app/xcode/id497799835>`_
needs to be installed from the Mac App Store.
Homebrew then can be installed using the command following the
instructions on their webpage (linked above).

Next, `install Git-annex <https://git-annex.branchable.com/install/OSX/>`_.

Once Git-annex is available, DataLad can be installed via Pythons package
manager ``pip`` as described below.

Using Pythons package manager ``pip``
"""""""""""""""""""""""""""""""""""""

DataLad can be installed via Pythons package manager
`pip <https://pip.pypa.io/en/stable/>`_.
``pip`` comes with Python distributions, e.g. the Python distributions
downloaded from `python.org <https://www.python.org>`_. When downloading
Python, make sure to chose a recent Python **3** distribution.

If you have Python and ``pip`` set up,
to automatically install DataLad and its software dependencies, type

.. code-block:: bash

   $ pip install datalad

If this results in a ``permission denied`` error, install DataLad into
a user's home directory:

.. code-block:: bash

   $ pip install --user datalad

In addition, it is necessary to have a current version of :term:`Git-annex` installed which is
not set up automatically by using the ``pip`` method.
You can find detailed installation instructions on how to do this
`here <https://git-annex.branchable.com/install/>`_.

.. todo::

   how to install Git-annex without sudo permissions. Currently the docs say:
   "Git-annex can be deployed by extracting pre-built binaries from a tarball
   (that also includes an up-to-date Git installation). Obtain the tarball,
   extract it, and set the PATH environment variable to include the root of the
   extracted tarball. Fingers crossed and good luck!" This could be turned into
   a less intimidating step-by-step guide.

   It is actually sufficient to just extract the provided EXE installer into an
   existing Git installation directory (`example of how this is done in
   DataLad's own test environment on Windows
   <https://github.com/datalad/datalad/blob/master/appveyor.yml#L59>`__). If done
   this way, no PATH variable manipulation is necessary, and things just start to
   work.


Windows 10
""""""""""

There are two ways to get DataLad on Windows 10: one is within Windows itself,
the other is using WSL, the Windows Subsystem for Linux. **We** *strongly*
**recommend the latter.**

Note: Using Windows comes with some downsides.
In general, DataLad can feel a bit sluggish on Windows systems. This is because of
a range of filesystem issues that also affect the version control system :term:`Git` itself,
which DataLad relies on. The core functionality of DataLad should work, and you should
be able to follow the contents covered in this book.
You will notice, however, that some
Unix commands displayed in examples may not work given the installation that you
chose, and that terminal output can look different from what is displayed here.
If you are a Windows user and want to help improve the handbook for Windows users,
please `get in touch <https://github.com/datalad-handbook/book/issues/new>`_.



.. container:: toggle

   .. container:: header

      **1) Install within WSL [recommended]**

   The Windows Subsystem for Linux (WSL) allows Windows users to have full access
   to a Linux distribution within Windows.
   The improves the DataLad experience on Windows *greatly*.

   If you have always used Windows be prepared for some user experience changes when
   using Linux compared to Windows. For one, there will be no graphical user interface
   (GUI). Instead, you will work inside a terminal window. This however
   mirrors the examples and code snippets provided in this handbook exactly.
   Also, note that there will be incompatibilities between the Windows and Linux filesystems.
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
        will start a terminal. Don't worry -- there is a dedicated section (:ref:`howto`)
        on how to work with the terminal if you haven't so far.

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

      **2) Install within WSL2 [TODO; will be the recommendation soon]**

   .. todo::

      - find out how to install/enable WSL2

      - find out what changes about the above instructions


.. container:: toggle

   .. container:: header

      **3) Install within Windows**

   Note: This installation method will get you a working version of
   DataLad, but be aware that many Unix commands shown in the book
   examples will not work for you, and DataLad-related output might
   look different from what we can show in this book.

   - **Step 1**: If you haven't, install Python3

      - Check the official
        `Python docs on installing on Windows <https://docs.python.org/3/using/windows.html>`_
        for instructions here. Please read the recommendation below,
        though

      - **Check the box "Add Python <version> to PATH** at the bottom
        of the window, and select "Customize installation".

      - Stay with the default options to install all optional features,
        and additionally tick
        "Add Python to environment variables" on the second page.
        Optionally, tick the box
        "Install for all users" to ensure that other users on the computer
        are able to use Python.

      - Finish the installation. After successful installation, instruct the installer
        to bypass the 260 character file path limit (option available at the bottom
        of the window).

      - Check the installation by opening CMD (type ``cmd`` into the Windows
        search bar and press ``Enter``) and typing python + ``Enter``. You should
        see Python start up in the terminal. This means that Python is working
        and the ``PATH`` is set correctly. Yay!

   - **Step 2**: Install Git

      - Go to https://git-scm.com/downloads, select Windows, and
        **download the 32-bit Git for Windows Setup** (not the 64-bit version!)

   - **Step 3**: Install Git-annex

      - Obtain the current Git-annex versions installer
        `from here <https://downloads.kitenet.net/git-annex/windows/current/>`_.
        Save the file, and double click the downloaded
        :command:`git-annex-installer.exe` in your Downloads.

      - During installation, you will be prompted to "Choose Install Location".
        **Specify the directory in which Git is installed**.

   - **Step 4**: Install DataLad via pip

      - ``pip`` should be installed together with recent Python versions on
        Windows. Open ``cmd`` and type ``pip install --user datalad``.


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
   % git config --global --add user.name Bob McBobFace
   % git config --global --add user.email bob@example.com

This information is used to track changes in the DataLad projects you will
be working on. Based on this information, changes you make are associated
with your name and email address, and you should use a real email address
and name -- it does not establish a lot of trust nor is it helpful after a few
years if your history, especially in a collaborative project, shows
that changes were made by ``Anonymous`` with the email
``youdontgetmy@email.fu``.
And don't worry, you won't get any emails from Git or DataLad.
