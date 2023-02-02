.. _metalad:

Metadata-Management with MetaLad
--------------------------------

For many years, :term:`metadata` related functionality was included in the DataLad core package.
A modernized approach, however, is now developed in the `datalad-metalad extension <http://docs.datalad.org/projects/metalad/en/latest/>`_.

.. figure:: ../artwork/src/metadata.svg

MetaLad is a :term:`DataLad extension` that allows you to

* associate :term:`metadata` with a dataset, a subdataset, or a file,
* extract metadata automatically from primary data or handle manually supplied metadata,
* transport metadata separately from primary data,
* dump metadata and, for example, store it in a file, or search through it with a tool of your choice.

The basic philosophy of MetaLad is: A user provides arbitrary metadata, gives it a name, and associates it with a specific version of a file or dataset. MetaLad will store this association, enable metadata transport, and allow  metadata queries.

Primary Data versus Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You now might ask: "What is 'metadata' then?"
Very simply put: Metadata is data about data.
In principle, any kind of data could be metadata. What makes it metadata is the fact that it is associated with some "primary" data, and usually describes the primary data in some way.
Consider two simple examples from the physical and the digital world: A library catalog contains metadata about the library's books, such as their *location*; and a file system stores the *creation time* of a file as well as the *user ID* of its creator.
The location, creation time, or creator ID is metadata, while the book in the library or the file on the file system are the primary data the metadata is associated with.

And what does metadata do for you?
Generally, metadata provides additional information about primary data.
This allows to identify primary data with certain properties.
These properties could either be contained within the primary data and (automatically) extracted from it, such as digital photographs captured in a specific time frame, or assigned to primary data based on an external policy (such as the directory "Hiking in the alps 2019" on your phone).
Importantly, primary data can have virtually unlimited different metadata associated with it, depending on what is relevant in a given context.
Consider a publication in a medical field, and a few examples for metadata about it from the virtually unlimited metadata space:

1. The full text for the scanned PDF (manually created, or automatically extracted by `optical character recognition <https://en.wikipedia.org/wiki/Optical_character_recognition>`_)
2. Citation information, such as the geographic origin of citing papers or type of media outlet reporting about it
3. Context information, e.g. publications based on similar data
4. Structural data about the underlying medical acquisitions, (such as dataset containment, modification date, or hash) which can provide basic
   structural information even without access to the primary data
5. Special search indices, e.g. graph-based search indices, medical abbreviations
6. Anonymized information extracted from medical documents.
7. Information about the used software, e.g. security assessments, citation.cff

Often, specific metadata is known as metadata of a given format or an ontology, and different metadata formats are useful in different contexts.

Adding metadata with MetaLad
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Whether metadata is associated with the dataset or individual files inside of it is dependent on the nature of the metadata and the envisioned use.
Metadata that describe *dataset level* properties should be associated with the dataset, e.g. dataset owner, dataset authors, dataset licenses, or names of contained files.
Metadata that describes *file level* properties should be associated with the file, e.g. file :term:`checksum`\s.
Although it seems unnecessary to record the names of contained files or file properties in metadata, it can be very useful if a user receives only metadata and not primary data, for example in case of highly sensitive data where actual file content cannot be shared.

