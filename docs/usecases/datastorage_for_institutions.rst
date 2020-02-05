.. _usecase_datastore:

Building a scalable data storage for scientific computing
---------------------------------------------------------

.. index:: ! Remote Indexed Archive (RIA) store

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

#. How to implement a scalable Remote Indexed Archive (RIA) store to flexibly
   store large amounts of DataLad datasets, potentially remote to lower storage
   strains on computing infrastructure,
#. How disk-space aware computing can be eased by DataLad based workflows and
   enforced by infrastructural incentives and limitations, and
#. How to reduce technical complexities for users and encourage reproducible,
   version-controlled, and scalable scientific workflows.

.. note::

   This usecase is technical in nature and aimed at IT/data management
   personnel seeking insights into the technical implementation and
   configuration of a RIA store or into its workflows. In particular, it
   describes the RIA data storage and workflow implementation as done in INM-7,
   research centre Juelich, Germany.


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
multiple researchers. Every member of the institute has an account on an expensive
and large compute cluster, and all of the data exists in dedicated directories
on this server. However, researchers struggle with the technical overhead of
data management *and* data science.
In order to work on their research questions without modifying
original data, every user creates their own copies of the full data in their
user account on the cluster -- even if it contains many files that are not
necessary for their analysis. In addition, as version control is not a standard
skill, they add all computed derivatives and outputs, even old versions, out of
fear of losing work that may become relevant again. Thus, an excess of (unorganized)
data copies and derivatives exists in addition to the already substantial
amount of original data. At the same time, the compute cluster is both the
data storage and the analysis playground for the institute. With data
directories of several TB in size, *and* computationally heavy analyses, the
compute cluster is quickly brought to its knees: Insufficient memory and
IOPS starvation make computations painstakingly slow, and hinder scientific
progress. Despite the elaborate and expensive cluster setup, exciting datasets
can not be stored or processed, as there just doesn't seem to be enough disk
space.

Therefore, the challenge is two-fold: On an infrastructural level, institute XYZ
needs a scalable, flexible, and maintainable data storage solution for their
growing collection of large datasets.
On the level of human behavior, researchers not formerly trained in data
management need to apply and adhere to advanced data management principles.

The DataLad approach
^^^^^^^^^^^^^^^^^^^^

The compute cluster is refurbished to a state-of-the-art data management
system.
For a scalable and flexible dataset storage, the data store is a Remote Indexed
Archive (RIA) store -- an extendable, file-system based storage solution for
DataLad datasets that aligns well with the requirements of scientific computing
(infrastructure).
The RIA store is configured as a git-annex
`RIA-remote special remote <https://libraries.io/pypi/ria-remote>`_ for access
to annexed keys in the store and so that full datasets can be (compressed)
7-zip archives. The latter is especially useful in case of filesystem inode
limitations, such as on HPC storage systems: Regardless of a dataset's number of
files and size, (compressed) 7zipped datasets use only few inodes, but retain the
ability to query available files.
Unlike traditional solutions, both because of the size of the large
amounts of data, and for more efficient use of compute power for
calculations instead of data storage, the RIA store is set up *remote*: Data is
stored on a different machine than the one the scientific analyses are computed
on. While unconventional, it is convenient, and perfectly possible with DataLad.

The infrastructural changes are accompanied by changes in the mindset and
workflows of the researchers that perform analyses on the cluster.
By using a RIA store, the institute's work routines are adjusted around
DataLad datasets. Simple configurations, distributed system-wide with DataLad's
run-procedures, or basic data management principles improve the efficiency and
reproducibility of research projects:
Analyses are set-up inside of DataLad datasets, and for every
analysis, an associated ``project`` is created under the namespace of the
institute on the institute's :term:`GitLab` instance automatically. This does
not only lead to vastly simplified version control workflows, but also to
simplified access to projects and research logs for collaborators and supervisors.
Input data gets installed as subdatasets from the RIA store. This automatically
links analyses projects to data sets, and allows for fine-grained access of up
to individual file level. With only precisely needed data, analyses datasets are
already much leaner than with previous complete dataset copies, but as data can
be re-obtained on-demand from the store, original input files or files that are
easily recomputed can safely be dropped to save even more disk-space.
Finally, upon creation of an analysis project, the associated GitLab project it
is automatically configured as a remote with a publication dependency on the
data store, thus enabling vastly simplified data publication routines and
backups of pristine results: After computing their results, a
:command:`datalad publish` is all it takes to backup and share ones scientific
insights. Thus, even with a complex setup of data store, compute infrastructure,
and repository hosting, configurations adjusted to the compute infrastructure
can be distributed and used to mitigate any potential remaining technical overhead.
Finally, with all datasets stored in a RIA store and in a single place, any remaining
maintenance and query tasks in the datasets can be performed by data management
personnel without requiring domain knowledge about dataset contents.


