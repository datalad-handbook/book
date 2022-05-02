.. _executive_summary:

What you really need to know
----------------------------

DataLad is a data management multitool that can assist you in handling the entire
life cycle of digital objects. It is a command-line tool, free and open source, and
available for all major operating systems.

This document is the 10.000 feet overview of important concepts, commands, and
capacities of DataLad. Each section briefly highlights one type of functionality or
concept and the associated commands, and the upcoming Basics chapters will demonstrate
in detail how to use them.

DataLad datasets
^^^^^^^^^^^^^^^^

Every command affects or uses DataLad *datasets*, the core data structure of
DataLad. A *dataset* is a directory on a computer that DataLad manages.

.. figure:: ../artwork/src/dataset.svg
   :alt: Create DataLad datasets
   :width: 70%

You can create new, empty datasets from scratch and populate them,
or transform existing directories into datasets.

Simplified local version control workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Building on top of :term:`Git` and :term:`git-annex`, DataLad allows you to
version control arbitrarily large files in datasets.

.. figure:: ../artwork/src/local_wf.svg
   :alt: Version control arbitrarily large contents
   :width: 70%

Thus, you can keep track of revisions of data of any size, and view, interact with or
restore any version of your dataset's history.


Consumption and collaboration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad lets you consume datasets provided by others, and collaborate with them.
You can install existing datasets and update them from their sources, or create
sibling datasets that you can publish updates to and pull updates from for
collaboration and data sharing.

.. figure:: ../artwork/src/collaboration.svg
   :alt: Consume and collaborate
   :width: 130%

Additionally, you can get access to publicly available open
data collections with :term:`the DataLad superdataset ///`.

Dataset linkage
^^^^^^^^^^^^^^^

Datasets can contain other datasets (subdatasets), nested arbitrarily deep. Each
dataset has an independent revision history, but can be registered at a precise version
in higher-level datasets. This allows to combine datasets and to perform commands recursively across
a hierarchy of datasets, and it is the basis for advanced provenance capture abilities.

.. figure:: ../artwork/src/linkage_subds.svg
   :alt: Dataset nesting
   :width: 100%

Full provenance capture and reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad allows to capture full :term:`provenance`: The origin of datasets, the
origin of files obtained from web sources, complete machine-readable and
automatically reproducible records of how files were created (including software
environments).

.. figure:: ../artwork/src/reproducible_execution.svg
   :alt: provenance capture
   :width: 100%

You or your collaborators can thus re-obtain or reproducibly recompute content
with a single command, and make use of extensive provenance of dataset content
(who created it, when, and how?).

Third party service integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Export datasets to third party services such as
`GitHub <https://github.com/>`_, `GitLab <https://about.gitlab.com/>`_, or
`Figshare <https://figshare.com/>`_ with built-in commands.

.. figure:: ../artwork/src/thirdparty.svg
   :alt: third party integration
   :width: 100%

Alternatively, you can use a multitude of other available third party services such as
`Dropbox <https://dropbox.com>`_, `Google Drive <https://drive.google.com/drive/my-drive>`_,
`Amazon S3 <https://aws.amazon.com/de/s3/>`_, `owncloud <https://owncloud.org/>`_,
or many more that DataLad datasets are compatible with.

Metadata handling
^^^^^^^^^^^^^^^^^
Extract, aggregate, and query dataset metadata. This allows to automatically obtain
metadata according to different metadata standards (EXIF, XMP, ID3, BIDS, DICOM,
NIfTI1, ...), store this metadata in a portable format, share it, and search dataset
contents.

.. figure:: ../artwork/src/metadata_prov_imaging.svg
   :alt: meta data capabilities
   :width: 100%

All in all...
^^^^^^^^^^^^^

You can use DataLad for a variety of use cases. At its core, it is a domain-agnostic
and self-effacing tool: DataLad allows to improve your data management without
custom data structures or the need for central infrastructure or third party
services.
If you are interested in more high-level information on DataLad, you can find
answers to common questions in the section :ref:`FAQ`, and a concise command
cheat-sheet in section :ref:`cheat`.

But enough of the introduction now -- let's dive into the
:ref:`basics-intro`