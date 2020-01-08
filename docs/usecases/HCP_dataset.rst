.. _usecase_HCP_dataset:

The HPC data as a dataset
-------------------------

This usecase outlines how a large neuroimaging data collection can be
published in an accessible manner using DataLad. Using the
`Human Connectome Project <http://www.humanconnectomeproject.org/>`_ (HCP) data
as an example, it shows how...

#. A large data collection is split into nested DataLad datasets to modularize
   storage and access.
#. A single, top-level "HCP" superdataset contains all nested subdatasets, and is
   published to GitHub as the access point for the full HCP dataset.
#. The complete, vastly nested dataset is published to
   `store.datalad.org <store.datalad.org>`_, and references ... the S3 bucket?
#. (Sub)dataset URLs for DataLad-internal referencing to the store are
   flexibly generated based on dataset ID.

The Challenge
^^^^^^^^^^^^^

The `Human Connectome Project <http://www.humanconnectomeproject.org/>`_ aims
to provide an unparalleled compilation of neural data through a customized
database. Its largest data collection is the
`1200 subjects Data Release <https://humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release/>`_,
consisting of neuroimaging and behavioral data for 1206 subjects. Its large
amount of data, however, constitutes a challenge: Several hundred GB of data
in a non-standard format are difficult to store, structure, access, and version
control.


The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

The data collection is aggregated into a large (N ~= 5000) amount of subdatasets:
A top-level superdataset consists of one subdataset for every subject in the
data collection. Within each subject's subdataset, several subdirectories
(constituting different data types) are turned into further subdatasets.

The superdataset is published to :term:`GitHub`. This exposes one lean superdataset
for anyone to install. Afterwards, subsequent :command:`datalad get [-n]` commands
allow to flexibly retrieve the subsets of the HCP dataset that are needed -- whether
its subjects, data modalities, or individual files.

.. todo::

   where does the data come from, S3? If so, how are the AWS credentials handled?


Step-by-Step
^^^^^^^^^^^^

