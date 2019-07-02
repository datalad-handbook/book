##############################
Installation and Configuration
##############################

Install DataLad
^^^^^^^^^^^^^^^

The content on this site is copied from the `DataLad website <https://www.datalad.org/get_datalad.html>`_
and the `DataLad documentation <http://docs.datalad.org/en/latest/gettingstarted.html>`_.

When there isn't anything more convenient
*****************************************

When there isn't anything more convenient (i.e. availability via package managers; see below),
DataLad is most easily installed via
`pip <https://pip.pypa.io/en/stable/>`_.
To automatically install DataLad and its software dependencies type

.. code-block:: bash

   $ pip install datalad

In addition, it is necessary to have a current version of Git-annex installed which is
not set up automatically by using the pip method.
You can find detailed installation instructions on how to do this
`here <https://git-annex.branchable.com/install/>`_.

.. admonition:: If you do not have admin powers…
   :class: note

   pip supports installation into a user’s home directory with the ``--user`` option:

   .. code-block:: bash

      $ pip install --user datalad


.. todo::

   how to install Git-annex without sudo permissions. Currently the docs say:
   "Git-annex can be deployed by extracting pre-built binaries from a tarball
   (that also includes an up-to-date Git installation). Obtain the tarball,
   extract it, and set the PATH environment variable to include the root of the
   extracted tarball. Fingers crossed and good luck!" This could be turned into
   a less intimidating step-by-step guide.


(Neuro)Debian, Ubuntu, and similar systems
******************************************
For Debian-based operating systems, the most convenient installation method
is to enable the `NeuroDebian <http://neuro.debian.net/>`_ repository.
If you are on a Debian-based system, but do not have the NeuroDebian repository
enabled, you should very much consider enabling it right now. The above hyperlink links
to a very easy instruction, and it only requires copy-pasting three lines of code.

The following command installs
DataLad and all of its software dependencies (including the Git-annex-standalone package):

.. code-block:: bash

   $ sudo apt-get install datalad


OS X
****

A common way to install packages on OS X is via the
`homebrew <https://brew.sh/>`_ package manager.
Git-annex can be installed using the command

.. code-block:: bash

   $ brew install git-annex

Once Git-annex is available, DataLad can be installed via ``pip`` as described above.
``pip`` comes with Python distributions, such as `anaconda <https://www.continuum.io/downloads>`_.



HPC environments or any system with singularity installed
*********************************************************

If you want to use DataLad on a high-performance computing (HPC) environment, such as a
computer cluster or a similar multi-user machine, where you don't have admin privileges,
chances are that `Singularity <http://singularity.lbl.gov/>`_ is already installed.
And if it isn't installed, the singularity website has a page dedicated to helping
you make a `solid case <http://singularity.lbl.gov/install-request>`_ to help convince
your admin why they really want to install it.

On any system with Singularity installed, you can pull a container with a full installation
of DataLad (~300 MB) straight from `Singularity Hub <https://singularity-hub.org/collections/667>`_.
The following command pulls the latest container for the DataLad development version
(check on Singularity Hub for alternative container variants)

.. code-block:: bash

   $ singularity pull shub://datalad/datalad:fullmaster

This will produce an executable image file. You can rename this image to ``datalad`` and
put the directory it is located in into your ``PATH`` environment variable.
From there on, you will have a ``datalad`` command available from the command line that
transparently executes all DataLad functionality through the container.

.. todo::

   What about Windows?
   mih says: "For windows people: it does work somewhat. Core functionality should be OK
   (current main focus of this effort), and is covered by tests. There are numerous issues
   with SSH connections on windows, though. It works much better on Win10 within the linux
   subsystem, and this is also where the hopes for the future are focused on. DataLad generally
   feels sluggish on Windows, because of a range of filesystem issues that also affect Git itself."
   Lets put that into some sort of instruction.


Initial configuration
^^^^^^^^^^^^^^^^^^^^^

Initial configurations only concern the setup of a :term:`Git` identity. If you
are a Git-User, you should hence be good to go.
If you have not used the version control system Git before, you will need to
tell Git some information about you. This needs to be done only once.
In the following example, exchange ``Bob McBobFace`` with your own name, and
``bob@example.com`` with your own email address.

.. code-block:: bash

   # enter your home directory using the ~ shortcut
   % cd ~
   % git-config --global --add user.name Bob McBobFace
   % git-config --global --add user.email bob@example.com

This information is used to track changes in the DataLad projects you will
be working on. Based on this information, changes you make are associated
with your name and email address, and you should use a real email address
and name - it does not establish a lot of trust nor is it helpful after a few
years if your history, especially in a collaborative project, shows
that changes were made by ``Anonymous`` with the email
``youdontgetmy@email.fu``.
And don't worry, you won't get any emails from Git or DataLad.
