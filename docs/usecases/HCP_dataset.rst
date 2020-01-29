.. _usecase_HCP_dataset:

The HCP data as a dataset
-------------------------

This usecase outlines how a large data collection can be version controlled
and published in an accessible manner with DataLad in a remote indexed
archive (RIA) data store. Using the
`Human Connectome Project <http://www.humanconnectomeproject.org/>`_
(HCP) data as an example, it shows how large-scale datasets can be managed
with the help of modular nesting, and how access to data that is contingent on
usage agreements and external service credentials is possible via DataLad
without circumventing or breaching the data providers terms:

#. The :command:`datalad addurls` command is used to automatically aggregate
   files and information about their sources from public
   `AWS S3 <https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html>`_
   bucket storage into a small-sized, modular DataLad datasets.
#. Modular datasets are structured into a hierarchy of nested datasets, with a
   single HCP superdataset at the top. This modularizes storage and access,
   and mitigates performance problems that would arise in oversized standalone
   datasets, but maintains access to any subdataset from the top-level dataset.
#. Individual datasets are stored in an remote indexed archive (RIA) store
   at `store.datalad.org <store.datalad.org>`__ under their :term:`dataset ID`.
   This results in a flexible and scalable storage solution in which dataset
   locations are derived from their properties.
#. The top-level dataset is published to GitHub as a public access point for the
   full HCP dataset. As the RIA store only file availability and source
   information instead data contents, :command:`datalad get` retrieves file
   contents from the original AWS S3 sources.
#. With DataLad's authentication management, users will authenticate once -- and
   are thus required to accept the HCP projects terms to obtain valid
   credentials --, but subsequent :command:`datalad get` commands work swiftly
   without logging in.

The Challenge
^^^^^^^^^^^^^

The `Human Connectome Project <http://www.humanconnectomeproject.org/>`_ aims
to provide an unparalleled compilation of neural data through a customized
database. Its largest open access data collection is the
`WU-Minn HCP1200 Data <https://humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release/>`_.
It is made available via a public AWS S3 bucket and includes high-resolution 3T
`magnetic resonance <https://en.wikipedia.org/wiki/Magnetic_resonance_imaging>`_
scans from young healthy adult twins and non-twin siblings (ages 22-35)
using four imaging modalities: structural images (T1w and T2w),
`resting-state fMRI (rfMRI) <https://en.wikipedia.org/wiki/Resting_state_fMRI>`_,
task-fMRI (tfMRI), and high angular resolution
`diffusion imaging (dMRI) <https://en.wikipedia.org/wiki/Diffusion_MRI>`_.
It further includes behavioral and other individual subject measure
data for all, and `magnetoencephalography <https://en.wikipedia.org/wiki/Magnetoencephalography>`_
data and 7T MR data for a subset of subjects (twin pairs).
In total, the data release encompasses around 80TB of data, and is of immense
value to the field of neuroscience.

Its large amount of data, however, also constitutes a data management challenge:
Such amounts of data are difficult to store, structure, access, and version
control. Even tools such as DataLad, and its foundations, :term:`Git` and
:term:`git-annex`, will struggle or fail with datasets of this size or number
of files. Simply transforming the complete data release into a single DataLad
dataset would at best lead to severe performance issues, but quite likely result
in software errors and crashes.
Moreover, access to the HCP data is contingent on consent to the
`data usage agreement <http://www.humanconnectomeproject.org/wp-content/uploads/2010/01/HCP_Data_Agreement.pdf>`_
of the HCP project and requires valid AWS S3 credentials. Instead of hosting
this data or providing otherwise unrestrained access to it, an HCP
DataLad dataset would need to enable data retrieval from the original sources,
conditional on the user agreeing to the HCP usage terms.


The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Using the :command:`datalad addurls` command, the HCP data release is
aggregated into a large amount (N ~= 5000) of datasets. A lean top-level dataset
combines all datasets into a nested dataset hierarchy that recreates the original
HCP data releases structure. The topmost dataset contains one subdataset per
subject with the subject's release notes, and within each subject's subdataset,
each additional available subdirectory is another subdataset. This preserves
the original structure of the HCP data release, but builds it up from sensible
components that resemble standalone dataset units. As with any DataLad dataset,
dataset nesting and operations across dataset boundaries are seamless, and
allow to easily retrieve data on a subject, modality, or file level.

