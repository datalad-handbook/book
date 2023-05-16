.. _dgpa:

An introduction to DataLad at the ReproNim DGPA workshop
--------------------------------------------------------

Welcome to this introduction to DataLad during the ReproNim-DGPA workshop!

.. image:: https://www.repronim.org/images/logo-square-256.png
   :align: center

On this website you will find the code from the live demonstrations together with a few additional pointers and explanations, so that you can work through the materials at any later point or in your own time or find out more about a workflow, command or concepts.
If you have all relevant software installed, open up a terminal on your computer and copy-paste the code snippets in this section into your terminal to code along (if you hover above the right corner of a snippet, you can copy it into your clipboard).

Introduction & set-up
^^^^^^^^^^^^^^^^^^^^^

In order to code along, you should have ...

* a recent DataLad version, e.g., ``0.15.5`` installed (you may have done that before the workshop already),

If you need them, installation, updating, and configuration instructions for DataLad and Git are in the section :ref:`install`.
If you are unsure about your version of DataLad, you can check it using the following command::

   datalad --version


* a configured :term:`Git` identity (you may have done this during the introduction to version control with Git)

If you are unsure if you have configured your Git identity already, you can check if your name and email are printed to the terminal when you run

.. code-block:: bash

   git config --get user.name
   git config --get user.email

If nothing is returned, you need to configure your :term:`Git` identity (:ref:`install` shows you how).

* the :term:`DataLad extension` `"datalad-container" <http://docs.datalad.org/projects/container/en/latest/>`_ installed

In order to install ``datalad-container``, use a package manager such as :term:`pip`::

   pip install datalad-container

* an SSH key and account on `gin.g-node.org <https://gin.g-node.org>`_

Beyond software usage, this tutorial will show you how to publish data.
For this, we will be using :term:`Gin`, a free dataset hosting service.
If you want to code along to this part of the tutorial, you may want to create a free user account and upload your :term:`SSH key` -- but worry not, you can also do this at a later stage, too.
Detailed instructions are in section :ref:`gin`.


How to use DataLad
^^^^^^^^^^^^^^^^^^

DataLad is a command line tool and it has a Python API.
It is operated in your :term:`terminal` using the command line (as done above), or used it in scripts such as shell scripts, Python scripts, Jupyter Notebooks, and so forth.
This is how you would import DataLad's Python API::

   ipython       # if not installed, use python
   >>> import datalad.api as dl
   >>> dl.create(path='mydataset')
   >>> exit

In scripts using other programming languages, DataLad commands can be invoked via system calls.
Here is an example with R::

    R       # or use in RStudio
    > system("datalad create mydataset")


DataLad datasets
^^^^^^^^^^^^^^^^

All actions we do happen in or involve DataLad datasets.
Creating a dataset from scratch is done with the ``datalad create`` command.

.. find-out-more:: How can I turn an existing directory into a dataset?

   By navigating into a directory, and running :command:`datalad create -f .` (with the ``-f/--force`` option).
   Section :ref:`dataladdening` provides more info on how to transform existing directories into DataLad datasets.
   It is advised, though, to first learn a bit of DataLad Basics first, so stay tuned.


:command:`datalad create` only needs a name, and it will subsequently create a new directory under this name and instruct DataLad to manage it.
Here, the command also has an additional option, the ``-c text2git`` option.
With the -c option, datasets can be configured in a certain way at the time of creation, and ``text2git`` is a so-called :term:`run procedure`::

   datalad create -c text2git bids-data

``bids-data`` dataset is now a new directory, and you can "change directories" (``cd``) inside it::

   cd bids-data

The "text2git" procedure pre-created a useful dataset configuration that will make version control workflows with files of varying sizes and types easier.

Version control
^^^^^^^^^^^^^^^

Version controlling a file means to record its changes over time, associate those changes with an author, date, and identifier, creating a lineage of file content, and being able to revert changes or restore previous file versions.
DataLad datasets use two established version control tools: :term:`Git` and :term:`git-annex`.
Thanks to those tools, datasets can version control their contents, regardless of size.
Let's start small, and just create a ``README``::

   echo "# A BIDS structured dataset for my input data" > README.md

:command:`datalad status` can report on the state of a dataset.
As we added a new file, the README show up as being "untracked" if you run it::

   datalad status

In order to save a modification in a dataset use the :command:`datalad save` command.
:command:`datalad save` will save the current state of your dataset: It will save both modifications to known files and yet untracked files.
The ``-m/--message`` option lets you attach a concise summary of your changes.
Such a :term:`commit message` makes it easier for others and your later self to understand a dataset's history::

   datalad save -m "Add a short README"

