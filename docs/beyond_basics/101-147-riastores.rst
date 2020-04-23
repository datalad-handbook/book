.. _riastore:

Remote Indexed Archives for dataset storage and backup
------------------------------------------------------

If DataLad datasets should be backed-up, made available for collaborations
with others, or stored in a central location or on systems that do not have
DataLad installed, :term:`remote indexed archive (RIA) store`\s may be a suitable
solution.


Put simply, a RIA store is a dataset storage location that allows for access to
and collaboration on DataLad datasets. On a more technical level, RIA stores
are flat, file-system based repository representations (i.e., no data base involved)
of any number of datasets. These stores can be flexibly
extended with new datasets, and the dataset representation is independent of
static dataset names or directory hierarchies. RIA stores can (as a whole or
in parts) be (automatically) maintained or queried: Within a RIA store, it is
possible to perform (automated) searches for dataset dependencies, or do any query that Git
allows across a range of datasets without requiring expert or domain knowledge about
the data inside of the datasets. Importantly, RIA stores do not require that
DataLad or git-annex are installed - it is possible to set up a RIA store on
a machine without a DataLad installation and publish datasets to or clone
datasets from the store onto a machine that has DataLad and its underlying tools
installed. The only requirements for a machine to host a RIA store are sufficient
disk space for the amount of datasets and potentially the program `7zip <https://www.7-zip.org/>`_.

The high-level workflow overview is as follows: Create a dataset,
use the :command:`datalad create-sibling-ria` command to establish a connection
to an either pre-existing or not-yet-existing RIA store, publish dataset contents
with :command:`datalad push`, (let others) clone the dataset from the
RIA store, and (let others) publish and pull updates. In the
case of large, institute-wide datasets, a RIA store (or multiple RIA stores)
can serve as a central storage location that enables fine-grained data access to
everyone who needs it, and as a storage and back-up location for all analyses datasets.

Technical details
^^^^^^^^^^^^^^^^^

Layout
""""""