Let's look at a concrete example.
We have a DataLad dataset ``dataset_0` that contains a single PNG-file called ``picture_1.png``::

   $ tree dataset_0
   dataset_0
      └── picture_1.png
   0 directories, 1 file


Let's assume there is metadata stemming from an advance AI called ``Picture2Words`` that is able to describe the content of images.
In this case the AI describes the image as::

  A lake with waterlilies in front of snow covered mountains


We would like to add this description as metadata to the file ``./picture_1.png``.
One distinct feature of MetaLad is that it can simultaneously use various metadata formats.
The only requirement is that each different metadata format is uniquely named.
Therefore, we have to select a name to identify the metadata format.
We chose: ``Picture2Words``.
Now we can use the :command:`meta-add` command to add metadata.
``meta-add`` adds metadata into the dataset (or any :term:`Git` repository that you chose).

In order to include metadata in the dataset, ``meta-add`` requires a metadata entry to be in a certain format, in particular, a JSON object [#f1]_.
Such objects can then be read from the command line or from standard input (:term:`stdin`).
Each metadata JSON object must contain information about the level the metadata applies to (``file`` or ``dataset``), the file or dataset with which metadata should be associated as a path, the :term:`dataset ID` and version, the name of the metadata format, and the metadata itself.
The examplary, hand-crafted record below even contains a few additional properties, describing the author of the metadata, the name of the metadata extractor, its version, and its parameterization::

    {
      "type": "file",
      "dataset_id": "52142b84-dc76-11ea-98c5-7cdd908c7490",
      "dataset_version": "244a8ad43b00622989ae7f0d2b59c80697dadb80",
      "path": "picture_1.png",
      "extractor_name": "Picture2Words",
      "extractor_version": "0.1",
      "extraction_parameter": {},
      "extraction_time": 1675113291.1464975,
      "agent_name": "Datalad User",
      "agent_email": "datalad.user@example.com",
      "extracted_metadata": {
        "description": "A lake with waterlilies in a front of snow covered mountains"
      }
    }

For convenience, we can create such a JSON object in an editor, and save it as ``metadata-image_1.json``.
Afterwards, we can redirect the content of the file into the :command:`meta-add` command in the command line.
The call below would add the metadata to the current dataset, ``dataset_0``::

    $ datalad meta-add -d dataset_0 - < metadata-image_1.json

If you want to try it out yourself, make sure to adjust the ``dataset_id`` to the ID of your own dataset, found via the command ``datalad configuration get datalad.dataset.id``.
Alternatively, provide the switch ``-i`` to ``meta-add``, which tells it to just warn about ID mismatches instead of erroring out.

Generally, metadata can either be provided

* manually,
* by running :term:`extractor`\s (``datalad-metalad`` plugins that extract certain metadata from primary data),
* or by any other means that create correct metadata records. For example, you could copy the complete metadata from ``dataset_0`` to ``dataset_1``, by dumping it from one dataset into another::

    $ datalad meta-dump -d dataset_0 -r | \
      datalad meta-add -d dataset_1 --json-lines -

After the metadata has been added, you can view it via the command :command:`meta-dump`.
The simplest form of this command is ``meta-dump -r``, which will show all metadata that is stored in dataset in the current directory.
To get more specific metadata records, you can give a dataset-file-path-pattern to ``meta-dump``, much like an argument to ``ls``, that identifies :term:`dataset ID`, version and a file within the dataset.
The two parts are separated by ``:``. So::

    $ datalad meta-dump -d dataset_0 .:picture_1.png

would just dump all metadata for ``picture_1.png``.


Distributing and Getting Metadata
"""""""""""""""""""""""""""""""""

Instead of creating and adding metadata yourself, you can download metadata from remote DataLad datasets.
Likewise, metadata added into one dataset can be exported into other dataset.
Such an export will only export the metadata itself, not the primary data.

Download Metadata from a Git-Repository
"""""""""""""""""""""""""""""""""""""""

First create a git repository that should hold the downloaded metadata::

    $ git init metadata-repo
    $ cd metadata-repo

Now fetch metadata from the demo repository on :term:`GitHub`, i.e. from ``https://github.com/christian-monch/metadata-test.git`` demo repository::

    $ git fetch "https://github.com/christian-monch/metadata-test.git" "refs/datalad/*:refs/datalad/*"

The metadata is now locally available in the Git repository ``metadata-repo``.
You can verify this by issuing the command ``datalad meta-dump -r``, which will list all metadata in the repository.


Publish metadata to a Git-Repository
""""""""""""""""""""""""""""""""""""

You can also push your metadata to a remote Git-repository (if you have write-authorization). Let's assume you are in the directory that contains the git repository with your metadata, then you can push your metadata to a remote git repository ``<your repository>``::

 > git push "<your repository>" "refs/datalad/*:refs/datalad/*"

You will notice that no primary data is stored in the repository ``metadata-destination``. That allows you to publish metadata without publishing the primary data at the same time.


Querying metadata remotely
""""""""""""""""""""""""""

You do not have to download metadata to dump it. It is also possible to specify a git-repository, and let metalad only read the metadata that it requires to fulfill your request. For example::

 > datalad meta-dump -d  https://github.com/christian-monch/metadata-test.git ./study-100

Would only download enough data to dump all metadata in the specified dataset tree-path. If you want to see all metadata in the git repository you could issue the following command::

 > datalad meta-dump -d  https://github.com/christian-monch/metadata-test.git -r

This will take a lot longer than the previous command because datalad has to fetch more item from the remote repository. If you use the remote meta-dump option properly, you can quickly examine small subsets of very large metadata repositories.


Installation
^^^^^^^^^^^^

MetaLad is a stand-alone Python package, and can be installed using

.. code-block:: bash

   pip install datalad-metalad

As with DataLad and other Python packages, you might want to do the installation in a :term:`virtual environment`.


.. rubric:: Footnotes

.. [#f1] `JSON <https://en.wikipedia.org/wiki/JSON>`_ is a language-independent, open and lightweight data interchange format. Data is represented as human readable text, organized in key-value pairs (e.g., 'name': 'Bob') or arrays, and thus easily readable by both humans and machines. A *JSON object* is a collection of key-value pairs. Its enclosed in curly brackets, and individual pairs in the object are separated by commas.