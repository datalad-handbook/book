.. _nemar:

NEMAR Quickstart Guide: Accessing NEMAR datasets via DataLad
-------------------------------------------------------------

`NEMAR <https://nemar.org>`__ (NeuroElectroMagnetic Archive) hosts research datasets in `Brain Imaging Data Structure (BIDS) <https://bids.neuroimaging.io>`__ format that cannot be hosted on public repositories due to restrictive licenses, while remaining freely available for research use.

.. figure:: ../artwork/src/nemar.png
   :target: https://github.com/nemarDatasets

NEMAR publishes its hosted data as DataLad datasets on :term:`GitHub` with data files stored on AWS S3, and each dataset can be installed with DataLad as a DataLad dataset.
If you want to find out about this option, this section contains basic insights and commands to get you started even if you haven't used DataLad before.

Quickstart
^^^^^^^^^^

The entire collection of NEMAR datasets can be found at `github.com/nemarDatasets <https://github.com/nemarDatasets>`_, where each dataset is identified by its NEMAR dataset ID (e.g., ``nm000104``, ``nm000105``).
A url to a NEMAR dataset on GitHub thus always takes the following form:
``https://github.com/nemarDatasets/nm0001xx``.
After you have :ref:`installed DataLad <install>`, you can obtain the datasets just as any other DataLad dataset with :dlcmd:`clone`:

.. code-block:: bash

   $ datalad clone https://github.com/nemarDatasets/nm000107.git
     install(ok): /tmp/nm000107 (dataset)

