.. _usecase_datastore:

Building a scalable data storage for scientific computing
---------------------------------------------------------

Research can require enormous amounts of data. Such data needs to be accessed by
multiple people at the same time, and is used across a diverse range of
computations or research questions.
The size of the dataset, the need for simultaneous access and transformation
of this data by multiple people, and the subsequent storing of multiple copies
or derivatives of the data constitutes a challenge for computational clusters
and requires state-of-the-art data management solutions.
This use case details a model implementation for a scalable data storage
solution, suitable to serve the computational and logistic demands of data
science in big (scientific) institutions, while keeping workflows for users
as simple as possible. It elaborates on

#. How to implement a scalable, remote data store so that data are
   stored in a different place than where people work with it,
#. How to configure the data store and general cluster setup for easy and
   fast accessibility of data, and
#. How to reduce technical complexities for users and encourage reproducible,
   version-controlled scientific workflows.

.. note::

   This usecase is technical in nature and aimed at IT/data management
   personnel seeking insights into the technical implementation and
   configuration of a scalable data storage. In particular, it describes the
   RIA data storage implementation as done in INM-7, research centre Juelich,
   Germany.


The Challenge
^^^^^^^^^^^^^

The data science institute XYZ consists of dozens of people: Principle
investigators, PhD students, general research staff, system administration,
and IT support. It does research on important global issues, and prides
itself with ground-breaking insights obtained from elaborate and complex
computations run on a large scientific computing cluster.
The data sets used in the institute are big both in size and number of files,
and expensive to collect.
Therefore, datasets are used for various different research questions, by
multiple researchers.

Every member of the institute has an account on an expensive and large compute cluster, and all
of the data exists in dedicated directories on this server. In order to work on
their research questions without modifying original data, every user creates their own
copies of the full data in their user account on the cluster -- even if it
contains many files that are not necessary for their analysis. In addition,
they add all computed derivatives and outputs, even old versions, out of fear
of losing work that may become relevant again.
This is because version control is not a standard skill in the institute, and
especially PhD students and other trainees struggle with the technical
overhead of data management *and* data science. Thus, an excess of
data copies and derivatives exists in addition to the already substantial
amount of original data. At the same time, the compute cluster is both the
data storage and the analysis playground for the institute. With data
directories of several TB in size, *and* computationally heavy analyses, the
compute cluster is quickly brought to its knees: Insufficient memory and
IOPS starvation make computations painstakingly slow, and hinder scientific
progress, despite the elaborate and expensive cluster setup.

Therefore, the challenge is two-fold: On an infrastructural level, institute XYZ
needs a scalable, flexible, and maintainable data storage solution for their
growing collection of large datasets.
On the level of human behavior, researchers not formerly trained in data
management need to apply and adhere to advanced data management principles.

The DataLad approach
^^^^^^^^^^^^^^^^^^^^

The compute cluster is refurbished to a state-of-the-art data management
system.
Unlike traditional solutions, both because of the size of the large
amounts of data, and for more efficient use of compute power for
calculations instead of data storage, the cluster gets a remote data
store: Data lives as DataLad datasets on a different machine than the one
the scientific analyses are computed on.
For a scalable and flexible dataset storage and access to the annexed data in
datasets, the data store is a Remote Indexed Archive (RIA) store, an extendable,
file-system based storage solution for DataLad datasets that aligns well with the
requirements of scientific computing (infrastructure), and is configured as a
git-annex `RIA-remote <https://libraries.io/pypi/ria-remote>`_.
In case of filesystem inode limitations on the machine the RIA store exists on
(e.g., HPC storage systems), full datasets can be (compressed) 7-zip archives,
without losing the ability to query available files. Regardless of the number of
file and size of them, such datasets thus use only few inodes.

.. todo::

   Is this still the case?

DataLad's run-procedures can be used to distribute institute-wide
configurations adjusted to the compute infrastructure among users to mitigate any
potential remaining technical overhead to interact with the data store.

The infrastructural changes are accompanied by changes in the mindset and workflows
of the researchers that perform analyses on the cluster.
By using a RIA store, the institute's work routines are adjusted around
DataLad datasets.

.. todo::

   Update the workflow overview, if necessary

