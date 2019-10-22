.. _usecase_datastore:

Building a scalable data storage for scientific computing
---------------------------------------------------------

This use case details a model implementation for a scalable data storage
solution, suitable to serve the computational and logistic demands of data
science in big (scientific) institutions, while keeping workflows for users
user as simple as possible. It elaborates on

#. how to setup a computational cluster or supercomputer as a data store
#. configure the data store and ...
#. ...

.. note::

   This section is technical in nature and aimed at IT/data management
   personnel seeking insights into the technical implementation and
   configuration of a scalable data storage. It is not meant for users of
   such a data store. A use case about user-facing interactions and workflows
   with such a data storage is detailed in

   .. todo::

      write and link HAMMERPANTS usecase


The Challenge
^^^^^^^^^^^^^

Research in many areas of science requires enormous amounts of data. Such
data is often accessed by multiple people at the same time and used for various
computations and different research questions.

The size of the data set, the need for simultaneous access and transformation
of this data by multiple people, and the subsequent storing of multiple copies
or derivatives of the data constitutes a challenge for computational clusters
and data management solutions.

The data science institute XYZ consists of 70 people: Principle
investigators, PhD students, general research staff, system's administration,
and IT support. It does research on important global issues, and prides
itself with ground-breaking insights obtained from elaborate and complex
computations run on a large scientific computing cluster.
The data sets used in the institute are big both in size and number of files,
and expensive to collect.
Therefore, datasets are used for various different research questions, by
multiple researchers.
Every member of the institute has an account on the compute cluster, and all
of the data exists in dedicated directories on the server. In order to work on
their research questions without modifying original data, every user creates own
copies of the data they need, and stores it together with the multitude of
output files on the cluster. Version control is not a standard skill in the
institute, and especially PhD students and other trainees struggle with the
technical overhead of data management *and* data science. Thus, an excess of
data copies and derivatives exists in addition to the already substantial
amount of original data. With data directories of several TB in size, the
compute cluster quickly is quickly brought to its knees: Insufficient memory and
IOPS starvation make computations painstakingly slow, and hinder scientific
progress.

The DataLad approach
^^^^^^^^^^^^^^^^^^^^

- distributed data store: data is stored in a different place than where you
  work with it
- configure git annex ria remote for indexed files
- data is version controlled and in a datalad dataset: no need to keep outdated
  choatic derivatives because they are version controlled), installed datasets
  are lightweight and only necessary data can be retrieved, data that can be
  reobtained/recomputed easily can be dropped to save space.
- 7zipping files mitigates any inode limitation

Step-by-step
^^^^^^^^^^^^

- needs a few sentences on what a special remote is. third party sharing WIP
  PR could already have this
- distributed nature of the data storage: JSC, brainbfast
- detail on the nested trees: dataset ID, what can lie beneath (bare repo,
  object tree, archive...)



- copies of stuff (lack of version control)
- play with data where it is stored
- all is on this space -- this has problems (Which???)

performance IOPS starvations --> gets worse at RAID (multiple write operations)
waiting on disk: shared infra for writing/reading and computing

TODO: data close to compute nodes

With data directories of several TB in size, the compute cluster quickly is
quickly brought to its knees: Insufficient memory, immense computational
effort to copy

infrastructure: harddrives,
hammerpants: modular store, the user should never know
big systems: expensive, scalability
we're doing sharding -->
everything on one dataserver tough bc size -- would need to be on multiple
machines, have to behave in the same way.
Instead: multiple differnt independent machines
With datalad it is irrelevant where the data is located, its encoded into
special remote
