.. _usecase_using_globus_as_datastore:

Using Globus as a data store for the Canadian Open Neuroscience Portal
----------------------------------------------------------------------

.. index:: ! Usecase; Using Globus as data store

This use case shows how the `Canadian Open Neuroscience Portal (CONP) <https://conp.ca/>`_
disseminates data as DataLad datasets using the `Globus <https://www.globus.org/>`_
network with :term:`git-annex`, a custom git-annex :term:`special remote`, and
Datalad. It demonstrates

#. How to enable the git-annex `Globus special remote  <https://github.com/CONP-PCNO/git-annex-remote-globus>`_
   to access files content from `Globus.org <https://www.globus.org/>`_,
#. The workflows used to access datasets via the
   `Canadian Open Neuroscience Portal (CONP) <https://conp.ca/>`_,
#. An example of disk-space aware computing with large datasets distributed
   across systems that avoids unnecessary replication, eased by DataLad and
   :term:`git-annex`.

The Challenge
^^^^^^^^^^^^^

Every day, researchers from different fields strive to advance present
state-of-the-art scientific knowledge by generating and publishing novel
results. Crucially, they must share such results with the scientific
community to enable other researchers to further build on existing data
and avoid duplicating work.

The `Canadian Open Neuroscience Portal (CONP) <https://conp.ca/>`_ is a publicly
available platform that aims to remove the technical barriers to practicing open science
and improve the accessibility and reusability of neuroscience research to accelerate
the pace of discovery. To this end, the platform will provide a unified interface
that -- among other things -- enables sharing and open dissemination of both neuroscience
data and methods to the global community.
Managing the scientific data ecosystem is extremely challenging given
the amount of new data generated every day, however.
CONP must take a strategic solution to allow researchers to

- dynamically work on present data,
- upload new versions of the data, and
- generate additional scientific work.

An underlying data management system to achieve this must be flexible, dynamic
and light-weight. It would need to have the ability to easily distribute datasets
across multiple locations to reduce the need of re-collecting or replicating
data that is similar to already existing datasets.

The Datalad Approach
^^^^^^^^^^^^^^^^^^^^

CONP makes use of Datalad as a data management tool to enable efficient analysis
and work on datasets: Datalad minimizes the computational cost of holding full storage of
datasets versions, it allows files in a dataset to be distributed across
multiple download sources, and to be retrieved on demand only to save disk space.
Therefore, it is common practice for researchers to both download and
publish research content in a dataset format via a CONP, which provides them
with a vast dataset repository.

.. findoutmore:: Basic principles of DataLad for new readers

    If you are new to DataLad, the introduction of the handbook and the chapter
    :ref:`chapter_datasets` can give you a good idea of what DataLad and its
    underlying tools can to, as well as a hands-on demonstration. This findoutmore,
    in the meantime, sketches a high-level overview of the principles behind DataLad's
    data sharing capacities.

    Datalad is built on top of `Git <https://git-scm.com/>`_ and
    `git-annex <https://git-annex.branchable.com/>`_, and enables data version
    control. A one-page overview can be found in section :ref:`executive_summary`.

    :term:`git-annex` is a useful tool that extends Git with the ability to manage
    repositories in a lightweight fashion even if they contain large amounts of
    data. One main principle of git-annex lies storing data that should not be
    stored in Git (e.g., due to size limits) in an :term:`annex`. In its place, it
    generates symbolic links (:term:`symlink`\s) to these *annexed* files that encode
    their file content. Only the symlinks are committed into :term:`Git` while
    :term:`git-annex` handles data management in the annex. A detailed explanation
    of this process can be found in the section :ref:`symlink`, but the outcome
    of it is a light-weight Git repository that can be cloned fast and yet contains
    access to arbitrarily large data managed by :term:`git-annex`.

    In the case of data sharing procedures, annexed data can be stored in various
    third party hosting services configured as
    `special remotes <https://git-annex.branchable.com/special_remotes/>`_.
    When retrieving data, :term:`git-annex` requests access to the primary data
    source storing those files to retrieve actual files content when the user
    needs it.

The workflows for users to get data are straightforward:
Users log into the CONP portal and install Datalad datasets with
``datalad install -r <dataset>``. This gives them access to the annexed files
(as mentioned in the findoutmore above, large files replaced by their symlinks).
To request the content of the annexed files, they simply download those files
locally in their filesystem using ``datalad get path/to/file``. So simple!

On a technical level, under the hood, :term:`git-annex` needs to have a connection
established with the primary data source, the :term:`special remote`, that hosts
and provides the requested files' contents.
In some cases, annexed files are stored in `Globus.org <https://www.globus.org/>`__.
Globus is an efficient transfer files system suitable for researchers to share
and transfer files between so called *endpoints*, locations in Globus.org where
files get uploaded by their owners or get transferred to, that can be either
private or public. Annexed file contents are stored in such
`Globus endpoints <https://docs.globus.org/faq/globus-connect-endpoints/#what_is_an_endpoint>`_.
Therefore, when users download annexed files, Globus communicates with git-annex
to provide access to files content. Given this functionality, we can say that
Globus works as a data store for git-annex, or in technical terms, that Globus is
configured to work as a :term:`special remote` for git-annex. This is
possible via the git-annex backend interface implementation for Globus
called `git-annex-globus-remote <https://github.com/CONP-PCNO/git-annex-remote-globus>`_
developed by CONP.
In conjunction, CONP and the git-annex-globus-remote constitute the building
blocks that enable access to datasets and its data: CONP hosts small-sized
datasets, and Globus.org is the data store that (large) file content can be
retrieved from.

