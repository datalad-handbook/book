.. _neurohackademy22:

Neurohackdemy 2022: Data Management for Neuroimaging with DataLad
-----------------------------------------------------------------

Welcome to this introduction to DataLad at the Neurohackademy 2022.
You can follow the tutorial by copy-pasting the code snippets on this page into
a terminal in the Neurohackademy's Jupyterhub - a small copy-button appears in each
code cell if you hover over it at the upper right hand corner.
The additional text references additional resources and explanations if you want to find out more about a workflow, command or concepts, or if you are revisiting this resource after Neurohackademy.

Introduction & set-up
^^^^^^^^^^^^^^^^^^^^^

The Jupyterhub has all software readily installed. This entails a recent version of DataLad, e.g., ``0.17.2``, and some additional Python package we will make use of, such as the :term:`DataLad extension` "datalad-container", the `nilearn <https://nilearn.github.io/stable/index.html>`_ package, and the `black <https://black.readthedocs.io/en/stable/>`_ Python formatter.

Beyond this, you need to have a configured :term:`Git` identity, which you likely set-up during the Neurohackademy's sessions on Git.
If you need them for your own system, installation, updating, and configuration instructions for DataLad and Git are in the section :ref:`install`.
If you are unsure about your version of DataLad, you can check it using the following command::

   datalad --version

If you are unsure if you have configured your Git identity already, you can check if your name and email are printed to the terminal when you run

.. code-block:: bash

   git config --get user.name
   git config --get user.email

If nothing is returned, you need to configure your :term:`Git` identity.

.. code-block:: bash

   git config --global --add user.name "Bob McBobface"
   git config --global --add user.email "bobmcbobface@uw.edu"

In order to install ``datalad-container``, use a package manager such as :term:`pip`::

   pip install datalad-container


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

In the command line, typical usage consists of the ``datalad`` main command, optionally parametrized with additional flags, followed by a subcommand and its own optional flags.

.. image:: ../artwork/src/command-structure.png

Here is an example with a main command, subcommand, and subcommand option::

   # print some information about the system to the terminal
   datalad wtf -S system

You can get help about available commands by running ``datalad -h/--help`` or about specific commands and their options by running ``datalad <subcommand> -h/--help``::

   datalad wtf -h

We will glimpse into some of DataLad's functionality by setting up a toy analysis.

DataLad datasets
^^^^^^^^^^^^^^^^

Everything happens in or involves DataLad datasets - DataLad's core data structure.

.. figure:: ../artwork/src/dataset_extended.svg

You either create datasets yourself, or clone an existing dataset.
Creating a dataset from scratch is done with the ``datalad create`` command.

.. find-out-more:: How can I turn an existing directory into a dataset?

   By navigating into a directory, and running :command:`datalad create -f .` (with the ``-f/--force`` option).
   Section :ref:`dataladdening` provides more info on how to transform existing directories into DataLad datasets.
   It is advised, though, to first learn a bit of DataLad Basics first, so stay tuned.


:command:`datalad create` only needs a name, and it will subsequently create a new directory under this name and instruct DataLad to manage it.
Here, the command also has an additional option, the ``-c text2git`` option.
With the -c option, datasets can be configured in a certain way at the time of creation, and ``text2git`` is a so-called :term:`run procedure`::

   datalad create -c text2git my-analysis

``my-analysis`` dataset is now a new directory, and you can "change directories" (``cd``) inside it::

   cd my-analysis

The "text2git" procedure pre-created a useful dataset configuration that will make version control workflows with files of varying sizes and types easier.
It will also help us later to understand the two version control tools involved in DataLad datasets.

Version control
^^^^^^^^^^^^^^^

Version controlling a file means to record its changes over time, associate those changes with an author, date, and identifier, creating a lineage of file content, and being able to revert changes or restore previous file versions.
DataLad datasets make use of two established version control tools, :term:`Git` and :term:`git-annex`, to version control files regardless of size or type.


Let's build a dataset for an analysis by adding a README.
The command below writes a simple header into a new file ``README.md``::

   echo "# My example DataLad dataset" > README.md

:command:`datalad status` can report on the state of a dataset: What has changed, compared to the last saved version?
As we added a new file, ``README.md`` shows up as being "untracked"::

   datalad status


Procedurally, version control with DataLad commands can be simpler that what you might be used to:
In order to save any new file or modification to an existing file in a dataset you use the :command:`datalad save` command.
The ``-m/--message`` option lets you attach a concise summary of your changes.
Such a :term:`commit message` makes it easier for others and your later self to understand a dataset's history::

   datalad save -m "Create a short README"

Let us modify this file by extending the description a bit further.
The command below appends a short description to the existing contents of the README::

   echo "This dataset contains a toy data analysis" >> README.md

