.. _executive_summary:

What you really need to know
----------------------------

DataLad is a data management multitool that can assist you at all times during the
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

-> something about nesting


Simplified local version control workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Building on top of :term:`Git` and :term:`git-annex`, DataLad allows you to
version control arbitrarily large content in datasets:

.. figure:: ../artwork/src/local_wf.svg
   :alt: Version control arbitrarily large contents
   :width: 70%

Collaboration
^^^^^^^^^^^^^

Consume existing datasets and update them from their sources, or create sibling
datasets you can publish updates to and pull updates from for collaboration and
sharing.

-> datalad install, datalad update, datalad create-sibling, datalad publish

Full provenance capture and reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Capture full :term:`provenance` of content in your dataset: Record where files
or datasets came from, or how they were created, including software environments.

-> datalad run, datalad rerun, datalad download-url,

Third party service integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-> datalad create-sibling-github, datalad create-sibling-gitlab, datalad export-to-figshare

Metadata handling
^^^^^^^^^^^^^^^^^

???

Extensions
^^^^^^^^^^

???