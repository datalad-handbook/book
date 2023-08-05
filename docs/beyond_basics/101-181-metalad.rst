.. _metalad:

Metadata-Management with MetaLad
--------------------------------

For many years, :term:`metadata` related functionality was included in the DataLad core package.
A modernized approach, however, is now developed in the `datalad-metalad extension <https://github.com/datalad/datalad-metalad>`_.

.. figure:: ../artwork/src/metadata.svg

MetaLad is a :term:`DataLad extension` that allows you to

* associate :term:`metadata` in any format with a dataset, a subdataset, or a file,
* extract metadata automatically from primary data or handle manually supplied metadata,
* transport metadata separately from primary data,
* dump metadata and, for example, store it in a file, or search through it with a tool of your choice.

The following section illustrates relevant concepts, commands, and workflows.

Primary Data versus Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might ask upfront: "What is 'metadata'?"
Very simply put: Metadata is data about data.
In principle, any kind of data could be metadata. What makes it metadata is the fact that it is associated with some "primary" data, and usually describes the primary data in some way.
Consider two simple examples from the physical and the digital world: A library catalog contains metadata about the library's books, such as their *location*; and a file system stores the *creation time* of a file as well as the *user ID* of its creator.
The location, creation time, or creator ID is metadata, while the book in the library or the file on the file system are the primary data the metadata is associated with.

And what does metadata do for you?
Generally, metadata provides additional information about primary data.
This allows to identify primary data with certain properties.
These properties could either be contained within the primary data and (automatically) extracted from it, such as digital photographs captured in a specific time frame at a specific GPS location, or assigned to primary data based on an external policy, such as the directory "Hiking in the alps 2019" on your phone.

Importantly, primary data can have virtually unlimited different metadata associated with it, depending on what is relevant in a given context.
Consider a publication in a medical field, and a few examples for metadata about it from the virtually unlimited metadata space:

1. The full text for the scanned PDF (manually created, or automatically extracted by `optical character recognition <https://en.wikipedia.org/wiki/Optical_character_recognition>`_)
2. Citation information, such as the geographic origin of citing papers or type of media outlet reporting about it
3. Context information, e.g. publications based on similar data
4. Structural data about the underlying medical acquisitions (such as dataset containment, modification date, or hash), which can provide basic
   structural information even without access to the primary data
5. Special search indices, e.g. graph-based search indices, medical abbreviations
6. Anonymized information extracted from medical documents.
7. Information about the used software, e.g. security assessments, `citation.cff <https://citation-file-format.github.io>`_

MetaLad's *extractor* concept
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the context of MetaLad, each one of those metadata examples above would be called a *schema*, and a process or tool deriving or generating a given schema would be called an *extractor*.

Different metadata schemas are useful in different contexts:
In the example above, citation metadata might come in handy when evaluating the impact of the scientific finding, whereas the publications full text and special search indices could be used for automated meta-analyses.
To allow a variety of metadata use cases, MetaLad can use various metadata schemas simultaneously - if you want to, all schemas from the example above and many more could be created and managed in the same dataset in parallel.

To handle different schemas in parallel, MetaLad represents them based on unique identifiers of the extraction process that generated them.
For example, the automatically scanned full text might be identified with an extractor name ``OCR``, and that of the citation data could be called "`altmetric <https://en.wikipedia.org/wiki/Altmetric>`_".
But while the term "extractor" has a technical feel to it, an "extractor" can also be the manual process of annotating arbitrary information about a file - nothing prevents metadata from medical annotations to be called ``Sam-tracing-brain-regions-by-hand``.

In addition to identifying schemas via extractor names, MetaLad and other :term:`DataLad extension`\s ship with specialized extractor tools to extract metadata of a certain schema.
Likewise, `anyone can build their own extractor to generate schemas of their choice <http://docs.datalad.org/projects/metalad/en/latest/user_guide/writing-extractors.html>`_.
But before we take a closer look into that, let's illustrate the metadata concepts and commands of MetaLad with a toy example.

