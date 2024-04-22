.. index::
   pair: clone; DataLad command
.. _cloneprio:

Prioritizing subdataset clone locations
---------------------------------------

When obtaining a superdataset, the subdatasets it contains can have multiple sources.
Depending on the use case and precise context, different sources, sometimes referred to as "clone candidates", are more or less "useful".
By attaching *costs* to subdataset clone candidates, one can gain precise control over the locations from which subdatasets are retrieved, and the order in which retrieval is attempted.
This can create a more flawless and less error-prone user experience as well as speedier dataset installations.

.. figure:: ../artwork/src/origin.svg
   :width: 50%

.. index::
   single: configuration item; datalad.get.subdataset-source-candidate-<name>

Clone candidates
^^^^^^^^^^^^^^^^

Let's first exemplify how a dataset can have several clone candidate locations.
Consider the case of the ``midterm_project`` subdataset that was created during the "Basics" part of the handbook:
Initially, as this dataset was created as a subdataset of ``DataLad-101``, its submodule entry in ``DataLad-101/.gitmodules`` [#f1]_ was a relative path (``./midterm_project``).
After it was published to :term:`GitHub` in the section on :ref:`yoda_project`, this dataset had a second clone candidate location: A URL to its GitHub repository.
A third location, finally, was created when publishing the dataset to the RIA store in the previous section :ref:`riastore`.
This makes three locations from where the ``midterm_project`` subdataset could potentially be obtained from.

Each of these locations can be encoded in the superdataset's ``.gitmodules`` file, but ``.gitmodules`` can encode only a single clone candidate.
Many use cases, however, benefit from or even require access to several clone candidates.
Consider the problem highlighted in :ref:`subdspublishing`:

When the ``DataLad-101`` dataset was published to :term:`GIN` in section :ref:`gin`, the ``.gitmodules`` entry of the ``midtermproject`` subdataset was still a relative path (``./midterm_project``).
While this relative path resolves locally on the same machine ``DataLad-101`` was created on, it does not resolve on :term:`Gin`.
Cloning ``DataLad-101`` recursively with ``midterm_project`` thus works when cloned locally from a path, but not when cloned from Gin.

Back in section :ref:`gin`, this problem was fixed by replacing the relative path in ``.gitmodules`` with the URL to the dataset sibling on GitHub.
But a more convenient solution would be to have several known locations for subdatasets that are attempted in succession -- if cloning from a local path fails, try the GitHub URL, and then the RIA store, and so forth.
Therefore, other than the ``.gitmodules`` entry, a dataset can encode other clone candidate sources  with a configuration variable as well.
Here is an overview on where subdataset clone candidates can be found:

#. Without any additional configuration, a subdataset is either registered underneath its superdataset with a relative path (if it was originally created in this dataset), or from the path or URL it was originally installed from. This is recorded in the ``.gitmodules`` file of the superdataset.

#. Alternatively, subdataset source candidates can be configured under the configuration variable ``datalad.get.subdataset-source-candidate-<name>``, where ``<name>`` is an arbitrary identifier, within either ``.datalad/config`` (if the configuration should stick with the dataset) or ``.git/config`` (if it should only apply to the dataset, but not its :term:`sibling`\s or clones).

A concrete example of a clone candidate configuration as well as further details can be found in the next paragraph.

Clone candidate priority
^^^^^^^^^^^^^^^^^^^^^^^^

We have established that subdatasets can come from several sources.
Let's now motivate *why* it might be useful to prioritize one subdataset clone location over another one.

Consider a hierarchy of datasets that exist in several locations, for example, one :term:`Remote Indexed Archive (RIA) store` *with* a storage special remote [#f2]_, and one without a special remote.
The topmost superdataset is published to a human-readable and accessible location such as :term:`GitHub` or :term:`GitLab`, and should be configured to always clone subdatasets from the RIA store *with* the storage special remote, even if it was originally created with subdatasets from the RIA store with no storage sibling.
In order to be able to retrieve subdataset *data* from the subdatasets after cloning the hierarchy of datasets, the RIA store with the storage special remote needs to be configured as a clone candidate.
Importantly, it should not only be configured as one alternative, but it should be configured as the first location to try to clone from -- else, cloning from the wrong RIA store could succeed and prevent any configured second clone candidate location from being tried.

.. importantnote:: Use case for clone priorities

   The most likely use case for such a scenario is in the case of centrally managed data with data administrators that provide and manage the data for their users.

The priority of subdataset clone locations is configured by attaching a *cost* to a source candidate ``<name>``.
The cost is a three digit value (range ``000-999``), and the lower the cost of a candidate, the higher its priority, i.e., the candidate with the lowest cost is attempted first.
In order to prefer any particular RIA store for subdataset cloning, one could configure the superdataset with the following command [#f3]_::

    $ git config -f .datalad/config datalad.get.subdataset-source-candidate-000mypreferredRIAstore ria+https://store.datalad.org#{id}

where ``mypreferredRIAstore`` is the (arbitrary) ``<name>`` of the source candidate, and the ``000`` prefix is the (lowest possible) cost.
Such a configuration will ensure that the first location any subdataset is attempted to be installed from is the RIA store at ``store.datalad.org``.
Only if the dataset is not found in there under its ID, other sources are tried.
Note that in the case where no cost is provided together with the candidate name, a default cost of ``700`` is used.

.. find-out-more:: What are the "default" costs for preexisting clone candidates?

   The following list provides and overview of which locations are attempted for cloning and their associated costs:

    - ``500`` for the superdatasets' remote URL + submodule path
    - ``600`` for the configured submodule URL in ``.gitmodules``
    - ``700`` for any unprioritized ``datalad.get.subdataset-source-candidate`` config
    - ``900`` for the local subdataset path


With the ``datalad.get.subdataset-source-candidate`` configuration any number of (differently named) clone candidates can be set and prioritized.
This allows precise access control over subdataset clone locations, and can -- depending on how many subdataset locations are known and functional -- speed up dataset installation.


Placeholders
^^^^^^^^^^^^

Instead of adding configurations with precise URLs you can also make use of templates with placeholders to configure clone locations more flexibly.
A placeholder takes the form ``{placeholdername}`` and can reference any property that can be inferred from the parent dataset's knowledge about the target superset, specifically any subdataset information that exists as a key-value pair within ``.gitmodules``.
For convenience, an existing `datalad-id` record is made available under the shortened name `id`.
In all likelihood, the list of available placeholders will be expanded in the future.
Do you have a use case and need a specific placeholder?
`Reach out to us <https://github.com/datalad/datalad/issues/new>`_, we may be able to add the placeholders you need!

When could this be useful?
For an example, consider how the clone candidate configuration above did not specify a concrete dataset in the RIA store, but used the ``{id}`` placeholder, which will expand to the subdataset's :term:`dataset ID` upon cloning.
This ensures that the clone locations point to the same RIA store, but stay flexible and dataset-specific.
You could configure a specific path or URL as a clone location, but this configuration is applied to *all* subdatasets.
Thus, whenever more than one subdataset exists in a superdataset, make sure to not provide a clone candidate configuration to a single, particular subdataset, as this could jeopardize the clone location of any other subdataset.


.. rubric:: Footnotes

.. [#f1] To re-read about ``.gitmodules`` files and their contents, please go back to section :ref:`config2`.

.. [#f2] To re-read about RIA stores and their ORA special remote storage siblings, please take a look at the section :ref:`riastore`.

.. [#f3] If you are unsure how the :gitcmd:`config` command works, please check out section :ref:`config`.
