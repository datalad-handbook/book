A YODA-compliant data analysis project with DataLad
---------------------------------------------------

Now that you know about the YODA principles and DataLad's Python API, it is
time to start working on ``DataLad-101``'s midterm project.
In order to combine the previous sections, this midterm project is a
YODA-compliant data analysis project, written in Python, and set up in a
DataLad dataset.

For your submission, you decide to analyse the
`iris flower data set <https://en.wikipedia.org/wiki/Iris_flower_data_set>`_.
It is a multivariate data set on 50 samples of each of three species of Iris
flowers (*Setosa*, *Versicolor*, or *Virginica*), with four variables: the length and width of the sepals and petals
of the flowers in centimeters. It is often used in introductory data science
courses for statistical classification techniques in machine learning, and
widely available, among many other sources as
`Github gists <https://gist.github.com/netj/8836201>`_.

To start your analysis project and comply to the YODA principles, you set up
an independent data dataset with your project's raw data. For this, create a
new dataset outside of ``DataLad-101``:

.. runrecord:: _examples/DL-101-130-101
   :language: console
   :workdir: dl-101/DataLad-101

   # make sure to move outside of DataLad-101!
   $ cd ../
   $ datalad create iris_data

Inside of this newly created dataset, get the data. It is publicly
available from a
`Github Gist <https://gist.github.com/netj/8836201>`_,
and we can use :command:`datalad download-url` to get it:

.. findoutmore:: What are Github Gists?

   Github Gists are a particular service offered by Github that allow users
   to share pieces of code snippets and other short/small standalone
   information. Find out more on Gists
   `here <https://help.github.com/en/github/writing-on-github/creating-gists#about-gists>`__.


.. runrecord:: _examples/DL-101-130-102
   :workdir: dl-101
   :language: console

   $ cd iris_data
   $ datalad download-url https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv

.. todo::

   or do we rather want to install/clone the dataset?

This downloaded the iris dataset as a comma-seperated (``.csv``) file, and,
importantly, recorded where it was obtained from. "Nice, this way I have
sufficient provenance capture for my input dataset!" you think as you
mentally tick of YODA principle 2 for your input data.

