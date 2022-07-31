.. _yoda_project:

YODA-compliant data analysis projects
-------------------------------------

Now that you know about the YODA principles, it is time to start working on
``DataLad-101``'s midterm project. Because the midterm project guidelines
require a YODA-compliant data analysis project, you will not only have theoretical
knowledge about the YODA principles, but also gain practical experience.

In principle, you can prepare YODA-compliant data analyses in any programming
language of your choice. But because you are already familiar with
the `Python <https://www.python.org/>`__ programming language, you decide
to script your analysis in Python. Delighted, you find out that there is even
a Python API for DataLad's functionality that you can read about in :ref:`a Findoutmore on DataLad in Python<fom-pythonapi>`.

.. find-out-more:: DataLad's Python API
   :name: fom-pythonapi
   :float:

    .. _python:

    "Whatever you can do with DataLad from the command line, you can also do it with
    DataLad's Python API", begins the lecturer.
    "In addition to the command line interface you are already very familiar with,
    DataLad's functionality can also be used within interactive Python sessions
    or Python scripts.
    This feature can help to automate dataset operations, provides an alternative
    to the command line, and it is immensely useful when creating reproducible
    data analyses."

    All of DataLad's user-oriented commands are exposed via ``datalad.api``.
    Thus, any command can be imported as a stand-alone command like this::

       >>> from datalad.api import <COMMAND>

    Alternatively, to import all commands, one can use

    .. code-block:: python

       >>> import datalad.api as dl

    and subsequently access commands as ``dl.get()``, ``dl.clone()``, and so forth.


    The `developer documentation <http://docs.datalad.org/en/latest/modref.html>`_
    of DataLad lists an overview of all commands, but naming is congruent to the
    command line interface. The only functionality that is not available at the
    command line is ``datalad.api.Dataset``, DataLad's core Python data type.
    Just like any other command, it can be imported like this::

       >>> from datalad.api import Dataset

    or like this::

       >>> import datalad.api as dl
       >>> dl.Dataset()

    A ``Dataset`` is a `class <https://docs.python.org/3/tutorial/classes.html>`_
    that represents a DataLad dataset. In addition to the
    stand-alone commands, all of DataLad's functionality is also available via
    `methods <https://docs.python.org/3/tutorial/classes.html#method-objects>`_
    of this class. Thus, these are two equally valid ways to create a new
    dataset with DataLad in Python::

       >>> from datalad.api import create, Dataset
       # create as a stand-alone command
       >>> create(path='scratch/test')
       [INFO   ] Creating a new annex repo at /home/me/scratch/test
       Out[3]: <Dataset path=/home/me/scratch/test>

       # create as a dataset method
       >>> ds = Dataset(path='scratch/test')
       >>> ds.create()
       [INFO   ] Creating a new annex repo at /home/me/scratch/test
       Out[3]: <Dataset path=/home/me/scratch/test>

    As shown above, the only required parameter for a Dataset is the ``path`` to
    its location, and this location may or may not exist yet.

    Stand-alone functions have a ``dataset=`` argument, corresponding to the
    ``-d/--dataset`` option in their command-line equivalent. You can specify
    the ``dataset=`` argument with a path (string) to your dataset (such as
    ``dataset='.'`` for the current directory, or ``dataset='path/to/ds'`` to
    another location). Alternatively, you can pass a ``Dataset`` instance to it::

        >>> from datalad.api import save, Dataset
        # use save with dataset specified as a path
        >>> save(dataset='path/to/dataset/')
        # use save with dataset specified as a dataset instance
        >>> ds = Dataset('path/to/dataset')
        >>> save(dataset=ds, message="saving all modifications")
        # use save as a dataset method (no dataset argument)
        >>> ds.save(message="saving all modifications")


    **Use cases for DataLad's Python API**

    "Why should one use the Python API? Can we not do everything necessary via the
    command line already? Does Python add anything to this?" asks somebody.

    It is completely up to on you and dependent on your preferred workflow
    whether you decide to use the command line or the Python API of DataLad for
    the majority of tasks. Both are valid ways to accomplish the same results.
    One advantage of using the Python API is the ``Dataset`` though:
    Given that the command line ``datalad`` command has a startup time (even when doing nothing) of
    ~200ms, this means that there is the potential for substantial speed-up when
    doing many calls to the API, and using a persistent Dataset object instance.

.. importantnote:: Use DataLad in languages other than Python

   While there is a dedicated API for Python, DataLad's functions can of course
   also be used with other programming languages, such as Matlab, via standard
   system calls.

   Even if you do not know or like Python, you can just copy-paste the code
   and follow along -- the high-level YODA principles demonstrated in this
   section generalize across programming languages.

