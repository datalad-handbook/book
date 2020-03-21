.. _usecase_HCP_dataset:

Scaling up: Managing 80TB and 15 million files from the HCP release
-------------------------------------------------------------------

.. index:: ! Usecase; Scaling up: 80TB and 15 million files

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
   bucket storage into small-sized, modular DataLad datasets.
#. Modular datasets are structured into a hierarchy of nested datasets, with a
   single HCP superdataset at the top. This modularizes storage and access,
   and mitigates performance problems that would arise in oversized standalone
   datasets, but maintains access to any subdataset from the top-level dataset.
#. Individual datasets are stored in a remote indexed archive (RIA) store
   at `store.datalad.org <http://store.datalad.org/>`__ under their :term:`dataset ID`.
   This setup constitutes a flexible, domain-agnostic, and scalable storage
   solution, while dataset configurations enable seamless automatic dataset
   retrieval from the store.
#. The top-level dataset is published to GitHub as a public access point for the
   full HCP dataset. As the RIA store contains datasets with only file source
   information instead of hosting data contents, a :command:`datalad get` retrieves
   file contents from the original AWS S3 sources.
#. With DataLad's authentication management, users will authenticate once -- and
   are thus required to accept the HCP projects terms to obtain valid
   credentials --, but subsequent :command:`datalad get` commands work swiftly
   without logging in.

The Challenge
^^^^^^^^^^^^^

