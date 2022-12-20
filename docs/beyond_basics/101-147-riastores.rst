.. _riastore:

Remote Indexed Archives for dataset storage and backup
------------------------------------------------------

If DataLad datasets should be backed-up, made available for collaborations
with others, or stored or managed in a central location,
:term:`remote indexed archive (RIA) store`\s, dataset storage
locations that allow for access to and collaboration on DataLad datasets, may be
a suitable solution. They are flat, flexible, file-system based repository
representations of any number of datasets, and they can exist on all standard computing
infrastructure, be it personal computers, servers or compute clusters, or even
super computing infrastructure -- even on machines that do not have DataLad
installed.

.. importantnote:: RIA availability

   Setting up and interacting with RIA stores requires DataLad version ``0.13.0``
   or higher.

   Note a breaking API change of :command:`create-sibling-ria` in DataLad versions ``>0.16.0``:
   A new store isn't set up unless ``--new-store-ok`` is passed.

   In order to understand this section, some knowledge on Git-internals
   and overcoming any fear of how checksums and UUIDs look can be helpful.

Technical details
^^^^^^^^^^^^^^^^^

RIA stores can be created or extended with a single command from within any
dataset. DataLad datasets can subsequently be published into the datastore as a
means of backing up a dataset or creating a dataset sibling to collaborate on
with others. Alternatively, datasets can be cloned and updated from a RIA store
just as from any other dataset location.
The subsection :ref:`riaworkflows` a few paragraphs down will demonstrate RIA-store
related functionality. But prior to introducing the user-facing commands, this
section starts by explaining the layout and general concept of a RIA store.

Layout
""""""

RIA stores store DataLad datasets. Both the layout of the RIA store and the layout
of the datasets in the RIA store are different from typical dataset layouts, though.
If one were to take a look inside of a RIA store as it is set up by default, one
would see a directory that contains a flat subdirectory tree with datasets
represented as :term:`bare Git repositories` and an annex. Usually, looking inside
of RIA stores is not necessary for RIA-related workflows, but it can help to
grasp the concept of these stores.

