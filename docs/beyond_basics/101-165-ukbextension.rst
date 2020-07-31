.. _ukbextension:

Data retrieval with DataLad's UKBiobank extension
-------------------------------------------------

A fundamental aspect of the UKBiobank project is retrieving and structuring the
files. Downloading the data is a complex and lengthy process, however. In order
to ease the data download and further use of the data with DataLad, the
``datalad-ukbiobank`` extension has been developed.

General aspects of the data download of UKBiobank
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Understanding the ``datalad-ukbiobank`` extension requires some fundamental
understanding on how downloading UKBiobank data works.
The UKBiobank differentiates between the *main dataset*, an encrypted file that
contains information such as socio-demographics, life-style, cognitive function,
or health outcomes, and *bulk data*, which encompasses data such as MRI images
and electrocardiographic data. An application to use UKBiobank data needs to
specify exactly which parts of the data are needed, and the main dataset will
contain exactly the data that was applied for.

The main dataset is downloaded as a single ``.enc`` file, and can be decrypted
to ``.csv`` or other formats with tools the UKBiobank provides. This dataset
does not contain any neuroimaging data, but data ID fields that indicate whether
or not certain data is in principle available for the given participant. For
example, all subjects with resting state fMRI data in the second session
have data field ``20227_2_0`` in their main dataset.
The bulk data associated with these data fields is downloaded using the
``ukbfetch`` commandline tool, and requires authentication with a keyfile.

.. findoutmore:: On ukbfetch

   ``ukbfetch`` is a software that downloads specified data from the UKBiobank given appropriate authentication, provided by the UKBiobank.
   The program can be downloaded from a browser `here <https://biobank.ctsu.ox.ac.uk/showcase/download.cgi>`_ or from the terminal using ``wget -nd  biobank.ctsu.ox.ac.uk/showcase/util/ukbfetch``.

Usually, one creates a *bulk file* that lists all required subject IDs and data
field IDs, and uses ``ukbfetch`` to download the data specified in the bulk file.

.. findoutmore:: See a snippet from a bulk file

   This snippet of a bulk file specifies downloads of MRI bulk data as identified via
   their data field ID (functional images, diffusion-weighted images, susceptibility-weighted images, and resting state data in DICOM and NifTI format, T1-weighted and T2-FLAIR images in NifTI format, Eprime experiment files, and resting state correlation matrices) for two subjects (``1000244`` and ``1000339``):

   .. code-block:: bash

      1000244 20217_2_0
      1000244 20218_2_0
      1000244 20219_2_0
      1000244 20225_2_0
      1000244 20227_2_0
      1000244 20249_2_0
      1000244 20250_2_0
      1000244 20251_2_0
      1000244 20252_2_0
      1000244 20253_2_0
      1000244 25747_2_0
      1000244 25748_2_0
      1000244 25749_2_0
      1000244 25750_2_0
      1000244 25751_2_0
      1000244 25752_2_0
      1000244 25753_2_0
      1000244 25754_2_0
      1000244 25755_2_0
      1000339 20217_2_0
      1000339 20218_2_0
      1000339 20219_2_0
      1000339 20225_2_0
      1000339 20227_2_0
      1000339 20249_2_0
      1000339 20250_2_0
      1000339 20251_2_0
      1000339 20252_2_0
      1000339 20253_2_0
      1000339 25747_2_0
      1000339 25748_2_0
      1000339 25749_2_0
      1000339 25750_2_0
      1000339 25751_2_0
      1000339 25752_2_0
      1000339 25753_2_0
      1000339 25754_2_0
      1000339 25755_2_0


A DataLad extension for UKBiobank downloads
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``datalad-ukbiobank`` is a `DataLad extension <101-144-intro_extensions.html/>`_ that equips DataLad with a set of commands to obtain, monitor, and restructure imaging data releases of the UKBiobank.
More specifically, the extension is concerned with downloading MRI bulk data, updating it from its source if changes are released, and, optionally, restructuring the data into BIDS-like formats.

The unit that this extension's commands operate on are single UKBiobank subjects.
The first command, ``ukb-init``, initializes a dataset for a UKBiobank participant.
The second command, ``ukb-update``, updates an existing dataset for a UKBiobank participant.
In principle, the extension serves as a wrapper around the ``ukb-fetch`` tool and enables UKBiobank data ingestion into DataLad, and thus longitudinal tracking, version control, and integration into DataLad-centric analsyis workflows.
In addition, it can restructure data into a BIDS-like format to ease further use of the data with BIDS compliant tools.
The complete set of actions of the extension are thus, given a successful application and a keyfile, creating one dataset per UKBiobank participant, retrieving their data and restructuring it into a `BIDS <https://bids.neuroimaging.io/>`_-like format, and updating it on demand.

