.. _metalad:

Metadata-Management with MetaLad
--------------------------------

For many years, :term:`metadata` related functionality was included in the DataLad core package.
A modernized approach, however, is developed in the `datalad-metalad extension <http://docs.datalad.org/projects/metalad/en/latest/>`_.

.. figure:: ../artwork/src/metadata.svg


What is MetaLad?
................

MetaLad is an extension to DataLad that allows you to associate metadata with a dataset, a subdataset, or a file. "What is 'metadata' then?" you might ask. Very simply put: metadata is data about data. In principle any kind of data could be metadata. What makes it metadata is the fact that is associated with some "primary" data and usually describes the primary data in some way. For example: in a library, the catalog contains metadata about the items in the library, including, for example, their location. Another example for metadata is the creation time of a file on a file system. The creation time is metadata about the file. The file itself is the primary data. Another example for metadata that is often associated with a file would be the id of the creator. File systems have mechanisms to associate metadata with files. DataLad has also a mechanism to associate metadata with datalad datasets and their items. This mechanism is MetaLad.

Metadata can be extracted automatically from primary data, it can be created manually and it can be transported separately from primary data. You can dump all metadata and, for example, store it in a file, or search through it with a tool of your choice.

The basic philosophy of metalad is: you provide arbitrary metadata, give it a name, and associate it with a specific version of a file or dataset. Metalad will store this association, allow you to transport metadata, and allow you to query the metadata.

Installation of metalad:

Metalad is installed by using `pip install datalad-metalad`. As with datalad, you might want to do that in a virtual environment.


Primary Data and Metadata
.........................

Which metadata can be associated:

MetaLad can associate metadata with dataset items, i.e. with a dataset, subdatasets, and files. Each item can have an arbitrary number of metadata elements assigned to them. The metadata elements are distinguished and identified by a name that identifies their type. The metadata content is defined to be a JSON-object. This object can have an arbitrary structure. This allows you to create your own metadata format and to represent all existing metadata formats. Metalad is able to associate paths in datasets with an arbitrary number of metadata in different formats. Metalad recognizes whether the path points to a dataset of

Metadata Example
----------------

What does metadata do for you? Generally metadata provides additional information about primary data. This allows to identify primary data that has certain properties which may be in contained within the primary data -and probably automatically extracted from there- or may be assigned to primary data based on an external policy.

Here are just a few examples for metadata from the virtually unlimited metadata space:

1. Full text for scanned book pages (automatically extracted by OCR or manually created)
2. Usage information, e.g. license, in-group, in-organization, global
3. Context information, e.g. publications based on data
4. Structural data (dataset containment, modification date, hash) this can provide basic
   structural information even without access to the primary data
5. Special search indices, e.g. graph-based search indices, search index for chess-games....
6. Anonymized information extracted from medical documents.
7. Information about software, e.g. security assessments, citation.cff

As long as the metadata-format has unique names, they can all be used simultaneously.

Whether metadata is associated with the dataset or individual files is dependent on the nature of the metadata and the envisioned use. Metadata that describe dataset level properties should be associated with the dataset, e.g. dataset owner, dataset authors, dataset licenses, names of contained files, etc. Metadata that describes file level properties should be associated with the file, e.g. file-checksum. Although it seems unnecessary to record the names of contained files or file properties in metadata, it can be very useful, if a user receives only metadata and not primary data (see chapter XXX).


Let's look at a more concrete example. We have a datalad dataset that contains a single PNG-file called "picture.png"

dataset_0
     picture_1.png

Let's assume there is metadata stemming from an advance AI called "Picture2Words" that is able to describe the content of images. In this case the AI describes the image as::

  A lake with waterlilies in a front of snow covered mountains