Let us modify this file further::

   echo "Contains functional data of one subject who underwent a localizer task" >> README.md

As the file now differs from its last known state, it shows up as being "modified"::

   datalad status

Again, :command:`datalad save` will save these dataset modifications::

   datalad save -m "Add information on the dataset contents to the README"

Note that ``datalad save`` will save **all** modifications in the dataset at once!
If you have several modified files, you can supply a path to the file or files you want to save.
Importantly, you can version control data of any size - yes, even if the data reaches the size of the `human connectome project <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_, of the `UK Biobank <https://github.com/datalad/datalad-ukbiobank>`_, or even larger.

With each saved change, you build up a dataset history. Tools such as :command:`git log` or :term:`tig` allow you to interrogate this history, and if you want to, you can use this history to find out what has been done in a dataset, reset it to previous states, and much more::

   git log


Data consumption & transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Individual datasets can be installed from local paths or remote URLs using :command:`datalad clone`.
Cloning is a fast operation, and the resulting dataset typically takes up only a fraction of the total size of the data that it tracks::

   cd ../
   datalad clone https://github.com/psychoinformatics-de/studyforrest-data-phase2.git

What we have cloned is the `studyforrest dataset <https://studyforrest.org>`_, a neuroimaging dataset with a few Gigabytes of data.
After installations, the directory tree can be browsed, but most files in datasets will not yet contain file content.
This makes cloning fast and datasets lightweight::

   cd studyforrest-data-phase2
   ls
   # print the size of the directory in human readable sizes
   du -sh

.. find-out-more:: How large can it get actually?

   Cloned datasets can have a lot of file contents.
   ``datalad status`` can report on how much data actually is accessible with the ``--annex`` and ``--annex all`` options::

      datalad status --annex

On demand, content for files, directories, or the complete dataset can be downloaded using :command:`datalad get`.
The snippet below uses :term:`globbing` to get the content of all NIfTI files for a localization task of one subject, but you could also get a full directory, a single file, all files, etc.::

   datalad get sub-01/ses-localizer/func/sub-01_ses-localizer_task-objectcategories_run-*.nii.gz

This works because DataLad datasets contain information on where file contents are available from.
If the origin of a file (such as a web source) is known, you can drop file *content* to free up disk space::

   datalad drop sub-01/ses-localizer/func/sub-01_ses-localizer_task-objectcategories_run-4_bold.nii.gz

You retain access to the file via :command:`datalad get`::

   datalad get sub-01/ses-localizer/func/sub-01_ses-localizer_task-objectcategories_run-4_bold.nii.gz

