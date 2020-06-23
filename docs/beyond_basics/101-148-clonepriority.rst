.. _cloneprio:

Prioritizing subdataset clone locations
---------------------------------------

When obtaining a superdataset, the subdatasets it contains can have multiple sources.
Depending on the use case and precise context, different sources, sometimes referred to as "clone candidates", are more or less "useful".
By attaching *costs* to subdataset clone candidates, one can gain precise control over the locations from which subdatasets are retrieved, and the order in which retrieval is attempted.

.. figure:: ../artwork/src/origin.svg
   :figwidth: 50%


Clone candidate priority
^^^^^^^^^^^^^^^^^^^^^^^^

Let's start by motivating *why* it might be useful to prioritize subdataset clone locations.
Consider the case of the ``midterm_project`` subdataset that was created during the "Basics" part of the handbook:
Initially, as this dataset was created as a subdataset of ``DataLad-101``, its submodule entry in ``DataLad-101/.gitmodules`` [#f1]_ was a relative path (``./midterm_project``).
After it was published to :term:`GitHub` in section :ref:`yoda_project`, this dataset  had a second clone candidate location: A URL to its GitHub repository.
A third location, finally, was created when publishing the dataset to the RIA store in the previous section :ref:`riastore`.

Each of these locations was encoded in the superdataset's ``.gitmodules`` file, but ``.gitmodules`` can encode only a single clone candidate.



.. findoutmore:: Overview on clone candidate sources

    Clone candidates can come from the following sources:
    Without any additional configuration, a subdataset is either registered underneath its superdataset with a relative path (if it was originally created in this dataset), or from the path or URL it was originally installed from.
    This is recorded in the ``.gitmodules`` file of the superdataset.

    Alternatively, subdataset source candidates can be configured under the configuration variable ``datalad.get.subdataset-source-candidate-<name>`` within either ``.datalad/config`` or ``.git/config``.

The priority of subdataset clone locations is configured by attaching a *cost* to location name.
The cost is a three digit value, and lower values indicate a higher priority.
In order to set a

- lower cost -> high priority, i.e., lower values first

1. URL from superdataset remote with submodule path appended (> 1 possible)
2. URL/abs. path in .gitmodules
3. rel. path from URL in .gitmodules appended to superdataset path


matt

.. rubric:: Footnotes

.. [#f1] To re-read about ``.gitmodules`` files and their contents, please go back to section :ref:`config2`.