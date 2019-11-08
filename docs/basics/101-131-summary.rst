.. _summary_python:

Summary
-------

DataLad's Python API makes all of DataLad's functionality available in
Python, either as standalone functions that are exposed via ``datalad.api``,
or as methods of the ``Dataset`` class.
This provides an alternative to the command line, but it also opens up the
possibility of performing DataLad commands directly inside of scripts -- a
useful way to ensure that inputs are retrieved, subdatasets are installed,
or similar operations are performed, without the need for command line
interactions with DataLad. An example of this is the usecase
:ref:`usecase_reproducible_paper`.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad's Python API is a useful alternative to the command line functions
you are already very familiar with. Especially cool, however, is how useful
they become in data analysis projects that rely on Python code:
Equipping your code with commands that ensure that subdatasets are installed
or analysis inputs are retrieved will fool-proof your dataset. By embedding
DataLad's Python API into your scripts, you can make sure that your data
analysis stays functional -- even when your collaborator or the person you share
your dataset with does not use DataLad at all. This spares you the hassle of
explaining to them what "subdatasets", or "metadata on file availability"
are, and gives them DataLad magic without them being aware of it.