Step-by-step
^^^^^^^^^^^^

The following section will elaborate on the details of the technical
implementation of a RIA store, and the workflow requirements and incentives for
researchers. Both of them are aimed at making scientific analyses on a
compute cluster scale, but can be viewed as independent (yet complimentary).

.. note::

   Some hardware-specific implementation details are unique to the real-world
   example this usecase is based on, and are not a requirement. In this particular
   case of application, for example, a *remote* setup for a RIA store made sense:
   Parts of an old compute cluster and of the super computer at the Juelich
   supercomputing centre (JSC) instead of the institutes compute cluster are used
   to host the data store. This may be an unconventional storage location,
   but it is convenient: The data does not strain the compute cluster, and with
   DataLad, it is irrelevant where the RIA store is located. The next subsection
   introduces the general layout of the compute infrastructure and some
   DataLad-unrelated incentives and restrictions.

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

Remote indexed archive (RIA) stores
"""""""""""""""""""""""""""""""""""

**The looks and feels of a RIA store**

A RIA store is a storage solution for DataLad datasets that can be flexibly
extended with new datasets, independent of static file names or directory
hierarchies, and that can be (automatically) maintained or queried without
requiring expert or domain knowledge about the data. At its core, it is a flat,
file-system based repository representation of any number of datasets, limited
only by disk-space constrains of the machine it lies on.

Put simple, a RIA store is a dataset storage location that allows for access to
and collaboration on DataLad datasets (or, just as well, :term:`git-annex`
repositories). The high-level workflow overview is as follows: Create a dataset,
use the :command:`datalad create-sibling-ria` command to establish a connection
to an either pre-existing or not-yet-existing RIA store, publish dataset contents
with :command:`datalad publish`, (let others) clone the dataset from the
RIA store, and (let others) publish and pull updates. In the
case of large, institute-wide datasets, the RIA store can serve as a singular,
central storage location that enables fine-grained data access to everyone who
needs it, and as a storage and back-up location for all analyses datasets.

The layout of a RIA store is a tree of datasets. The first level of subdirectories
in this tree consists of the first three characters of the :term:`dataset ID`,
and the second level of subdatasets contains the remaining characters of the
dataset ID. Thus, the first two levels of subdirectories in the tree are split
dataset IDs of the datasets that are stored in them [#f1]_. The code block below
illustrates how a single DataLad dataset looks like in a RIA store, and the
dataset ID of the dataset (``946e8cac-432b-11ea-aac8-f0d5bf7b5561``) is
highlighted:

.. code-block::
   :emphasize-lines: 2-3

    /path/to/my_riastore
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
    ├── error_logs
    └── ria-layout-version

Beyond datasets, the RIA store only contains the directory ``error_logs``
for error logging and the file ``ria-layout-version`` for a specification of the
dataset tree layout in the store (last two lines in the code block above).
If a second dataset gets published to the RIA store, it will be represented in a
similar tree structure under its dataset ID. Note that subdatasets are not
represented *underneath* another dataset, but are stored on the same hierarchy
level as their superdataset in the RIA store.
With this setup, the location of a particular dataset in the RIA store is only
dependent on its :term:`dataset ID`. As the dataset ID is universally unique,
gets assigned to a dataset at the time of creation, and does not change across
the life time of a dataset, no two different datasets could have the same location
in a RIA store.

.. findoutmore:: What about the ID if it is a git-annex repository?

   If you want to store :term:`git-annex` repositories in a RIA store, the repository
   will not have a dataset ID. Instead, the repository will be identified by its
   :term:`annex UUID` in the store. This is ID is also universally unique, but unlike
   :term:`dataset ID`\s, each repository clone will have a different :term:`annex UUID`.
   Thus, while datasets can be identified across their entire lifetime, flavors,
   and clones, each clone of a git-annex repository will get a new :term:`annex UUID`.

The directory underneath the two dataset ID based subdirectories contains a
*bare git repository* that is a clone of the dataset.

.. findoutmore:: What is a bare Git repository?

   Bare repositories are the contents of the ``.git`` directory  of regular
   DataLad datasets or Git/git-annex repositories. They are typically used as
   *remote* repositories to *share* repositories among several people and make
   collaborative workflows possible. As a bare Git repository is the contents of
   the ``.git`` directory, it does not contain a *working tree* (the directory tree
   of files you can see or edit in a regular repository or dataset) or *checkout*
   (a pointer to a specific state of the repository). Because of this, no-one can work
   inside of a bare repository -- modifications to files or the repository require
   a working tree. However, bare repositories can be cloned, pulled from, and
   pushed to, and thus enable collaboration.

   In a collaborative Git/git-annex/DataLad workflow, one commonly creates a bare
   repository in a centralized place (such as a RIA store, but also -- you
   guessed it -- :term:`GitHub` or :term:`GitLab`) and lets others clone
   repositories, pull updates, or push their changes to them.
   Thus, you are already familiar with bare Git repositories, you may just not
   have been aware. Whenever you publish a dataset to GitHub, it is the ``.git``
   directory that will be transferred to GitHub's server. Whenever you clone a
   dataset, regardless of whether you clone it from GitHub, another hosting service,
   or a file path, it is a ``.git`` directory that is copied to your machine.

   At this point, you may be confused about the fact that all repositories
   that GitHub/GitLab hosts are bare Git repositories, but that it appears as if
   repositories on GitHub or GitLab -- unlike the bare repositories in a RIA
   store that you have seen -- retain their directory hierarchy and their file
   names, or that edits directly within GitHubs interface are possible, as if
   those repositories would actually have a working tree:
   GitHub's/GitLab's web-interface creates a *representation* of the repository content
   and a *temporary* working tree to modify files directly from the web UI that
   enables browsing and modifying file content. If you would push a bare
   repository from a RIA store to GitHub/GitLab, it would also be represented with the
   file and directory hierarchy of the original dataset.

   Apart from enabling collaboration (a bare repository is required if you want to push to
   it at all times), bare repositories have further advantages: Because they
   do not contain a working tree or checkout, the repositories are leaner, and it
   is easier for administrators to perform garbage collections and maintenance.
   If you are interested in finding out more, you can read up on bare repositories
   and how to use them
   `here <https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a
   -Server>`_.


Inside of the bare :term:`Git` repository, the ``annex`` directory -- just as in
any standard dataset or repository -- contains the dataset's keystore (object
tree) under ``annex/objects`` [#f2]_. In conjunction, keystore and bare Git
repository are the original dataset -- just differently represented, with no
*working tree*, i.e., directory hierarchy that exists in the original dataset,
and without the name it was created under, but stored under its dataset ID.

If necessary, the keystores can be (compressed) `7zipped <https://www.7-zip.org/>`_
(``archives/``), either for compression gains, or for use on HPC-systems with
`inode <https://en.wikipedia.org/wiki/Inode>`_ limitations.
Despite being 7zipped, those archives could be indexed and support
relatively fast random read access. Thus, the entire key store be put into an
archive, re-using the exact same directory structure, and remains fully
accessible while only using a handful of inodes, regardless of file number and size.

On an infrastructural level, a RIA store is fully self-contained, and is a plain
file system storage, not a database. It can be set up on any infrastructure that
a dataset can be created on, with only few additional software requirements.

.. findoutmore:: Software Requirements

   .. todo::

      @mih, @bpoldrack: please check!

   - git-annex version 7.20 or newer
   - DataLad version 0.12.3 (or later)
   - Server side: 7z needs to be in the path.
   - Only relevant for the application at hand: The ``cfg_inm7`` run procedure as provided with
     ``pip install git+https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad.git``


**Advantages of RIA stores**

Storing datasets in RIA stores has a number of advantages that align well with
the demands of large datasets and scientific compute infrastructure, but are also
well suited for most back-up and storage applications.
In a RIA store layout, the first two levels of subdirectories can host any
number of keystores and bare repositories. As datasets are identified via ID and
stored *next to eachother* underneath the top-level RIA store directory, the
store is completely flexible and extendable, and regardless of the number or
nature of datasets inside of the store, a RIA store keeps a homogeneous directory
structure. This aids the handling of large numbers of repositories, because
unique locations are derived from *dataset/repository properties* (their ID)
rather than a dataset name or a location in a complex dataset hierarchy.
Because the dataset representation in the RIA store is a bare repository,
"house-keeping" as well as query tasks can be automated or performed by data
management personnel with no domain-specific knowledge about dataset contents.
Short maintenance scripts can be used to automate basically any task that is
of interest and possible in a dataset, but across the full RIA store.
A few examples are:

- Copy or move annex objects into a 7z archive.
- Find dataset dependencies across all stored datasets by returning the dataset
  IDs of subdatasets recorded in each dataset.
- Automatically return the number of commits in each repository.
- Automatically return the author and time of the last dataset update.
- Find all datasets associated with specific authors.
- Clean up unnecessary files and minimize a (or all) repository with :term:`Git`\s
  `garbage collection (gc) <https://git-scm.com/docs/git-gc>`_ command.

If all datasets of an institute are kept in a single RIA store, questions such
as "Which projects use this data as their input?", "In which projects was the
student with this Git identity involved?", "Give me a complete research log
of what was done for this publication", or "Which datasets weren't used in the
last 5 years?" can be answered automatically with Git tools, without requiring
expert knowledge about the contents of any of the datasets, or access to the
original creators of the dataset.

**git-annex ria-remote special remotes**

On a technical level, beyond being a tree of datasets, a RIA store is by default
a :term:`git-annex` `ria-remote special remote <https://libraries.io/pypi/ria-remote>`_.

.. findoutmore:: What is a special remote?

   A `special-remote <https://git-annex.branchable.com/special_remotes/>`_ is an
   extension to Git's concept of remotes, and can enable git-annex to transfer
   data to and from places that are not Git repositories (e.g., cloud services
   or external machines such as an HPC system). Don't envision a special-remote as a
   physical place or location -- a special-remote is just a protocol that defines
   the underlying *transport* of your files *to* and *from* a specific location.

The git-annex ria-remote special remote is similar to git-annex's built-in
`directory <https://git-annex.branchable.com/special_remotes/directory/>`_
special remote, and results in the facts that regular git-annex key storage is
possible and that retrieval of keys from (compressed) 7z archives in the RIA
store works.

Certain applications will not require special remote features. The usecase

.. todo::

   link HCP usecase

shows an example where git-annex key storage is explicitly not wanted. For most
storage or back-up scenarios, special remote capabilities are useful, though,
and thus the default [#f4]_.
The :command:`datalad create-sibling-ria` command will automatically create a
dataset representation in a RIA store (and set up the RIA store, if it does not
exist), and configure a sibling to allow publishing to the RIA store and updating
from it.
With special remote capabilities enabled, the command will create a second
sibling to the git-annex special remote. With these two siblings set up, upon an
invocation of :command:`datalad publish --to <sibling> --transfer-data all`,
the complete dataset contents, including annexed contents, will be published
to the RIA store, with no further setup or configuration required [#f5]_.

RIA store workflows
"""""""""""""""""""

.. index:: ! datalad command; create-sibling-ria

A RIA store can be created or extended by running the :command:`datalad create-sibling-ria`
command (:manpage:`datalad-create-sibling-ria` manual) in an existing dataset.
Supply a sibling name of your choice with the ``-s/--sibling`` option, and specify
the location of the store as a ``ria+`` URL. Beyond this, there are no further
required arguments.

.. findoutmore:: What about optional arguments?

   - unless it is explicitly given via ``--ria-remote-name``, the sibling to the
     ria-remote special remote will have the same sibling name suffixed with ``-ria``.
   - Special remote capabilities of a RIA store can be disabled at the time of
     RIA store creation by using the option ``--no-ria-remote``
   - :term:`Permissions` in the RIA store can be configured via ``--shared``. It
     will default to multi-user access, but can take any specification of
     the :command:`git init --shared` argument (find out more in the
     `documentation <https://git-scm.com/docs/git-init>`__ of the command).


RIA stores can be used under different types of file transfer protocols.
Depending on the file transfer protocol, the looks of the URL can differ:

- :term:`SSH`: ``ria+ssh://[user@]hostname:/absolute/path/to/ria-store``
- Local file system: ``ria+file:///absolute/path/to/ria-store``
- :term:`http` (e.g., to a RIA store like `store.datalad.org <http://store.datalad.org/>`_):
  ``ria+http://store.datalad.org:/absolute/path/to/ria-store``

Note that it is required to specify an :term:`absolute path` in the URL. Here is
how one could create two siblings, ``server_juseless`` and ``server_juseless-ria``,
to a RIA store (which can, but does not need to exist yet) on an :term:`SSH server`
from within an existing dataset:

.. code-block:: bash

   $ datalad create-sibling-ria -s server_juseless \
     ria+ssh://user@juseless.inm7.de:/home/user/scratch/myriastore
   [INFO   ] create siblings 'server_juseless' and 'server_juseless-ria' ...
   [INFO   ] Fetching updates for <Dataset path=/tmp/my_dataset>
   [INFO   ] Configure additional publication dependency on "server_juseless-ria"
   create-sibling-ria(ok): /tmp/my_dataset (dataset)

   $ datalad siblings
    .: here(+) [git]
    .: server_juseless(-) [ (git)]
    .: server_juseless-ria(+) [ria]

Once the siblings to the RIA store are created, a
:command:`datalad publish --to <sibling> --transfer-data all` publishes the
dataset to the RIA store. With git-annex special remote capabilities enabled as
in the example above, annexed contents will be published automatically.

To clone a dataset from the RIA store, the RIA URL needs to be passed to the
:command:`datalad clone` command, following a similar scheme as outlined above:

- A ``ria+`` identifier for a RIA URL, followed by a protocol specification and
  a path to the RIA store (identical to the URL before).
- A ``#`` sign,
- The :term:`dataset ID`,
- (Optionally) a ``@`` followed by a version identifier such as a tag or a branch
  name.

Here is how to clone a dataset with the ID ``1d368e0a-439e-11ea-b341-d0c637c523bc``
in the version identified by the tag ``ready4analysis`` from a RIA store on an
SSH server:

.. code-block:: bash

   $ datalad clone \
     ria+ssh://user@juseless.inm7.de/home/user/scratch/myriastore#1d368e0a-439e-11ea-b341-d0c637c523bc@ready4analysis \
     mydataset

.. note::

   When cloning from a RIA store with a RIA URL, the optional path with a dataset
   name becomes more important than usually. It is still optional, but without
   an explicit target dataset name (``mydataset``), the clone would be called
   ``1d368e0a-439e-11ea-b341-d0c637c523bc``.

.. findoutmore:: On cloning datasets with subdatasets from RIA stores

   The usecase

   .. todo::

      link HCP usecase

   details a RIA-store based publication of a large dataset, split into a nested
   dataset hierarchy with about 4500 subdatasets in total. But how can links to
   subdatasets work, if datasets in a RIA store are stored in a flat hierarchy,
   with no nesting?

   The key to this lies in flexibly regenerating subdataset's URLs based on their
   ID and a path to the RIA store. The :command:`datalad get` command is
   capable of generating RIA URLs to subdatasets on its own, if the higher level
   dataset containts a ``datalad get`` configuration on ``subdataset-source-candidate-origin``
   that points to the RIA store the subdataset is published in. Here is how the
   ``.datalad/config`` configuration looks like for the top-level dataset of the
   `HCP dataset <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_::

      [datalad "get"]
          subdataset-source-candidate-origin = "ria+http://store.datalad.org#{id}"

   With this configuration, a :command:`datalad get` can use the URL and insert
   the dataset ID in question into the ``{id}`` placeholder to clone directly
   from the RIA store.

   The configuration either needs to be done by hand with a :command:`git config`
   command [#f6]_, or exists automatically in ``.git/config`` if the dataset is
   cloned from a RIA store.

**Configurations can hide the technical layers**

Setting up a RIA store and appropriate siblings is fairly easy -- it requires
only the :command:`datalad create-sibling-ria` command.
However, in the institute this usecase describes, in order to spare users
knowing about RIA stores, custom configurations are distributed via DataLad's
run-procedures to simplify workflows further and hide the technical layers of
the RIA setup:

A `custom procedure <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_
performs the relevant sibling setup with a fully configured link to the RIA store,
and, on top of it, also creates an associated repository with a publication
dependency on the RIA store to an institute's GitLab instance [#f3]_.
With a procedure like this in place system-wide, an individual researcher only
needs to call the procedure right at the time of dataset creation, and have a
fully configured and set up analysis dataset afterwards:

.. code-block:: bash

   $ datalad create -c inm7 <PATH>

Working in this dataset will require only :command:`datalad save` and
:command:`datalad publish` commands, and configurations ensure that the projects
history and results are published where they need to be: The RIA store, for storing
and archiving the project including data, and GitLab, for exposing the projects
progress to the outside and ease collaboration or supervision. Users do not need
to know the location of the store, its layout, or how it works -- they can go
about doing their science, while DataLad handles publications routines.

In order to get input data from datasets hosted in the datastore without requiring
users to know about dataset IDs or construct ``ria+`` URLs, RIA store hosted
datasets get a :term:`sibling` on :term:`GitLab` or :term:`GitHub` with their
human readable name.
Users can clone the datasets from the web hosting service, and obtain data
via :command:`datalad get`. While :command:`datalad get` will retrieve file
or subdataset contents from the RIA store, users will not need to bother where
the data actually comes from.

Summary
"""""""

The infrastructural and workflow changes around DataLad datasets in RIA stores
improve the efficiency of the institute:

With easy local version control workflows and DataLad-based data management routines,
researchers are able to focus on science and face barely any technical overhead for
data management. As file content for analyses is obtained *on demand*
via :command:`datalad get`, researchers selectively obtain only those data they
need instead of having complete copies of datasets as before, and thus save disk
space. Upon :command:`datalad publish`, computed results and project histories
can be pushed to the data store and the institute's GitLab instance, and be thus
backed-up and accessible for collaborators or supervisors. Easy-to-reobtain input
data can safely be dropped to free disk space on the compute cluster. Sensible
incentives for computing and limitations on disk space prevent unmanaged clutter.
With a RIA store full of bare git repositories, it is easily maintainable by data
stewards or system administrators. Common compression or cleaning operations of
Git and git-annex are performed without requiring knowledge about the data
inside of the store, as are queries on interesting aspects of datasets, potentially
across all of the datasets of the institute.
With a remote data store setup, the compute cluster is efficiently used for
computations instead of data storage. Researchers can not only compute their
analyses faster and on larger datasets than before, but with DataLad's version
control capabilities their work also becomes more transparent, open, and
reproducible.


.. rubric:: Footnotes

.. [#f1]  The two-level structure (3 ID characters as one subdirectory, the
          remaining ID characters as the next subdirectory) exists to avoid exhausting
          file system limits on the number of files/folders within a directory.

.. [#f2] To re-read about how git-annex's object tree works, check out section
         :ref:`symlink`, and pay close attention to the hidden section.
         Additionally, you can find much background information in git-annex's
         `documentation <https://git-annex.branchable.com/internals/>`_.

.. [#f3] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on GitLab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_.

.. [#f4] Special remote capabilities of a RIA store can be disabled at the time of RIA
         store creation by passing the option ``--no-ria-remote`` to the
         :command:`datalad create-sibling-ria` command.

.. [#f5] To re-read about publication dependencies and why this is relevant to
         annexed contents in the dataset, checkout section :ref:`sharethirdparty`.

.. [#f6] To re-read on configuring datasets with the :command:`git config`, go
         back to sections :ref:`config` and :ref:`config2`.
