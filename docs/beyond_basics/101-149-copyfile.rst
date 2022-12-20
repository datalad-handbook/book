.. _copyfile:

Subsample datasets using datalad copy-file
------------------------------------------

If there is a need for a dataset that contains only a subset of files of one or more other dataset, it can be helpful to create subsamples special-purpose datasets with the :command:`datalad copy-file` command (:manpage:`datalad-copy-file` manual).
This command is capable of transferring files from different datasets or locations outside of a dataset into a new dataset, unlocking them if necessary, and preserving and copying their availability information.
As such, the command is a superior, albeit more technical alternative to :ref:`copying dereferenced files out of datasets <copydata>`.

This section demonstrates the command based on a published data, a subset of the Human Connectome Project dataset that is subsampled for structural connectivity analysis.
This dataset can be found on GitHub at `github.com/datalad-datasets/hcp-structural-connectivity <https://github.com/datalad-datasets/hcp-structural-connectivity>`_.

Copy-file in action with the HCP dataset
""""""""""""""""""""""""""""""""""""""""

Consider a real-life example: A large number of scientists use the `human connectome project (HCP) dataset <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_ for `structural connectivity analyses <https://en.wikipedia.org/wiki/Brain_connectivity_estimators>`_.
This dataset contains data from more than 1000 subjects, and exceeds 80 million files.
As such, as explained in more detail in the chapter :ref:`chapter_gobig`, it is split up into a hierarchy of roughly 4500 subdatasets [#f1]_.
The installation of all subdatasets takes around 90 minutes, if parallelized, and a complete night if performed serially.
However, for a structural connectivity analysis, only eleven files per subject are relevant::

  - <sub>/T1w/Diffusion/nodif_brain_mask.nii.gz
  - <sub>/T1w/Diffusion/bvecs
  - <sub>/T1w/Diffusion/bvals
  - <sub>/T1w/Diffusion/data.nii.gz
  - <sub>/T1w/Diffusion/grad_dev.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_BIAS_32CH.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_AFI.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_BIAS_BC.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_FieldMap_Magnitude.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_FieldMap_Phase.nii.gz
  - <sub>/unprocessed/3T/T1w_MPR1/*_3T_T1w_MPR1.nii.gz

In order to spare others the time and effort to install thousands of subdatasets, a one-time effort can create and publish a subsampled, single dataset of those files using the :command:`datalad copy-file` command.

.. index:: ! datalad command; copy-file

:command:`datalad copy-file` is able to copy files with their availability metadata into other datasets.
The content of the files does not need to be retrieved in order to do this.
Because the subset of relevant files is small, all structural connectivity related files can be copied into a single dataset.
This speeds up the installation time significantly, and reduces the confusion that the concept of subdatasets can bring to DataLad novices.
The result is a dataset with a subset of files (following the original directory structure of the HCP dataset), created reproducibly with complete provenance capture.
Access to the files inside of the subsampled dataset works via valid AWS credentials just as it does for the full dataset [#f1]_.

The Basics of copy-file
^^^^^^^^^^^^^^^^^^^^^^^

This short demonstration gives an overview of the functionality of :command:`datalad copy-file` - Feel free to follow along by copy-pasting the commands into your terminal.
Let's start by cloning a dataset to work with:

.. runrecord:: _examples/DL-101-149-01
   :language: console
   :workdir: beyond_basics/HPC

   $ datalad clone https://github.com/datalad-datasets/human-connectome-project-openaccess.git hcp

In order to use :command:`copy-file`, we need to install a few subdatasets, and thus install 9 subject subdatasets recursively.
Note that we don't retrieve any data, using ``-n``/``--no-data``.
(The output of this command is omitted -- it is quite lengthy as 36 subdatasets are being installed)

.. runrecord:: _examples/DL-101-149-02
   :language: console
   :workdir: beyond_basics/HPC
   :lines: 1-3

   $ cd hcp
   $ datalad get -n -r HCP1200/130*

Afterwards, we can create a new dataset to copy any files into.
This dataset will later hold the relevant subset of the data in the HCP dataset.

.. runrecord:: _examples/DL-101-149-03
   :language: console
   :workdir: beyond_basics/HPC/hcp

   $ cd ..
   $ datalad create dataset-to-copy-to

With the prerequisites set up, we can start to copy files.
The command :command:`datalad copy-file` works as follows:
By providing a path to a file to be copied (which can be annex'ed, not annex'ed, or not version-controlled at all) and either a second path (the destination path), a target directory inside of a dataset, or a dataset specification, :command:`datalad copy-file` copies the file and all of its availability metadata into the specified dataset.
Let's copy a single file (``hcp/HCP1200/130013/T1w/Diffusion/bvals``) from the ``hcp`` dataset into ``dataset-to-copy-to``:

.. runrecord:: _examples/DL-101-149-04
   :language: console
   :workdir: beyond_basics/HPC

   $ datalad copy-file \
      hcp/HCP1200/130013/T1w/Diffusion/bvals  \
      -d dataset-to-copy-to

When the ``-d/--dataset`` argument is provided instead of a target directory or a destination path, the copied file will be `saved` in the new dataset.
If a target directory or a destination path is given for a file, however, the copied file will be not be saved:

.. runrecord:: _examples/DL-101-149-05
   :language: console
   :workdir: beyond_basics/HPC

   $ datalad copy-file \
      hcp/HCP1200/130013/T1w/Diffusion/bvecs \
      -t dataset-to-copy-to

Note that instead of a as dataset, we specify it as a target path, and how the file is added, but not saved afterwards:

.. runrecord:: _examples/DL-101-149-06
   :language: console
   :workdir: beyond_basics/HPC

   $ cd dataset-to-copy-to
   $ datalad status

Providing a second path as a `destination` path allows one to copy the file under a different name, but it will also not save the new file in the destination dataset unless ``-d/--dataset`` is specified as well:

.. runrecord:: _examples/DL-101-149-07
   :language: console
   :workdir: beyond_basics/HPC

   $ datalad copy-file \
      hcp/HCP1200/130013/T1w/Diffusion/bvecs \
      dataset-to-copy-to/anothercopyofbvecs

.. runrecord:: _examples/DL-101-149-08
   :language: console
   :workdir: beyond_basics/HPC

   $ cd dataset-to-copy-to
   $ datalad status

Those were the minimal basics of the command syntax - the original location, a specification where the file should be copied to, and an indication if the file should be saved or not.
Let's save those two unsaved files:

.. runrecord:: _examples/DL-101-149-09
   :language: console
   :workdir: beyond_basics/HPC/dataset-to-copy-to

   $ datalad save

With the ``-r/--recursive`` flag enabled, the command can copy complete *subdirectory* (not subdataset!) hierarchies -- Let's copy a complete directory, and save it in its target dataset:

.. runrecord:: _examples/DL-101-149-10
   :language: console
   :workdir: beyond_basics/HPC/hcp

   $ cd ..
   $ datalad copy-file hcp/HCP1200/130114/T1w/Diffusion/* \
    -r \
    -d dataset-to-copy-to \
    -t dataset-to-copy-to/130114/T1w/Diffusion

Here is how the dataset that we copied files into looks like at the moment:

.. runrecord:: _examples/DL-101-149-11
   :language: console
   :workdir: beyond_basics/HPC

   $ tree dataset-to-copy-to

Importantly, all of the copied files had yet unretrieved contents.
The copy-file process, however, also copied the files' availability metadata to their new location.
Retrieving file contents works just as it would in the full HCP dataset via :command:`datalad get` (the authentication step is omitted in the output below):

.. runrecord:: _examples/DL-101-149-12
   :language: console
   :workdir: beyond_basics/HPC

   $ cd dataset-to-copy-to
   $ datalad get bvals anothercopyofbvecs 130114/T1w/Diffusion/eddylogs/eddy_unwarped_images.eddy_parameters

What's especially helpful for automation of this operation is that :command:`copy-file` can take source and (optionally) destination paths from a file or from :term:`stdin` with the option ``--specs-from <source>``.
In the case of specifications from a file, ``<source>`` is a path to this file.

In order to use ``stdin`` for specification, such as the output of a ``find`` command that is piped into :command:`datalad copy-file` with a `Unix pipe (|) <https://en.wikipedia.org/wiki/Pipeline_(Unix)>`_, ``<source>`` needs to be a dash (``-``). Below is an example ``find`` command:

.. runrecord:: _examples/DL-101-149-13
   :language: console
   :workdir: beyond_basics/HPC

   $ cd hcp
   $ find HCP1200/130013/T1w/ -maxdepth 1 -name T1w*.nii.gz

This uses ``find`` to get a list of all files matching the specified pattern in the specified directory.
And here is how the outputted paths can be given as source paths to :command:`datalad copy-file`, copying all of the found files into a new dataset:

.. runrecord:: _examples/DL-101-149-14
   :language: console
   :workdir: beyond_basics/HPC/hcp

   # inside of hcp
   $ find HCP1200/130013/T1w/ -maxdepth 1 -name T1w*.nii.gz \
     | datalad copy-file -d ../dataset-to-copy-to --specs-from -

To preserve the directory structure, a target directory (``-t ../dataset-to-copy-to/130013/T1w/``) or a destination path could be given, because the above command copied all files into the root of ``dataset-to-copy-to``:

.. runrecord:: _examples/DL-101-149-15
   :language: console
   :workdir: beyond_basics/HPC/hcp

   $ ls ../dataset-to-copy-to

With this trick, you can use simple search commands to assemble a list of files as a ``<source>`` for :command:`copy-file`: simply create a file or a command like ``find`` that specifies tho relevant files or directories line-wise.
``--specs-from`` can take information on both ``<source>`` and ``<destination>``, though.


Specify files with source AND destination paths for --specs-from
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifying source *and* destination paths comes with a twist: Source and destination paths need to go into the same line, but need to be separated by a `nullbyte <https://en.wikipedia.org/wiki/Null_character>`_.
This is not a straightforward concept, but trying it out and seeing it in action will help.

One way it can be done is by using the stream editor :term:`sed`.
Here is how to pipe source AND destination paths into :command:`datalad copy-file`:

 .. code-block:: bash

	$ find HCP1200/130518/T1w/ -maxdepth 1 -name T1w*.nii.gz \
	  | sed -e 's#\(HCP1200\)\(.*\)#\1\2\x0../dataset-to-copy-to\2#' \
	  | datalad copy-file -d ../dataset-to-clone-to -r --specs-from -

As always, the regular expressions used for sed are a bit hard to grasp upon first sight.
Here is what this command does:

- In general, :term:`sed`\'s :command:`s` (substitute) command will take a string specified between the first set of ``#``\'s (``\(HCP1200\)\(.*\)``) and replace it with what is between the second and third ``#`` (``\1\2\x0\2``).
- The first part splits the paths ``find`` returns (such as ``HCP1200/130518/T1w/T1w_acpc_dc.nii.gz``) into two groups:

   - The start of the path (``HCP1200``), and
   - the remaining path (``/130518/T1w/T1w_acpc_dc.nii.gz``).

   - The second part then prints the first and the second group (``\1\2``, the source path), a nullbyte (``\x0``), and a relative path to the destination dataset together with the second group only (``../dataset-to-copy-to\2``, the destination path).

Here is how an output of ``find`` piped into ``sed`` looks like:

.. runrecord:: _examples/DL-101-149-16
   :language: console
   :workdir: beyond_basics/HPC/hcp

   $ find HCP1200/130518/T1w -maxdepth 1 -name T1w*.nii.gz \
	 | sed -e 's#\(HCP1200\)\(.*\)#\1\2\x0../dataset-to-copy-to\2#'

Note how the nullbyte is not visible to the naked eye in the output.
To visualize it, you could redirect this output into a file and open it with an editor like :term:`vim`.
Let's now see a :command:`copy-file` from :term:`stdin` in action:

.. runrecord:: _examples/DL-101-149-17
   :language: console
   :workdir: beyond_basics/HPC/hcp

   $ find HCP1200/130518/T1w -maxdepth 1 -name T1w*.nii.gz \
    | sed -e 's#\(HCP1200\)\(.*\)#\1\2\x0../dataset-to-copy-to\2#' \
    | datalad copy-file -d ../dataset-to-copy-to -r --specs-from -

Done!
A complex looking command with regular expressions and unix pipes, but it does powerful things in only a single line.

Copying reproducibly
^^^^^^^^^^^^^^^^^^^^

To capture the provenance of subsampled dataset creation, the :command:`copy-file` command can be wrapped into a :command:`datalad run` call.
Here is a sketch how it was done in the structural connectivity subdataset:

**Step 1:** Create a dataset

.. code-block:: bash

   $ datalad create hcp-structural-connectivity

**Step 2:** Install the full dataset as a subdataset

.. code-block:: bash

   $ datalad clone -d . \
     https://github.com/datalad-datasets/human-connectome-project-openaccess.git \
     .hcp

**Step 3:** Install all subdataset of the full dataset with ``datalad get -n -r``

**Step 4:** Inside of the new dataset, draft a ``find`` command that returns all 11 desired files, and a subsequent ``sed`` substitution command that returns a nullbyte separated source and destination path.
For this subsampled dataset, this one would work::

   $ find .hcp/HCP1200  -maxdepth 5 -path '*/unprocessed/3T/T1w_MPR1/*' -name '*' \
    -o -path '*/T1w/Diffusion/*' -name 'b*' \
    -o -path '*/T1w/Diffusion/*' -name '*.nii.gz' \
    | sed -e 's#\(\.hcp/HCP1200\)\(.*\)#\1\2\x00.\2#' \

**Step 5:** Pipe the results into :command:`datalad copy-file`, and wrap everything into a :command:`datalad run`.
Note that ``-d/--dataset`` is not specified for :command:`copy-file` -- this way, :command:`datalad run` will save everything in one go at the end.

.. code-block:: bash

   $ datalad run \
     -m "Assemble HCP dataset subset for structural connectivity data. \

	Specifically, these are the files:

    - T1w/Diffusion/nodif_brain_mask.nii.gz
	- T1w/Diffusion/bvecs
	- T1w/Diffusion/bvals
	- T1w/Diffusion/data.nii.gz
	- T1w/Diffusion/grad_dev.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_BIAS_32CH.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_AFI.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_BIAS_BC.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_FieldMap_Magnitude.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_FieldMap_Phase.nii.gz
	- unprocessed/3T/T1w_MPR1/*_3T_T1w_MPR1.nii.gz

	for each participant. The structure of the directory tree and file names
	are kept identical to the full HCP dataset." \
	"find .hcp/HCP1200  -maxdepth 5 -path '*/unprocessed/3T/T1w_MPR1/*' -name '*' \
	  -o -path '*/T1w/Diffusion/*' -name 'b*' \
	  -o -path '*/T1w/Diffusion/*' -name '*.nii.gz' \
	| sed -e 's#\(\.hcp/HCP1200\)\(.*\)#\1\2\x00.\2#' \
	| datalad copy-file -r --specs-from -"

**Step 6:** Publish the dataset to :term:`GitHub` or similar hosting services to allow others to clone it easily and get fast access to a relevant subset of files.

Afterwards, the slimmed down structural connectivity dataset can be installed completely within seconds.
Because of the reduced amount of files it contains, it is easier to transform the data into BIDS format.
Such a conversion can be done on a different :term:`branch` of the dataset.
If you have published your subsampled dataset into a RIA store, as it was done with this specific subset, a single command can clone a BIDS-ified, slimmed down HCP dataset for structural connectivity analyses because RIA stores allow cloning of datasets in specific versions (such as a branch or tag as an identifier)::

   $ datalad clone ria+http://store.datalad.org#~hcp-structural-connectivity@bids

Summary
"""""""

:command:`datalad copy-file` is a useful command to create datasets from content of other datasets.
Although it requires some Unix-y command line magic, it can be automated for larger tasks, and, when combined with a :command:`datalad run`, produce suitable provenance records of where files have been copied from.


.. rubric:: Footnotes

.. [#f1] You can read about the human connectome dataset in the usecase :ref:`usecase_HCP_dataset`.