It will represent the data in different forms on up to three :term:`branch`\es:

- ``incoming`` tracks UKB downloads, as published by the UKB (i.e., zipfiles)
- ``incoming-native`` is a "native" representation of the extracted downloads for single file access using UKB naming conventions
- ``incoming-bids``, if enabled, is a BIDS-like representation of the extracted downloads.

The ``master`` branch of the dataset will by default be identical to ``incoming-bids``, and a ``datalad ukb-update --merge`` will update and merge all existing ``incoming-`` branches of the dataset.

.. findoutmore:: Using the extension for predownloaded data

   If you have UKBiobank data downloaded already and want to make ues of ``datalad-ukbiobank`` for version control or BIDSification, you can replace ``ukbfetch`` with a shim that obtains the relevant files from where they have been downloaded to.
   An example for this is included in the `sourcecode of the extension <https://github.com/datalad/datalad-ukbiobank/tree/master/tools>`_ and a demonstration of it is in the example below.

Requirements
""""""""""""

In order to use ``datalad-ukbiobank`` to retrieve data from the UKBiobank, you
will need the following:

- A DataLad installation as detailed in section :ref:`install`
- The ``datalad-ukbiobank`` extension (installable via ``pip install datalad_ukbiobank``)
- A successful `application <https://www.ukbiobank.ac.uk/register-apply/>`_ to access
  the UKBiobank data, and the resulting a link and a key file to retrieve it.

General usage
"""""""""""""

.. todo::

   This section would benefit from a short demonstration how the extension is
   to be used. This could also be relevant for the README of the extension

.. findoutmore:: How to make the ukbfetch tool executable and available

   First, after download, grant executive :term:`permissions` to it using the Unix command `chmod <https://en.wikipedia.org/wiki/Chmod>`_::

      $ chmod 775 ukbfetch

   Afterwards, make it available by placing it into your ``PATH`` environment variable.
   Run ``echo $PATH`` to find out which paths are in your ``PATH``, and then either place the ukbfetch file into a directory that already is in your path (e.g., ``sudo mv ukbfetch /usr/lib/bin/``), or add a new path that points to the file to your ``PATH`` variable.
   The latter can be done by either posting the line below into a terminal to make it available for this session, or by adding the line below into a ``.bashrc`` file (or equivalent) to make the file permanently available::

      $ export PATH=$PATH:/home/path/to/ukbfetch

   Afterwards, typing ``ukbfetch`` into the command line anywhere on your system will invoke the ukbfetch tool.

Using the ukbiobank extension to handle UKBiobank data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This subsection introduces the first set of tools and tricks used to retrieve,
store, and transfer the UKBiobank data. Each paragraph demonstrates how one
particular difficulty or problem was mitigated or solved.

.. note::

   As the storage project had a too tight limit on inodes and data was supposed
   to be downloaded in parallel, the ``datalad-ukbiobank`` extension was used in
   a slightly altered fashion. This section does not demonstrate how to use the
   tool in general, but how it was utilized and used in conjunction with other
   tools to navigate difficulties and limitations imposed on the UKBiobank project.

