.. _executive_summary:

What you really need to know
----------------------------

DataLad is a data management multitool that can assist you during all steps in the
evolution of digital objects. It is a command-line tool, free and open source, and
available for all major operating systems.

This document is the 1000 feet overview of important concepts, commands, and
capacities of DataLad.

DataLad datasets
^^^^^^^^^^^^^^^^

Every command affects or uses DataLad *datasets*, the core data structure of
DataLad. A *dataset* is any directory on a computer that DataLad is instructed
to manage.

.. figure:: ../artwork/src/dataset.svg
   :alt: Create DataLad datasets
   :width: 70%


Simplified local version control workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Building on top of :term:`Git` and :term:`git-annex`, DataLad allows you to
version control arbitrarily large content in datasets:

.. figure:: ../artwork/src/local_wf.svg
   :alt: Version control arbitrarily large contents
   :width: 70%

Dataset linkage
^^^^^^^^^^^^^^^

Datasets can contain other datasets (subdatasets), nested arbitrarily deep. Each
dataset has an independent revision history, but can be registered in higher-level
datasets. This allows to combine datasets and to perform commands recursively across
a hierarchy of datasets.

.. figure:: ../artwork/src/linkage_subds.svg
   :alt: Dataset nesting
   :width: 100%

Consumption and collaboration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consume existing datasets and update them from their sources, or create sibling
datasets you can publish updates to and pull updates from for collaboration and
sharing. Additionally, get access to publicly available open data collections
with :term:`the DataLad superdataset ///`.

.. figure:: ../artwork/src/collaboration.svg
   :alt: Consume and collaborate
   :width: 130%

Full provenance capture and reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capture full :term:`provenance` of content in your dataset: Dataset origin is
always captured, but moreover, record where files obtained from web sources
came from, or how files were created, including software environments.
This way, content can be re-obtained or reproducibly recomputed with a single
command, and the provenance of dataset content (who created it, when, and how?)
can be queried and used.

.. figure:: ../artwork/src/reproducible_execution.svg
   :alt: provenance capture
   :width: 100%


Third party service integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Export datasets to third party services such as
`GitHub <https://github.com/>`_, `GitLab <https://about.gitlab.com/>`_, or
`Figshare <https://figshare.com/>`_ with built-in commands, or use a multitude
of other available third party services such as `Dropbox <https://dropbox.com>`_,
`Google Drive <https://drive.google.com/drive/my-drive>`_,
`Amazon S3 <https://aws.amazon.com/de/s3/>`_, `owncloud <https://owncloud.org/>`_,
or many more.

.. figure:: ../artwork/src/thirdparty.svg
   :alt: third party integration
   :width: 100%


Metadata handling
^^^^^^^^^^^^^^^^^

???

Extensions
^^^^^^^^^^

???

.. todo::

   crawler?