Now that you have this raw dataset, it is time to create an analysis for your
midterm project.
You start by creating an analysis dataset. Let's do it as a subdataset
of ``DataLad-101``. Remember to specify the ``--dataset`` option within
:command:`datalad create` to link it as a subdataset!
After the last lecture, you naturally want your dataset to follow the YODA
principles. As a start, you use the ``cfg_yoda`` procedure to help you
structure the dataset [#f1]_.

.. runrecord:: _examples/DL-101-130-103
   :language: console
   :workdir: dl-101/iris_data

   # go back into DataLad-101
   $ cd ../DataLad-101
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

As a next step you take care of linking your raw dataset
adequately to your ``midterm_project`` dataset by installing it as a
subdataset. Make sure to install it as a subdataset of ``midterm_project``,
and not ``DataLad-101``!

.. runrecord:: _examples/DL-101-130-105
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   # we are in midterm_project, thus -d . points to the root of it.
   $ datalad install -d . --source ../../iris_data input/

After this directory is created, the directory structure of ``DataLad-101``
looks like this:

.. runrecord:: _examples/DL-101-130-106
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ cd ../
   $ tree -d

Now that you have an ``input/`` directory with data, and a ``code/`` directory
(created by the YODA procedure) for your scripts, it is time to work on the script
for your analysis. Within ``midterm_project``, the ``code/`` directory is where
you want to place your scripts. Finally you can try out the Python API of DataLad!

But first, you plan your research question. You decide to do a
classification analysis with a k-nearest neighbors algorithm [#f2]_. The iris
dataset works well for such questions. Based on the features of the flowers
(sepal and petal width and length) you will try to predict what type of
flower (*Setosa*, *Versicolor*, or *Virginica*) a particular flower in the
dataset is. You settle on two objectives for your analysis:

#. Explore and plot the relationship between variables in the dataset and save
   the resulting graphic as a first result.
#. Perform a k-nearest neighbour classification on a subset of the dataset to
   predict class membership (flower type) of samples in a left-out test set.
   Your final result should be a statistical summary of this prediction.

To compute the analysis you create the following Python script inside of ``code/``:

.. runrecord:: _examples/DL-101-130-107
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :emphasize-lines: 8, 10, 13-14, 23, 42

   $ cat << EOT > code/script.py

   import pandas as pd
   import seaborn as sns
   from sklearn import model_selection
   from sklearn.neighbors import KNeighborsClassifier
   from sklearn.metrics import classification_report
   from datalad.api import get

   data = "input/iris.csv"

   # make sure that the data is obtained:
   get(data)

   # prepare the data as a pandas dataframe
   df = pd.read_csv(data)
   attributes = ["sepal_length", "sepal_width", "petal_length","petal_width", "class"]
   df.columns = attributes

   # create a pairplot to plot pairwise relationships in the dataset
   plot = sns.pairplot(df, hue='class')
   plot.savefig('pairwise_relationships.png')

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
   df_report = pd.DataFrame(report).transpose().to_csv('prediction_report.csv')

   EOT

This script will

- make sure to install the linked subdataset and retrieve the data prior to reading it in (l. 12), and
- save the resulting figure (l. 21) and ``.csv`` file (l 40) into the root of
  ``midterm_project/``. This will help to fulfil YODA principle 1 on modularity
  by storing results away from the input subdataset.

Note how all paths (to input data and output files) are *relative*, such that the
``midterm_project`` analysis is completely self-contained within the dataset.

Let's run a quick :command:`datalad status`...

.. runrecord:: _examples/DL-101-130-108
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad status

... and save the script to the subdataset's history. As the script completes your
analysis setup, we *tag* the state of the dataset to refer to it easily at a later
point.

.. runrecord:: _examples/DL-101-130-109
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad save -m "add script for kNN classification and plotting" --version-tag ready4analysis code/script.py

.. findoutmore:: What is a tag?

   :term:`tag`\s are markers that you can attach to commits in your dataset history.
   They can have any name, and can help you and others to identify certain commits
   or dataset states in the history of a dataset. Let's take a look at how the tag
   you just created looks like in your history:

   .. runrecord:: _examples/DL-101-130-110
      :workdir: dl-101/DataLad-101/midterm_project
      :language: console
      :emphasize-lines: 3

      $ git log -p -n 1

   Later we can use this tag to identify the version state of the dataset in which
   the analysis setup was ready -- much more intuitive than a 40-character shasum!

Finally, with your directory structure being modular and intuitive,
the input data installed, the script ready, and the dataset status clean,
you can wrap the execution of the script in a :command:`datalad run` command.

.. note::

   Note that you need to have the following Python packages installed to run the
   analysis [#f3]_:

   - `pandas <https://pandas.pydata.org/>`_
   - `seaborn <https://seaborn.pydata.org/>`_
   - `sklearn <https://scikit-learn.org/>`_

   The packages can be installed via ``pip``. Check the footnote [#f3]_ for code
   snippets to copy and paste. However, if you do not want to install any
   Python packages, do not execute the remaining code examples in this sections
   -- an upcoming section on ``datalad containers-run`` will allow you to
   perform the analysis without changing with your Python software-setup.

.. runrecord:: _examples/DL-101-130-111
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad run -m "analyze iris data with classification analysis" \
     --input "input/iris.csv" \
     --output "prediction_report.csv" \
     --output "pairwise_relationships.png" \
     "python3 code/script.py"

As the successful command summary indicates, your analysis seems to work! Two
files were created and saved to the dataset: ``output/pairwise_relationships.png``
and ``output/prediction_report.csv``. If you want, take a look and interpret
your analysis. But what excites you even more than a successful data science
project on first try is that you achieved complete provenance capture:

- Every single file in this dataset is associated with an author and a time
  stamp for each modification thanks to :command:`datalad save`.
- The raw dataset knows where the data came from thanks to
  :command:`datalad download-url`.
- The subdataset is linked to the superdataset thanks to
  :command:`datalad install -d`.
- The :command:`datalad run` command took care of linking the outputs of your
  analysis with the script and the input data it was generated from.

Let's take a look at the history of the ``midterm_project`` analysis
dataset:

.. runrecord:: _examples/DL-101-130-112
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ git log

"Wow, this is so clean an intuitive!" you congratulate yourself. "And I think
this was and will be the fastest I have ever completed a midterm project!"
But what is still missing is a human readable description of your dataset.
The YODA procedure kindly placed a ``README.md`` file into the root of your
dataset that you can use for this [#f4]_.

.. runrecord:: _examples/DL-101-130-113
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

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

   $ datalad status

.. runrecord:: _examples/DL-101-130-115
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad save -m "Provide project description" README.md


Note that one feature of the YODA procedure was that it configured certain files
(for examples everything inside of ``code/`` and the ``README.md`` file in the
root of the dataset) to be saved in Git instead of Git-annex. This was the
reason why the ``README.md`` in the root of the dataset was easily modifiable [#f4]_.

.. findoutmore:: Saving contents with Git regardless of configuration with --to-git

   .. index:: datalad command; save --to-git

   The ``yoda`` procedure in ``midterm_project`` applied a different configuration
   within ``.gitattributes`` than the ``text2git`` procedure did in ``DataLad-101``.
   Within ``DataLad-101``, any text file is automatically stored in :term:`Git`.
   This is not true in ``midterm_project``: Only the existing ``README.md`` files and
   anything within ``code/`` are stored -- everything else will be annexed.
   That means that if you create any other file, even text files, inside of
   ``midterm_project`` (but not in ``code/``), it will be managed by :term:`Git-annex`
   and content-locked after a :command:`datalad save` -- an inconvenience if it
   would be a file that is small enough to be handled by Git.

   Luckily, there is a handy shortcut to saving files in Git that does not
   require you to edit configurations in ``.gitattributes``: The ``--to-git``
   option for :command:`datalad save`.

   .. code-block:: bash

      $ datalad save -m "add sometextfile.txt" --to-git sometextfile.txt

After adding this short description to your ``README.md`` your dataset now also
contains sufficient human-readable information to ensure that others can understand
everything you did easily.
The only thing left to do is to hand in your assignment. According to the
syllabus, this should be done via :term:`Github`.

.. findoutmore:: What is Github?

   Github is a web based hosting service for Git repositories. Among many
   different other useful perks it adds features that allow collaboration on
   Git repositories. `Gitlab <https://about.gitlab.com/>`_ is a similar
   service with highly similar features, but its source code is free and open,
   whereas Github is a subsidiary of Microsoft.

   Web-hosting services like Github and Gitlab integrate wonderfully with
   DataLad. They are especially useful for making your dataset publicly available,
   if you have figured out storage for your large files otherwise (as large content
   can not be hosted by Github). You can make DataLad publish large file content to one location
   and afterwards automatically push an update to Github, such that
   users can install directly from Github/Gitlab and seemingly also obtain large file
   content from Github. Github can also resolve subdataset links to other Github
   repositories, which lets you navigate through nested datasets in the web-interface.

   .. todo::

      maybe a screenshot here.

.. note::

   The upcoming part requires a Github account. If you do not have one you
   can either

   - Create on now -- it is fast, free, and you can get rid of it afterwards,
     if you want to.
   - Or exchange the command ``create-sibling-github`` with
     ``create-sibling-gitlab`` if you have a Gitlab account instead of a Github
     account.
   - Don't listen to me and not follow along. I'm only a book, not your mom.

For this, you need to

- create a repository for this dataset on Github,
- configure this Github repository to be a :term:`sibling` of the ``midterm_project`` dataset,
- and *publish* your dataset to Github.

Luckily, DataLad can make all of this very easy with the
:command:`datalad create-sibling-github` command (or, for
`Gitlab <https://about.gitlab.com/>`_, :command:`datalad create-sibling-gitlab`).

.. index:: ! datalad command; create-sibling-github
.. index:: ! datalad command; create-sibling-gitlab

The command takes a repository name and Github authentication credentials
(either in the command line call with options ``github-login <NAME>`` and
``github-passwd <PASSWORD>``, with an *oauth* token stored in the Git
configuration [#f5]_, or interactively). Based on the credentials and the
repository name, it will create a new, empty repository on Github, and
configure this repository as a sibling of the dataset. If the ``-r/--recursive``
option is specified, siblings will be created *recursively*, i.e., not only a
repository for the ``midterm_project`` dataset will be created, but also one
for the ``iris_data`` dataset:

.. runrecord:: _examples/DL-101-130-116
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :realcommand: datalad --log-level critical siblings add -d . --name github --url https://github.com/adswa/midtermproject.git

   $ datalad create-sibling-github -d . -r midtermproject

Verify that this worked by listing the siblings of the dataset:

.. runrecord:: _examples/DL-101-130-117
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ datalad siblings

.. gitusernote::

   Creating a sibling on Github will create a new empty repository under the
   account that you provide and set up a *remote* to this repository. Upon a
   :command:`datalad publish` to this sibling, your datasets history
   will be pushed there.

On Github, you will see two new, empty repository with the names
``midtermproject``, and ``inputs``. However, none of these repositories yet contain
any of your dataset's history or files. This requires *publishing* the current
state of the dataset to this sibling. As before, we do this recursively with
``-r/--recursive``.

.. code-block:: bash

   $ datalad publish -r --to github
   [INFO] Publishing <Dataset path=/home/me/dl-101/DataLad-101/midterm_project> to github
   publish(ok): . (dataset) [pushed to github: ['[new branch]', '[new branch]']]

.. gitusernote::

   The :command:`datalad publish` uses ``git push``, and ``git annex copy`` under
   the hood. Publication targets need to either be configured remote Git repositories,
   or Git-annex special remotes (if they support data upload).

Yay! Consider your midterm project submitted! Others can now install your
dataset and check out your data science project -- and even better: they can
reproduce your data science project easily from scratch!

.. findoutmore:: On the looks and feels of this published dataset

   Now that you have created and published such a YODA-compliant dataset, you
   are understandably excited how this dataset must look and feel for others.
   Therefore, you decide to install this dataset in a new location on your
   computer, just to get a feel for it.

   Replace the ``url`` in the :command:`install` command below with the path
   to your own ``midtermproject`` Github repository:

   .. runrecord:: _examples/DL-101-130-118
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ cd ../../
      $ datalad install -r --source "https://github.com/adswa/midtermproject.git"

   Note that we performed a *recursive* installation by providing the ``-r``
   option. Thus, we don't need to install the ``input/`` subdataset anymore.
   Let's start with the subdataset, and see whether we can retrieve the
   input ``iris.csv`` file. This should not be a problem, since it's origin
   is recorded:


   .. runrecord:: _examples/DL-101-130-119
      :language: console
      :workdir: dl-101

      $ cd midtermproject
      $ datalad get input/iris.csv

   Nice, this worked well. The output files, however, can not be easily
   retrieved:

   .. runrecord:: _examples/DL-101-130-120
      :language: console
      :workdir: dl-101/midtermproject

      $ datalad get output/*

   Why is that? The file content of these files is managed by Git-annex, and
   thus only information about the file name and location is known to Git.
   Because Github does not host large data, annexed file content always
   needs to be deposited somewhere else (e.g., a webserver) to make it
   accessible via :command:`datalad get`. A later section

   .. todo::

      link 3rd party infra section

   will demonstrate how this can be done. For this dataset, it is not
   necessary to make the outputs available, though: Because all provenance
   on their creation was captured, we can simply recompute them with the
   :command:`datalad rerun` command.

   .. runrecord:: _examples/DL-101-130-121
      :language: console
      :workdir: dl-101/midtermproject
      :realcommand: echo "datalad rerun $(git rev-parse HEAD~2)" && datalad rerun $(git rev-parse HEAD~2)

   Hooray, your analysis was reproduced! Note however that none of the DataLad
   commands would have been necessary to reproduce the analysis -- simply
   executing the Python script would have installed and retrieved the inputs thanks
   to the DataLad functions used in the script, as long as DataLad is installed
   on the system.

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
            pip install seaborn, pandas, sklearn

.. [#f4] Note that all ``README.md`` files the YODA procedure created are
         version controlled by Git, not Git-annex, thanks to the
         configurations that YODA supplied. This makes it easy to change the
         ``README.md`` file. If you want to re-read the chapter on configurations
         and run-procedures, start with section :ref:`config`.

.. [#f5] Such a token can be obtained, for example, using the commandline
         Github interface (https://github.com/sociomantic/git-hub) by running:
         ``git hub setup`` (if no 2FA is used).