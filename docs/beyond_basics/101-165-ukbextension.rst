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
Usually, one creates a *bulk file* that lists all required subject IDs and data
field IDs, and uses ``ukbfetch`` to download the data specified in the bulk file.

.. findoutmore:: See a snippet from a bulk file

   This snippet of a bulk file specifies downloads of MRI bulk data as identified via
   their data field ID (functional images, diffusion-weighted images, susceptibility-weighted
   images, and resting state data in DICOM and NifTI format, T1-weighted and T2-FLAIR
   images in NifTI format, Eprime experiment files, and resting state correlation
   matrices) for two subjects (``1000244`` and ``1000339``):

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

``datalad-ukbiobank`` is a `DataLad extension <101-144-intro_extensions.html/>`_
that equips DataLad with a
set of commands to obtain and monitor imaging data releases of the UKBiobank.
Thus, the extension is concerned with downloading MRI bulk data.
It comes with two commands, ``ukb-init`` to initialize a dataset for a UKBiobank
participant, and ``ukb-update`` to update an existing dataset for a UKBiobank
participant:
In principle, it is a wrapper around the ``ukb-fetch`` tool. Given a successful
application and a keyfile, the commands of ``datalad-ukbiobank`` create
one dataset per UKBiobank participant, retrieve their data and restructure it into
a `BIDS <https://bids.neuroimaging.io/>`_-like format, and update it on demand.

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

.. todo::

   - elaborate on why ukbfetch tool instead of ukb-fetch command
   - maybe some insights into the substitute script

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