This mechanism gives you access to data without the necessity to store all of the data locally.
As long as there is one location where data is available from (a dataset on a shared cluster, a web source, cloud storage, a USB-stick, ...) and this source is known, there is no need for storing data when it is not in use.
If you want to try it with large amount of data, checkout `github.com/OpenNeuroDatasets <https://github.com/OpenNeuroDatasets>`_ (a collection of all neuroimaging datasets from `OpenNeuro <https://openneuro.org>`_), or `datasets.datalad.org <http://datasets.datalad.org/>`_, a collection of almost 500TB of open data (also called :term:`The DataLad superdataset ///` because it is a dataset hierarchy that includes a large range of public datasets and can be obtained by running ``datalad clone ///``).

Dataset nesting
^^^^^^^^^^^^^^^

Datasets can be nested in superdataset-subdataset hierarchies.

This overcomes scaling issues.
Sometimes datasets that we work with become incredibly large, and when they exceed a few 100k files version control tools can struggle and break.
By nesting datasets, you can overcome this and split a dataset into manageable pieces.
If you are interested in finding out more, take a look into the usecase :ref:`usecase_HCP_dataset` or the chapter :ref:`chapter_gobig`.

But it also helps to link datasets as modular units together, and maximizes the potential for reuse of the individual datasets.
In the context of data analysis, it is especially helpful to do this to link input data to an analysis dataset -- it helps to reuse data in multiple analysis, to link input data in a precise version, and to create an intuitively structured dataset layout.

.. figure:: ../artwork/src/linkage_subds.svg

Let's nest something into our bids-dataset::

   cd ../bids-data

For this example, we use a number of publicly available DICOM files. Luckily,
at the time of data acquisition, these DICOMs were already equipped with the
relevant metadata: Their headers contain all necessary information to
identify the purpose of individual scans and encode essential properties to
create a BIDS compliant dataset from them. The DICOMs are stored on GitHub
(as a Git repository), so they can be installed as a subdataset. As
they are the raw inputs of the analysis, we store them in a directory we call
``inputs/raw``::

   datalad clone --dataset . \
    https://github.com/datalad/example-dicom-functional.git  \
    inputs/rawdata

Prior to performing actual computations, the data needs to be
transformed into appropriate formats (NIfTI) and standardized to an intuitive
layout (BIDS).
For the task at hand, the `ReproIn <https://github.com/ReproNim/reproin>`_ suite
is the software of choice. It is build on
`HeudiConv <https://heudiconv.readthedocs.io/en/latest/>`_, and beyond converting
DICOMs to NIfTI, it also provides assistance in converting a raw data set to the
BIDS standard, and it integrates with DataLad to place converted and original
data under version control, while automatically annotating files with
sensitive information (e.g., non-defaced anatomicals, etc).

To take extra care to know exactly what software is used both to be
able to go back to it at a later stage should we have the
need to investigate an issue, and to capture *full* provenance of the
transformation process, we can use a software container that contains the
relevant software setup.
A ready-made container collection of container images is available from `ReproNim <https://www.repronim.org/>`_ as a DataLad dataset at
`github.com/ReproNim/containers/ <https://github.com/ReproNim/containers/>`_.
It can be installed as a subdataset::

   datalad clone -d . \
     https://github.com/ReproNim/containers.git \
     code/containers

Run the command :command:`datalad containers-list` from the :term:`DataLad extension` ``datalad-container`` to see to which containers you
have easy access with this subdataset. Because we're performing this query across
dataset boundaries, the command gets a ``--recursive`` flag::

   datalad containers-list --recursive

Also, run the :command:`datalad subdatasets` to see which datasets are registered as subdatasets
to your ``bids-data`` superdataset::

   datalad subdatasets

Computationally reproducible execution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad has a set of commands for reproducible execution and re-execution:
The :command:`datalad run` command can run any command in a way that links the command or script to the results it produces and the data it was computed from.
The :command:`datalad rerun` can take this recorded provenance and recompute the command.
And the :command:`datalad containers-run`, from the :term:`DataLad extension` ``datalad-container``, can capture software provenance in the form of software containers in addition to the provenance that ``datalad run`` captures.

Let's perform a computationally reproducible, provenance-tracked DICOM conversion.
The ``reproin`` has heudiconv as its entrypoint, and we only need to plug in the parameters for the
conversion. The installed subdataset contains functional data for subject ``02``::

   datalad containers-run -m "Convert subject 02 to BIDS" \
    --container-name code/containers/repronim-reproin \
    --input inputs/rawdata/dicoms \
    --output sub-02 \
    "-f reproin -s 02 --bids -l '' --minmeta -o . --files inputs/rawdata/dicoms"

This execution retrieved input data and software container, and linked this information together with a record of the container invocation and all computed outputs.

Let's find out what has changed by comparing the current state of the dataset to
the previous state (identified with the pointer ``HEAD~1``, which translates to
"one state prior to the current one")::

   datalad diff -f HEAD~1

As the command output shows, a range of files have been added to the dataset, and ``bids-data`` now holds BIDS-converted data from one subject.
Importantly, we have a complete provenance record of everything that has happened::

   git log -n 1

Publishing datasets
^^^^^^^^^^^^^^^^^^^

Let's share this data with our friends and collaborators.
There are many ways to do this (section :ref:`chapter_thirdparty` has all the details), but
a convenient way is `Gin <https://gin.g-node.org>`_, a free hosting service for DataLad datasets.

First, you need to head over to `gin.g-node.org <https://gin.g-node.org/>`__, log in, and upload an :term:`SSH key`. Then, under your user account, create a new repository, and copy it's SSH URL.
A step by step instruction with screenshots is in the section :ref:`gin`.

.. importantnote:: The 0.16 release will have a convenience command

   The upcoming DataLad ``0.16`` release comes with a set of commands that automatically create new repositories on your favourite hosting service for you, for example :command:`datalad create-sibling-gin`. For more information on how to create repositories either manually or automatically, take a look at :ref:`share_hostingservice`.

You can register this URL as a sibling dataset to your own dataset using :command:`datalad siblings add`::

   datalad siblings add -d . \
    --name gin \
    --url git@gin.g-node.org:/adswa/bidsdata.git

It is now a known sibling dataset to which you can publish data::

   datalad siblings

Note that Gin is a particularly handy hosting service because it has annex support.
This means that you can publish your complete dataset, including all data, to it in one command::

   datalad push --to gin

Your data is now published!
If you make your repository public (it is private by default), anyone can clone your dataset via its https URL.
If you keep it private, you can invite your collaborators via the Gin webinterface.

By the way: Now that your data is stored in a second place, you can drop the local copies to save
disk space.
If necessary, you can reobtain the data from Gin again via :command:`datalad get`.

Using published datasets
^^^^^^^^^^^^^^^^^^^^^^^^

Let's take the published dataset and use it for an analysis.
The process is similar to what we have done before.
First, we create a dataset - this time, we use a different dataset procedure, the YODA procedure.
You can find out about the details of the yoda procedure in the datalad handbook in sections :ref:`procedures`, but in general this configuration is a very useful standard configuration for datasets for data analysis, as it preconfigures a dataset according to the :ref:`yoda princples <yoda>` and creates a few useful configurations::

   cd ../
   datalad create -c yoda myanalysis

Next, let's install the input data from Gin.
For this, we use its https URL - even if you do not have an account on Gin, you will be able to run the following command::

   cd myanalysis
   datalad clone -d . \
    https://gin.g-node.org/adswa/bids-data \
    input

Now that we have input data, let's get a script to analyze it.
You could write your own script, but here we'll use a pre-existing one to extract a brain mask from the data, based on a `Nilearn tutorial <https://nilearn.github.io/stable/auto_examples/01_plotting/plot_visualization.html#sphx-glr-auto-examples-01-plotting-plot-visualization-py>`_.
This script is available from `GitHub <https://raw.githubusercontent.com/datalad-handbook/resources/master/get_brainmask.py>`_.
While you can add and save any file into your dataset, it is often useful to know where files came from.
If you add a file from a web-source into your dataset, you can use the command ``datalad download-url`` in order to download the file, save it together with a commit message into the dataset, and record its origin internally.
This allows you to drop and re-obtain this file at any point, and makes it easier to share that dataset with others::

   datalad download-url -m "Download code for brain masking from Github" \
    -O code/get_brainmask.py \
    https://raw.githubusercontent.com/datalad-handbook/resources/master/get_brainmask.py

Finally, we need to register a software container to the dataset.
Importantly, this container does not need to contain the analysis script.
It just needs the correct software that the script requires -- in this case, a Python 3 environment with nilearn installed.

At this point in the tutorial, you should have created your own Docker container with the necessary Python environment.
In addition to this Docker container, we're also providing a `singularity <http://singularity.lbl.gov/>`_ image. Singularity is a useful alternative to Docker, because, unlike Docker, it can be run on shared computational infrastructure such as HPC systems without posing a security risk.

.. find-out-more:: Creating a Singularity container with Neurodocker

   In order to create a Singularity image, you first need a recipe.
   `Neurodocker <https://github.com/ReproNim/neurodocker>`_ makes this really easy.
   Here's the command used for minimal nilearn :term:`container recipe`::

      docker run --rm repronim/neurodocker:latest generate singularity \
      --base=debian:stretch --pkg-manager=apt \
      --install git \
      --miniconda create_env=neuro \
                  pip_install='nilearn matplotlib' \
      --entrypoint "/neurodocker/startup.sh python"

   The resulting recipe can be saved into a Git repository or DataLad dataset.
   A ``sudo singularity build <container-name> <recipe>`` builds the image locally, and you can add it from a path to your dataset.

Let's add this container to the dataset using :command:`datalad containers-add`.
Decide for yourself whether you want to use the Docker image or the Singularity image.

**Docker**: For Docker, run the following command, or, if you want, replace the url with your own container::

   datalad containers-add nilearn \
    --url dhub://djarecka/nilearn:yale

**Singularity**: For Singularity, run the following command, which pulls a Singularity image from :term:`Singularity-hub`.
Note how we explicitly define how the container should be called - the placeholders ``{img}`` and ``{cmd}`` will expand to the container image and the supplied command when this container is called::

   datalad containers-add nilearn \
    --url shub://adswa/nilearn-container:latest \
    --call-fmt "singularity exec {img} {cmd}"

Finally, call :command:`containers-run` to execute the script inside
of the container.
Here's how this looks like::

   datalad containers-run -m "Compute brain mask" \
    -n nilearn \
    --input input/sub-02/func/sub-02_task-oneback_run-01_bold.nii.gz \
    --output figures/ \
    --output "sub-02*" \
    "python code/get_brainmask.py"

You can query an individual file how it came to be...::

   git log sub-02_brain-mask.nii.gz

... and the computation can be redone automatically based on the recorded provenance using ``datalad rerun``::

   datalad rerun

If this has intrigued you, you're at the right place to learn more about DataLad.
Checkout the :ref:`Basics <basics-intro>` of the handbook, or take a closer look into specific :ref:`usecases <usecase-intro>`.
