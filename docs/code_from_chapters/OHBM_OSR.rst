.. _OHBMOSR2020:

OHBM 2020 Open Science Room: Reproducible Research Objects with DataLad
-----------------------------------------------------------------------

This is a detailed write-up of the OHBM Open Science Room demonstration on Reproducible Research Objects with DataLad.
You can find the slides `here <https://docs.google.com/presentation/d/1KzSJv9j-NwGOZv3dwuM4bgaDQmDbjIQvp8eQ3cOfysw/edit?usp=sharing>`_.
If you have attended the talk and are looking for resources to read up on in your own pace, then you're correct here.
You will find the code snippets executed in the talk together with detailed background descriptions and references to the appropriate handbook chapters.
If you're new to DataLad and want to find out more, the DataLad handbook could be exactly what you need.

Workflow description
^^^^^^^^^^^^^^^^^^^^

The software demonstration at the OHBM open science room is part of the open workflows theme.
Therefore, this demonstration performed a complete data consumption, data analysis, and data publication routine.

.. note::

   This workflow requires DataLad version 0.13 or higher.
   In particular, this version requirement stems from the :term:`remote indexed archive (RIA) store` used in this demonstration.
   You can find installation instructions in the section :ref:`install`.


Step 1: Setting up a dataset
""""""""""""""""""""""""""""

When using DataLad, everything happens in datasets, DataLad's core data structure.
You can find out more about datasets in the section :ref:`chapter_datasets`.

.. note::

    Reading this chapter is absolutely required if haven't yet heard of DataLad as it introduces and demonstrates common features (dataset nesting, dataset installation, data retrieval) you should be aware of in order to follow the demonstration.

In short, a dataset is a directory on your computer that is managed by DataLad,
and a git/git-annex repository.
Datasets can

- version control their contents,
- they can be shared and installed, and
- they can be nested in order to link them.

The :command:`datalad create <path>` creates a new dataset:

.. code-block:: bash

   $ datalad create OSRdemo
     [INFO   ] Creating a new annex repo at /home/adina/scratch/OSRdemo
     create(ok): /home/adina/scratch/OSRdemo (dataset)

When using Datalad for analysis projects, a set of principles called "The YODA principles" can help to create a modular project structure.
Those principles are detailed and explained in the section :ref:`yoda`.
Typical analysis datasets will hold results and code, consume or create so-called "toolbox datasets" with containerized and appropriately configured analysis pipelines, and have all relevant datasets linked to the analysis as subdatasets.

Step 2: Linking data
""""""""""""""""""""

One of the analysis components for this and most other workflows is data.
DataLad makes it easy to "install" data as if it would be software, and the Datalad 0.13 release comes with some even more exiting features for data consumption than what DataLad can already do.

For example, the human connectome project (HCP) data exists as a datalad dataset on :term:`Github` now. You can find and install it at `github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_.
If you are interested in the creation of this dataset, the usecase :ref:`usecase_hcp_dataset` will talk about the details.
Beyond access to the full HCP data, there are also subsets of the HCP data being created and transformed into BIDS-like formats, and the newly introduced feature of RIA stores makes it possible to install these HCP data subsets in specific versions, for example BIDS formatted.
You can read up on this new feature in the section :ref:`riastore`.
Here is how to install the "structural preprocessed" subset of the HCP dataset that has been transformed into a bids like format from a public datalad RIA store into a directory called ``.source``:

.. code-block:: bash

    $ datalad clone -d . 'ria+http://store.datalad.org#~hcp-structural-preprocessed@bids' .source
    [INFO   ] Configured RIA store not found at ria+file:///ds/hcp/srv
    install(ok): .source (dataset)
    add(ok): .source (file)
    add(ok): .gitmodules (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 2)
      install (ok: 1)
      save (ok: 1)

.. findoutmore:: Why is it called ".source"?

   By installing data into a hidden directory (anything that starts with a ``.``), the input data is linked, but doesn't show up at first sight when browsing the dataset.
   This is not a requirement, but helpful if you want to be extraordinarily organized.

Step 3: Space for outputs
"""""""""""""""""""""""""

To later link code execution, input data, and results, the results should be saved in the analysis dataset, i.e., in the top level dataset ``OSRdemo``.
If the amount of files becomes too large (beyond ~100-200k files), datasets can struggle, though.
Large-scale analysis thus may require splitting outputs across subdatasets in order to create several smaller-sized datasets.
More information on this can be found in the chapter :ref:`chapter_gobig`.
Here, in anticipation of up to 500.000 files, two output subdatasets are used to collect the results.

Usually, you can just create a new, empty dataset with :command:`datalad create` as in ``datalad create -d <root-to-dataset> <path>``.
In the demonstration, empty, pre-created datasets (``fmriprep`` for fmriprep outputs, ``freesurfer`` for freesurfer outputs) are installed from :term:`GIN`.

.. code-block:: bash

   # Note: don't execute these lines - the datasets are not empty anymore!
   $ datalad clone -d . git@gin.g-node.org:/adswa/OSRfmriprep.git fmriprep
   $ datalad clone -d . git@gin.g-node.org:/adswa/OSRfreesurfer.git freesurfer

.. findoutmore:: Why install empty datasets?

   The choice to install empty datasets was a convenience hack for easy publishing routines.
   At the end of the workflow, a recursive :command:`datalad push` was able to publish all results and the complete hierarchy of datasets in one go.
   This was only this easy because by installing the ``fmriprep`` and ``freesurfer`` datasets those subdatasets already had a :term:`sibling` configuration to :term:`GIN`.
   Had the subdatasets been created from scratch, each subdataset would have required setting up a sibling before hand, in the same way it was done with the top-level dataset.
   You can read more about this in the section :ref:`gin`, in particular the paragraph :ref:`subdspublishing`.


Step 4: Linking software
""""""""""""""""""""""""

Containerized pipelines can be linked to datasets.
One can either create such a toolbox dataset from scratch, or consume pre-existing containers from `github.com/ReproNim/containers <https://github.com/ReproNim/containers>`_.
`This ReproNim Webinar <https://www.youtube.com/watch?v=ix3lC6HGo-Q&feature=youtu.be>`_ walks through a complete workflow, if you are interested in more details on how to use them.

Here is how to create a custom fmriprep toolbox:

First, create a dataset for it:

.. code-block:: bash

   $ datalad create -c text2git fmriprep_toolbox

Because fmriprep requires a freesurfer license file, you can add this file to your dataset:

.. code-block:: bash

   $ cd fmriprep_toolbox
   $ cp ../license.txt .
   $ datalad save -m "add freesurfer license file"

Note that due to the ``text2git`` configuration of the dataset this file will be available right away after this dataset is cloned and does not need to be retrieved in an extra step.
To understand this, chapter :ref:`chapter_gitannex` is very much recommended, and to find out more about procedures, read on in the section :ref:`procedures`.

Finally, a Docker or Singularity container that contains the pipeline or required software can be added.
Note that this requires the :term:`DataLad extension` ``datalad-container``.
A demonstration can be found in the section :ref:`containersrun`.
The pipeline can be configured with custom call specifications with the ``--call-fmt`` option.
In this demonstration,  programmatic bind mounts are attached.
Whenever this toolbox is installed as a subdataset called ``.tools``, running the container in this dataset with bind-mount the parent directory (i.e., the analysis dataset), and the license file inside of the toolbox.
Note that the placeholders ``{img}`` and ``{cmd}`` will expand to the container and the command line call given to :command:`datalad containers-run`.

.. code-block:: bash

    $ datalad containers-add fmriprep \
    --url shub://ReproNim/containers:bids-fmriprep--20.1.1 \
    --call-fmt 'singurity run --cleanenv -B $PWD,$PWD/.tools/license.txt {img} {cmd}'

This toolbox dataset can be added just as data as a subdataset of the analysis.
In the code block below, the dataset is installed from a local path.

.. code-block:: bash

   $ datalad clone -d . ~/fmriprep_toolbox .tools

.. findoutmore:: Could I share such a toolbox dataset?

   Note that unlike the ``fmriprep`` and ``freesurfer`` subdatasets, this subdataset of ``OSRdemo`` will not be pushed anywhere public when the results are published later.
   This is because it does not have a sibling on :term:`Gin` or a similar web-based hosting service.
   As this dataset also contains a personal license file, it isn't intended for publication anywhere.
   This toolbox dataset serves an individual user or a group of users on shared infrastructure as a standard frmiprep analysis toolbox.
   In order to share such a toolbox, create a sibling for the dataset on a repository-hosting service like :term:`Github` or :term:`Gin`, make sure that no personal files are included, and publish as demonstrated later in this workflow.

Step 5: Running an analysis
"""""""""""""""""""""""""""