The layout of a RIA store is a directory tree with datasets. The first level of
subdirectories in this tree consists of the first three characters of the
:term:`dataset ID`, and the second level of subdatasets contains the remaining
characters of the dataset ID.
Thus, the first two levels of subdirectories in the tree are split
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
for error logging and the file ``ria-layout-version`` [#f2]_ for a specification of the
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

The directory underneath the two dataset ID based subdirectories contains a
*bare git repository* that is a clone of the dataset.

.. findoutmore:: What is a bare Git repository?

   A bare Git repository is a repository that contains the contents of the ``.git``
   directory of regular DataLad datasets or Git repositories, but no worktree
   or checkout. This has advantages: The repository is leaner, it is easier
   for administrators to perform garbage collections, and it is required if you
   want to push to it at all times. You can find out more on what bare repositories
   are and how to use them
   `here <https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server>`__.

Inside of the bare :term:`Git` repository, the ``annex`` directory -- just as in
any standard dataset or repository -- contains the dataset's keystore (object
tree) under ``annex/objects`` [#f3]_. In conjunction, keystore and bare Git
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
a dataset can be created on, with only few additional software requirements (see
below), and access to datasets can be managed by using file system :term:`permissions`.
With these attributes, a RIA store is a suitable solution for a number of
usecases (back-up, single or multi-user dataset storage, central point for
collaborative workflows, ...), be that on private workstations, webservers,
compute clusters, or other IT infrastructure.

.. findoutmore:: Software Requirements

   On the server side, only 7z is to be installed, if desired. Specifically, no
   git, no git-annex, and no otherwise running daemons are necessary.
   If the RIA store is setup remotely, the server needs to be SSH-accessible.

   On the client side, you need DataLad version 0.12.3 (or later; has the
   :command:`create-sibling-ria` command and the git-annex ria-remote special remote).
   Alternatively, DataLad version 0.12.2 and a stand-alone installation of
   `git-annex-ria-remote <https://github.com/datalad/git-annex-ria-remote>`_
   works.

git-annex ORA-remote special remotes
""""""""""""""""""""""""""""""""""""

On a technical level, beyond being a directory tree of datasets, a RIA store
is by default a :term:`git-annex` ORA-remote (optional remote access) special remote
of a dataset. This allows to not only store the history of a dataset, but also
all annexed contents.

.. findoutmore:: What is a special remote?

   A `special-remote <https://git-annex.branchable.com/special_remotes/>`_ is an
   extension to Git's concept of remotes, and can enable git-annex to transfer
   data to and from places that are not Git repositories (e.g., cloud services
   or external machines such as an HPC system). Don't envision a special-remote as a
   physical place or location -- a special-remote is just a protocol that defines
   the underlying *transport* of your files *to* and *from* a specific location.

The git-annex ora-remote special remote is referred to as a "storage sibling" of
the original dataset. It is similar to git-annex's built-in
`directory <https://git-annex.branchable.com/special_remotes/directory/>`_
special remote (but works remotely and uses the ``hashdir_mixed`` [#f2]_ keystore
layout), and results in the facts that regular git-annex key storage is
possible and that retrieval of keys from (compressed) 7z archives in the RIA
store works.

Certain applications will not require special remote features. The usecase
:ref:`usecase_HCP_dataset`
shows an example where git-annex key storage is explicitly not wanted. For most
storage or back-up scenarios, special remote capabilities are useful, though,
and thus the default [#f5]_.
The :command:`datalad create-sibling-ria` command will automatically create a
dataset representation in a RIA store (and set up the RIA store, if it does not
exist), and configure a sibling to allow publishing to the RIA store and updating
from it.
With special remote capabilities enabled, the command will automatically create
and link the git-annex special remote. With the sibling and special remote set up,
upon an invocation of :command:`datalad push --to <sibling>`,
the complete dataset contents, including annexed contents, will be published
to the RIA store, with no further setup or configuration required [#f6]_.

Advantages of RIA stores
""""""""""""""""""""""""
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

The usecase :ref:`usecase_datastore` demonstrates the advantages of this in a
large scientific institute.
Due to the git-annex ora-remote special remote, datasets can be exported and
stored as archives to save disk space.

.. todo::

   link to ukb chapter as example

RIA store workflows
^^^^^^^^^^^^^^^^^^^

.. index:: ! datalad command; create-sibling-ria

A RIA store can be created or extended by running the :command:`datalad create-sibling-ria`
command (:manpage:`datalad-create-sibling-ria` manual) in an existing dataset.
Supply a sibling name of your choice with the ``-s/--sibling`` option, and specify
the location of the store as a ``ria+`` URL. Beyond this, there are no further
required arguments.

.. findoutmore:: What about optional arguments?

   - unless it is explicitly given via ``--ria-remote-name``, the
     ria-remote special remote will have the same sibling name suffixed with ``-ria``.
   - Special remote capabilities of a RIA store can be disabled at the time of
     RIA store creation by using the option ``--no-storage-sibling``
   - :term:`Permissions` in the RIA store can be configured via ``--shared``. It
     will default to multi-user access, but can take any specification of
     the :command:`git init --shared` argument (find out more in the
     `documentation <https://git-scm.com/docs/git-init>`__ of the command).

RIA stores can be used under different types of file transfer protocols.
Depending on the file transfer protocol, the looks of the ``ria+`` URL can differ:

- :term:`SSH`: ``ria+ssh://[user@]hostname:/absolute/path/to/ria-store``
- Local file system: ``ria+file:///absolute/path/to/ria-store``
- :term:`http` (e.g., to a RIA store like `store.datalad.org <http://store.datalad.org/>`_):
  ``ria+http://store.datalad.org:/absolute/path/to/ria-store``

Note that it is required to specify an :term:`absolute path` in the URL. Here is
how one could store a dataset in a RIA store (which can, but does not need to
exist yet) on an :term:`SSH server` from within an existing dataset:

.. code-block:: bash

   $ datalad create-sibling-ria -s server_backup \
     ria+ssh://user@some.server.edu:/home/user/scratch/myriastore
   [INFO   ] create siblings 'server_backup' and 'server_backup-ria' ...
   [INFO   ] Fetching updates for <Dataset path=/tmp/my_dataset>
   [INFO   ] Configure additional publication dependency on "server_backup-ria"
   create-sibling-ria(ok): /tmp/my_dataset (dataset)

   $ datalad siblings
    .: here(+) [git]
    .: server_backup(-) [ (git)]
    .: server_backup-ria(+) [ria]

The sibling name of the store in the example above is ``server_backup``, and
the link to its storage sibling was automatically named
``server_backup-ria``.

.. todo::

   Check whether this naming is still the case after the RF

Once the sibling to the RIA store and the special remote link to the RIA store
are created, a :command:`datalad push --to <sibling>`
publishes the dataset to the RIA store. With the git-annex special remote
capabilities enabled as in the example above, annexed contents will be published
automatically.

To clone a dataset from the RIA store, the RIA URL needs to be passed to the
:command:`datalad clone` command, following a similar scheme as outlined above:

- A ``ria+`` identifier for a RIA URL, followed by a protocol specification and
  a path to the RIA store (identical to the URL before).
- A ``#`` sign,
- The :term:`dataset ID`,
- (Optionally) a ``@`` followed by a version identifier such as a tag or a branch
  name.

Here is how to clone a dataset with the ID ``1d368e0a-439e-11ea-b341-d0c637c523bc``
in the version identified by the tag ``ready4analysis`` from a RIA store on a
webserver:

.. code-block:: bash

   $ datalad clone \
     ria+http://store.datalad.org#d1ca308e-3d17-11ea-bf3b-f0d5bf7b5561@ready4analysis \
     mydataset

.. note::

   When cloning from a RIA store with a RIA URL, the optional path with a dataset
   name becomes more important than usually. It is still optional, but without
   an explicit target dataset name (``mydataset``), the clone would be called
   ``1d368e0a-439e-11ea-b341-d0c637c523bc``.

.. todo::

   This should be outdated by the time the refactoring is done.
   Update

Be aware of one caveat:
If the RIA store has special remote capabilities, depending on whether a RIA
store is created and used over the same protocol or not, or if URLs with
user names or other individual information were used, additional configurations
may be necessary to ensure that not only cloning datasets from the store, but
also *file retrieval* from the special remote afterwards is functional.
Problems that can arise with this stem from :term:`git-annex`\'s internal
representation of the special remote that is constructed once the RIA siblings
are created. While the problem seems obvious once known and relates to mismatching
protocol or log-in specifications for file retrieval, finding it can be tedious
as it is hidden in :term:`git-annex` internal files. To find out more about
this, check out the hidden section below.

.. findoutmore:: Configuring appropriate protocols, store locations, or log-ins for special remote access

   At the time of the creation of the ``-ria`` sibling, the ``ria+`` URL specification
   is used by :term:`git-annex` to save availability-location information about
   all files that are published to the RIA store: :term:`git-annex`
   records where file contents are stored from the ``ria+`` URL used in the
   :command:`create-sibling-ria` command. At sibling creation, the ``ria+`` URL
   is resolved to a proper URL -- an http or SSH URL, or an absolute path, depending
   on whether the :term:`http`, :term:`ssh`, or file protocol is used in the
   ``ria+`` URL specification -- and stored in the file ``remote.log`` in the
   git-annex :term:`branch` of the repository.

   This information on file content location allows to retrieve files from the
   RIA store, and it is propagated into all clones of the dataset. Usually, this
   allows anyone to not only clone datasets, but also get their contents. If the
   protocol or -- in the case of an SSH protocol -- user name to an
   :term:`SSH server` does not apply to a specific user or clone, though,
   file retrieval from the special remote will be impossible.
   To illustrate how such a problem can arise, consider the following examples:

   1) A RIA store is set up on a shared compute cluster. A dataset gets published
   into the store via file protocol from a different location on the server. The
   URL about where file contents can be retrieved from will be an :term:`absolute path`
   on the server. If a dataset gets cloned from outside of the server
   (via SSH), the absolute path does not resolve on the new system and a
   :command:`datalad get` command fails.

   2) User Bob publishes a dataset to a RIA store on a shared :term:`SSH server`
   from his local machine. When specifying the ``+ria`` URL, he uses the SSH protocol,
   but needs to use his user name (bob@some.server.edu) to log in. When Alice
   clones Bob's dataset from the store to her local machine, she uses the correct
   protocol (SSH), but a :command:`datalad get` command tries to log into
   the server under Bob's user account, which fails.

   The information about the remote location is stored in the file ``remote.log``
   in the git-annex :term:`branch` of each dataset. We can take a look at it
   with the :command:`git cat-file` command. Below we exemplify how this would
   look to Alice in the example of user Bob, who created a RIA sibling on a
   shared server, but used his user name for login:

   .. code-block:: bash
      :emphasize-lines: 6

      git cat-file -p git-annex:remote.log
      d585ec1c-a8b9-4eb9-a276-4ffc4c645f81 \
      archive-id=ae5713fa-48ee-11ea-b341-d0c637c523bc \
      autoenable=true encryption=none externaltype=ria \
      name=backup_server-ria type=external \
      url=ria+ssh://bob@some.server.edu:/data/datasets/RIAstore timestamp=1581000354.064541765s

   In general, it is recommended to keep ``ria+`` URLs as generic and widely
   applicable as needed for the user base of the RIA store. However, in cases
   where some store serves a large number of repositories, and serves them with
   multiple access methods, and some users need to use different access methods,
   a configuration allows individual users to specify alternative URLs with
   the key ``url.<new_RIA_base>.insteadOf``::

      $ git config url."ria+ssh://bob@some.server.edu:/data/datasets/RIAstore".insteadOf "ria+ssh://alice@some.server.edu:/data/datasets/RIAstore"

   With this configuration, all URLs beginning with
   ``ria+ssh://bob@some.server.edu:/data/datasets/RIAstore`` will be dynamically
   rewritten to start with ``ria+ssh://alice@some.server.edu:/data/datasets/RIAstore``
   and allow Alice to retrieve files successfully.
   Thus, by configuring ``url.<base>.insteadOf``, URL mismatches can be fixed
   fast.


.. findoutmore:: On cloning datasets with subdatasets from RIA stores

   The usecase :ref:`usecase_HCP_dataset`
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
   command [#f7]_, or exists automatically in ``.git/config`` if the dataset is
   cloned from a RIA store.

**Configurations can hide the technical layers**

In order to spare users knowing about RIA stores, custom configurations can
be distributed via DataLad's run-procedures to simplify workflows further and
hide the technical layers of the RIA setup. Custom procedures could not only
perform a sibling setup in a RIA store, but also create an associated GitLab
repository with a publication dependency to the RIA store to ease publishing
data or cloning the dataset. The usecase :ref:`usecase_datastore` details the
setup of RIA stores in a scientific institute and demonstrates this example.

To ease repository access, the datasets stored in a RIA store can be installed
under human-readable names in a single superdataset. Cloning the superdataset
exposes the underlying datasets under a non-dataset-ID name.
User can thus get data from datasets hosted in a datastore without any
knowledge about the dataset IDs or the need to construct ``ria+`` URLs.
A concrete example for this is described in the usecase :ref:`usecase_HCP_dataset`.
While :command:`datalad get` will retrieve file or subdataset contents from the
RIA store, users will not need to bother where the data actually comes from.



.. rubric:: Footnotes

.. [#f1] The two-level structure (3 ID characters as one subdirectory, the
         remaining ID characters as the next subdirectory) exists to avoid exhausting
         file system limits on the number of files/folders within a directory.

.. [#f2] The ``ria-layout-version`` is important because it identifies whether
         the keystore uses git-annex's ``hashdirlower`` (git-annex's default for
         bare repositories) or ``hashdirmixed`` layout (which is necessary to
         allow symlinked annexes, relevant for :term:`ephemeral clone`\s). To read
         more about hashing in the key store, take a look at
         `the docs <https://git-annex.branchable.com/internals/hashing/>`_.

.. [#f3] To re-read about how git-annex's object tree works, check out section
         :ref:`symlink`, and pay close attention to the hidden section.
         Additionally, you can find much background information in git-annex's
         `documentation <https://git-annex.branchable.com/internals/>`_.

.. [#f4] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on GitLab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_.

.. [#f5] Special remote capabilities of a RIA store can be disabled at the time of RIA
         store creation by passing the option ``--no-ria-remote`` to the
         :command:`datalad create-sibling-ria` command.

.. [#f6] To re-read about publication dependencies and why this is relevant to
         annexed contents in the dataset, checkout section :ref:`sharethirdparty`.

.. [#f7] To re-read on configuring datasets with the :command:`git config`, go
         back to sections :ref:`config` and :ref:`config2`.
