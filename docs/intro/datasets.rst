****************
DataLad Datasets
****************

A DataLad dataset is the core data type of DataLad.
Once created, it looks like any other directory on your filesystem.
However, all files and directories within the DataLad dataset can be
tracked (should you want them to be tracked), regardless of their size.
Large content is tracked in an *annex* that is automatically
created and handled by DataLad. Whether text files or larger files change,
all of these changes can be written to your DataLad datasets history.

.. admonition:: Note for git users:

   A DataLad dataset is a git repository. Large file content in the
   dataset in the annex is tracked with git-annex.

Users can *create* new DataLad datasets from scratch, or install existing
DataLad datasets from paths, urls, or open-data collections. This makes
sharing and accessing data fast and easy. Moreover, when sharing or installing
a DataLad dataset, all copies also include the datasets history. An installed DataLad
dataset knows the dataset it was installed from, and if changes
in this original DataLad dataset happen, the installed dataset can simply be updated.

Upon installation of a DataLad dataset, DataLad retrieves only (small) metadata
information about the dataset. This exposes the datasets file hierarchy
for exploration, and speeds up the installation of a DataLad dataset
of many TB in size to a few seconds. Retrieval of the actual, potentially large
file content can happen at any later time for the full dataset or subsets
of files.

Within DataLad datasets one can *nest* other DataLad
datasets arbitralily deep. This does not seem particulary spectacular -
after all, any directory on a filesystem can have other directories inside it.
The possibility for nested Datasets, however, is one of many advantages
DataLad datasets have:
Any lower-level DataLad dataset (the *subdataset*) has a stand-alone
history. The top-level DataLad dataset (the *superdataset*) only stores
*which version* of the subdataset is currently used.

.. todo::

   Elaborate in an example. points to make:
   - modularity: you can have a code, data, images, (maybe different albums?)
   subdatasets and do not need to keep track of everything all at once
   - you can update individual subdatasets


.. figure:: ../img/virtual_dirtree.png
   :scale: 100%
   :alt: Virtual directory tree of a nested DataLad dataset



A *new* DataLad dataset is instantiated from scratch with ``datalad create``.
A new DataLad dataset is always created empty, even if the target
directory already contains additional files or directories. After creation,
arbitralily large amounts of data can be added via ``datalad add``.


.. admonition:: Note for git users:

   ``datalad create`` uses the ``git init`` and ``git annex init`` commands.


An already existing datalad dataset can be obtained with the ``datalad install``
command from a url or path, or from the datalad open-data collection.


.. admonition:: Note

   ``datalad install`` used the ``git clone`` command.


.. todo::
   more examples with some simple ``tree`` visualization or fancy diagrams