For your midterm project submission, you decide to create a data analysis on the
`iris flower data set <https://en.wikipedia.org/wiki/Iris_flower_data_set>`_.
It is a multivariate dataset on 50 samples of each of three species of Iris
flowers (*Setosa*, *Versicolor*, or *Virginica*), with four variables: the length and width of the sepals and petals
of the flowers in centimeters. It is often used in introductory data science
courses for statistical classification techniques in machine learning, and
widely available -- a perfect dataset for your midterm project!

.. importantnote:: Turn data analysis into dynamically generated documents

   Beyond the contents of this section, we have transformed the example analysis also into a template to write a reproducible paper, following the use case :ref:`usecase_reproducible_paper`.
   If you're interested in checking that out, please head over to `github.com/datalad-handbook/repro-paper-sketch/ <https://github.com/datalad-handbook/repro-paper-sketch/>`_.

Raw data as a modular, independent entity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first YODA principle stressed the importance of modularity in a data analysis
project: Every component that could be used in more than one context should be
an independent component.

The first aspect this applies to is the input data of your dataset: There can
be thousands of ways to analyze it, and it is therefore immensely helpful to
have a pristine raw iris dataset that does not get modified, but serves as
input for these analysis.
As such, the iris data should become a standalone DataLad dataset.
For the purpose of this analysis, the DataLad handbook provides an ``iris_data``
dataset at `https://github.com/datalad-handbook/iris_data <https://github.com/datalad-handbook/iris_data>`_.

You can either use this provided input dataset, or find out how to create an
independent dataset from scratch in a :ref:`dedicated Findoutmore <fom-iris>`.

.. find-out-more:: Creating an independent input dataset
   :name: fom-iris
   :float:

   If you acquire your own data for a data analysis, it will not magically exist as a
   DataLad dataset that you can simply install from somewhere -- you'll have
   to turn it into a dataset yourself. Any directory with data that exists on
   your computer can be turned into a dataset with :command:`datalad create --force`
   and a subsequent :command:`datalad save -m "add data" .` to first create a dataset inside of
   an existing, non-empty directory, and subsequently save all of its contents into
   the history of the newly created dataset.
   And that's it already -- it does not take anything more to create a stand-alone
   input dataset from existing data (apart from restraining yourself from
   modifying it afterwards).

   To create the ``iris_data`` dataset at https://github.com/datalad-handbook/iris_data
   we first created a DataLad dataset...

   .. runrecord:: _examples/DL-101-130-101
      :language: console
      :workdir: dl-101/DataLad-101

      # make sure to move outside of DataLad-101!
      $ cd ../
      $ datalad create iris_data

   and subsequently got the data from a publicly available
   `GitHub Gist <https://gist.github.com/netj/8836201>`_, a code snippet or other short standalone information (more on Gists `here <https://docs.github.com/en/github/writing-on-github/editing-and-sharing-content-with-gists/creating-gists#about-gists>`__), with a
   :command:`datalad download-url` command:

    .. runrecord:: _examples/DL-101-130-102
       :workdir: dl-101
       :language: console

       $ cd iris_data
       $ datalad download-url https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv

   Finally, we *published* (more on this later in this section) the dataset
   to :term:`GitHub`.

   With this setup, the iris dataset (a single comma-separated (``.csv``)
   file) is downloaded, and, importantly, the dataset recorded *where* it
   was obtained from thanks to :command:`datalad download-url`, thus complying
   to the second YODA principle.
   This way, upon installation of the dataset, DataLad knows where to
   obtain the file content from. You can :command:`datalad clone` the iris
   dataset and find out with a ``git annex whereis iris.csv`` command.


"Nice, with this input dataset I have sufficient provenance capture for my
input dataset, and I can install it as a modular component", you think as you
mentally tick off YODA principle number 1 and 2. "But before I can install it,
I need an analysis superdataset first."

Building an analysis dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is an independent raw dataset as input data, but there is no place
for your analysis to live, yet. Therefore, you start your midterm project
by creating an analysis dataset. As this project is part of ``DataLad-101``,
you do it as a subdataset of ``DataLad-101``.
Remember to specify the ``--dataset`` option of :command:`datalad create`
to link it as a subdataset!