With containerized pipeline and data set up, the :command:`datalad containers-run` command can be used to execute fmriprep preprocessing on the data.
This command will retrieve and use the container linked inside the toolbox, retrieve any input data that is specified with the ``--input`` flag(s), and execute the final command inside of the container (the ``{cmd}`` placeholder in the call format specification will be replaced by it).
In the example below, a single subject is preprocessed:

.. code-block:: bash

   $ datalad containers-run -n .tools/fmriprep \
       -m "preprocess examplary subject with fmriprep" \
       --input .source/sub-170631 \
       --output fmriprep \
       --output freesurfer \
       ".source . participant --participant-label 170631 --skip-bids-validation --anat-only -w /tmp --fs-license-file .tools/license.txt"

The results will be saved into the subdatasets because they were conveniently named after the output directories that fmriprep produces, and the command will produce and save a machine-readable and re-executable :term:`run record` from this that allows others or yourself to rerun the computation, for example if data has been updated.
A complete, small-stepped introduction to :command:`datalad run` can be found in chapter :ref:`chapter_run`.


Step 6: Result publication
""""""""""""""""""""""""""

The results and their provenance (on which data, with which software, with what command line call, by whom, and when were the results created?) can be published.
This demonstration focuses on public access and therefore shows a publication routine to the repository-hosting service :term:`Gin`.
A complete write-up on dataset publishing to Gin is in section :ref:`gin`.