If you want to, you can also use git or git-annex commands in DataLad datasets.
Git commands such as ``git status`` or ``git diff`` are equally able to tell you that the file now differs from its last saved state and is thus "modified"::

   git diff

Let's save this modifications with a helpful message again::

   datalad save -m "Add information on the dataset contents to the README"


.. find-out-more:: What if I have several modifications?

   When run without any file constraints, ``datalad save`` will save **all** modifications in the dataset at once - every untracked file and every modification made to existing files.
   If you have several unrelated modifications, it is advisable to save them individually.
   To do this, you can supply the command with a path to the file (or files) you want to save, e.g., ``datalad save -m "adding raw data" raw/``


With each saved change, you build up your dataset's revision history.
Tools such as :command:`git log` allow you to interrogate this history, and if you want to, you can use this history to find out what has been done in a dataset, reset it to previous states, and much more::

   git log


Importantly, you can version control data **of any size** - yes, even if the data reaches the size of the `human connectome project <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_, of the `UK Biobank <https://github.com/datalad/datalad-ukbiobank>`_, or even larger.
``datalad save`` is all you need.

.. figure:: ../artwork/src/local_wf.svg
   :width: 200%

And version control does not stop at research data - as long as something is a digital file, you can save it to a DataLad dataset.
This includes **software containers**, such as :term:`Docker` or :term:`Singularity` containers.

As you know from previous Neurohackademy lectures, :term:`software container`\s are useful to capture, share, and use a specific software environment for an analysis.
The :term:`DataLad extension` ``datalad-container`` therefore equips DataLad with additional commands that go beyond version controlling software containers, adding additional convenience commands for reproducible science.
``datalad containers-add``, for example, can register a container from a path or a URL inside a dataset in a way that can allow us to perform a provenance-captured data analysis inside of it.

.. importantnote:: We can't run containers on the hub, but we can add them

   The Jupyterhub doesn't support container executions, but we can nevertheless take a look at how you can add containers to datasets.
   The following command will add a prepared :term:`Singularity` container from a remote source and register it under the name ``nilearn`` (as the container we would use entails a Python environment with nilearn inside)::

	   datalad containers-add nilearn \
		--url shub://adswa/nilearn-container:latest

   If your own system supports Docker rather than Singularity, you can get the very same container from Dockerhub by running::

	   datalad containers-add nilearn \
		 --url dhub://djarecka/nilearn:yale

   If you are interested in using containers for your data analysis, checkout `github.com/repronim/containers <https://github.com/repronim/containers>`_, a curated DataLad dataset with a variety of neuroimaging-related software containers ready for you to use.

The command ``datalad containers-list`` can show you which containers are registered in your datasets::

    datalad containers-list


Digital provenance
^^^^^^^^^^^^^^^^^^

Digital provenance is information on how a file came to be and an essential element in the `FAIR principles <https://www.go-fair.org/fair-principles>`_.
Version control already captures some digital provenance, such as the date, time, and author of a file or file modification. DataLad can add additional provenance.
One useful piece of provenance information is the origin of files.

Imagine that you are getting a script from a colleague to perform your analysis, but they email it to you or upload it to a random place for to download::

    # download a script without provenance information
    wget -P code/ \
       https://raw.githubusercontent.com/datalad-handbook/resources/master/get_brainmask.py

The ``wget`` command downloaded a script for extracting a brain mask from the web into a code directory::

   datalad status

You can save it into your dataset to have the script ready for your analysis::

   datalad save -m "Adding a nilearn-based script for brain masking"

But... in a years time, would you remember where you downloaded this from?

Let's use a DataLad command to download and save a file, and also register the original location of this file internally::

   # in addition to a nilearn-based script, let's get a nilearn tutorial
   datalad download-url -m "Add a tutorial on nilearn" \
      -O code/nilearn-tutorial.pdf \
      https://raw.githubusercontent.com/datalad-handbook/resources/master/nilearn-tutorial.pdf

This command downloads a file from the web, saves it under the provided commit message, and, internally, registers the original location of this file.
We will see in a short while how this location provenance information is *actionable*, and can be used to automatically re-retrieve it.

.. code-block:: bash

   # download-url spares you a save - the dataset state is already clean
   datalad status

A different useful piece of provenance is information on processes that generated or modified files, such as the information that executing a specific script generates a specific figure.
DataLad has a set of commands for reproducible execution and re-execution:
The :command:`datalad run` command can run any command execution in a way that links the command or script to the results it produces.
This provenance, similar to the provenance ``download-url`` stores internally, is actionable, and the :command:`datalad rerun` can take this recorded provenance and recompute the command automatically.

Let's imagine that the script you got from your colleague does not follow the formatting guidelines you typically use, so you let `black <https://black.readthedocs.io/en/stable/>`_, a Python code formatter, run over the code to reformat it.