Analyses are set-up inside of DataLad datasets, and for every
analysis, an associated ``project`` is created under the namespace of the
institute on the institute's :term:`GitLab` instance automatically. This has
the advantage of vastly simplified version control and
simplified access to projects for collaborators and supervisors. Data
from the data store is cloned as subdatasets. This comes with several
benefits: Analyses are automatically linked to data, no unused file
copies waste disk space on the compute cluster as data can be retrieved
on-demand, and files that are easily re-obtained or recomputed can safely be
dropped locally to save even more disk-space. Moreover, upon creation of an analysis
project, the associated GitLab project it is automatically configured as a remote
with a publication dependency on the data store, thus enabling vastly simplified
data publication routines and backups of pristine results.


Step-by-step
^^^^^^^^^^^^

The following section will elaborate on the details of the technical
implementation of a RIA store, and the workflow requirements and incentives for
researchers. Both of them are aimed at making scientific analyses on a
compute cluster scale, but can be viewed as independent (yet complimentary).
Some hardware-specific implementation details are unique to the real-world
example this usecase is based on. For example, to create a data store, parts of
the old compute cluster and parts of the super computer at the Juelich
supercomputing centre (JSC) are used to store large amounts of data. Thus,
multiple different, independent machines take care of warehousing the data.
While this is unconventional, it is convenient: The data does not strain the
compute cluster, and with DataLad, it is irrelevant where the data are located.
While such a setup for a RIA store made sense in this particular case of
application and is possible with DataLad, a remote setup is not a requirement
for a RIA store.


Incentives and imperatives for disk-space aware computing
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

One aspect of the problem are disk-space unaware computing workflows. Researchers
make and keep numerous copies of data in their home directory and perform
computationally expensive analyses on the headnode of a compute cluster because
they don't know better, and/or want to do it in the easiest way possible.
A general change for the better can be achieved by imposing sensible limitations
and restrictions on what can be done at which scale on a new compute cluster.
On a high level, this can be summarized as the *Trinity of research data handling*
in the figure below:

.. figure:: ../artwork/src/ephemeral_infra.svg
   :alt: A simple, local version control workflow with datalad.
   :figwidth: 80%

   Trinity of research data handling: The data store (``$DATA``) is managed and
   backed-up. The compute cluster (``$COMPUTE``) has an analysis-appropriate structure
   with adequate resources, but just as users workstations/laptops (``$HOME``),
   it is not concerned with data hosting.

Data from the RIA store (``$DATA``) is accessible for researchers for exploration
and computation, but the scale of the operations they want to perform can require
different approaches.
On their own machines or ``$HOME`` directories on the cluster (``$HOME``),
researchers are free to do whatever they want as long as it is within the limits
of their machines or their user accounts. On the clusters head node, with 100GB
storage per person, researchers can explore data from the store (``$DATA``),
test and develop code, or visualize results, but they can not create complete
dataset copies or afford to keep an excess of unused data around.
Only the cluster's compute nodes (``$COMPUTE``) have the necessary hardware
requirements for expensive computations, and can also pull from ``$DATA``.
Thus, within ``$HOME``, researchers are free to explore data from ``$DATA``
as they wish, but scaling requires them to use ``$COMPUTE``. By using a job
scheduler, compute jobs of multiple researchers are distributed fairly across
the available compute infrastructure. Version controlled (and potentially
reproducible) research logs and the results of the analyses can be pushed from
``COMPUTE`` to ``$DATA`` for back-up and archival, and hence anything that is
relevant for a research project is tracked, backed-up, and stored, all without
straining available disk-space on the cluster afterwards. While the imposed
limitations are independent of DataLad, DataLad can make sure that the necessary
workflows are simple enough for researchers of any seniority, background, or
skill level.

A Remote Indexed Archive Store
""""""""""""""""""""""""""""""