You naturally want your dataset to follow the YODA principles, and, as a start,
you use the ``cfg_yoda`` procedure to help you structure the dataset [#f1]_:

.. runrecord:: _examples/DL-101-130-103
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 10_yoda
   :notes: Let's create a data analysis project with a yoda procedure

   # inside of DataLad-101
   $ datalad create -c yoda --dataset . midterm_project

.. index:: ! datalad command; datalad subdatasets

The :command:`datalad subdatasets` command can report on which subdatasets exist for
``DataLad-101``. This helps you verify that the command succeeded and the
dataset was indeed linked as a subdataset to ``DataLad-101``:

.. runrecord:: _examples/DL-101-130-104
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad subdatasets

Not only the ``longnow`` subdataset, but also the newly created
``midterm_project`` subdataset are displayed -- wonderful!

But back to the midterm project now. So far, you have created a pre-structured
analysis dataset. As a next step, you take care of installing and linking the
raw dataset for your analysis adequately to your ``midterm_project`` dataset
by installing it as a subdataset. Make sure to install it as a subdataset of
``midterm_project``, and not ``DataLad-101``!

.. runrecord:: _examples/DL-101-130-105
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 10_yoda
   :notes: Now clone input data as a subdataset

   $ cd midterm_project
   # we are in midterm_project, thus -d . points to the root of it.
   $ datalad clone -d . \
     https://github.com/datalad-handbook/iris_data.git \
     input/

Note that we did not keep its original name, ``iris_data``, but rather provided
a path with a new name, ``input``, because this much more intuitively comprehensible.

After the input dataset is installed, the directory structure of ``DataLad-101``
looks like this:

.. runrecord:: _examples/DL-101-130-106
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: here is how the directory structure looks like

   $ cd ../
   $ tree -d
   $ cd midterm_project

Importantly, all of the subdatasets are linked to the higher-level datasets,
and despite being inside of ``DataLad-101``, your ``midterm_project`` is an independent
dataset, as is its ``input/`` subdataset:

.. figure:: ../artwork/src/virtual_dstree_dl101_midterm.svg
   :alt: Overview of (linked) datasets in DataLad-101.
   :width: 50%



YODA-compliant analysis scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you have an ``input/`` directory with data, and a ``code/`` directory
(created by the YODA procedure) for your scripts, it is time to work on the script
for your analysis. Within ``midterm_project``, the ``code/`` directory is where
you want to place your scripts.

But first, you plan your research question. You decide to do a
classification analysis with a k-nearest neighbors algorithm [#f2]_. The iris
dataset works well for such questions. Based on the features of the flowers
(sepal and petal width and length) you will try to predict what type of
flower (*Setosa*, *Versicolor*, or *Virginica*) a particular flower in the
dataset is. You settle on two objectives for your analysis:

#. Explore and plot the relationship between variables in the dataset and save
   the resulting graphic as a first result.
#. Perform a k-nearest neighbor classification on a subset of the dataset to
   predict class membership (flower type) of samples in a left-out test set.
   Your final result should be a statistical summary of this prediction.

To compute the analysis you create the following Python script inside of ``code/``:

.. runrecord:: _examples/DL-101-130-107
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :emphasize-lines: 11-13, 23, 42
   :cast: 10_yoda
   :notes: Let's create code for an analysis

   $ cat << EOT > code/script.py

   import argparse
   import pandas as pd
   import seaborn as sns
   from sklearn import model_selection
   from sklearn.neighbors import KNeighborsClassifier
   from sklearn.metrics import classification_report

   parser = argparse.ArgumentParser(description="Analyze iris data")
   parser.add_argument('data', help="Input data (CSV) to process")
   parser.add_argument('output_figure', help="Output figure path")
   parser.add_argument('output_report', help="Output report path")
   args = parser.parse_args()

   # prepare the data as a pandas dataframe
   df = pd.read_csv(args.data)
   attributes = ["sepal_length", "sepal_width", "petal_length","petal_width", "class"]
   df.columns = attributes

   # create a pairplot to plot pairwise relationships in the dataset
   plot = sns.pairplot(df, hue='class', palette='muted')
   plot.savefig(args.output_figure)

   # perform a K-nearest-neighbours classification with scikit-learn
   # Step 1: split data in test and training dataset (20:80)
   array = df.values
   X = array[:,0:4]
   Y = array[:,4]
   test_size = 0.20
   seed = 7
   X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,
                                                                       test_size=test_size,
                                                                       random_state=seed)
   # Step 2: Fit the model and make predictions on the test dataset
   knn = KNeighborsClassifier()
   knn.fit(X_train, Y_train)
   predictions = knn.predict(X_test)

   # Step 3: Save the classification report
   report = classification_report(Y_test, predictions, output_dict=True)
   df_report = pd.DataFrame(report).transpose().to_csv(args.output_report)

   EOT

This script will

- take three positional arguments: The input data, a path to save a figure under, and path to save the final prediction report under. By including these input and output specifications in a :command:`datalad run` command when we run the analysis, we can ensure that input data is retrieved prior to the script execution, and that as much actionable provenance as possible is recorded [#f5]_.
- read in the data, perform the analysis, and save the resulting figure and ``.csv`` prediction report into the root of ``midterm_project/``. Note how this helps to fulfil YODA principle 1 on modularity:
  Results are stored outside of the pristine input subdataset.

A short help text explains how the script shall be used:

.. code-block:: bash

   python code/script.py -h                                                  2 !
   usage: script.py [-h] data output_figure output_report

   Analyze iris data

   positional arguments:
      data           Input data (CSV) to process
      output_figure  Output figure path
      output_report  Output report path

   optional arguments:
   -h, --help     show this help message and exit

The script execution would thus be ``python3 code/script.py <path-to-input> <path-to-figure-output> <path-to-report-output>``.
When parametrizing the input and output path parameters, we just need make sure that all paths  are *relative*, such that the ``midterm_project`` analysis is completely self-contained within the dataset, contributing to fulfill the second YODA principle.

Let's run a quick :command:`datalad status`...

.. runrecord:: _examples/DL-101-130-108
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: datalad status will show a new file

   $ datalad status

... and save the script to the subdataset's history. As the script completes your
analysis setup, we *tag* the state of the dataset to refer to it easily at a later
point with the ``--version-tag`` option of :command:`datalad save`.

.. runrecord:: _examples/DL-101-130-109
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Save the analysis to the history

   $ datalad save -m "add script for kNN classification and plotting" \
     --version-tag ready4analysis \
     code/script.py

.. find-out-more:: What is a tag?

   :term:`tag`\s are markers that you can attach to commits in your dataset history.
   They can have any name, and can help you and others to identify certain commits
   or dataset states in the history of a dataset. Let's take a look at how the tag
   you just created looks like in your history with :command:`git show`.
   Note how we can use a tag just as easily as a commit :term:`shasum`:

   .. runrecord:: _examples/DL-101-130-110
      :workdir: dl-101/DataLad-101/midterm_project
      :lines: 1-13
      :language: console

      $ git show ready4analysis

   This tag thus identifies the version state of the dataset in which this script
   was added.
   Later we can use this tag to identify the point in time at which
   the analysis setup was ready -- much more intuitive than a 40-character shasum!
   This is handy in the context of a :command:`datalad rerun` for example::

      $ datalad rerun --since ready4analysis

   would rerun any :command:`run` command in the history performed between tagging
   and the current dataset state.

Finally, with your directory structure being modular and intuitive,
the input data installed, the script ready, and the dataset status clean,
you can wrap the execution of the script in a :command:`datalad run` command. Note that
simply executing the script would work as well -- thanks to DataLad's Python API.
But using :command:`datalad run` will capture full provenance, and will make
re-execution with :command:`datalad rerun` easy.

.. importantnote:: Additional software requirements: pandas, seaborn, sklearn

   Note that you need to have the following Python packages installed to run the
   analysis [#f3]_:

   - `pandas <https://pandas.pydata.org/>`_
   - `seaborn <https://seaborn.pydata.org/>`_
   - `sklearn <https://scikit-learn.org/>`_

   The packages can be installed via ``pip``. Check the footnote [#f3]_ for code
   snippets to copy and paste. However, if you do not want to install any
   Python packages, do not execute the remaining code examples in this section
   -- an upcoming section on ``datalad containers-run`` will allow you to
   perform the analysis without changing your Python software-setup.

.. windows-wit:: You may need to use "python", not "python3"

   If executing the code below returns an exit code of 9009, there may be no ``python3`` -- instead, it is called solely ``python``.
   Please run the following instead (adjusted for line breaks, you should be able to copy-paste this as a whole)::

      datalad run -m "analyze iris data with classification analysis" ^
       --input "input/iris.csv" ^
       --output "pairwise_relationships.png" ^
       --output "prediction_report.csv" ^
       "python code/script.py {inputs} {outputs}"

.. runrecord:: _examples/DL-101-130-111
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: The datalad run command can reproducibly execute a command reproducibly

   $ datalad run -m "analyze iris data with classification analysis" \
     --input "input/iris.csv" \
     --output "pairwise_relationships.png" \
     --output "prediction_report.csv" \
     "python3 code/script.py {inputs} {outputs}"

As the successful command summary indicates, your analysis seems to work! Two
files were created and saved to the dataset: ``pairwise_relationships.png``
and ``prediction_report.csv``. If you want, take a look and interpret
your analysis. But what excites you even more than a successful data science
project on first try is that you achieved complete provenance capture:

- Every single file in this dataset is associated with an author and a time
  stamp for each modification thanks to :command:`datalad save`.
- The raw dataset knows where the data came from thanks to :command:`datalad clone`
  and :command:`datalad download-url`.
- The subdataset is linked to the superdataset thanks to
  :command:`datalad clone -d`.
- The :command:`datalad run` command took care of linking the outputs of your
  analysis with the script and the input data it was generated from, fulfilling
  the third YODA principle.

Let's take a look at the history of the ``midterm_project`` analysis
dataset:

.. runrecord:: _examples/DL-101-130-112
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Let's take a look at the history

   $ git log --oneline

"Wow, this is so clean an intuitive!" you congratulate yourself. "And I think
this was and will be the fastest I have ever completed a midterm project!"
But what is still missing is a human readable description of your dataset.
The YODA procedure kindly placed a ``README.md`` file into the root of your
dataset that you can use for this [#f4]_.

.. importantnote:: Template for introduction to DataLad

   If you plan to share your own datasets with people that are unfamiliar with
   DataLad, it may be helpful to give a short explanation of what a DataLad
   dataset is and what it can do. For this, you can use a ready-made text
   block that the handbook provides. To find this textblock, go to
   :ref:`dataset_textblock`.

.. runrecord:: _examples/DL-101-130-113
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: create human readable information for your project

   # with the >| redirection we are replacing existing contents in the file
   $ cat << EOT >| README.md

   # Midterm YODA Data Analysis Project

   ## Dataset structure

   - All inputs (i.e. building blocks from other sources) are located in input/.
   - All custom code is located in code/.
   - All results (i.e., generated files) are located in the root of the dataset:
     - "prediction_report.csv" contains the main classification metrics.
     - "output/pairwise_relationships.png" is a plot of the relations between features.

   EOT

.. runrecord:: _examples/DL-101-130-114
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: The README file is now modified

   $ datalad status

.. runrecord:: _examples/DL-101-130-115
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Let's save this change

   $ datalad save -m "Provide project description" README.md

Note that one feature of the YODA procedure was that it configured certain files
(for example everything inside of ``code/``, and the ``README.md`` file in the
root of the dataset) to be saved in Git instead of git-annex. This was the
reason why the ``README.md`` in the root of the dataset was easily modifiable [#f4]_.

.. find-out-more:: Saving contents with Git regardless of configuration with --to-git

   .. index:: ! datalad command; save --to-git

   The ``yoda`` procedure in ``midterm_project`` applied a different configuration
   within ``.gitattributes`` than the ``text2git`` procedure did in ``DataLad-101``.
   Within ``DataLad-101``, any text file is automatically stored in :term:`Git`.
   This is not true in ``midterm_project``: Only the existing ``README.md`` files and
   anything within ``code/`` are stored -- everything else will be annexed.
   That means that if you create any other file, even text files, inside of
   ``midterm_project`` (but not in ``code/``), it will be managed by :term:`git-annex`
   and content-locked after a :command:`datalad save` -- an inconvenience if it
   would be a file that is small enough to be handled by Git.

   Luckily, there is a handy shortcut to saving files in Git that does not
   require you to edit configurations in ``.gitattributes``: The ``--to-git``
   option for :command:`datalad save`.

   .. code-block:: bash

      $ datalad save -m "add sometextfile.txt" --to-git sometextfile.txt

After adding this short description to your ``README.md``, your dataset now also
contains sufficient human-readable information to ensure that others can understand
everything you did easily.
The only thing left to do is to hand in your assignment. According to the
syllabus, this should be done via :term:`GitHub`.

.. find-out-more:: What is GitHub?

   GitHub is a web based hosting service for Git repositories. Among many
   different other useful perks it adds features that allow collaboration on
   Git repositories. `GitLab <https://about.gitlab.com/>`_ is a similar
   service with highly similar features, but its source code is free and open,
   whereas GitHub is a subsidiary of Microsoft.

   Web-hosting services like GitHub and :term:`GitLab` integrate wonderfully with
   DataLad. They are especially useful for making your dataset publicly available,
   if you have figured out storage for your large files otherwise (as large content
   can not be hosted for free by GitHub). You can make DataLad publish large file content to one location
   and afterwards automatically push an update to GitHub, such that
   users can install directly from GitHub/GitLab and seemingly also obtain large file
   content from GitHub. GitHub can also resolve subdataset links to other GitHub
   repositories, which lets you navigate through nested datasets in the web-interface.

   .. image:: ../artwork/src/screenshot_midtermproject.png
      :alt: The midterm project repository, published to GitHub

   The above screenshot shows the linkage between the analysis project you will create
   and its subdataset. Clicking on the subdataset (highlighted) will take you to the iris dataset
   the handbook provides, shown below.

   .. image:: ../artwork/src/screenshot_submodule.png
      :alt: The input dataset is linked

.. index:: ! datalad command; create-sibling-github
.. _publishtogithub:

Publishing the dataset to GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. importantnote:: Demo needs a GitHub account or alternative

   The upcoming part requires a GitHub account. If you do not have one you
   can either

   - Create one now -- it is fast, free, and you can get rid of it afterwards,
     if you want to.
   - Or exchange the command ``create-sibling-github`` with
     ``create-sibling-gitlab`` if you have a GitLab account instead of a GitHub
     account (checkout `the documentation <http://docs.datalad.org/en/stable/generated/man/datalad-create-sibling-gitlab.html>`_ for differences in invocation beforehand, though).
   - Decide to not follow along.

For this, you need to

- create a repository for this dataset on GitHub,
- configure this GitHub repository to be a :term:`sibling` of the ``midterm_project`` dataset,
- and *publish* your dataset to GitHub.

.. index:: ! datalad command; create-sibling-gitlab

Luckily, DataLad can make all of this very easy with the
:command:`datalad create-sibling-github` (:manpage:`datalad-create-sibling-github` manual)
command (or, for `GitLab <https://about.gitlab.com/>`_, :command:`datalad create-sibling-gitlab`,
:manpage:`datalad-create-sibling-gitlab` manual).

The two commands have different arguments and options.
Here, we look at :command:`datalad create-sibling-github`.
The command takes a repository name and GitHub authentication credentials
(either in the command line call with options ``github-login <NAME>`` and
``github-passwd <PASSWORD>``, with an *oauth* `token <https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_ stored in the Git
configuration, or interactively).

.. importantnote:: GitHub deprecated User Password authentication

   GitHub `decided to deprecate user-password authentication <https://developer.github.com/changes/2020-02-14-deprecating-password-auth/>`_ and will only support authentication via personal access token from November 13th 2020 onwards.
   Upcoming changes in DataLad's API will reflect this change starting with DataLad version ``0.13.6`` by removing the ``github-passwd`` argument.
   Starting with DataLad ``0.16.0``, a new set of commands for interactions with a variety of hosting services will be introduced (for more information, see section :ref:`share_hostingservice`).

   To ensure successful authentication, please create a personal access token at `github.com/settings/tokens <https://github.com/settings/tokens>`_ [#f6]_, and either

   * supply the token with the argument ``--github-login <TOKEN>`` from the command line,
   * or supply the token from the command line when queried for a password

Based on the credentials and the
repository name, it will create a new, empty repository on GitHub, and
configure this repository as a sibling of the dataset:


.. ifconfig:: internal

    .. runrecord:: _examples/DL-101-130-116
       :language: console

       $ python3 /home/me/makepushtarget.py '/home/me/dl-101/DataLad-101/midterm_project' 'github' '/home/me/pushes/midterm_project' False True

.. windows-wit:: Your shell will not display credentials

   Don't be confused if you are prompted for your GitHub credentials, but can't seem to type -- the terminal protects your private information by not displaying what you type.
   Simply type in what is requested, and press enter.

.. code-block:: bash

   $ datalad create-sibling-github -d . midtermproject
   .: github(-) [https://github.com/adswa/midtermproject.git (git)]
   'https://github.com/adswa/midtermproject.git' configured as sibling 'github' for <Dataset path=/home/me/dl-101/DataLad-101/midterm_project>


Verify that this worked by listing the siblings of the dataset:

.. code-block:: bash

   $ datalad siblings
   [WARNING] Failed to determine if github carries annex.
   .: here(+) [git]
   .: github(-) [https://github.com/adswa/midtermproject.git (git)]

.. gitusernote:: Create-sibling-github internals

   Creating a sibling on GitHub will create a new empty repository under the
   account that you provide and set up a *remote* to this repository. Upon a
   :command:`datalad push` to this sibling, your datasets history
   will be pushed there.

   .. index:: ! datalad command; push

On GitHub, you will see a new, empty repository with the name
``midtermproject``. However, the repository does not yet contain
any of your dataset's history or files. This requires *publishing* the current
state of the dataset to this :term:`sibling` with the :command:`datalad push`
(:manpage:`datalad-push` manual) command.

.. importantnote:: Learn how to push "on the job"

    Publishing is one of the remaining big concepts that this handbook tries to
    convey. However, publishing is a complex concept that encompasses a large
    proportion of the previous handbook content as a prerequisite. In order to be
    not too overwhelmingly detailed, the upcoming sections will approach
    :command:`push` from a "learning-by-doing" perspective:
    You will see a first :command:`push` to GitHub below, and the :ref:`Findoutmore on the published dataset <fom-midtermclone>`
    at the end of this section will already give a practical glimpse into the
    difference between annexed contents and contents stored in Git when pushed
    to GitHub. The chapter :ref:`chapter_thirdparty` will extend on this,
    but the section :ref:`push`
    will finally combine and link all the previous contents to give a comprehensive
    and detailed wrap up of the concept of publishing datasets. In this section,
    you will also find a detailed overview on how :command:`push` works and which
    options are available. If you are impatient or need an overview on publishing,
    feel free to skip ahead. If you have time to follow along, reading the next
    sections will get you towards a complete picture of publishing a bit more
    small-stepped and gently.
    For now, we will start with learning by doing, and
    the fundamental basics of :command:`datalad push`: The command
    will make the last saved state of your dataset available (i.e., publish it)
    to the :term:`sibling` you provide with the ``--to`` option.

.. runrecord:: _examples/DL-101-130-118
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad push --to github

Thus, you have now published your dataset's history to a public place for others
to see and clone. Below we will explore how this may look and feel for others.

.. importantnote:: Cave! Your default branch may be git-annex

   If your published dataset looks weird, with cryptic directories names instead of file names, GitHub may have made the :term:`git-annex branch` your repositories' default branch.
   Learn how to fix this in the  corresponding :ref:`FAQ <gitannexdefault>`.

There is one important detail first, though: By default, your tags will not be published.
Thus, the tag ``ready4analysis`` is not pushed to GitHub, and currently this
version identifier is unavailable to anyone else but you.
The reason for this is that tags are viral -- they can be removed locally, and old
published tags can cause confusion or unwanted changes. In order to publish a tag,
an additional :command:`git push`  with the ``--tags`` option is required:

.. code-block:: bash

   $ git push github --tags

.. gitusernote:: Pushing tags

    Note that this is a :command:`git push`, not :command:`datalad push`.
    Tags could be pushed upon a :command:`datalad push`, though, if one
    configures (what kind of) tags to be pushed. This would need to be done
    on a per-sibling basis in ``.git/config`` in the ``remote.*.push``
    configuration. If you had a :term:`sibling` "github", the following
    configuration would push all tags that start with a ``v`` upon a
    :command:`datalad push --to github`::

       $ git config --local remote.github.push 'refs/tags/v*'

    This configuration would result in the following entry in ``.git/config``::

       [remote "github"]
             url = git@github.com/adswa/midtermproject.git
             fetch = +refs/heads/*:refs/remotes/github/*
             annex-ignore = true
             push = refs/tags/v*

Yay! Consider your midterm project submitted! Others can now install your
dataset and check out your data science project -- and even better: they can
reproduce your data science project easily from scratch (take a look into the :ref:`Findoutmore <fom-midtermclone>` to see how)!

.. find-out-more:: On the looks and feels of this published dataset
   :name: fom-midtermclone
   :float:

   Now that you have created and published such a YODA-compliant dataset, you
   are understandably excited how this dataset must look and feel for others.
   Therefore, you decide to install this dataset into a new location on your
   computer, just to get a feel for it.

   Replace the ``url`` in the :command:`clone` command below with the path
   to your own ``midtermproject`` GitHub repository, or clone the "public"
   ``midterm_project`` repository that is available via the Handbook's GitHub
   organization at `github.com/datalad-handbook/midterm_project <https://github.com/datalad-handbook/midterm_project>`_:

   .. runrecord:: _examples/DL-101-130-119
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ cd ../../
      $ datalad clone "https://github.com/adswa/midtermproject.git"

   Let's start with the subdataset, and see whether we can retrieve the
   input ``iris.csv`` file. This should not be a problem, since its origin
   is recorded:

   .. runrecord:: _examples/DL-101-130-120
      :language: console
      :workdir: dl-101

      $ cd midtermproject
      $ datalad get input/iris.csv

   Nice, this worked well. The output files, however, can not be easily
   retrieved:

   .. runrecord:: _examples/DL-101-130-121
      :language: console
      :workdir: dl-101/midtermproject

      $ datalad get prediction_report.csv pairwise_relationships.png

   Why is that? This is the first detail of publishing datasets we will dive into.
   When publishing dataset content to GitHub with :command:`datalad push`, it is
   the dataset's *history*, i.e., everything that is stored in Git, that is
   published. The file *content* of these particular files, though, is managed
   by :term:`git-annex` and not stored in Git, and
   thus only information about the file name and location is known to Git.
   Because GitHub does not host large data for free, annexed file content always
   needs to be deposited somewhere else (e.g., a web server) to make it
   accessible via :command:`datalad get`. The chapter :ref:`chapter_thirdparty`
   will demonstrate how this can be done. For this dataset, it is not
   necessary to make the outputs available, though: Because all provenance
   on their creation was captured, we can simply recompute them with the
   :command:`datalad rerun` command. If the tag was published we can simply
   rerun any :command:`datalad run` command since this tag:

   .. code-block:: bash

      $ datalad rerun --since ready4analysis

   But without the published tag, we can rerun the analysis by specifying its
   shasum:

   .. runrecord:: _examples/DL-101-130-122
      :language: console
      :workdir: dl-101/midtermproject
      :realcommand: echo "$ datalad rerun $(git rev-parse HEAD~1)" && datalad rerun $(git rev-parse HEAD~1)

   Hooray, your analysis was reproduced! You happily note that rerunning your
   analysis was incredibly easy -- it would not even be necessary to have any
   knowledge about the analysis at all to reproduce it!
   With this, you realize again how letting DataLad take care of linking input,
   output, and code can make your life and others' lives so much easier.
   Applying the YODA principles to your data analysis was very beneficial indeed.
   Proud of your midterm project you can not wait to use those principles the
   next time again.

    .. image:: ../artwork/src/reproduced.svg
       :width: 50%

.. gitusernote:: Push internals

   The :command:`datalad push` uses ``git push``, and ``git annex copy`` under
   the hood. Publication targets need to either be configured remote Git repositories,
   or git-annex special remotes (if they support data upload).


.. only:: adminmode

    Add a tag at the section end.

      .. runrecord:: _examples/DL-101-130-123
         :language: console
         :workdir: dl-101/DataLad-101

         $ git branch sct_yoda_project


.. rubric:: Footnotes

.. [#f1] Note that you could have applied the YODA procedure not only right at
         creation of the dataset with ``-c yoda``, but also after creation
         with the :command:`datalad run-procedure` command::

           $ cd midterm_project
           $ datalad run-procedure cfg_yoda

         Both ways of applying the YODA procedure will lead to the same
         outcome.

.. [#f2] If you want to know more about this algorithm,
         `this blogpost <https://towardsdatascience.com/machine-learning-basics-with-the-k-nearest-neighbors-algorithm-6a6e71d01761>`_
         gives an accessible overview. However, the choice of analysis method
         for the handbook is rather arbitrary, and understanding the k-nearest
         neighbor algorithm is by no means required for this section.

.. [#f3] It is recommended (but optional) to create a
         `virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ and
         install the required Python packages inside of it:

         .. code-block:: bash

            # create and enter a new virtual environment (optional)
            $ virtualenv --python=python3 ~/env/handbook
            $ . ~/env/handbook/bin/activate

         .. code-block:: bash

            # install the Python packages from PyPi via pip
            pip install seaborn pandas sklearn

.. [#f4] Note that all ``README.md`` files the YODA procedure created are
         version controlled by Git, not git-annex, thanks to the
         configurations that YODA supplied. This makes it easy to change the
         ``README.md`` file. The previous section detailed how the YODA procedure
         configured your dataset. If you want to re-read the full chapter on
         configurations and run-procedures, start with section :ref:`config`.


.. [#f5]  Alternatively, if you were to use DataLad's Python API, you could import and expose it as ``dl.<COMMAND>`` and ``dl.get()`` the relevant files. This however, would not record them as provenance in the dataset's history.

.. [#f6] Instead of using GitHub's WebUI you could also obtain a token using the command line GitHub interface (https://github.com/sociomantic-tsunami/git-hub) by running ``git hub setup`` (if no 2FA is used).
         If you decide to use the command line interface, here is help on how to use it:
         Clone the `GitHub repository <https://github.com/sociomantic-tsunami/git-hub>`_ to your local computer.
         Decide whether you want to build a Debian package to install, or install the single-file Python script distributed in the repository.
         Make sure that all `requirements <https://github.com/sociomantic-tsunami/git-hub>`_ for your preferred version are installed , and run either ``make deb`` followed by ``sudo dpkg -i deb/git-hub*all.deb``, or ``make install``.