Afterwards, you can browse the dataset for files that you need and obtain them with the :dlcmd:`get` command.
:dlcmd:`get .` will download the entire dataset content from S3, while paths or :term:`globbing` expressions (such as ``sub-*/emg/*``) can define a precise subset of to-be-retrieved files.

.. code-block:: bash

   $ datalad get sub-01/emg/
   get(ok): /<path-to-dataset>/sub-01/emg/sub-01_task-wrist_emg.edf (file) [from s3-PUBLIC...]
     action summary:
        get (ok: 1)

You can also access NEMAR data files directly from S3 if needed:

.. code-block:: bash

   # List dataset files
   $ aws s3 ls s3://nemar/nm000107/ --recursive --no-sign-request

   # Download specific file
   $ aws s3 cp s3://nemar/nm000107/path/to/file.edf . --no-sign-request

What's DataLad and why should I use it to do this?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad is a data management and data publication tool, building up on the tools :term:`Git` and :term:`git-annex`.
It allows you to :term:`version control` data alongside to code and even software environments, it can transparently and reproducibly link and share command executions, and it provides transport logistics for dataset consumption, sharing and collaboration.
Using DataLad can make your science more open, transparent, and reproducible.
You can find a short overview (5 min read) of its main features in the section :ref:`executive_summary`.
Below, we've listed a few bullet points on why it may be useful for you to download a NEMAR dataset via DataLad.

* Potential for **small disk usage**: Cloning datasets is fast, and typically done in a matter of seconds.
  The resulting dataset contains the names and content identities of all files in the dataset, but it is only a fraction of the total data size as all those files do not yet contain file content.
  On demand, you can retrieve file contents of your choice via :dlcmd:`get` which downloads the specified files or directories from S3.
  If you do not need file contents anymore and want to free up diskspace, a :dlcmd:`drop` drops the file contents, reducing the file size significantly, but you retain access to the file via :dlcmd:`get`.
  Thus, if your hard drive overflows, you can drop file contents without losing access to them, or keep a very lightweight reference to your input data next to your analysis results.
* Easy **updating mechanisms**: Should a dataset get updated, you do not need to re-download a new version of the dataset, but run a ``datalad update --how merge`` in the dataset instead to automatically obtain the new or updated files.
* **Open and transparent science**: Share analysis together with data by creating a dataset for your code and results and installing your NEMAR dataset of choice as a :term:`DataLad subdataset` inside of it.
  This links the data you are using in a precise version to your code and results.
  If you want to, you can even use :dlcmd:`run` or :dlcmd:`containers-run` for provenance-tracked execution of commands or scripts, or the ``datalad-containers`` :term:`DataLad extension` to attach software environments to your computation.
  Your analysis dataset can then be shared with others via :term:`GitHub` or similar services and will not only link your code and analyses, but also the data you have used for it.
  The section :ref:`yoda_project` has an example of how to do this.
* **Access to restrictively licensed data**: NEMAR hosts datasets that are freely available for academic and research use but have license restrictions preventing hosting on fully public repositories like OpenNeuro or Zenodo.
  DataLad provides efficient access to these datasets while respecting their license constraints.

These are only a few reasons why DataLad datasets can be beneficial -- if you want to find out more about DataLad's features, this handbook can give you a complete overview of everything the tool can do.

What should I be mindful of when using DataLad datasets?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While DataLad datasets -- in our opinion -- have many advantages, it may be good to know what you shouldn't do in a dataset if you don't have much experience with DataLad yet:

* **Don't copy or move files out of a dataset without dereferencing**. A dataset is a self-contained entity, and its version control features for (large) data work because it handles those files in an internal dataset :term:`annex`.
  Opening a file viewer window and moving a file out of its dataset can be very harmful, because in all likelihood this will copy a symlink that points into the dataset annex instead of the actual file.
  Here's what you should do if you want to copy or move a file out of a dataset into a non-dataset location: Make sure that the file content is present (:dlcmd:`get`), and copy or move the file with a tool that can *dereference* (i.e., resolve to canonical paths) :term:`symlink`\s.
  The command line tool ``cp`` for copying can do this with the ``-L/--dereference`` option, for example, any command can do it if the file path is wrapped in a ``readlink -f <path>`` command.
  Alternatively, run :dlcmd:`unlock` prior to moving with any tool of your choice.
  See also the FAQ on :ref:`Getting data out of datasets <copydata>` or the section :ref:`file system`.

* **Don't force-overwrite files**: Many files in datasets are *annexed* for version control and, by default (on any non-Windows operating system), write-protected to ensure file integrity.
  If you encounter a file that will not let you change it right away and responds, for example, with a "permission denied" error, it is important to not forcefully modify this data.
  Instead, whenever you want to modify data, you need to :dlcmd:`unlock` it to remove the write protection.
  Afterwards, you can save any changes you have made to this file without jeopardizing version control and file integrity.
  Alternatively, use the :dlcmd:`run` command that can automatically unlock files for you.
  The chapter :ref:`chapter_gitannex` contains the details about this.

* **Make sure to retrieve data content prior to opening it with any tool**: If file content isn't yet retrieved, many tools emit confusing errors if they try to open these "empty files".
  If you encounter a software that can't find a file, complains that it can't handle the file type you are giving to it, or behaves strange in another way, the first thing you should check is whether file content is present.
  If this isn't a problem, you should try again after running :dlcmd:`unlock` -- this command turns the file type from symlink into file and can help tools that don't operate on symlinks cope.

* **Respect dataset licenses**: Each NEMAR dataset has its own license specified in ``dataset_description.json`` and the root ``LICENSE`` file.
  While datasets are freely available for academic and research use, they typically have restrictions on commercial use and redistribution.
  Always check and comply with the dataset's license terms before use.

Available NEMAR Datasets
^^^^^^^^^^^^^^^^^^^^^^^^

NEMAR currently hosts several EMG (electromyography) datasets in BIDS format, with more datasets being added over time.
You can browse all available datasets at the `nemarDatasets GitHub organization <https://github.com/nemarDatasets>`_.

Example datasets include:

* **nm000104** - EMG data from typing tasks
* **nm000105** - Hand gesture recognition EMG data
* **nm000106** - Handwriting EMG recordings
* **nm000107** - Wrist control EMG data

Each dataset includes comprehensive metadata, participant information, and task descriptions following BIDS conventions.