The first level of subdirectories in this RIA store tree consists of the first three
characters of the :term:`dataset ID`\s of the datasets that lie in the store,
and the second level of subdatasets contains the remaining characters of the
dataset IDs.
Thus, the first two levels of subdirectories in the tree are split
dataset IDs of the datasets that are stored in them [#f1]_. The code block below
illustrates how a single DataLad dataset looks like in a RIA store, and the
dataset ID of the dataset (``946e8cac-432b-11ea-aac8-f0d5bf7b5561``) is
highlighted:

.. code-block::
   :emphasize-lines: 2-3, 18-41

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

If a second dataset gets published to the RIA store, it will be represented in a
similar tree structure underneath its individual dataset ID.
If *subdatasets* of a dataset are published into a RIA store, they are not
represented *underneath* their superdataset, but are stored on the same hierarchy
level as any other dataset. Thus, the dataset representation in a RIA store is
completely flat [#f2]_.
With this hierarchy-free setup, the location of a particular dataset in the RIA
store is only dependent on its :term:`dataset ID`. As the dataset ID is universally
unique, gets assigned to a dataset at the time of creation, and does not change across
the life time of a dataset, no two different datasets could have the same location
in a RIA store.

The directory underneath the two dataset-ID-based subdirectories contains a
*bare git repository* (highlighted above as well) that is a :term:`clone` of the
dataset.

.. find-out-more:: What is a bare Git repository?

   A bare Git repository is a repository that contains the contents of the ``.git``
   directory of regular DataLad datasets or Git repositories, but no worktree
   or checkout. This has advantages: The repository is leaner, it is easier
   for administrators to perform garbage collections, and it is required if you
   want to push to it at all times. You can find out more on what bare repositories
   are and how to use them
   `here <https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server>`__.

   Note that bare Git repositories can be cloned, and the clone of a bare Git repository
   will have a checkout and a worktree, thus resuming the shape that you are
   familiar with.

Inside of the bare :term:`Git` repository, the ``annex`` directory -- just as in
any standard dataset or repository -- contains the dataset's keystore (object
tree) under ``annex/objects`` [#f3]_. In conjunction, keystore and bare Git
repository are the original dataset -- just differently represented, with no
*working tree*, i.e., directory hierarchy that exists in the original dataset,
and without the name it was created under, but stored under its dataset ID instead.

If necessary, the keystores (annex) can be (compressed) `7zipped <https://www.7-zip.org/>`_
archives (``archives/``), either for compression gains, or for use on HPC-systems with
`inode <https://en.wikipedia.org/wiki/Inode>`_ limitations [#f4]_.
Despite being 7zipped, those archives can be indexed and support
relatively fast random read access. Thus, the entire key store can be put into an
archive, re-using the exact same directory structure, and remains fully
accessible while only using a handful of inodes, regardless of file
number and size. If the dataset contains only annexed files, a complete dataset
can be represented in about 25 inodes.

Taking all of the above information together, on an infrastructural level,
a RIA store is fully self-contained, and is a plain file system storage, not a
database. Everything inside of a RIA store is either a file, a directory, or
a zipped archive. It can thus be set up on any infrastructure that has a file
system with directory and file representation, and has barely any additional
software requirements (see below). Access to datasets in the store can be managed
by using file system :term:`permissions`.
With these attributes, a RIA store is a suitable solution for a number of
usecases (back-up, single or multi-user dataset storage, central point for
collaborative workflows, ...), be that on private workstations, web servers,
compute clusters, or other IT infrastructure.

.. find-out-more:: Software Requirements

   On the RIA store hosting infrastructure, only 7z is to be installed, if the
   archive feature is desired. Specifically, no :term:`Git`, no :term:`git-annex`,
   and no otherwise running daemons are necessary.
   If the RIA store is set up remotely, the server needs to be SSH-accessible.

   On the client side, you need DataLad version 0.13.0 or later. Starting with
   this version, DataLad has the  :command:`create-sibling-ria` command and the
   git-annex ora-remote special remote that is required to get annexed dataset
   contents into a RIA store.

git-annex ORA-remote special remotes
""""""""""""""""""""""""""""""""""""

On a technical level, beyond being a directory tree of datasets, a RIA store
is by default a :term:`git-annex` ORA-remote (optional remote access) special remote
of a dataset. This allows to not only store the history of a dataset, but also
all annexed contents.

.. find-out-more:: What is a special remote?

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
layout). Thanks to the git-annex ora-remote, RIA stores can have regular
git-annex key storage and retrieval of keys from (compressed) 7z archives in
the RIA store works. Put simple, annexed contents of datasets can only be
pushed into RIA stores if they have a git-annex ora-remote.


Certain applications will not require special remote features. The usecase
:ref:`usecase_HCP_dataset`
shows an example where git-annex key storage is explicitly not wanted.
Other applications may require *only* the special remote, such as cases where Git isn't installed on the RIA store hosting infrastructure.
For most storage or back-up scenarios, special remote capabilities are useful, though,
and thus the default.

.. index:: ! datalad command; create-sibling-ria

The command :command:`datalad create-sibling-ria` can both create datasets in RIA stores and the RIA stores themselves.
With DataLad versions lower than ``0.16.0``, :command:`datalad create-sibling-ria` sets up a new RIA store if it does not find one under the provided URL, but starting with ``0.16.0``, one needs to pass the parameter ``--new-store-ok`` in order to set up a new store.
By default, the command will automatically create a dataset representation in a RIA store and configure a sibling to allow publishing to the RIA store and updating
from it.
With special remote capabilities enabled, the command will automatically create
the special remote as a ``storage-sibling`` and link it to the RIA-sibling.
With the sibling and special remote set up, upon an invocation of
:command:`datalad push --to <sibling>`, the complete dataset contents, including
annexed contents, will be published to the RIA store, with no further setup or
configuration required [#f6]_.

To disable the storage sibling completely, invoke :command:`datalad create-sibling-ria` with the argument ``--storage-sibling=off``.
Note that DataLad versions ``<0.14`` need to use the flag ``--no-storage-sibling``, which is deprecated starting with DataLad ``0.14.0``.
To create a RIA store with *only* special remote storage, starting from DataLad version ``0.14.0`` you can invoke :command:`datalad create-sibling-ria` with the argument ``--storage-sibling=only``.

Advantages of RIA stores
""""""""""""""""""""""""
Storing datasets in RIA stores has a number of advantages that align well with
the demands of central dataset management on shared compute infrastructure, but are also
well suited for most back-up and storage applications.
In a RIA store layout, the first two levels of subdirectories can host any
number of keystores and bare repositories. As datasets are identified via ID and
stored *next to each other* underneath the top-level RIA store directory, the
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
large scientific institute with central data management.
Due to the git-annex ora-remote special remote, datasets can be exported and
stored as archives to save disk space.

.. todo::

   link to ukb chapter as example

.. _riaworkflows:

RIA store workflows
^^^^^^^^^^^^^^^^^^^

The user facing commands for interactions with a RIA store are barely different
from standard DataLad workflows. The paragraphs below detail how to create and
populate a RIA store, how to clone datasets and retrieve data from it, and also
how to handle permissions or hide technicalities.

.. index:: ! datalad command; create-sibling-ria

Creating or publishing to RIA stores
""""""""""""""""""""""""""""""""""""

A dataset can be added into an existing or not yet existing RIA store by
running the :command:`datalad create-sibling-ria` command
(:manpage:`datalad-create-sibling-ria` manual), and subsequently published into
the store using :command:`datalad push`.
Just like the :command:`datalad siblings add` command,
for :command:`datalad create-sibling-ria`, an arbitrary sibling name
(with the ``-s/--name`` option) and a URL to the location of the store (as a
positional argument) need to be specified. In the case of RIA stores, the URL
takes the form of a ``ria+`` URL, and the looks of this URL are dependent
on where the RIA store (should) exists, or rather, which file transfer protocol
(``SSH`` or ``file``) is used:

- A URL to an :term:`SSH`\-accessible server has a ``ria+ssh://`` prefix, followed
  by user and hostname specification and an **absolute** path:
  ``ria+ssh://[user@]hostname:/absolute/path/to/ria-store``
- A URL to a store on a local file system has a ``ria+file://`` prefix,
  followed by an **absolute** path: ``ria+file:///absolute/path/to/ria-store``

.. find-out-more:: RIA stores with HTTP access

   Setting up RIA store with access via HTTP requires additional server-side configurations for Git.
   `Git's http-backend documentation <https://git-scm.com/docs/git-http-backend>`_ can point you the relevant configurations for your webserver and usecase.

Note that it is always required to specify an :term:`absolute path` in the URL!

In addition, as a convenience for cloning, you can supply an ``--alias`` parameter
with a name under which the dataset can later be cloned from the dataset.

.. importantnote:: If you code along, make sure to check the next findoutmore!

   The upcoming demonstration of RIA stores uses the ``DataLad-101`` dataset
   the was created throughout the Basics of this handbook.
   If you want to execute these code snippets on a ``DataLad-101``
   dataset you created, the modification described in the findoutmore below
   needs to be done first.

.. find-out-more:: If necessary, adjust the submodule path!

   Back in :ref:`subdspublishing`, in order to appropriately reference and link
   subdatasets on hostings sites such as :term:`GitHub`, we adjusted the
   submodule path of the subdataset in ``.gitmodules`` to point to a published
   subdataset on GitHub:

   .. runrecord:: _examples/DL-101-147-101
      :language: console
      :workdir: dl-101/DataLad-101
      :emphasize-lines: 9

      # in DataLad-101
      $ cat .gitmodules

   Later in this demonstration we would like to publish the subdataset to a
   RIA store and retrieve it automatically from this store -- retrieval is only
   attempted from a store, however, if no other working source is known. Therefore,
   we will remove the reference to the published dataset prior to this
   demonstration and replace it with the path it was originally referenced under.

   .. runrecord:: _examples/DL-101-147-102
      :language: console
      :workdir: dl-101/DataLad-101

      # in DataLad-101
      $ datalad subdatasets --contains midterm_project --set-property url ./midterm_project


To demonstrate the basic process, we will create a RIA store on a local file
system to publish the ``DataLad-101`` dataset from the handbook's "Basics"
section to. In the example below, the RIA sibling gets the name ``ria-backup``.
The URL uses the ``file`` protocol and points with an absolute path to the not
yet existing directory ``myriastore``.
When you are using DataLad version ``0.16`` or higher, make sure that the ``--new-store-ok`` parameter is set to allow the creation of a new store.


.. runrecord:: _examples/DL-101-147-103
   :language: console
   :workdir: dl-101/DataLad-101

   # inside of the dataset DataLad-101
   # do not use --new-store-ok with datalad < 0.16
   $ datalad create-sibling-ria -s ria-backup --alias dl-101 --new-store-ok "ria+file:///home/me/myriastore"

Afterwards, the dataset has two additional siblings: ``ria-backup``, and
``ria-backup-storage``.

.. runrecord:: _examples/DL-101-147-104
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad siblings

The storage sibling is the git-annex ora-remote and is set up automatically --
unless :command:`create-sibling-ria` is run with ``--storage-sibling=off`` (in DataLad versions ``>0.14.``) or ``--no-storage-sibling`` (in versions ``<0.14``).
By default, it has the name of the RIA sibling, suffixed with ``-storage``,
but alternative names can be supplied with the ``--storage-name`` option.



.. find-out-more:: Take a look into the store

    Right after running this command, a RIA store has been created in the specified
    location:

    .. runrecord:: _examples/DL-101-147-105
       :language: console
       :workdir: dl-101/DataLad-101

       $ tree /home/me/myriastore

    Note that there is one dataset represented in the RIA store. The two-directory
    structure it is represented under corresponds to the dataset ID of ``DataLad-101``:

    .. runrecord:: _examples/DL-101-147-106
       :language: console
       :workdir: dl-101/DataLad-101

       # The dataset ID is stored in .datalad/config
       $ cat .datalad/config

In order to publish the dataset's history and all its contents into the RIA store,
a single :command:`datalad push` to the RIA sibling suffices:

.. runrecord:: _examples/DL-101-147-107
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad push --to ria-backup

.. find-out-more:: Take another look into the store

    Now that dataset contents have been pushed to the RIA store, the bare repository
    contains them, although their representation is not human-readable. But worry
    not -- this representation only exists in the RIA store. When cloning this
    dataset from the RIA store, the clone will be in its standard human-readable
    format.

    .. runrecord:: _examples/DL-101-147-108
       :language: console
       :workdir: dl-101/DataLad-101
       :lines: 1-25, 38-

       $ tree /home/me/myriastore

A second dataset can be added and published to the store in the very same way.
As a demonstration, we'll do it for the ``midterm_project`` subdataset:

.. runrecord:: _examples/DL-101-147-109
   :language: console
   :workdir: dl-101/DataLad-101

   $ cd midterm_project
   $ datalad create-sibling-ria -s ria-backup ria+file:///home/me/myriastore

.. runrecord:: _examples/DL-101-147-110
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad push --to ria-backup

.. find-out-more:: Take a look into the RIA store after a second dataset has been added

    With creating a RIA sibling to the RIA store and publishing the contents of
    the ``midterm_project`` subdataset to the store, a second dataset has been
    added to the datastore. Note how it is represented on the same hierarchy
    level as the previous dataset, underneath its dataset ID (note that the output is cut off for readability):


    .. runrecord:: _examples/DL-101-147-111
       :language: console
       :workdir: dl-101/DataLad-101/midterm_project

       $ cat .datalad/config

    .. runrecord:: _examples/DL-101-147-112
       :language: console
       :workdir: dl-101/DataLad-101
       :lines: 1-25, 38-58

       $ tree /home/me/myriastore

Thus, in order to create and populate RIA stores, only the commands
:command:`datalad create-sibling-ria` and :command:`datalad push` are required.

.. index:: ! datalad command; clone

Cloning and updating from RIA stores
""""""""""""""""""""""""""""""""""""

Cloning from RIA stores is done via :command:`datalad clone` from a ``ria+`` URL,
suffixed with a dataset identifier.
Depending on the protocol being used, the URLs are composed similarly to during
sibling creation:

- A URL to a RIA store on an :term:`SSH`\-accessible server takes the
  same format as before: ``ria+ssh://[user@]hostname:/absolute/path/to/ria-store``
- A URL to a RIA store on a local file system also looks like during sibling
  creation: ``ria+file:///absolute/path/to/ria-store``
- A URL for read (without annex) access to a store via :term:`http` (e.g., to a RIA store like
  `store.datalad.org <http://store.datalad.org/>`_, through which the
  :ref:`HCP dataset is published <usecase_HCP_dataset>`) looks like this:
  ``ria+http://store.datalad.org:/absolute/path/to/ria-store``

The appropriate ``ria+`` URL needs to be suffixed with a ``#`` sign and a dataset
identifier. One way this can be done is via the dataset ID.
Here is how to clone the ``DataLad-101`` dataset from the RIA store using its
dataset ID:

.. runrecord:: _examples/DL-101-147-120
   :language: console
   :workdir: dl-101
   :realcommand: echo "$ datalad clone ria+file:///home/me/myriastore#$(datalad -C DataLad-101 -f'{infos[dataset][id]}' wtf) myclone" && datalad clone ria+file:///home/me/myriastore#$(datalad -C DataLad-101 -f'{infos[dataset][id]}' wtf) myclone

There are two downsides to this method: For one, it is hard to type, remember, and
know the dataset ID of a desired dataset. Secondly, if no additional path is given to
:command:`datalad clone`, the resulting dataset clone would be named after its ID.
An alternative, therefore, is to use an *alias* for the dataset. This is an
alternative dataset identifier that a dataset in a RIA store can be configured
with - either with a parameter at the time of running ``datalad create-sibling-ria``
as done above, or manually afterwards. For example, given that the dataset also has
an alias ``dl-101``, the above call would simplify to

.. code-block:: bash

   $ datalad clone ria+file:///home/me/myriastore#~dl-101

.. find-out-more:: Configure an alias for a dataset manually

   In order to define an alias for an individual dataset in a store, one needs
   to create an ``alias/`` directory in the root of the datastore and place
   a :term:`symlink` of the desired name to the dataset inside of it. Here is how it is
   done, for the midterm project dataset:

   First, create an ``alias/`` directory in the store, if it doesn't yet exist:

   .. runrecord:: _examples/DL-101-147-121
      :language: console
      :workdir: dl-101
      :realcommand: echo "$ mkdir /home/me/myriastore/alias"


   Afterwards, place a :term:`symlink` with a name of your choice to the dataset
   inside of it. Here, we create a symlink called ``midterm_project``:

   .. runrecord:: _examples/DL-101-147-122
      :language: console
      :workdir: dl-101
      :realcommand: echo "$ ln -s /home/me/myriastore/$(datalad -C DataLad-101/midterm_project -f'{infos[dataset][id]}' wtf | sed 's/^\(...\)\(.*\)/\1\/\2/') /home/me/myriastore/alias/midterm_project" && ln -s /home/me/myriastore/$(datalad -C DataLad-101/midterm_project -f'{infos[dataset][id]}' wtf | sed 's/^\(...\)\(.*\)/\1\/\2/') /home/me/myriastore/alias/midterm_project

   Here is how it looks like inside of this directory. You can see both the automatically created alias as well as the newly manually created one:

   .. runrecord:: _examples/DL-101-147-123
      :language: console
      :workdir: dl-101

      $ tree /home/me/myriastore/alias

   Afterwards, the alias name, prefixed with a ``~``, can be used as a dataset
   identifier:

   .. runrecord:: _examples/DL-101-147-124
      :language: console
      :workdir: dl-101

      datalad clone ria+file:///home/me/myriastore#~midterm_project

   This makes it easier for others to clone the dataset and will provide a sensible
   default name for the clone if no additional path is provided in the command.

   Note that it is even possible to create "aliases of an aliases" -- symlinking an existing alias-symlink (in the example above ``midterm_project``) under another name in the ``alias/`` directory is no problem.
   This could be useful if the same dataset needs to be accessible via several aliases, or to safeguard against common spelling errors in alias names.

The dataset clone is just like any other dataset clone. Contents stored in
:term:`Git` are present right after cloning, while the contents of annexed files
is not yet retrieved from the store and can be obtained with a :command:`datalad get`.

.. runrecord:: _examples/DL-101-147-125
   :language: console
   :workdir: dl-101

   $ cd myclone
   $ tree

To demonstrate file retrieval from the store, let's get an annexed file:

.. runrecord:: _examples/DL-101-147-126
   :language: console
   :workdir: dl-101/myclone

   $ datalad get books/progit.pdf


.. find-out-more:: What about creating RIA stores and cloning from RIA stores with different protocols

   Consider setting up and populating a RIA store on a server via the ``file``
   protocol, but cloning a dataset from that store to a local computer via
   ``SSH`` protocol. Will this be a problem for file content retrieval?
   No, in all standard situations, DataLad will adapt to this. Upon cloning
   the dataset with a different URL than it was created under,
   enabling the special remote will initially fail, but DataLad will adaptive
   try out other URLs (including changes in hostname, path, or protocol) to
   enable the ora-remote and retrieve file contents.

Just as expected, the subdatasets are not pre-installed. How will subdataset installation
work for datasets that exist in a RIA store as well, like ``midterm_project``?
Just as with any other subdataset! DataLad cleverly handles subdataset
installations from RIA stores in the background: The location of the subdataset
in the RIA store is discovered and used automatically:

.. runrecord:: _examples/DL-101-147-127
   :language: console
   :workdir: dl-101/myclone

   $ datalad get -n midterm_project

More technical insights into the automatic ``ria+`` URL generation are outlined
in the findoutmore below:

.. find-out-more:: On cloning datasets with subdatasets from RIA stores

   The usecase :ref:`usecase_HCP_dataset`
   details a RIA-store based publication of a large dataset, split into a nested
   dataset hierarchy with about 4500 subdatasets in total. But how can links to
   subdatasets work, if datasets in a RIA store are stored in a flat hierarchy,
   with no nesting?

   The key to this lies in flexibly regenerating subdataset's URLs based on their
   ID and a path to the RIA store. The :command:`datalad get` command is
   capable of generating RIA URLs to subdatasets on its own, if the higher level
   dataset contains a ``datalad get`` configuration on ``subdataset-source-candidate-origin``
   that points to the RIA store the subdataset is published in. Here is how the
   ``.datalad/config`` configuration looks like for the top-level dataset of the
   `HCP dataset <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_::

      [datalad "get"]
          subdataset-source-candidate-origin = "ria+http://store.datalad.org#{id}"

   With this configuration, a :command:`datalad get` can use the URL and insert
   the dataset ID in question into the ``{id}`` placeholder to clone directly
   from the RIA store.

   This configuration is automatically added to a dataset that is cloned from a
   RIA store, but it can also be done by hand with a :command:`git config`
   command [#f7]_.


Beyond straightforward access to datasets, RIA stores also allow very fine-grained
cloning operations: Datasets in RIA stores can be cloned in specific versions.

.. find-out-more:: Cloning specific dataset versions

   Optionally, datasets can be cloned in a specific version, such as a :term:`tag`
   or :term:`branch` by appending ``@<version-identifier>`` after the dataset ID
   or the dataset alias.
   Here is how to clone the `BIDS <https://bids.neuroimaging.io/>`_ version of the
   `structural preprocessed subset of the HCP dataset <https://github.com/datalad-datasets/hcp-structural-preprocessed>`_
   that exists on the branch ``bids`` of this dataset:

   .. code-block:: bash

      $ datalad clone ria+http://store.datalad.org#~hcp-structural-preprocessed@bids

   If you are interested in finding out how this dataset came into existence,
   checkout the use case :ref:`usecase_HCP_dataset`.

Updating datasets works with the :command:`datalad update` and :command:`datalad update --merge`
commands introduced in chapter :ref:`chapter_collaboration`. And because a
RIA store hosts :term:`bare Git repositories`, collaborating becomes
easy. Anyone with access can clone the dataset from the store, add changes, and
push them back -- this is the same workflow as for datasets hosted on sites such
as :term:`GitHub`, :term:`GitLab`, or :term:`Gin`.

Permission management
"""""""""""""""""""""

In order to limit access or give access to datasets in datastores, permissions can be set
at the time of RIA sibling creation with the ``--shared`` option.
If it is given, this option configures the permissions in the RIA store for
multi-users access. Possible values for this option are identical to those of
``git init --shared`` and are described in its
`documentation <https://git-scm.com/docs/git-init#Documentation/git-init.txt---sharedfalsetrueumaskgroupallworldeverybodyltpermgt>`__.
In order for the dataset to be accessible to everyone, for example, ``--shared all``
could be specified. If access should be limited to a particular Unix
`group <https://en.wikipedia.org/wiki/File_system_permissions#Traditional_Unix_permissions>`_
(``--shared group``), the group name needs to be specified with the
``--group`` option.


Configurations and tricks to hide technical layers
""""""""""""""""""""""""""""""""""""""""""""""""""

In setups with a central, DataLad-centric data management, in order to spare
users knowing about RIA stores, custom configurations can
be distributed via DataLad's run-procedures to simplify workflows further and
hide the technical layers of the RIA setup. For example, custom procedures provided
at dataset creation could automatically perform a sibling setup in a RIA store,
and also create an associated GitLab repository with a publication dependency to
the RIA store to ease publishing data or cloning the dataset.
The usecase :ref:`usecase_datastore` details the setup of RIA stores in a
scientific institute and demonstrates this example.

To simplify repository access beyond using aliases, the datasets stored in a RIA
store can be installed under human-readable names in a single superdataset.
Cloning the superdataset exposes the underlying datasets under a non-dataset-ID name.
Users can thus get data from datasets hosted in a datastore without any
knowledge about the dataset IDs or the need to construct ``ria+`` URLs, just as
it was done in the usecases :ref:`usecase_HCP_dataset` and :ref:`usecase_datastore`.
From a user's perspective, the RIA store would thus stay completely hidden.

Standard maintenance tasks by data stewards with knowledge about RIA stores and
access to it can be performed easily or even in an automated fashion. The
usecase :ref:`usecase_datastore` showcases some examples of those operations.

Summary
^^^^^^^

RIA stores are useful, lean, and undemanding storage locations for DataLad datasets.
Their properties make them suitable solutions to back-up, central data management,
or collaboration use cases. They can be set up with minimal effort, and the few
technical details a user may face such as cloning from :term:`dataset ID`\s can
be hidden with minimal configurations of the store like aliases or custom
procedures.


.. rubric:: Footnotes

.. [#f1] The two-level structure (3 ID characters as one subdirectory, the
         remaining ID characters as the next subdirectory) exists to avoid exhausting
         file system limits on the number of files/folders within a directory.

.. [#f2] Beyond datasets, the RIA store only contains the directory ``error_logs``
         for error logging and the file ``ria-layout-version`` for a specification of the
         dataset tree layout in the store (last two lines in the code block above).
         The ``ria-layout-version`` is important because it identifies whether
         the keystore uses git-annex's ``hashdirlower`` (git-annex's default for
         bare repositories) or ``hashdirmixed`` layout (which is necessary to
         allow symlinked annexes, relevant for :term:`ephemeral clone`\s). To read
         more about hashing in the key store, take a look at
         `the docs <https://git-annex.branchable.com/internals/hashing/>`_.

.. [#f3] To re-read about how git-annex's object tree works, check out section
         :ref:`symlink`, and pay close attention to the hidden section.
         Additionally, you can find a lot of background information in git-annex's
         `documentation <https://git-annex.branchable.com/internals/>`_.

.. [#f4] The usecase

         .. todo::

            Link UKBiobank on supercomputer usecase once ready

         shows how this feature can come in handy.

.. [#f6] To re-read about publication dependencies and why this is relevant to
         annexed contents in the dataset, checkout section :ref:`sharethirdparty`.

.. [#f7] To re-read on configuring datasets with the :command:`git config`, go
         back to sections :ref:`config` and :ref:`config2`.