.. index:: ! Human Connectome Project (HCP)

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
In total, the data release encompasses around 80TB of data in 15 million files,
and is of immense value to the field of neuroscience.

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
aggregated into a large amount (N ~= 4500) of datasets. A lean top-level dataset
combines all datasets into a nested dataset hierarchy that recreates the original
HCP data release's structure. The topmost dataset contains one subdataset per
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
several thousand subdatasets has performance advantages. If :term:`Git` or
:term:`git-annex` repositories exceed a certain size (either in terms of
file sizes or the number of files), performance can drop severely [#f2]_.
By dividing the vast amount of data into many subdatasets,
this can be prevented: Subdatasets are small-sized units that are combined to the
complete HCP dataset structure, and nesting comes with no additional costs or
difficulties, as DataLad can work smoothly across hierarchies of subdatasets.

In order to simplify access to the data instead of providing data access
that could circumvent HCP license term agreements for users, DataLad does not
host any HCP data. Instead, thanks to :command:`datalad addurls`, each
data file knows its source (the public AWS S3 bucket of the HCP project), and a
:command:`datalad get` will retrieve HCP data from this bucket.
With this setup, anyone who wants to obtain the data will still need to consent
to data usage terms and retrieve AWS credentials from the HCP project, but can
afterwards obtain the data solely with DataLad commands from the command line
or in scripts. Only the first :command:`datalad get` requires authentication
with AWS credentials provided by the HCP project: DataLad will prompt any user at
the time of retrieval of the first file content of the dataset.
Afterwards, no further authentication is needed, unless the credentials become
invalid or need to be updated for other reasons.
Thus, in order to retrieve HCP data of up to single file level with DataLad,
users only need to:

- :command:`datalad clone` the superdataset from :term:`GitHub`
  (`github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_)
- Create an account at http://db.humanconnectome.org to accept data use terms
  and obtain AWS credentials
- Use :command:`datalad get [-n] [-r] PATH` to retrieve file, directory, or
  subdataset contents on demand. Authentication is necessary only
  once (at the time of the first :command:`datalad get`).

The HCP data release, despite its large size, can thus be version controlled and
easily distributed with DataLad.

Step-by-Step
^^^^^^^^^^^^

Building and publishing a DataLad dataset with HCP data consists of several steps:
1) Creating all necessary datasets, 2) publishing them to a RIA store, and 3) creating
an access point to all files in the HCP data release. The upcoming subsections
detail each of these.

Dataset creation with ``datalad addurls``
"""""""""""""""""""""""""""""""""""""""""

.. index:: ! datalad command; addurls

The :command:`datalad addurls` command (:manpage:`datalad-addurls` manual)
allows you to create (and update) potentially nested DataLad datasets from a list
of download URLs that point to the HCP files in the S3 buckets.
By supplying subject specific ``.csv`` files that contain S3 download links,
a subject ID, a file name, and a version specification per file in the HCP dataset,
as well as information on where subdataset boundaries are,
:command:`datalad addurls` can download all subjects' files and create (nested) datasets
to store them in. With the help of a few bash commands, this task can be
automated, and with the help of a `job scheduler <https://en.wikipedia.org/wiki/Job_scheduler>`_,
it can also be parallelized.
As soon as files are downloaded and saved to a datasets, their content can be
dropped with :command:`datalad drop`: The origin of the file was successfully
recorded, and a :command:`datalad get` can now retrieve file contents on demand.
Thus, shortly after a complete download of the HCP project data, the datasets in
which it has been aggregated are small in size, and yet provide access to the HCP
data for anyone who has valid AWS S3 credentials.

At the end of this step, there is one nested dataset per subject in the HCP data
release. If you are interested in the details of this process, checkout the
hidden section below.

.. findoutmore:: How exactly did the datasets came to be?

   .. note::

      All code and tables necessary to generate the HCP datasets can be found on
      GitHub at `github.com/TobiasKadelka/build_hcp <https://github.com/TobiasKadelka/build_hcp>`_.

   The :command:`datalad addurls` command is capable of building all necessary nested
   subject datasets automatically, it only needs an appropriate specification of
   its tasks. We'll approach the function of :command:`datalad addurls` and
   how exactly it was invoked to build the HCP dataset by looking at the
   information it needs. Below are excerpts of the ``.csv`` table of one subject
   (``100206``) that illustrate how :command:`addurls` works:

   .. code-block::
      :caption: Table header and some of the release note files

      "original_url","subject","filename","version"
      "s3://hcp-openaccess/HCP_1200/100206/release-notes/Diffusion_unproc.txt","100206","release-notes/Diffusion_unproc.txt","j9bm9Jvph3EzC0t9Jl51KVrq6NFuoznu"
      "s3://hcp-openaccess/HCP_1200/100206/release-notes/ReleaseNotes.txt","100206","release-notes/ReleaseNotes.txt","RgG.VC2mzp5xIc6ZGN6vB7iZ0mG7peXN"
      "s3://hcp-openaccess/HCP_1200/100206/release-notes/Structural_preproc.txt","100206","release-notes/Structural_preproc.txt","OeUYjysiX5zR7nRMixCimFa_6yQ3IKqf"
      "s3://hcp-openaccess/HCP_1200/100206/release-notes/Structural_preproc_extended.txt","100206","release-notes/Structural_preproc_extended.txt","cyP8G5_YX5F30gO9Yrpk8TADhkLltrNV"
      "s3://hcp-openaccess/HCP_1200/100206/release-notes/Structural_unproc.txt","100206","release-notes/Structural_unproc.txt","AyW6GmavML6I7LfbULVmtGIwRGpFmfPZ"

   .. code-block::
      :caption: Some files in the MNINonLinear directory

      "s3://hcp-openaccess/HCP_1200/100206/MNINonLinear/100206.164k_fs_LR.wb.spec","100206","MNINonLinear//100206.164k_fs_LR.wb.spec","JSZJhZekZnMhv1sDWih.khEVUNZXMHTE"
      "s3://hcp-openaccess/HCP_1200/100206/MNINonLinear/100206.ArealDistortion_FS.164k_fs_LR.dscalar.nii","100206","MNINonLinear//100206.ArealDistortion_FS.164k_fs_LR.dscalar.nii","sP4uw8R1oJyqCWeInSd9jmOBjfOCtN4D"
      "s3://hcp-openaccess/HCP_1200/100206/MNINonLinear/100206.ArealDistortion_MSMAll.164k_fs_LR.dscalar.nii","100206","MNINonLinear//100206.ArealDistortion_MSMAll.164k_fs_LR.dscalar.nii","yD88c.HfsFwjyNXHQQv2SymGIsSYHQVZ"
      "s3://hcp-openaccess/HCP_1200/100206/MNINonLinear/100206.ArealDistortion_MSMSulc.164k_fs_LR.dscalar.nii","100206","MNINonLinear

   The ``.csv`` table contains one row per file, and includes the columns
   ``original_url``, ``subject``, ``filename``, and ``version``. ``original_url``
   is an s3 URL pointing to an individual file in the S3 bucket, ``subject`` is
   the subject's ID (here: ``100206``), ``filename`` is the path to the file
   within the dataset that will be build, and ``version`` is an S3 specific
   file version identifier.
   The first table excerpt thus specifies a few files in the directory ``release-notes``
   in the dataset of subject ``100206``. For :command:`datalad addurls`, the
   column headers serve as placeholders for fields in each row.
   If this table excerpt is given to a :command:`datalad addurls` call as shown
   below, it will create a dataset and download and save the files in precise
   versions in it::

      $ datalad addurls -d <Subject-ID> <TABLE> '{original_url}?versionId={version}' '{filename}'

   This command translates to "create a dataset with the name of the subject ID
   (``-d <Subject-ID>``) and use the provided table (``<TABLE>``) to assemble the
   dataset contents. Iterate through the table rows, and perform one download per
   row. Generate the download URL from the ``original_url`` and ``version``
   field of the table (``{original_url}?versionId={version}'``), and save the
   downloaded file under the name specified in the ``filename`` field (``'{filename}'``)".

   If the file name contains a double slash (``//``), for example seen in the second
   table excerpt in ``"MNINonLinear//...``, this file will be created underneath a
   *subdataset* of the name in front of the double slash. The rows in the second
   table thus translate to "save these files into the subdataset ``MNINonLinear``,
   and if this subdataset does not exist, create it".

   Thus, with a single subject's table, a nested, subject specific dataset is built.
   Here is how the directory hierarchy looks for this particular subject once
   :command:`datalad addurls` worked through its table:

   .. code-block:: bash

       100206
       ├── MNINonLinear     <- subdataset
       ├── release-notes
       ├── T1w              <- subdataset
       └── unprocessed      <- subdataset

   This is all there is to assemble subject specific datasets. The interesting
   question is: How can this be done as automated as possible?

   **How to create subject-specific tables**

   One crucial part of the process are the subject specific tables for
   :command:`datalad addurls`. The information on the file url, its name, and its
   version can be queried with the :command:`datalad ls` command (:manpage:`datalad-ls`
   manual). It is a DataLad-specific version of the Unix ``ls`` command and can
   be used to list summary information about s3 URLs and datasets. With this
   command, the public S3 bucket can be queried and the command will output the
   relevant information.

   .. note::

      The :command:`datalad ls` command is a rather old command and less user-friendly
      than other commands demonstrated in the handbook. One problem for automation
      is that the command is made for interactive use, and it outputs information in
      a non-structured fashion. In order to retrieve the relevant information,
      a custom Python script was used to split its output and extract it. This
      script can be found in the GitHub repository as
      `code/create_subject_table.py <https://github.com/TobiasKadelka/build_hcp/blob/master/code/create_subject_table.py>`_.

   **How to schedule datalad addurls commands for all tables**

   Once the subject specific tables exist, :command:`datalad addurls` can start
   to aggregate the files into datasets. To do it efficiently, this can be done
   in parallel by using a job scheduler. On the computer cluster the datasets
   were aggregated, this was `HTCondor <https://research.cs.wisc.edu/htcondor/>`_.

   The jobs (per subject) performed by HTCondor consisted of

   - a :command:`datalad addurls` command to generate the (nested) dataset
     and retrieve content once [#f3]_::

        datalad -l warning addurls -d "$outds" -c hcp_dataset "$subj_table" '{original_url}?versionId={version}' '{filename}'

   - a subsequent :command:`datalad drop` command to remove file contents as
     soon as they were saved to the dataset to save disk space (this is possible
     since the S3 source of the file is known, and content can be reobtained using
     :command:`get`)::

        datalad drop -d "$outds" -r --nocheck

   - a few (Git) commands to clean up well afterwards, as the system the HCP dataset
     was downloaded to had a strict 5TB limit on disk usage.


   **Summary**

   Thus, in order to download the complete HCP project and aggregate it into
   nested subject level datasets (on a system with much less disk space than the
   complete HCP project's size!), only two DataLad commands, one custom configuration,
   and some scripts to parse terminal output into ``.csv`` tables and create
   subject-wise HTCondor jobs were necessary. With all tables set up, the jobs
   ran over the Christmas break and finished before everyone went back to work.
   Getting 15 million files into datasets? Check!

Using a Remote Indexed Archive Store for dataset hosting
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. index:: Remote Indexed Archive (RIA) store

All datasets were built on a scientific compute cluster. In this location, however,
datasets would only be accessible to users with an account on this system.
Subsequently, therefore, everything was published with
:command:`datalad push` to the publicly available
`store.datalad.org <http://store.datalad.org/>`_, a remote indexed archive (RIA)
store.

A RIA store is a flexible and scalable data storage solution for DataLad datasets.
While its layout may look confusing if one were to take a look at it, a RIA store
is nothing but a clever storage solution, and users never consciously interact
with the store to get the HCP datasets.
On the lowest level, `store.datalad.org <http://store.datalad.org/>`__
is a directory on a publicly accessible server that holds a great number of datasets
stored as :term:`bare git repositories`. The only important aspect of it for this
usecase is that instead of by their names (e.g., ``100206``), datasets are stored
and identified via their :term:`dataset ID`.
The :command:`datalad clone` command can understand this layout and install
datasets from a RIA store based on their ID.

.. findoutmore:: How would a datalad clone from a RIA store look like?

   In order to get a dataset from a RIA store, :command:`datalad clone` needs
   a RIA URL. It is build from the following components:

   - a ``ria+`` identifier
   - a path/url to the store in question. For store.datalad.org, this is
     ``http://store.datalad.org``, but it could also be an SSH url, such as
     ``ssh://juseless.inm7.de/data/group/psyinf/dataset_store``
   - a pound sign (``#``)
   - the dataset ID
   - and optionally a version or branch specification (appended with a leading ``@``)

   Here is how a valid :command:`datalad clone` command from the data store
   for one dataset would look like:

   .. code-block:: bash

      datalad clone 'ria+http://store.datalad.org#d1ca308e-3d17-11ea-bf3b-f0d5bf7b5561' subj-01

   But worry not! To get the HCP data, no-one will ever need to compose
   :command:`clone` commands to RIA stores apart from DataLad itself.

A RIA store is used, because -- among other advantages -- its layout makes the
store flexible and scalable. With datasets of sizes like the HCP project,
especially scalability becomes an important factor. If you are interested in
finding out why, you can find more technical details on RIA stores, their advantages,
and even how to create and use one yourself in the use case :ref:`usecase_datastore`.


Making the datasets accessible
""""""""""""""""""""""""""""""

At this point, roughly 1200 nested datasets were created and published to a publicly
accessible RIA store. This modularized the HCP dataset and prevented performance
issues that would arise in oversized datasets. In order to make the complete dataset
available and accessible from one central point, the only thing missing is a
single superdataset.

For this, a new dataset, ``human-connectome-project-openaccess``, was created.
It contains a ``README`` file with short instructions how to use it,
a text-based copy of the HCP projects data usage agreement, -- and each subject
dataset as a subdataset. The ``.gitmodules`` file [#f1]_ of this superdataset
thus is impressive. Here is an excerpt::

    [submodule "100206"]
        path = HCP1200/100206
        url = ./HCP1200/100206
        branch = master
        datalad-id = 346a3ae0-2c2e-11ea-a27d-002590496000
    [submodule "100307"]
        path = HCP1200/100307
        url = ./HCP1200/100307
        branch = master
        datalad-id = a51b84fc-2c2d-11ea-9359-0025904abcb0
    [submodule "100408"]
        path = HCP1200/100408
        url = ./HCP1200/100408
        branch = master
        datalad-id = d3fa72e4-2c2b-11ea-948f-0025904abcb0
    [...]

For each subdataset (named after subject IDs), there is one entry (note that
individual ``url``\s of the subdatasets are pointless and not needed: As will be
demonstrated shortly, DataLad resolves each subdataset ID from the common store
automatically).
Thus, this superdatasets combines all individual datasets to the original HCP dataset
structure. This (and only this) superdataset is published to a public :term:`GitHub`
repository that anyone can :command:`datalad clone` [#f4]_.

Data retrieval and interacting with the repository
""""""""""""""""""""""""""""""""""""""""""""""""""

.. note::

   Using this dataset requires DataLad version 0.12.2 or higher. Upgrading
   an existing DataLad installation is detailed in section :ref:`install`.

Procedurally, getting data from this dataset is almost as simple as with any
other public DataLad dataset: One needs to :command:`clone` the repository
and use :command:`datalad get [-n] [-r] PATH` to retrieve any file, directory,
or subdataset (content). But because the data will be downloaded from the HCP's
AWS S3 bucket, users will need to create an account at
`db.humanconnectome.org <http://db.humanconnectome.org>`_ to agree to the projects
data usage terms and get credentials. When performing the first :command:`datalad
get` for file contents, DataLad will prompt for these credentials interactively
from the terminal. Once supplied, all subsequent :command:`get` commands will
retrieve data right away.

Internally, DataLad cleverly manages the crucial aspects of data retrieval:
Linking registered subdatasets to the correct dataset in the RIA store. If you
inspect the GitHub repository, you will find that the subdatasets links in it
will not resolve if you click on them, because none of the subdatasets was
published to GitHub [#f5]_, but lie in the RIA store instead.
Dataset or file content retrieval will nevertheless work automatically with
:command:`datalad get`: Each ``.gitmodule`` entry lists the subdatasets
dataset ID. Based on a configuration of "subdataset-source-candidates" in
``.datalad/config`` of the superdataset, the subdataset ID is assembled to a
RIA URL that retrieves the correct dataset from the store by :command:`get`:

.. code-block:: bash
   :emphasize-lines: 4-5

    $ cat .datalad/config
    [datalad "dataset"]
        id = 2e2a8a70-3eaa-11ea-a9a5-b4969157768c
    [datalad "get"]
        subdataset-source-candidate-origin = "ria+http://store.datalad.org#{id}"

This configuration allows :command:`get` to flexibly generate RIA URLs from the
base URL in the config file and the dataset ID's listed in ``.gitmodules``. In
the superdataset, it needed to be done "by hand" via the :command:`git config`
command.
Because the configuration should be shared together with the dataset, the
configuration needed to be set in ``.datalad/config`` [#f6]_::

   $ git config -f .datalad/config "datalad.get.subdataset-source-candidate-origin" "ria+http://store.datalad.org#{id}"

With this configuration, :command:`get` will retrieve all subdatasets from the
RIA store. Any subdataset that is obtained from a RIA store in turn gets the very
same configuration automatically into ``.git/config``. Thus, the configuration
that makes seamless subdataset retrieval from RIA stores possible is propagated
throughout the dataset hierarchy.
With this in place, anyone can clone the top most dataset from GitHub, and --
given they have valid credentials -- get any file in the HCP dataset hierarchy.

Summary
"""""""

This usecase demonstrated how it is possible to version control and distribute
datasets of sizes that would otherwise be unmanageably large for version control
systems. With the public HCP dataset available as a DataLad dataset, data access
is simplified, data analysis that use the HCP data can link it (in precise versions)
to their scripts and even share it, and the complete HCP release can be stored
at a fraction of its total size for on demand retrieval.



.. rubric:: Footnotes

.. [#f1] If you want to read up on how DataLad stores information about
         registered subdatasets in ``.gitmodules``, checkout section :ref:`config2`.

.. [#f2] Precise performance will always be dependent on the details of the
         repository, software setup, and hardware, but to get a feeling for the
         possible performance issues in oversized datasets, imagine a mere
         :command:`git status` or :command:`datalad status` command taking several
         minutes up to hours in a clean dataset.

.. [#f3] Note that this command is more complex than the previously shown
         :command:`datalad addurls` command. In particular, it has an additional
         `loglevel` configuration for the main command, and creates the datasets
         with an `hcp_dataset` configuration. The logging level was set (to
         ``warning``) to help with post-execution diagnostics in the HTCondors
         log files. The configuration can be found in
         `code/cfg_hcp_dataset <https://github.com/TobiasKadelka/build_hcp/blob/master/code/cfg_hcp_dataset.sh>`_
         and enables a :term:`special remote` in the resulting dataset.

.. [#f4] To re-read about publishing datasets to hosting services such as
         :term:`GitHub` or :term:`GitLab`, go back to :ref:`publishtogithub`.

.. [#f5] If you coded along in the Basics part of the book and published your
         dataset to :term:`Gin`, you have experienced in :ref:`subdspublishing`
         how the links to unpublished subdatasets in a published dataset do not
         resolve in the webinterface: Its path points to a URL that would resolve
         to lying underneath the superdataset, but there is not published
         subdataset on the hosting platform!

.. [#f6] To re-read on configurations of datasets, go back to sections :ref:`config`
         and :ref:`config2`.