To sum up, CONP makes a variety of datasets available and provides them to researchers
as Datalad datasets that have the regular, advantageous Datalad functionality.
All of this exists thanks to the ability of git-annex and Datalad to interface with
special remote locations across the web such as `Globus.org <https://www.globus.org>`__
to request access to data.
In this way, researchers have access to a wide research data ecosystem and can use
and reuse existing data, thus reducing the need of data replication.



Step-by-Step
^^^^^^^^^^^^

Globus as git-annex data store
""""""""""""""""""""""""""""""
A remote data store exists thanks to git-annex (which DataLad builds upon):
git-annex uses a key-value pair to reference files. In the git-annex object tree,
large files in datasets are stored as values while the key is generated from their
contents and is checked into Git. The key is used to reference the location of the value
in the object tree [#f1]_. The :term:`object-tree` (or keystore) with the data contents can
be located anywhere – its location only needs to be encoded using a special remote.
Therefore, thanks to the `git-annex-globus-remote <https://github.com/CONP-PCNO/git-annex-remote-globus>`_
interface, Globus.org provides git-annex with location information to retrieve
values and access files content with the corresponding keys.
To ultimately enable end users’ access to data,
git-annex registers Globus locations by assigning them to Globus-specific URLs,
such as ``globus://dataset_id/path/to/file``. Each Globus URL is associated
with a the key corresponding to the given file. The use of a Globus URL protocol
is a fictitious mean to assign each file of the dataset a unique location and
source and therefore, it is a wrapper for additional validation that is performed
by the git-annex-globus-remote to check on the actual presence of the file within
the Globus transfer file ecosystem. In other words, the ‘Globus URL’ is simply an
alias of an existing file located on the web and specifically available in Globus.org.
Registration of Globus URLs in git-annex is among the configuration procedures
carried out on an administrative, system-wide level, and users will only deal
with direct easy access of desired files.

With this, Globus is configured to receive data access requests from git-annex
and to respond back if data is available. Currently, the git-annex-globus-remote
only supports data *download* operations. In the future, it could be useful for
additional functionality as well.
When the globus special remote gets initialized for the first time, the user
has to authenticate to Globus.org using `ORCID <https://orcid.org/>`_ ,
`Gmail <https://mail.google.com>`_ or a specific Globus account.
This step will enable git-annex to then initialize the globus special remote and
establish the communication process. Instructions to use the globus special remote
are available at `github.com/CONP-PCNO/git-annex-remote-globus <https://github.com/CONP-PCNO/git-annex-remote-globus>`_.
Guidelines specifying the standard communication protocol to implement a custom
special remote can be found at
`git-annex.branchable.com/design/external_special_remote_protocol <https://git-annex.branchable.com/design/external_special_remote_protocol/>`_.


An example using Globus from a user perspective
"""""""""""""""""""""""""""""""""""""""""""""""
It always starts with a dataset, installed with either :command:`datalad install`
or :command:`datalad clone`.

.. code-block:: bash

   $ datalad install -r <dataset>
   $ cd <dataset>

In order to get access to annexed data stored on Globus.org, users need to
install the globus-special-remote. If it is the first time using
Globus, users will need to authenticate to Globus.org by running the
``git-annex-remote-globus setup`` command:

.. code-block:: bash

   $ pip install git-annex-remote-globus
   # if first time
   $ git-annex-remote-globus setup

After the installation of a dataset, we can see that most of the files in the
dataset are annexed: Listing a file with ``ls -l`` will reveal a :term:`symlink`
to the dataset's annex.

.. code-block:: bash

   $ ls -l NeuroMap_data/cortex/mask/mask.mat
    cortex/mask/mask.mat -> ../../../.git/annex/objects/object.mat

However, without having any content downloaded yet, the symlink currently points
into a void, and tools will not be able to open the file as its contents
are not yet locally available.

.. code-block:: bash

   $ cat NeuroMap_data/cortex/mask/mask.mat
     NeuroMap_data/cortex/mask/mask.mat: No such file or directory

However, data retrieval is easy. At first, users have to enable the globus remote.

.. code-block:: bash

   $ git annex enableremote globus
    enableremote globus ok
    (recording state in git...)

After that, they can download any file, directory, or complete dataset using
:command:`datalad get`:

.. code-block:: bash

   $ datalad get NeuroMap_data/cortex/mask/mask.mat
    get(ok): NeuroMap_data/cortex/mask/mask.mat (file) [from globus...]

   $ ls -l NeuroMap_data/cortex/mask/mask.mat
    cortex/mask/mask.mat -> ../../../.git/annex/objects/object.mat

   $ cat NeuroMap_data/cortex/mask/mask.mat
    # you can now access the file !


Downloaded! Researchers could now use this dataset to replicate previous analyses
and further build on present data to bring scientific knowledge forward.
CONP thus makes a variety of datasets flexibly available and helps to disseminate
data. The on-demand availability of files in datasets can help scientists to
save disk space. For this, they could get only those data files that they need
instead of obtaining complete copies of the dataset, or they could locally
:command:`drop` data that is hosted and thus easily re-available on Globus.org
after their analyses are done.


Resources
^^^^^^^^^

The ``README`` at `github.com/CONP-PCNO/git-annex-remote-globus <https://github.com/CONP-PCNO/git-annex-remote-globus>`_
provides an excellent and in-depth overview of how to install and use
the git-annex special remote for Globus.org.


.. rubric:: Footnotes

.. [#f1] More details on how :term:`git-annex` handles data underneath the hood and
         how the :term:`object-tree` works can be found in section :ref:`symlink`.