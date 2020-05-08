.. _usecase_using_globus_as_datastore:

Using Globus as a data store for the Canadian Open Neuroscience Portal
----------------------------------------------------------------------

.. index:: ! Usecase; Using Globus as data store

This use case sketches the basic steps to gain access to existing datasets
distributed across the `Globus <https://www.globus.org/>`_ network via Datalad
and git-annex. It elaborates on

#. How to enable the git-annex `Globus special remote  <https://github.com/CONP-PCNO/git-annex-remote-globus>`_
   to access files content from `Globus.org <https://www.globus.org/>`_ ,
#. How disk-space aware computing can be eased by DataLad and git-annex
#. How to work with large datasets distributed across systems avoiding unnecessary
   replication and maintaining a light-weight approach


The Challenge
^^^^^^^^^^^^^
Every day, researchers from different fields strive to advance present
state-of-the-art scientific knowledge by generating and publishing novel
results. Crucially, they must share such results with the scientific
community to enable other researchers to further build on existing data
and avoid duplicating work.

Therefore, it is common practice for researchers to both download and
publish research content in a dataset format via a publicly available
portal, the `Canadian Open Neuroscience Portal (CONP) <https://conp.ca/>`_,
which provides them with a vast dataset repository. Managing the scientific data
ecosystem is extremely challenging given the amount of new data generated
every day. CONP must take a strategic solution to allow researchers to dynamically
work on present data, upload new versions and generate additional work. Such
system must be flexible, dynamic and light-weight. It would be very useful to distribute
datasets across multiple locations are reduce the need of replicating data


The Datalad Approach
^^^^^^^^^^^^^^^^^^^^
CONP makes use of Datalad as a data management tool to enable efficient analysis
and work on datasets: Datalad minimizes the computational cost of holding full storage of
datasets versions, it allows files in a dataset to be distributed across
multiple download sources and to be retrieved on need. Datalad is built
on top of `Git <https://github.com/>`_ and `git-annex <https://git-annex.branchable.com/>`_
which provide data version control. In particular, git-annex is a useful
Git extension tool to manage datasets in a lightweight fashion. It works
by generating and storing symbolic links (symlinks) of very large files
that cannot be stored in Git due to size limits, hence dramatically reducing
storage space. Git-annex requests access to the primary data source storing
those files, also called `special remote <https://git-annex.branchable.com/special_remotes/>`_,
to retrieve actual files content, only on user need.

Users log into the CONP portal and install Datalad datasets with
``datalad install -r <dataset>`` to access annexed files (as mentioned
above, large files replaced by their symlinks). To request content, they simply
download those files locally in their filesystem using ``datalad get path/to/file``.
So simple! Behind the hood, git-annex must have a connection established with
the primary data source, the ‘special remote’ providing the requested files content.
In some cases, files are stored in `Globus.org <https://www.globus.org/>`_,
or more specifically in so called ‘endpoints’, hence locations in Globus.org where
files get uploaded by their owners or get transferred to. Globus is an efficient
transfer files system suitable for researchers to share and transfer files between
endpoints that can be private or public. Therefore, when users download annexed files,
Globus communicates with git-annex to provide access to files content. Given this
functionality, we can say that Globus works as a data store for git-annex, or in
other words it is configured to work as a special remote for git-annex. This is
possible via the git-annex backend interface implementation for Globus
called `git-annex-globus-remote <https://github.com/CONP-PCNO/git-annex-remote-globus>`_.

To sum up, CONP makes available a variety of datasets and provides them to researchers
as Datalad datasets, given the advantageous Datalad functionalities. In this way,
researchers have access to a wide research data ecosystem without need of data replication
thanks to the ability of git-annex and Datalad to interface with special remote locations
across the web and request access to data !


Step-by-Step
^^^^^^^^^^^^

Globus as git-annex data store
""""""""""""""""""""""""""""""
A remote data store exists thanks to git-annex (which DataLad builds upon):
Git-annex uses a key-value pair to reference files. In the git-annex object tree,
large files in datasets are stored as values while the key is generated from their
contents and is checked into Git. The key is used to reference the location of the value
in the object tree. The object tree (or keystore) with the data contents can
be located anywhere – its location only needs to be encoded using a special remote.
Therefore, thanks to the git-annex-globus-remote interface, Globus.org provides
git-annex with locations information to retrieve values and access files content
with the corresponding keys. To ultimately enable end users’ access to data,
git annex registers Globus locations assigning them to Globus-specific URLs,
such as `globus://datadet_id/path/to/file`, where each Globus URL is associated
with a the key corresponding to the given file. The use of a Globus URL protocol
is a fictitious mean to assign each file of the dataset a unique location and
source and therefore, it is a wrapper for additional validation that is performed
by the git-annex-globus-remote to check on the actual presence of the file within
the Globus transfer file ecosystem. In other words, the ‘Globus URL’ is simply an
alias of an existing file located on the web and specifically available in Globus.org.
Registration of Globus URLs in git-annex is among the configuration procedures
carried out on an administrative, system-wide level, and users will only deal
with direct easy access of desired files.

Therefore, Globus is configured to receive request for data access from the git-annex
side and to respond back if data is available. Currently, git-annex-globus-remote
only supports data download operations but it could potentially be useful for additional
functionalities. When the globus-remote get initialized for the first time, the user
has to authenticate to Globus.org using ORCHiD, Gmail or a specific Globus accounts:
this step will enable git-annex to then initialize the globus-remote and establish the
communication process. To use globus-remote, instructions are available here:
https://github.com/CONP-PCNO/git-annex-remote-globus. To implement a special remote,
guidelines specifying the standard communication protocol can be found here:
https://git-annex.branchable.com/design/external_special_remote_protocol/


An example using Globus
"""""""""""""""""""""""
It always starts with a dataset:

.. code-block:: bash

   $ datalad install -r <dataset>
   $ cd <dataset>

Now we need to install the globus-special-remote, then authenticate to Globus.org if it is the first time
by running the setup

.. code-block:: bash

   $ pip install git-annex-remote-globus
   # if first time
   $ git-annex-remote-globus setup

We can see that most of the files in the dataset are annexed. You can check the symlink does not enable access to the file

.. code-block:: bash

   $ ls -l NeuroMap_data/cortex/mask/mask.mat
    cortex/mask/mask.mat -> ../../../.git/annex/objects/object.mat

   $ cat NeuroMap_data/cortex/mask/mask.mat
     NeuroMap_data/cortex/mask/mask.mat: No such file or directory


At this point we have to enable the globus remote and after that, we can try to download the file

.. code-block:: bash

   $ git annex enableremote globus
    enableremote globus ok
    (recording state in git...)

   $ datalad get NeuroMap_data/cortex/mask/mask.mat
    get(ok): NeuroMap_data/cortex/mask/mask.mat (file) [from globus...]

   $ ls -l NeuroMap_data/cortex/mask/mask.mat
    cortex/mask/mask.mat -> ../../../.git/annex/objects/object.mat

   $ cat NeuroMap_data/cortex/mask/mask.mat
    # you can now access the file !


Downloaded!

This dataset could now be used for any researcher to replicate previous analyses and further
build on present data to bring scientific knowledge forward !