Adding metadata with meta-add
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the context of DataLad datasets, metadata can either be associated with entire datasets or individual files inside of it.
Whether a piece of information is *dataset level* or *file level* metadata is dependent on the nature of the metadata and the envisioned use.
Metadata that describe dataset level properties could be dataset owner, dataset authors, dataset licenses, or names of contained files [#f1]_, whereas metadata that describe file level properties could be file :term:`checksum`\s or file-specific information like the time-stamp of a photograph.

.. gitusernote:: Metadata is stored in Git

   When MetaLad adds metadata to your datasets, it will store the metadata in :term:`Git` only. Thus, even a plain Git repository is sufficient to work with ``datalad-metalad``. However, the metadata is stored in an unusual and somewhat hidden place, inside of the `Git object store <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>`_. If you're interested in the technical details, you can find a :ref:`Findoutmore <fom-metadataobjecttree>` a bit further down in this section.


Let's look at a concrete example.
We have a DataLad dataset ``cozy-screensavers`` that contains a single PNG-file called ``zen.png``.

.. runrecord:: _examples/DL-101-181-101
   :language: console
   :workdir: beyond_basics/meta

   $ datalad clone https://github.com/datalad-handbook/cozy-screensavers.git
   $ cd cozy-screensavers

.. runrecord:: _examples/DL-101-181-102
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ tree

.. runrecord:: _examples/DL-101-181-103
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ datalad get zen.jpg

Let's assume there is metadata stemming from an advanced AI called ``Picture2Words`` that is able to describe the content of images - in other words, this AI would be able to extract certain metadata from the file.
In this case the AI describes the image as

.. code-block:: bash

   "A lake with waterlilies in front of snow covered mountains"

We would like to add this description as metadata to the file ``./zen.png``, and will identify it with a name corresponding to its extractor, ``"Picture2Words"``.


In order to include metadata in a dataset, users need to provide a metadata entry to the :command:`meta-add` command.
This metadata entry has two major requirements: It needs to be supplied in a certain format, in particular, as a JSON object [#f2]_, and it needs to include a set of required information in defined fields.
Let's take a look at the JSON object we could generate as a metadata entry for ``zen.png`` and identify required fields::

    {
      "type": "file",
      "path": "zen.png",
      "dataset_id": "2d540a9d-2ef7-4b5f-8931-7c92f483f0c7",
      "dataset_version": "19f2d98d758116d099d467260a5a71082b2c6a29",
      "extractor_name": "Picture2Words",
      "extractor_version": "0.1",
      "extraction_parameter": {},
      "extraction_time": 1675113291.1464975,
      "agent_name": "Overworked CTO",
      "agent_email": "closetoburnout@randomtechconsultancy.com",
      "extracted_metadata": {
        "description": "A lake with waterlilies in a front of snow covered mountains"
      }
    }

When adding file-level metadata to a dataset that contains the file, the metadata JSON object must contain:

* information about the level the metadata applies to (``type``, with ``file`` instead of ``dataset`` as a value),
* the file the metadata belongs to with a ``path``,
* the :term:`dataset ID` (``dataset_id``) and version (``dataset_version``),
* an joint identifier for the metadata extractor and schema ``extractor_name`` (i.e., ``Picture2Words``, as well as details about the metadata extractor like its version (``extractor_version``), its parameterization (``extraction_parameter``), and the date and time of extraction (``extraction_time``) in the form of a Unix time stamp [#f3]_,
* information about the agent supplying the metadata (``agent_name`` and ``agent_email``),
* and finally the metadata itself (``extracted_metadata``).

While certain extractors can generate metadata entries automatically, or one could write scripts wrapping extracting tools to generate them, we can also create such a JSON object manually, for example in an editor.
A valid metadata entry can then be read into ``meta-add`` either from the command line or from standard input (:term:`stdin`).
For example, we can save the metadata entry above as ``metadata-zen.json``:

.. runrecord:: _examples/DL-101-181-104
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ cat << EOT > metadata-zen.json
   {
     "type": "file",
     "path": "zen.png",
     "dataset_id": "2d540a9d-2ef7-4b5f-8931-7c92f483f0c7",
     "dataset_version": "19f2d98d758116d099d467260a5a71082b2c6a29",
     "extractor_name": "Picture2Words",
     "extractor_version": "0.1",
     "extraction_parameter": {},
     "extraction_time": 1675113291.1464975,
     "agent_name": "Overworked CTO",
     "agent_email": "closetoburnout@randomtechconsultancy.com",
     "extracted_metadata": {
     "description": "A lake with waterlilies in a front of snow covered mountains"
	 }
   }
   EOT

Then, we redirect the content of the file into the :command:`meta-add` command in the command line.
The following call would add the metadata entry to the current dataset, ``cozy-screensavers``:


.. runrecord:: _examples/DL-101-181-105
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ datalad meta-add -d . - < metadata-zen.json

.. find-out-more:: meta-add validity checks

	When adding metadata for the first time, its not uncommon to run into errors.
	Its quite easy, for example, to miss a comma or quotation mark when creating a JSON object by hand.
	But there are also some internal checks that might be surprising.
	If you want to add the metadata above to your own dataset, you should make sure to adjust the ``dataset_id`` to the ID of your own dataset, found via the command ``datalad configuration get datalad.dataset.id`` - otherwise you'll see an error [#f4]_, and likewise the ``dataset_version``.
	And in case you'd supply the ``extraction_time`` as "this morning at 8AM" instead of a time stamp, the command will be unhappy as well.
	In case an error occurs, make sure to read the error message, and turn the the commands' ``--help`` for insights about requirements you might have missed.

After the metadata has been added, you can view it via the command :command:`meta-dump`.
The simplest form of this command is ``meta-dump -r``, which will show all metadata that is stored in the dataset in the current directory.
To get more specific metadata records, you can give a dataset-file-path-pattern to ``meta-dump``, much like an argument to ``ls``, that identifies :term:`dataset ID`, version and a file within the dataset.
The two parts are separated by ``:``. The following line would just dump all metadata for ``zen.png``.

.. runrecord:: _examples/DL-101-181-106
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ datalad meta-dump -d . .:zen.png

This could also be printed a bit more readable:

.. runrecord:: _examples/DL-101-181-107
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ datalad -f json_pp meta-dump -d . .:zen.png

.. find-out-more:: More complex metadata-dumps

   TODO: add complex Dataset-file-path-pattern examples, e.g., with UUIDs, versions, etc

Using existing extractors to add metadata
"""""""""""""""""""""""""""""""""""""""""

If writing JSON objects by hand sounds cumbersome, it indeed is.
To automate metadata extraction or generation, MetaLad can use extractors to do the job.
A few built-in extractors are already shipped with it, for example ``annex`` (reporting on information :term:`git-annex` provides about datasets or files), or ``studyminimeta`` (a `metadata schema for archived studies <https://github.com/christian-monch/datalad-metalad/blob/nf-archived_study_metadata/tools/archive_metadata_validator/docs/source/archived-study-metadata-handbook.rst>`_).
Once an extractor of choice is found, the :command:`datalad meta-extract` command can do its job:

.. runrecord:: _examples/DL-101-181-108
   :language: console
   :workdir: beyond_basics/meta/cozy-screensavers

   $ datalad meta-extract -d . metalad_core | jq

The extracted metadata can then either be saved into a file as before, or directly :term:`pipe`'d into :command:`meta-add`.

Creating your own extractor
"""""""""""""""""""""""""""

The MetaLad docs have a dedicated user guide that walks you through the process of creating your own extractor. Have a look at `docs.datalad.org/projects/metalad/user_guide/writing-extractors.html <http://docs.datalad.org/projects/metalad/en/latest/user_guide/writing-extractors.html>`_.


Distributing and Getting Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once metadata has been added to a dataset, it can be distributed and retrieved.
Instead of creating and adding metadata yourself, you could download fitting pre-existing metadata.
Similarly, instead of repeating a ``meta-add`` process for one and the same files across hierarchies of datasets, metadata added into one dataset can be exported into other datasets.
Regardless of whether it is a distribution or a retrieval process, though, an export with MetaLad will only concern the *metadata*, and never the primary data.

Download Metadata from a remote repository
""""""""""""""""""""""""""""""""""""""""""

Let's start by creating a place where someone else's metadata could live.

.. runrecord:: _examples/DL-101-181-110
   :language: console
   :workdir: beyond_basics/meta

   $ datalad create metadata-assimilation
   $ cd metadata-assimilation

Because MetaLad stores metadata in :term:`Git`'s object store, we use Git to directly fetch metadata from a remote repository, such as this demo on :term:`GitHub`: ``https://github.com/christian-monch/metadata-test.git``.
Because metadata added by MetaLad is not transported automatically but needs to be specifically requested, the command to retrieve it looks unfamiliar to non-Git-users: It identifies the precise location of the :term:`ref` that contains the metadata.

.. runrecord:: _examples/DL-101-181-111
   :language: console
   :workdir: beyond_basics/meta/metadata-assimilation

   $ git fetch \
      "https://github.com/christian-monch/metadata-test.git" \
      "refs/datalad/*:refs/datalad/*"


.. find-out-more:: Exactly where is metadata stored, and why?
   :name: fom-metadataobjecttree

   MetaLad employs an internal metadata model that makes the following properties possible:

   * Metadata has a version encoded, but isn't itself version controlled
   * Metadata should not be transported if not explicitly requested
   * It should be possible to only retrieve parts of the overall metadata tree, e.g. certain sub-nodes

   To fulfill this, metadata is stored in Git's internal object store as a `blob <https://git-scm.com/book/en/v2/Git-Internals-Git-Objects>`_, and Git :term:`ref`\'s are used to point to these blobs.
   To not automatically transport them, they are organized in a directory that isn't fetched or pushed by default, but can be transported by explicitly fetching or pushing it: ``.git/refs/datalad`` [#f5]_.

   After fetching these refs, they can be found in the ``metadata-assimilation`` dataset:

    .. runrecord:: _examples/DL-101-181-113
       :language: console
       :workdir: beyond_basics/meta/metadata-assimilation

       $ tree .git/refs

    Just like other Git :term:`ref`\s, these refs are files that identify Git objects or trees.
    By utilizing Git's internal plumbing commands, we can follow them:

    .. runrecord:: _examples/DL-101-181-114
       :language: console
       :workdir: beyond_basics/meta/metadata-assimilation

       $ cat .git/refs/datalad/dataset-tree-version-list

    .. runrecord:: _examples/DL-101-181-115
       :language: console
       :workdir: beyond_basics/meta/metadata-assimilation
       :realcommand: echo "$ git show $(cat .git/refs/datalad/dataset-tree-version-list) | jq" && git show $(cat .git/refs/datalad/dataset-tree-version-list) | jq

    .. runrecord:: _examples/DL-101-181-116
       :language: console
       :workdir: beyond_basics/meta/metadata-assimilation
       :realcommand: echo "$ git ls-tree $(git show $(cat .git/refs/datalad/dataset-tree-version-list) | jq | grep "location" | awk '{gsub(/"/, "", $2); print $2}') " && git ls-tree $(git show $(cat .git/refs/datalad/dataset-tree-version-list) | jq | grep "location" | awk '{gsub(/"/, "", $2); print $2}')

    The identifier ``study-100`` in a line such as ``040000 tree d1ad9bfa56f5aa25a1d28caf13db719b9e710d28	study-100`` is the ``dataset_path`` value of a given metadata entry.
    Commands such as ``meta-dump`` can use them to, e.g., only report on metadata for certain datasets, following the pattern

    .. code-block::

       [DATASET_PATH] ["@" VERSION-DIGITS] [":" [LOCAL_PATH]]

    e.g., ``./study-100``.
    While this is no workflow a user would have to do, this exploration might have nevertheless gotten you some insights into the inner workings of the commands and MetaLad's internal storage model.

The metadata is now locally available in the Git repository ``metadata-repo``.
You can verify this by issuing the command ``datalad meta-dump -r``, which will list all metadata from all ``dataset_path``\s in the repository.
Can you guess what type of metadata it contains [#f6]_ ?

.. runrecord:: _examples/DL-101-181-112
   :language: console
   :workdir: beyond_basics/meta/metadata-assimilation

   $ datalad meta-dump -r

A final note is that :command:`meta-dump` can also be a source of metadata for :command:`meta-add`.
While metadata can indeed be provided manually, or by running :term:`extractor`\s as outlined so far, it can also be provided by any other means that create correct metadata records, and :command:`meta-dump` is one of them.
For example, you could copy the complete metadata from ``dataset_0`` to ``dataset_1``, by dumping it from one dataset into another::

    $ datalad meta-dump -d dataset_0 -r | \
      datalad meta-add -d dataset_1 --json-lines -


Publish metadata to a Git-Repository
""""""""""""""""""""""""""""""""""""

You can also push your metadata to a remote :term:`sibling` (if you have write :term:`permissions`).
This, too, uses a Git command to push only specific :term:`ref`\s.
Let's assume you are in the directory that contains the git repository with your metadata, then you can push your metadata to a remote git repository ``<your repository>``::

    $ git push "<your repository>" "refs/datalad/*:refs/datalad/*"

You will notice that no primary data is stored in the repository ``metadata-destination``. That allows you to publish metadata without publishing the primary data at the same time.


Querying metadata
^^^^^^^^^^^^^^^^^

As the metadata is in a highly structured form, and could correspond to agreed-upon or established schemas, queries through such metadata can use flexible tooling and don't need to rely on DataLad.
One popular choice for working with JSON data, for example, is the JSON command line processor `jq <https://stedolan.github.io/jq>`_.
In conjunction with Unix :term:`pipe`\s, one can assemble powerful queries in a single line.
The (cropped) query below, for example, lists all unique family names of the authors in the institute's scientific project metadata in ``metadata-assimilation``:

.. runrecord:: _examples/DL-101-181-119
   :language: console
   :workdir: beyond_basics/meta/metadata-assimilation
   :lines: 1, 6-20

   $ datalad meta-dump -r | jq '.extracted_metadata["@graph"][3]["@list"][].familyName' | sort | uniq



Querying metadata remotely
""""""""""""""""""""""""""

You do not have to download metadata to dump it. It is also possible to specify a git-repository, and let metalad only read the metadata that it requires to fulfill your request. For example, in order to only retrieve metadata from a metadata entry that has the ``dataset_path`` value of ``study-100``, you can simply run:

.. runrecord:: _examples/DL-101-181-120
   :language: console
   :workdir: beyond_basics/meta

   $ datalad meta-dump \
      -d  https://github.com/christian-monch/metadata-test.git \
      ./study-100

As the output shows, this command only downloaded enough data from the remote repository to dump all metadata in the specified dataset tree-path.
If you want to query all metadata remotely from the repository you could issue the following command:

.. runrecord:: _examples/DL-101-181-121
   :language: console
   :workdir: beyond_basics/meta

   $ datalad meta-dump \
     -d https://github.com/christian-monch/metadata-test.git -r

This will take a lot longer than the previous command because datalad has to fetch more item from the remote repository. If you use the remote meta-dump option properly, you can quickly examine small subsets of very large metadata repositories.

Using metadata
^^^^^^^^^^^^^^

Now that we know all about metadata and how it is handled by MetaLad, here's a final note on its utility:
Metadata, especially when it originates from different sources and gets harmonized to a single schema, provides the powerful opportunity to aid data discoverability.
An example of a good use case for metadata is therefore a search or browsing interface, or data bases, such as data portals and graph query databases.
MetaLad-extracted metadata can be used in workflows to generate such interfaces, and a concrete example is the :ref:`DataLad Catalog <catalog>`, which the next section will introduce.
So to aid with the discoverability of data, one could add metadata to DataLad datasets, extract metadata with MetaLad and multiple extractors, translate extracted metadata to the catalog schema, submit it to ``datalad-catalog`` in order to generate catalog entries, which can all be browsed in a user friendly web-based interface.
Intrigued? Read on to the next section for more information.



Installation
^^^^^^^^^^^^

MetaLad is a stand-alone Python package, and can be installed using

.. code-block:: bash

   pip install datalad-metalad

As with DataLad and other Python packages, you might want to do the installation in a :term:`virtual environment`.



.. rubric:: Footnotes

.. [#f1] It may seem like an unnecessary duplicated effort to record the names of contained files or certain file properties as metadata in a dataset already containing these files. However, metadata can be very useful whenever the primary data can't be shared, for example due to its large size or sensitive nature, allowing consumers to, for example, derive anonymized information, aggregate data with search queries, or develop code and submit it to the data holders to be ran on their behalf.

.. [#f2] `JSON <https://en.wikipedia.org/wiki/JSON>`_ is a language-independent, open and lightweight data interchange format. Data is represented as human readable text, organized in key-value pairs (e.g., 'name': 'Bob') or arrays, and thus easily readable by both humans and machines. A *JSON object* is a collection of key-value pairs. Its enclosed in curly brackets, and individual pairs in the object are separated by commas.

.. [#f3] A Unix timestamp is widely used in computing and measures time as the number of seconds passed since January 1st, 1970. The timestamp in the example metadata entry (``1675113291.1464975``) translates to January 30th, 2023, 22:14:51.146497 with the code snippet below. Lots of software tools have the ability to generate timestamps for you, for example Python's `time <https://docs.python.org/3/library/time.html>`_ module or the command ``date +%s`` in a command line on Unix systems.

		>>> from datetime import datetime
		>>> datetime.fromtimestamp(1675113291.1464975)
		datetime.datetime(2023, 1, 30, 21, 14, 51, 146497)

.. [#f4] Alternatively, provide the switch ``-i`` to ``meta-add``, which tells it to just warn about ID mismatches instead of erroring out.

.. [#f5] Other directories underneath ``.git/refs`` are automatically transported, such as ``.git/refs/heads`` or ``.git/refs/remotes`` - this is configured for each remote with a repositories ``.git/config`` file

	.. code-block:: bash

		$ cat .git/config
		[core]
			repositoryformatversion = 0
			filemode = true
			bare = false
			logallrefupdates = true
			editor = vim
		[remote "origin"]
			url = git@github.com:my-user/my-dataset.git
			fetch = +refs/heads/*:refs/remotes/origin/*


.. [#f6] The answer is minimal information about archived scientific projects of a research institute. While some personal information has been obfuscated, you can still figure out which information is associated with each entry, such as the project name, its authors, or associated publications.