To publish a dataset, an empty repository needs to be created via Gin's webinterface.
The SSH url to this repository can be given to :command:`datalad siblings add` to register this repository as a sibling.

.. code-block:: bash

   $ datalad siblings add --name origin --url git@gin.g-node.org:/adswa/OSRdemo.git

Note that the name of the sibling is ``origin``.
This is because the two subdatasets have siblings of the same name.
A recursive :command:`push` will traverse down the dataset hierarchy and publish datasets to their ``origin`` sibling if they have one.
With a single operation from the dataset root, the superdataset and the two subdatasets that hold the results are published in one go.

.. code-block:: bash

   $ datalad push --to origin

Step 7: Result retrieval
""""""""""""""""""""""""

From GIN, you or others can now access this dataset without having an account on Gin via anonymous HTTP access.
For this, :command:`datalad clone` only needs the ``https`` url of the dataset, found in the webbrowsers address bar.
You can take a look at the data for yourself, if you want to:

.. code-block:: bash

   $ datalad clone https://gin.g-node.org/adswa/OSRdemo
   # retrieve data using datalad get
   $ datalad get fmriprep


Tada! We're done!

Hopefully, this workflow gave you an idea of how DataLad can be helpful in reproducible and open workflows.
It wouldn't be surprising if you are feeling a bit overwhelmed from this dense write-up.
This workflow was a very concise write-up of a large amount of many basic and advanced principles and commands of DataLad.
But if you found it intriguing and want to learn more, then stay right here in the handbook and find out more about DataLad.
At the end of the "Basics" part of this book, you should have all of the knowledge you need to perform a similar workflow on your own.
If you're also reading into the linked sections from the "Advanced" and "Usecases" part of the handbook, you will have a thorough understanding of everything that has happened in this workflow.

If you run into problems or have questions, `don't hesitate to get in touch <https://github.com/datalad-handbook/book/issues/new/choose>`_.