Problem 1: Enormous amounts of data downloads
"""""""""""""""""""""""""""""""""""""""""""""

Downloading 40.000 subjects is not done over night. In order to speed up the
process and use the available computational infrastructure (computational cluster
``juseless`` at the INM-7) efficiently, downloading was scheduled with the help of
the job scheduler `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ and its
meta-scheduler `DAGman <https://research.cs.wisc.edu/htcondor/dagman/dagman.html>`_.

.. todo::

   Maybe give some estimates of the duration of the downloads?

Downloading was scheduled with a DAGfile that parallelized over participants.
Instead of downloading the data with the extension, the ``ukbfetch`` tool was used
(more on why later) and stored all participant data as zip files on a dedicated
data node on the compute cluster ``juseless``.
A second DAGfile created participant datasets afterwards. Datasets were initialized
with the :command:`ubk-init` command and populated with the :command:`ukb-fetch`
command. Instead of calling the normal ``ukbfetch`` tool, this command was modified
to call a substitute ``ukbfetch`` that downloads and restructures the data from
the data node.

.. findoutmore:: Building subject specific datasets

   Datasets were generated on the INM-7's compute cluster.
   The general process consisted of

   #. Generating subject specific datasets in a temporary location
   #. Publish the datasets into a RIA store at a permanent location
   #. Removing the temporary directories


   Subject dataset creation was parallelized using a job scheduler -- else, the creation of ~42k would have taken about 180 days.
   Here is how this was done:

   Initially, directories for the data store, code and submit files, and log files were created.

   .. code-block:: bash

      # in /data/project/ukb_vbm
      $ mkdir dsstore
      $ mkdir -p init/code
      $ mkdir -p init/logs

   To build and push subject datasets into a RIA store, a generic script was created.
   This script takes a subject ID and their data record IDs as input, and initializes this subject's dataset in a temporary location, downloads their files, and pushes the result into a RIA store.
   Once the job finishes, the temporary directory is cleaned up, and the dataset is available in the RIA store.

   .. code-block:: bash

       #!/usr/bin/bash

       set -e -u

       # create a temporary dataset (note: when run through a job
       # scheduler, each job has its own /tmp)
       datalad create /tmp/ds
       cd /tmp/ds

       # Initialize a UKB subject dataset and BIDS restructuring.
       # $@ are all arguments passed to the script, which should be
       # subject ID and data record IDs
       datalad ukb-init --bids $@

       # run ukb-update --merge with a custom fetch file in the PATH (set in
       # job submission). A configuration ensure that datalad doesn't complain
       # about a missing keyfile
       PATH=$UKBFETCHPATH:$PATH \
            datalad -c datalad.ukbiobank.keyfile=none ukb-update --merge

       # After file retrieval and restructuring into all branches, drop data
       # and disregard this dataset annex
       git annex dead here
       git annex drop -A --force
       git annex forget --drop-dead --force

       # finally, create a RIA store sibling without storage sibling ...
       datalad create-sibling-ria \
           -s bulk1 \
           --no-storage-sibling \
           ria+file:///data/project/ukb_vbm/dsstore

       # ... and push the dataset into the store (using git to push
       # all branches)
       git push bulk1 --all

UKBiobank data was downloaded prior to the development of this extension.
In order to use the pre-downloaded data, :command:`ukb-update` is used with a custom-made fetch file. The details are included in the findoutmore below.

.. findoutmore:: Working with pre-downloaded UKBiobank data

   As the data was already downloaded and stored in its original form in a permanent and secure place on one node of the compute cluster, a shim ukbfetch tool was created.
   This file's purpose was to reference the data in the existing, permanent storage location with ``git annex addurl``, and replaces the ukbfetch utility that needs to be given to :command:`datalad ukb-update`.
   With this file, all data in the resulting subject datasets can be dropped and reobtained from the existing data location, with no dubplicate data records on the system.
   Here are the contents of this file::

       #!/bin/bash

       set -u -e

       cmd="git annex addurl --raw --pathdepth=-1"
       baseurl="https://some.host/ukb-downloads"

       for line in $(cat .ukbbatch |  sed 's/ /,/g'); do
           sub_id=${line%,*}
           modality=${line#*,}

           $cmd $baseurl/${sub_id}/${sub_id}_${modality}.zip \
              || $cmd $baseurl/${sub_id}/${sub_id}_${modality}.txt \
              || $cmd $baseurl/${sub_id}/${sub_id}_${modality}.adv \
              || $cmd $baseurl/${sub_id}/${sub_id}_${modality}.ed2 \
              || ( echo "Download failed: $line" ; exit 15 )
       done


   Note that an additional :term:`git-annex` configuration may be necessary if ``https://some.host`` is a private or local IP address (as retrieving files from these locations is disabled `as it poses a potential security threat <https://git-annex.branchable.com/security/>`_).
   This can be configured using :command:`git config`::

       $ git config --global --add annex.security.allowed-ip-addresses <relevant IP address>


.. todo::

   Submitfile generation:

   $ scp bulk1.htc.inm7.de:ukb/participant_ids.txt init
   create a table with subject ID and data records (one row per participant) for the submitfile to loop over.
   in submitfile: environment = "JOBID=$(Cluster).$(Process) UKBFETCHPATH=$ENV(PWD)/code

Problem 2: Storing data under severe inode limitations
""""""""""""""""""""""""""""""""""""""""""""""""""""""

As mentioned in the previous section (:ref:`ukbintro`), data storage on the data
access server JUDAC was limited to 4.4 million inodes. Right after download, the
raw data amounted to about 1000 files per subject. Given the initial 40k subjects,
the amount of files *for the raw data only* exceeded the available storage space
by a factor of 10.

In order to transfer and store the data nevertheless, datasets needed to be stored
as 7zipped archives in :term:`remote indexed archive (RIA) store`\s. These
stores can contain a complete dataset (regardless of the amount of files it
encompasses) using about 25 inodes. For this, the participant-wise datasets
assembled on ``juseless`` were exported to JUDAC as archives using the
:command:`ria-export-archive` command.

.. todo::

   In the end, a graphic visualizing the involved machines, storages, and transfer
   may be very valuable.