We would like to add this description as metadata to the file ``./picture_1.png``. As mentioned above we have to select a name to identify the metadata format. We chose: ``Picture2Words``. Now we can use the command ``meta-add`` to add metadata. ``meta-add`` adds metadata into the git repository of the dataset (or any git-repository that you chose). It reads individual metadata entries from the command line or from standard input. The entries are JSON objects that identify the type of metadata (``file`` or ``dataset``), the file or dataset with which metadata should be associated, the identifier of the dataset, the version of the dataset to which metadata is associated, the name of the metadata format, and the metadata itself. There are a few more properties in the JSON object, describing the author of the metadata, the name of the metadata extractor, its version, and its parameterization.
 For our example we could just handcraft the following record::

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

and, for convenience, save it as ``metadata-image_1.json``. Then we can use the command ``meta-add`` to add the metadata to the current dataset::

 > datalad meta-add -d dataset_0 - < metadata-image_1.json

This command will store metadata in the git repository of ``dataset_0``. You might have to adjust the dataset_id to the real id of the dataset, found via the command ``datalad configuration get datalad.dataset.id``, or you provide the switch ``-i`` to ``meta-add``, which tells it to just warn about id mismatches.

Generally metadata can either be provided manually, by running ``extractors`` (datalad-metalad plugins that extract certain metadata from primary data), or by any other means that create correct metadata records. For example, you could copy the complete metadata from ``dataset_0`` to ``dataset_1``, by issuing the command::

 > datalad meta-dump -d dataset_0 -r | datalad meta-add -d dataset_1 --json-lines -

After the metadata has been added, you can view it via the command ``meta-dump``. The simplest form is ``meta-dump -r``, which will show all metadata that is stored in the git-repository of the dataset in the current directory. You can give a dataset-file-path-pattern to ``meta-dump``, much like an argument to ``ls``, that identifies dataset-ids and versions and a file within the dataset. The two parts are separated by ``:``. So::

 > datalad meta-dump -d dataset_0 .:picture_1.png

would just dump all metadata for ``picture_1.png``.


Distributing and Getting Metadata
---------------------------------

Instead of creating and adding metadata yourself, you can download metadata from remote git repositories, i.e. from remote datalad datasets. Also, if you have created your metadata and added it to a git repository (of a datalad dataset), you can export it into other git-repositories. Note that this export will only export the metadata itself, not the primary data.

Download Metadata from a Git-Repository
---------------------------------------

First create a git repository that should hold the downloaded metadata::

 > git init metadata-repo
 > cd metadata-repo

Now fetch metadata from the demo repository on github, i.e. from ``https://github.com/christian-monch/metadata-test.git`` demo repository::

 > git fetch "https://github.com/christian-monch/metadata-test.git" "refs/datalad/*:refs/datalad/*"

The metadata is now locally available in the git repository ``metadata-repo``. You can verify this by issuing the command ``datalad meta-dump -r``, which will list all metadata in the repository.


Publish Metadata to a Git-Repository
------------------------------------

You can also push your metadata to a remote Git-repository (if you have write-authorization). Let's assume you are in the directory that contains the git repository with your metadata, then you can push your metadata to a remote git repository ``<your repository>``::

 > git push "<your repository>" "refs/datalad/*:refs/datalad/*"

You will notice that no primary data is stored in the repository ``metadata-destination``. That allows you to publish metadata without publishing the primary data at the same time.


Querying metadata remotely:
---------------------------

You do not have to download metadata to dump it. It is also possible to specify a git-repository, and let metalad only read the metadata that it requires to fulfill your request. For example::

 > datalad meta-dump -d  https://github.com/christian-monch/metadata-test.git ./study-100

Would only download enough data to dump all metadata in the specified dataset tree-path. If you want to see all metadata in the git repository you could issue the following command::

 > datalad meta-dump -d  https://github.com/christian-monch/metadata-test.git -r

This will take a lot longer than the previous command because datalad has to fetch more item from the remote repository. If you use the remote meta-dump option properly, you can quickly examine small subsets of very large metadata repositories.