The remote data store exists thanks to :term:`git-annex` (which DataLad builds upon):
Large files in datasets are stored as *values* in git-annex's object tree. A *key*
generated from their contents is checked into Git and used to reference the
location of the value in the object tree [#f1]_. The object tree (or *keystore*)
with the data contents can be located anywhere -- its location only needs to be
encoded using a *special remote*. This configuration is done on an
administrative, system-wide level, and users do not need to care or know
about where data are stored, as they can access it just as easily as before.

.. findoutmore:: What is a special remote?

   A `special-remote <https://git-annex.branchable.com/special_remotes/>`_ is an
   extension to Git's concept of remotes, and can enable git-annex to transfer
   data to and from places that are not Git repositories (e.g., cloud services
   or external machines such as an HPC system). Don't envision a special-remote as a
   physical place or location -- a special-remote is just a protocol that defines
   the underlying *transport* of your files *to* and *from* a specific location.

The machines in question, parts of an old compute cluster, and parts of the
supercomputer at the JSC are configured to receive and store data using the
git-annex remote for indexed file archives (`RIA <https://libraries.io/pypi/ria-remote>`_)
special remote. The git-annex RIA-remote is similar to git-annex's built-in
`directory <https://git-annex.branchable.com/special_remotes/directory/>`_
special remote, but distinct in certain aspects:

- It allows read access to (compressed) 7z archives, which is a useful
  feature on systems where light quotas on filesystem inodes are imposed
  on users, or where one wants to have compression gains.
  This way, the entire keystore (i.e., all data contents) of the
  remote that serves as the data store can be put into an archive that uses
  only a handful of inodes, while remaining fully accessible.

- It provides access to configurable directories via SSH.
  This makes it easier to accommodate infrastructural changes, especially when dealing
  with large numbers of repositories, as moving from local to remote operations, or
  switching target paths can be done by simply changing the configuration.

- It allows a multi-repository directory structure, in which keystore
  directories of multiple repositories can be organized in to a homogeneous
  archive directory structure. Importantly, the keystore location in an archive is defined
  using the **datasets UUID** (in case of DataLad datasets) or the annex remote
  UUID (in case of any non DataLad dataset). This aids handling of large
  numbers of repositories in a data store use case, because locations are
  derived from *repository properties* rather than having to re-configure them explicitly.

The structure under which data is stored in the data store looks like this:

.. code-block::
   :emphasize-lines: 1-2, 4-12, 21-24

    ├── 946
    │   └── e8cac-432b-11ea-aac8-f0d5bf7b5561
    │       ├── annex
    │       │   └── objects
    │       │       ├── 6q
    │       │       │   └── mZ
    │       │       │       └── MD5E-s93567133--7c93fc5d0b5f197ae8a02e5a89954bc8.nii.gz
    │       │       │           └── MD5E-s93567133--7c93fc5d0b5f197ae8a02e5a89954bc8.nii.gz
    │       │       ├── 6v
    │       │       │   └── zK
    │       │       │       └── MD5E-s2043924480--47718be3b53037499a325cf1d402b2be.nii.gz
    │       │       │           └── MD5E-s2043924480--47718be3b53037499a325cf1d402b2be.nii.gz
    │       │       ├── [...]
    │       │       └── [...]
    │       ├── archives
    │       │   └── archive.7z
    │       ├── branches
    │       ├── config
    │       ├── description
    │       ├── HEAD
    │       ├── hooks
    │       │   ├── applypatch-msg.sample
    │       │   ├── [...]
    │       │   └── update.sample
    │       ├── info
    │       │   └── exclude
    │       ├── objects
    │       │   ├── 05
    │       │   │   └── 3d25959223e8173497fa7f747442b72c31671c
    │       │   ├── 0b
    │       │   │   └── 8d0edbf8b042998dfeb185fa2236d25dd80cf9
    │       │   ├── [...]
    │       │   │   └── [...]
    │       │   ├── info
    │       │   └── pack
    │       ├── refs
    │       │   ├── heads
    │       │   │   ├── git-annex
    │       │   │   └── master
    │       │   └── tags
    │       ├── ria-layout-version
    │       └── ria-remote-ebce196a-b057-4c96-81dc-7656ea876234
    │           └── transfer

The code block above shows the representation of one dataset in the RIA store
and helps to illustrate how the RIA-remote features look like in real life:

- Datasets are identified via their :term:`UUID` (e.g.,
  ``946e8cac-432b-11ea-aac8-f0d5bf7b5561``). The UUID is split into the first
  two levels of the tree structure (as highlighted above in the first two
  lines). This two-level structure exists to avoid exhausting file system limits
  on the number of files/folders within a directory.
- This first, two-level tree structure can host keystores for any number of
  repositories.
- The third level holds a directory structure that is identical to a *bare* git
  repository, and is a clone of the dataset.

  .. findoutmore:: What is a bare Git repository?

     A bare Git repository is a repository that contains the contents of the ``.git``
     directory of regular DataLad datasets or Git repositories, but no worktree
     or checkout. This has advantages: The repository is leaner, it is easier
     for administrators to perform garbage collections, and it is required if you
     want to push to it at all times. You can find out more on what bare repositories are and how to use them
     `here <https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a
     -Server>`_.

- Inside of the bare Git repository, the ``annex`` directory -- just as in
  any standard dataset or repository -- contains the keystore (object tree) under
  ``annex/objects`` (highlighted above as well). Details on how this object tree
  is structured are outlined in the hidden section in :ref:`symlink`.
- These keystores can be 7zipped if necessary to hold (additional) git-annex objects,
  either for compression gains, or for use on HPC-systems with inode limitations.

This implementation is fully self-contained, and is a plain file system storage,
not a database.


--> advantages here

.. findoutmore:: How to create a RIA store

   This needs to be a step-by-step instruction how to create a RIA store

Workflows based on the RIA store
""""""""""""""""""""""""""""""""

Once it is set up, in order to retrieve data from the data store, special
remote access to the data store needs to be initialized.

This is done with a custom configuration (``cfg_inm7``) as a run-procedure [#f2]_ with a
:command:`datalad create` command::

   $ datalad create -c inm7 <PATH>

The configuration performs all the relevant setup of the dataset with a fully
configured link to ``$DATA``: It is configured as a remote to clone and pull
data from, but upon creation of the dataset, the dataset's directory is also created at the remote
end as a bare repository to enable pushing of results back to ``$DATA``. At the same
time, a GitLab :term:`sibling` in the institute's GitLab instance is created, with a
publication dependency on the data storage.

With this setup, a dataset of any size can be cloned in a matter of seconds
by providing its ID as a source in a :command:`datalad clone` command::

   $ datalad clone --dataset mynewdataset \
     --source <ID/URL> \
     mynewdataset/inputs

Actual data content can be obtained on demand via :command:`datalad get`. Thus,
users can selectively obtain only those contents they need instead of having
complete copies of datasets as before.

.. todo::

   maybe something about caching here

   The major advantages of such a store are its
   flexibility, scalability, and maintainability. Because datasets can be identified
   with their universally unique ID, there is no need for static, filename-based
   hierarchies. New datasets can be added to the store without consequences for
   existing ones

   .. todo::

      maybe contrast this to datasets.datalad.org).

   .. todo::

       - What are the advantages? --> flexible store: Can hold any amount of datasets,
         and as datasets are identified via ID, there is no need for static filename-based
         hierarchies.
       - Problem: Subdataset layout in superdataset does not reflect store layout. Where
         subdataset is referenced in superdataset as lying directly underneath the super
         dataset, it is referenced under their ID in the store. BUT: .gitmodules does
         not only hold path, but also dataset ID
       - Talk about 0.12.2 features: Resolving dataset IDs to URLs, subdataset-source-
         candidates in superdatasets, using ria+// URLs to point to RIA stores and
         dataset versions,

As the store consists of bare git repositories (with optionally 7zipped archives
or annexes), it is easily maintainable by data stewards or system administrators.
Common compression or cleaning operations of Git and git-annex can be performed
without requiring knowledge about the data inside of the store.

Upon :command:`datalad publish`, computed results can be pushed to the data store
and be thus backed-up. Easy-to-reobtain input data can safely be dropped to free
disk space on the compute cluster again.

With this remote data store setup, the compute cluster is efficiently used for
computations instead of data storage. Researchers can not only compute their
analyses faster and on larger datasets than before, but with DataLad's version
control capabilities their work also becomes more transparent, open, and reproducible.


.. findoutmore:: Software Requirements

   - git-annex version 7.20 or newer
   - DataLad version 0.12.5 (or later), or any DataLad development version more
     recent than May 2019 (critical feature: https://github.com/datalad/datalad/pull/3402)
   - The ``cfg_inm7`` run procedure as provided with ``pip install git+https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad.git``
   - Server side: 7z needs to be in the path.


.. rubric:: Footnotes

.. [#f1] To re-read about how git-annex's object tree works, check out section
         :ref:`symlink`, and pay close attention to the hidden section.
         Additionally, you can find much background information in git-annex's
         `documentation <https://git-annex.branchable.com/internals/>`_.

.. [#f2] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on GitLab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_.
