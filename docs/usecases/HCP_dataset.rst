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
without circumventing or breaching the data providers terms.
In particular, it shows how ...

#. The :command:`datalad addurls` command is used to automatically aggregate
   files and information about their sources from public AWS S3 bucket storage
   into a small-sized, modular DataLad datasets.
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
MR scans from young healthy adult twins and non-twin siblings (ages 22-35)
using four imaging modalities: structural images (T1w and T2w), resting-state
fMRI (rfMRI), task-fMRI (tfMRI), and high angular resolution diffusion imaging
(dMRI). It further includes behavioral and other individual subject measure
data for all, and MEG data and 7T MR data for a subset of subjects (twin pairs).
In total, the data release encompasses around 80TB of data, and is of immense
value to the field o neuroscience.

Its large amount of data, however, also constitutes a data management challenge:
Such amounts of data are difficult to store, structure, access, and version
control. Even tools such as DataLad, and its foundations, :term:`Git` and
:term:`git-annex`, will struggle or fail with datasets of this size or number
of files. Simply transforming the complete data release into a single DataLad
dataset would at best lead to severe performance issues, but quite likely result
in software errors and crashes.
Moreover, access to the HCP data is dependent on consent to the
`data usage agreement <http://www.humanconnectomeproject.org/wp-content/uploads/2010/01/HCP_Data_Agreement.pdf>`_
of the HCP project and requires valid AWS S3 credentials. Instead of providing
unrestrained access to the HCP data via DataLad, an HCP DataLad dataset would
need to only enable data retrieval given the user complied to the HCP usage terms,
and instead of hosting data, it would need to reference the public S3 bucket so
that valid AWS credentials are required for data access.


The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Using the :command:`datalad addurls` command, the HCP data release is
aggregated into a lean top-level dataset with a large amount (N ~= 5000) of
subdatasets. The top-level dataset contains one subdataset per
subject with the subject's release notes. Within each subject's subdataset,
each additional available subdirectory is another subdataset.

This highly modular structure has multiple advantages. For one, it preserves
the original structure of the HCP data release, but allows to easily retrieve
data on a subject, modality, or file level. Secondly, with barely any data in
the superdataset, the top-level dataset is very lean. The only big thing
about it is an impressive ``.gitmodules`` file [#f1]_ with almost 1200 registered
subdatasets. The superdataset is published to :term:`GitHub` at
`github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_
to expose this superdataset and allow anyone to install it with a single
:command:`datalad clone` command.

In order to only simplify access to the data instead of providing data access
that could circumvent HCP license term agreements for users, DataLad does not
host any HCP data. Instead, thanks to :command:`datalad download-url`, each
data file knows its origin from the public AWS S3 bucket, and a
:command:`datalad get` will retrieve HCP data from this bucket.
With this setup, anyone who wants to obtain the
data will still need to consent to data usage terms and retrieve AWS credentials
from the HCP project, but can afterwards obtain the data with DataLad commands.

To authenticate prior to data retrieval, DataLad will prompt any user at the time
of the first :command:`datalad get` in the HCP dataset for their AWS credentials.
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

Beyond modularity and a lean superdataset, splitting the data release into several
thousand subdatasets also has performance advantages. If Git or Git annex
repositories exceed certain amounts of files (in size or file numbers), the
performance drops severely. By dividing the vast amount of data into many subdatasets,
this can be prevented.


Step-by-Step
^^^^^^^^^^^^

.. index:: ! datalad command; addurls

The :command:`datalad addurls` (:manpage:`datalad-addurls` manual) allows to create
(and update) DataLad datasets from a list of URLs.
By supplying a ``.csv`` file that contains an S3 download link, a subject ID,
a file name, and a version specification per file in the HCP dataset,
:command:`datalad addurls` can download these files and create datasets to
store them in. With the help of a few bash commands, this task can be
automated. If you are interested in the details of this, checkout the hidden
section below.

.. findoutmore:: Details of the datasets came to be

   - ask Tobias about this

As soon as files are retrieved and registered in the resulting datasets,
their content can be dropped again via :command:`datalad drop`: The origin
of the file was successfully recorded, and a :command:`datalad get` could
retrieve file contents on demand, if required. Shortly after a complete
download of the HCP project data, the datasets in which it has been
aggregated are small in size, and yet provide access to the HCP data.

Subsequently, the datasets are published to
`store.datalad.org <http://store.datalad.org/>`_, a remote indexed archive (RIA)
store. A RIA store contains datasets as bare git repositories, identified via
their :term:`dataset ID`.

.. todo::

   a store layout here

You can find more technical details on RIA stores in the use case
:ref:`usecase_datastore`.

- how does the data get into the RIA store? Why (to make the datasets publicly
  accessible)


.. rubric:: Footnotes

.. [#f1] If you want to read up on how DataLad stores information about
         registered subdatasets in ``.gitmodules``, checkout section :ref:`config2`.
