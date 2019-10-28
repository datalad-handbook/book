.. _usecase_HCP_dataset:

The HPC data as a dataset
-------------------------

This usecase outlines how a large neuroimaging data collection can be
published in an accessible manner using DataLad. Using the
`Human Connectome Project <http://www.humanconnectomeproject.org/>`_ (HCP) data
as an example, it shows how...

#. A large data collection is split into ~5000 (nested) DataLad datasets,
   and stored inside a single, top-level "HCP" dataset
#. TODO: Something about how the submodule urls are generated...
#. TODO: how to interact with the top-level superdataset and where it is
   available from.

The Challenge
^^^^^^^^^^^^^

The `Human Connectome Project <http://www.humanconnectomeproject.org/>`_ aims
to provide an unparalleled compilation of neural data through a customized
database. Its largest data collection is the
`1200 subjects Data Release <https://humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release/>`_,
consisting of neuroimaging and behavioral data for 1206 subjects. Its large
amount of data, however, constitutes a challenge: Several hundred GB of data
in a non-standard format are difficult to store, structure, and access.


The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

The data collection is aggregated into a large (~5000) amount of subdatasets:
A top-level superdataset consists of one subdatasets for every subject in the
data collection. Within each subjects subdataset, various subdirectories
with different data types are turned into subdatasets as well.


Step-by-Step
^^^^^^^^^^^^

