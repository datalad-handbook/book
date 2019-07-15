Basic DataLad Magic: Summary
----------------------------

In the last two sections, we have discovered the basics of installing a published DataLad dataset,
and experienced the concept of modularly nesting datasets.

* A published dataset can be installed with the ``datalad install`` command:
  ``datalad install [--dataset PATH] --source PATH/URL PATH``.

* The command takes a location of an existing dataset (``--source``/``-s``),
  and a path to where you want the dataset to be installed. If you do not specify a path,
  the dataset will be installed in the current directory, with the original name of the
  dataset you are installing.

* If a dataset is installed inside of a dataset, the ``--dataset``/``-d`` option
  needs to specify the root of the superdataset.

* The source can be a URL (for example of a Github repository, as in section :ref:`installds`), but also
  paths, or open data collections.

* After installation, only small files and meta data about file availability are present locally.
  To retrieve actual file content of larger files, ``datalad get PATH`` downloads large file
  content on demand.

* ``datalad status --annex basic`` or ``datalad status --annex all`` are helpful to determine
  total repository size and the amount of data that is present locally.

* Remember: Super- and subdatasets have standalone histories. A superdataset only stores
  which version of the subdataset is currently used.


Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have procedurally experienced how to install a dataset, but simultaneously you have
learned a lot about the principles and features of DataLad datasets.
Installing datasets and getting their content allows you to consume published datasets.
By nesting datasets within eachother, you can modularly re-use datasets. While this may
appear abstract, upcoming section will demonstrate many example of why this can be handy.

