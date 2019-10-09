.. _meta:

Extracting metadata
-------------------

.. todo::

   - explain the concept of an extractor
   - showcase metadata extraction in the longnow subdataset
   - talk about the datalad-metalad extension. Possibly have a reference to some yet
     unwritten part about extensions.
   - commands to introduce: meta-dump (instead of metadata), meta-extract, meta-aggregate
   - make a point about metadata for potentially all kinds of domains, find examples on how to
     make use of them, mention Google dataset search.

Metadata extractors
^^^^^^^^^^^^^^^^^^^

An extractor provides the ability to extract and structure certain
information from a dataset and/or its contents. The exact type of
information that is obtained about dataset (content) is dependent
on the extractor used for this task: Some extractors can express
DataLad's or Git-annex's internal metadata representation, such
as the relationship of super- and subdatasets, or the date a file was
created. Others can express image metadata, XMP-compliant metadata,
or audio file metadata.

The extractors either come with DataLad [#f1]_ or with its extensions,
providing a range of extractors for particular domains and formats.
The command :command:`datalad aggregate-metadata` retrieves (*aggregates*)
the metadata within a dataset based on the extractors that are
*enabled* -- by default, not all possible types of metadata are
extracted. Rather, a user can enable as many extractors as they
wish for the precise type(s) of metadata they require. The only
metadata acquired by default are DataLad's and Git-annex's internal
metadata representations, using the extractors ``datalad_core`` and
``annex``.

As such, in order to use an extractor, one needs to enable it. This
is done on a dataset level within ``.datalad/config`` in the
``datalad.metadata.nativetype`` configuration variable -- either with
the :command:`git config` command or a text editor. For example, to
enable the ``audio`` extractor, one would run

.. runrecord:: _examples/DL-101-151-101
   :language: console
   :workdir: dl-101/tmp

   $ git config -f .datalad/config --add datalad.metadata.nativetype audio

To also enable metadata extraction from ``datapackage.json`` files from
the `Frictionlessdata <https://frictionlessdata.io/specs/data-package/>`_
specification with the ``frictionless_datapackage`` extractor, one would
run

.. runrecord:: _examples/DL-101-151-102
   :language: console
   :workdir: dl-101/tmp

   $ git config -f .datalad/config --add datalad.metadata.nativetype frictionless_datapackage

This leads to two new entries inside of ``.datalad/config``:

.. runrecord:: _examples/DL-101-151-103
   :language: console
   :workdir: dl-101/tmp

As enabling extractors is done in ``.datalad/config``, enabled extractors
are a dataset specific configuration that is shared together with
the dataset.

With this given configuration, upon using the
:command:`datalad aggregate-metadata` command,
metadata from four domains will be acquired, if possible:
DataLad's and Git-annex's internal metadata representation, metadata
about audio files, and metadata from ``datapackage.json`` files.

Metadata aggregation
^^^^^^^^^^^^^^^^^^^^

All extractors are run sequentially -- this means each of them can
throw their own error messages.

Metadata representation
^^^^^^^^^^^^^^^^^^^^^^^

Aggregated metadata is stored in ``.datalad/metadata``. If you are interested
in more details about the contents of the directory you can checkout the
following hidden section.


.. findoutmore:: Metadata representation in detail

   There are two main elements inside of ``.datalad/metadata``:

   - a metadata inventory ``aggregate_v1.json``, and
   - a store for metadata "objects"

   .. runrecord:: _examples/DL-101-151-120
      :language: console
      :workdir: dl-101/tmp

      $ tree --filelimit=5

   The file ``aggregate_v1.json`` (the inventory) is a JSON file. It contains
   (nested) dictionaries with ``key:value`` pairs. Within one top-level dictionary,
   each subdataset and the superdataset has an individual record. The relative
   path to the dataset from the superdataset is the key for this record, and each
   record is a dictionary that contains the following elements with information
   related to the given dataset:

   - id: the datasets :term:`UUID`.
   - refcommit: The :term:`shasum` of the last metadata-relevant commit in the
     history of the dataset. Metadata-relevant commits are any commits that modify
     dataset content that is not exclusively concerning DataLad’s own internal status and configuration.
   - datalad_version: version string of the DataLad version that was used to perform the metadata extraction [#f7]_.
   - extractors: list of all enabled extractors for the dataset.
   - content_info, dataset_info: Path to the object files containing the actual metadata on the dataset
     as a whole, and on individual files in a dataset (content). Paths are to be interpreted relative to
     the inventory file, and point to the metadata object store.

   .. todo::

      example json here, as in documentation

   As such, this JSON file summarizes very high-level information about the metadata
   for a dataset, but it does not contain the actual metadata. This is stored inside
   of ``.datalad/metadata/objects``, an object store for the actual metadata managed
   by :term:`Git-annex`. The paths in the ``content_info`` and ``dataset_info``
   elements in the inventory file point to the metadata content that lives inside of
   this object store. There is one file for all dataset metadata, and one file for
   all dataset content metadata.

   .. todo::

      - about possibility for compression, and storing in Git versus Git-annex
      - JSON-LD explanation/demonstration





.. rubric:: Footnotes

.. [#f1] An overview over DataLads metadata extractors can be found
         `here <http://docs.datalad.org/en/latest/metadata.html#supported-metadata-sources>`_.

.. [#f7] It is the version of DataLad used to perform *extraction*, not necessarily *aggregation*,
         as pre-extracted metadata can be aggregated from other superdatasets for a dataset that is
         itself not available locally