Without DataLad, you would run it like this: ``black code/get_brainmask.py``.
But if you wrap it into a basic :command:`datalad run` command you can capture the changes of the command execution automatically, and record provenance about it::

   datalad run -m "Reformat code with black" \
    "black code/get_brainmask.py"

The resulting commit captured the formatting changes::

   git show

And the provenance, saved in a structured record in the commit message, allows automatic re-execution::

   datalad rerun

Data consumption and dataset nesting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad makes data consumption very convenient: The :command:`datalad clone` command allows you to install datasets from local or remote sources.
And there are many public dataset sources, such as all of `OpenNeuro's <https://openneuro.org/>`_ datasets (`github.com/OpenNeuroDatasets <https://github.com/OpenNeuroDatasets>`_), the Human Connectome Project's open access data (`github.com/datalad-datasets/human-connectome-project-openaccess <https://github.com/datalad-datasets/human-connectome-project-openaccess>`_), or other collections of Open Neuroimaging data (`datasets.datalad.org <http://datasets.datalad.org/>`_), giving you streamlined access to several hundreds of Terabytes of neuroscientific data.

While you can clone datasets 'as is' as standalone data packages, you can also link datasets into one another in superdataset-subdataset hierarchies, a process we call "nesting".

.. figure:: ../artwork/src/linkage_subds.svg

Among several advantages, nesting helps to link datasets as modular units together, and maximizes the potential for reuse of the individual datasets. In the context of data analysis, it is especially helpful to link input data to an analysis dataset -- it helps to reuse data in multiple analysis, to link input data in a precise version, and to create an intuitively structured dataset layout.

Let's get input data for our analysis by cloning some BIDS-structured data under the name input.
We make sure to link it to the dataset by running the command inside of the dataset and pointing the ``-d/--dataset`` argument to its root - this will register the input data as a subdataset of it::

   # clone a remote dataset and register it as
   datalad clone -d . \
    https://gin.g-node.org/adswa/bids-data \
    input

The last commit will shed some light on how this linkage works::

   git show

It records the dataset's origin, and importantly, also the datasets version state.
This allows the analysis dataset to track exactly where the input data came from and which version of the data was used.
The subdatasets own version history is not impacted by this, and you could inspect it to learn how exactly the input dataset evolved.

Data transport
^^^^^^^^^^^^^^

The input dataset contains functional MRI data in BIDS format from a single subject.
While we cloned the dataset, you probably noticed that this process did not take long enough to involve downloads of sizeable neuroimaging data.
Indeed, after cloning the resulting dataset typically takes up only a fraction of the total size of the data that it tracks.
However, you can browse the directory tree to discover available files::

   ls input/sub-02/func

And you can get the file content of files, directories, or entire datasets on demand via the command :command:`datalad get` ::

   datalad get input/sub-02

If you don't need a file anymore, you can drop its content to free up disk space again::

   datalad drop input/sub-02

This mechanism gives you access to data without the necessity to store all of the data locally.
Your analysis dataset links the exact data it requires in just a few bytes, with actionable access to retrieve the data on demand, and your computer can have access to more data than your hard drive can store.

A look under the hood...
^^^^^^^^^^^^^^^^^^^^^^^^

Whenever a file's content is not available after cloning a dataset, this file is internally managed by the second version control tool, :term:`git-annex`.

.. figure:: ../artwork/src/publishing/publishing_gitvsannex.svg

Git will never know an annexed file's content, it will only know its content identity (to ensure data integrity at all times) and all the locations where file content of this file exists.
So when you clone a dataset, Git will show you the file name, and datalad get will retrieve the file contents on demand from wherever they are stored.

Consider the nilearn tutorial we added to the dataset.
This file is annexed, and its location information is kept internally.
If you run the following command, you will see a list of known file content locations were the content can be reretrieved from if you drop it locally::

   git annex whereis code/nilearn-tutorial.pdf