The highly modular structure has several advantages. For one, with barely any
data in the superdataset, the top-level dataset is very lean. It mainly consists
of an impressive ``.gitmodules`` file [#f1]_ with almost 1200 registered
(subject-level) subdatasets. The superdataset is published to :term:`GitHub` at
`github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_
to expose this superdataset and allow anyone to install it with a single
:command:`datalad clone` command in a few seconds.
Secondly, the modularity from splitting the data release into
several thousand subdatasets also has performance advantages. If :term:`Git` or
:term:`git-annex` repositories exceed certain a certain size (either in terms of
file sizes or the number of files), performance can drop severely [#f2]_.
By dividing the vast amount of data into many subdatasets,
this can be prevented, and it comes with no additional costs or difficulties,
as DataLad can work smoothly across subdatasets.


In order to only simplify access to the data instead of providing data access
that could circumvent HCP license term agreements for users, DataLad does not
host any HCP data. Instead, thanks to :command:`datalad addurls`, each
data file knows its source (the public AWS S3 bucket of the HCP project), and a
:command:`datalad get` will retrieve HCP data from this bucket.
With this setup, anyone who wants to obtain the data will still need to consent
to data usage terms and retrieve AWS credentials from the HCP project, but can
afterwards obtain the data solely with DataLad commands from the command line
or in scripts. Only the first :command:`datalad get`, requires authentication
with AWS credentials provided by the HCP project: DataLad will prompt any user at
the time of retrieval of the first file content of the dataset.
Afterwards, no further authentication is needed, unless the credentials become
invalid or need to be updated for other reasons.

Thus, in order to retrieve HCP data of up to single file level, users need to:

- :command:`datalad clone` the superdataset from :term:`GitHub`
  (`github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_)
- Create an account at http://db.humanconnectome.org to accept data use terms
  and obtain AWS credentials
- Use :command:`datalad get [-n] [-r] PATH` to retrieve file, directory, or
  subdataset contents on demand. Authentication is necessary only
  once (at the time of the first :command:`datalad get`).



Step-by-Step
^^^^^^^^^^^^

Dataset creation with ``datalad addurls``
"""""""""""""""""""""""""""""""""""""""""

.. index:: ! datalad command; addurls

The :command:`datalad addurls` command (:manpage:`datalad-addurls` manual)
allows to create (and update) DataLad datasets from a list of URLs.
By supplying a ``.csv`` file that contains an S3 download link, a subject ID,
a file name, and a version specification per file in the HCP dataset,
:command:`datalad addurls` can download these files and create datasets to
store them in. With the help of a few bash commands, this task can be
automated. If you are interested in the details of this, checkout the hidden
section below.

.. findoutmore:: Details of the datasets came to be

   ask Tobias about this
   - how was the original gigantic table created?
   - what determined subdataset names?
   - whats the hcp configuration for datalad create?

As soon as files are retrieved and registered in the resulting datasets,
their content can be dropped again via :command:`datalad drop`: The origin
of the file was successfully recorded, and a :command:`datalad get` could
retrieve file contents on demand, if required. Shortly after a complete
download of the HCP project data, the datasets in which it has been
aggregated are small in size, and yet provide access to the HCP data for anyone
who has valid AWS S3 credentials.

All of the dataset aggregation is done on a scientific compute cluster.
In this location, however, datasets would not be accessible to anyone without
an account on this system. Subsequently, therefore, the datasets are published
with :command:`datalad publish` to the publicly available
`store.datalad.org <http://store.datalad.org/>`_, a remote indexed archive (RIA)
store.

A Remote Indexed Archive Store
""""""""""""""""""""""""""""""

A RIA store contains datasets as bare git repositories, identified via
their :term:`dataset ID`.

.. todo::

   a store layout here

You can find more technical details on RIA stores in the use case
:ref:`usecase_datastore`. The major advantages of such a store are its
flexibility, scalability, and maintainability. Because datasets can be identified
with their universally unique ID, there is no need for static, filename-based
hierarchies. New datasets can be added to the store without consequences for
existing ones

.. todo::

    maybe contrast this to datasets.datalad.org).

As the store consists of bare git repositories (with optionally 7zipped archives
or annexes), it is easily maintainable by data stewards or system administrators.
Common compression or cleaning operations of Git and git-annex can be performed
without requiring knowledge about the data inside of the store.

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



.. rubric:: Footnotes

.. [#f1] If you want to read up on how DataLad stores information about
         registered subdatasets in ``.gitmodules``, checkout section :ref:`config2`.

.. [#f2] Precise performance will always be dependent on the details of the
         repository, software setup, and hardware, but to get a feeling for the
         possible performance issues in oversized datasets, imagine a mere
         :command:`git status` or :command:`datalad status` command taking several
         minutes up to hours in a clean dataset.