Just as your dataset can have multiple linked clones (in DataLad's terms, :term:`sibling`\s), each annexed file can have multiple possible registered sources, from web sources, cloud infrastructure, scientific clusters to USB-sticks.
This `decentral approach to data management <https://doi.org/10.1515/nf-2020-0037>`_ has advantages for data consumers and producers:
You can create a resilient, decentral network where several data sources can provide access even if some sources fail, and regardless of where data is hosted, data retrieval is streamlined and works with the same command.
As long as there is one location where data is available from (a dataset on a shared cluster, a web source, cloud storage, a USB-stick, ...) and this source is known, there is no need for storing data when it is not in use.
Moreover, this mechanism allows to exert fine-grained access control over files.
You can share datasets publicly, but only authorized actors might be able to get certain file contents.


Computational reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have all the building blocks for a reproducible analysis, so let's get started.
If you are on a system that supports container execution, you can skip the next code block and use ``datalad containers-run`` as shown in the important note below.

Otherwise, we'll stick to ``datalad run`` and parameterize it with a few more helpful options.
Those are the ``-i/--input`` and ``-o/--output`` parameter.
These flags have two purposes: For one, they add provenance information on inputs and outputs to the structured provenance. More importantly, they help command execution whenever handling annexed files: ``--input`` files contents will be retrieved prior to command execution, and ``--output`` files will be unlocked prior to command execution, allowing changes in the outputs over multiple reruns to save new versions of these files::

   datalad run -m "Compute brain mask" \
     --input input/sub-02/func/sub-02_task-oneback_run-01_bold.nii.gz \
     --output "figures/*" \
     --output "sub-02*" \
     "python code/get_brainmask.py"

.. importantnote:: Using containers-run

	If you are on a system that supports container execution, you can now use :command:`datalad containers-run` in order to perform a containerized and provenance-tracked analysis, executing the script inside of the software environment the container provides.
	In addition to ``datalad run``, ``datalad containers-run`` needs a container specification which container should be used. Other than that, the commands get the same arguments::

	   datalad containers-run -m "Compute brain mask" \
		-n nilearn \
		--input input/sub-02/func/sub-02_task-oneback_run-01_bold.nii.gz \
		--output "figures/*" \
		--output "sub-02*" \
		"python code/get_brainmask.py"

You can now query an individual file how it came to be...

.. code-block:: bash

   git log sub-02_brain-mask.nii.gz

... and the computation can be redone automatically and checked for computational reproducibility based on the recorded provenance using ``datalad rerun``::

   datalad rerun


Data publication
^^^^^^^^^^^^^^^^


Afterwards, you could publish your analysis for others to consume or collaborate with you.
You can choose from a variety of places, and even if the amount of data you want to share is sizeable, you will likely find a free solution to do it the chapter :ref:`chapter_thirdparty`.

If the annexed files in your repository, e.g., the nilearn tutorial, the figures, or the brain mask file, contain appropriate provenance to either reobtain them from public sources, or provenance to recompute them automatically, you could even skip the publication of annexed data, and use repository hosting services without support for annexed contents only.
For example, if you have a GitHub account and an SSH key setup for it on the JupyterHub, you could run ``datalad create-sibling-github --access-protocol ssh my-analysis`` followed by a ``datalad push`` to create a :term:`sibling` repository on GitHub and publish the Git part of your repository to it.

To get an overview on publishing datasets, however, you best go to :ref:`sharethirdparty` first, or view one of the many data publication tutorials on `YouTube <https://youtu.be/WwSp22zVwV8>`_.

.. figure:: ../artwork/src/publishing/startingpoint.svg


Cleaning up
^^^^^^^^^^^

The lecture wouldn't have the term "data management" in its title if we were to leave clutter in your home directory.
This gives us the chance to take a look at how to remove files or datasets, which, given that there are version control tools at work that protect your data, can be a challenging task (Spoiler: if you ``rm`` a file and save the deletion, the file can be brought back to life easily, and an ``rm -rf`` on a dataset with annexed files will cause an explosion of permission errors).

Two commands, :command:`datalad drop` and :command:`datalad remove`, come into play for this.
``datalad drop`` is the antagonist of :command:`datalad get`. By default, everything that ``drop`` does can be undone with a ``get``.

You already know that ``datalad drop`` drops file contents from the dataset to free up diskspace::

   datalad drop input/sub-02

But ``drop`` can also uninstall subdatasets::

   datalad drop --what all input

Importantly, ``datalad get`` can find information where that dataset came from and reinstall it::

   datalad get --no-data input

In order to permanently wipe a subdataset, you need ``remove`` (which internally uses a destructively parametrized ``drop``). ``remove`` is the antagonist to ``clone``, and will leave no trace of the dataset::

   datalad remove input

However, both commands have built-in security checks.
They require that dropped files can be re-obtained to prevent accidental data loss, and that removed datasets could be re-cloned in their most recent version from other places, i.e., that there is a sibling that has all revisions that exist locally.

Dropping one of the just computed figures will fail because of this check::

   datalad drop figures/sub-02_mean-epi.png

But it can be overridden with the ``--reckless`` parameter's ``availability`` mode::

   datalad drop figures/sub-02_mean-epi.png --reckless availability

Likewise, removing the top level dataset with ``remove`` will fail the availability check::

   cd ../
   datalad remove -d my-analysis

But it can be overridden the very same way::

   datalad remove -d my-analysis --reckless availability

And with this, we're done!
Thanks for following along, and reach out with any questions you might have!