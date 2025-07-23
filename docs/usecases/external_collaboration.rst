.. _usecase_external_collaboration:

Collaborations on sensitive data with remote analyses
-----------------------------------------------------

This usecase is based on a common problem:
An external collaborator would like to perform an analysis on a dataset that can't be shared outside of its host lab.
With DataLad, the collaboration can succeed:

#. A mock dataset with the same structure (organization, file names, potentially mock-content) but without (access to) the actual sensitive data is shared or made publicly available instead of the original dataset.
#. This mock dataset can assist others to develop their code, without disclosing personal information.
#. External collaborators create a new dataset for their analysis code, with the mock dataset as a subdataset.
#. The collaborator submits their dataset back to the lab that has all of the data. After code review, the code is executed on the actual data, its results are captured in the submitted dataset, and only results are pushed back to the external collaborators.

The Challenge
^^^^^^^^^^^^^

The ABC-Lab collected data from patients for one of their studies.
After publication, a Post-doc from the XYZ-Lab reaches out and proposes an interesting analysis of the same data on a new research question.
Everyone involved is excited about this collaboration:
The XYZ-Lab is happy that such a valuable dataset exists and is eager to give credit and co-authorship to collaborators in the ABC-Lab.
The ABC-Lab is happy that someone else is interested in using their data and appreciates the possibility of another publication with lab-members as co-authors.

However, the legal department in ABC's institute steps in: The data can not be shared with anyone outside the ABC-Lab as this would be a privacy violation.
The data contain potentially identifying or personal information of the patients they were collected from.

With such legal problems, the promising collaboration ceases before it even started, the data remain unused, and an interesting research question remains unanswered.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Scientists take their participants' privacy very seriously, and everyone is well aware that certain data can not leave the host institute's computational premises.
Nevertheless, valuable data can be made accessible without providing direct access.
To enable data analysis by others without disclosing private information researchers can make use of DataLad.

In order to *develop* analysis scripts that can analyze the data, the actual sensitive data is not needed.
A mock dataset that has the same structural layout and the same file names as the original dataset can already be sufficient information to create a working script.
Therefore, the ABC-Lab shares a mock dataset with its collaborators that does not contain sensitive information.
In the simplest case, this can be achieved by not making the annexed data available and thus providing only file names and availability information without content.
If certain properties of the data are relevant to develop analyses (for example because they don't follow a common standard or can't be anticipated otherwise for the external collaborators [#f1]_), simulated data with relevant properties can replace the actual file content.

Collaborators can install this dataset as a subdataset in their own analysis datasets, and develop their code against the layout and potentially mock-content.
This ensures that the script is adjusted to the actual file names and works "out-of-the-box".

Afterwards, the dataset with the analysis script is given back to the ABC-Lab.
The ABC-Lab can then review the provided code and exchange the mock dataset with the original, sensitive data.
With this, they can run the code provided by the collaborator such that sensitive data stays within their institute.
All results computed from this analysis are aggregated into the external collaborator's dataset.
Upon completion, only the results, not the sensitive input data, are pushed back.


.. find-out-more:: Advice for the provider of sensitive data

   When providing *data* in a remote analysis, the data provider should make an effort for external collaborators' computations to succeed in their own interest: In an ideal, smooth case, the data provider only reviews and runs the code, and doesn't need to spent time debugging.
   For this, the following pieces of advice can help:

   * If you can, make use of applicable organizational standards in your field. The more predictable your data layout, the easier it is to develop code against it.
   * Document relevant information about the data. This could be variable names and data ranges in tabular files, values used to denote missing data or other special cases, etc. Use your own analysis scripts for insights: Is there anything you adjust for? Maybe you can even share your own scripts for guidance.
   * A middle ground between keeping all data inaccessible and creating simulated data is to keep all real data inaccessible but add a "dummy" data point (e.g., a phantom scan or other example data) that is always publicly accessible.
   * Document relevant information about the compute environment. What would the external collaborator need to pay attention to? Is there specific architecture the code needs to be compatible with (e.g., GPUs?). Is there a specific container solution (e.g., Docker, Singularity) you can or wish to receive?


.. find-out-more:: Advice for the external collaborator

   When providing *code* in a remote analysis, the external collaborator should make the execution as easy as possible for the data provider.
   For this, the following pieces of advice can help:

   * Write clean and well-documented code to make a pre-execution review simple.
   * Write your code as generic as you can: If the data follows data organization standards, make use of existing tools that understand the standard (e.g., for data ingestion).
   * Provide detailed information about the required software, or, even better, provide a :term:`software container` that contains it. See the chapter :ref:`chapter_containersrun` on why and how.
   * Make your code portable: Use relative paths instead of absolute paths, define all necessary environment variables in your code, and test your code and software on a different computer to rule out that anything on your particular system is required for the code execution to succeed.
   * If your analysis shall run on specific data, either write your code to automatically "do the right thing", or provide detailed instructions on how the computation shall be done.

Toy Example
^^^^^^^^^^^

Let's play this through from start to end with a toy example.
You can decide whether you would like to take the collaborators' perspective, or the data providers' perspective - or both.

The dataset we will be working with is `The Palmer Penguins <https://hub.datalad.org/edu/penguins>`_ dataset, which contains data from several penguin species.
It is not sensitive data, but for the sake of the example, let us pretend it is.

Central to the dataset are ``.csv`` files, i.e., tabular data.
As a collaborator, you will want to script an analysis that makes use of this tabular data.
As a data provider, you will want to keep the true file contents of the tables private, but nevertheless provide enough information about them for collaborators to write successfully executable scripts.

1. Perspective: Prepare a dataset as a data provider
""""""""""""""""""""""""""""""""""""""""""""""""""""

You are a penguin expert and have devoted your life to study them.
After spending many months alone with no company but penguins, you have returned home and written a paper on your findings.
As you are sure that characteristics of various penguin species can be useful to other scientists as well, you decide to publish your dataset without infringing your wobbly participants' privacy.

A possible first step could be the initial creation of a DataLad dataset.
To be able to keep all or selected file contents private, data providers should make sure that

* any sensitive files are annexed [#f2]_;
* and file names do not contain sensitive information, regardless if they are annexed or in :term:`Git`.

If your data are already in a DataLad dataset, make sure the dataset adheres to the above points, too.
If it does not, for example because some sensitive content *is* (or *was*!) kept in Git, your revision history can leak information that should stay private.
In those cases, it's better to recreate the dataset from scratch for the purpose of publishing it in a "safe" version [#f3]_.

**Publishing an empty dataset**

If you want to publish a dataset by simply not making annexed file contents available, the next step is already about finding a suitable place for the dataset and pushing to it.
There are several easy ways to make a dataset but not its file contents available to external collaborators:

* Choose a hosting service that cannot host annexed data to begin with (e.g., :term:`GitHub` or :term:`GitLab`).
* If you are using annex-aware services like :term:`forgejo-aneksajo` or :term:`Gin`, make sure that annexed file contents are not pushed there. This could be done "manually" using the ``--data nothing`` option of :dlcmd:`push`, or with an ``annex wanted`` configuration [#f4]_.


.. importantnote:: Beware of autoenabled special remotes!

   DataLad Datasets are made for decentralization.
   As such, the availability information of their files can span an arbitrarily large network.
   Be mindful that the dataset you are sharing does not "accidentally" make file contents available with an autoenabled special remote that is accessible (to some).
   Before publishing a "public" dataset, consider running ``git annex dead [remote-name]`` for any special remotes that you want to hide.

Let's take a look at how this could look in practice.
We will first clone the dataset and get the relevant files:

.. runrecord:: _examples/remote-analysis-111
   :language: console
   :workdir: usecases/remote-analysis

   $ datalad clone https://hub.datalad.org/edu/penguins palmer-penguins
   $ cd palmer-penguins
   $ datalad get */*table*.csv

Let's take a look at where data could be coming from:

.. runrecord:: _examples/remote-analysis-112
   :language: console
   :workdir: usecases/remote-analysis/palmer-penguins

   $ git annex whereis adelie/table_219.csv

There are 4 copies of the table:
Your local copy, the :term:`forgejo-aneksajo` instance it was just cloned from, the "archivist" special remote and "jsheunis"' macbook.
As the square brackets indicate, both the archivist special remote as well as the forgejo-aneksajo instance are autoenabled and would provide data even if we were to publish the dataset without pushing file contents.
Thus, we can declare those locations "dead" to make the file contents they host inaccessible to the dataset:

.. runrecord:: _examples/remote-analysis-113
   :language: console
   :workdir: usecases/remote-analysis/palmer-penguins

   $ git annex dead archivist
   $ git annex dead origin

In real life, you will also want to document the unavailable data more.
You could add descriptions of file properties, variable names, or other important features to a README file.
Make sure that the file you are documenting this is is kept in *Git* so that it can be read by your new collaborators.

.. runrecord:: _examples/remote-analysis-114
   :language: console
   :workdir: usecases/remote-analysis/palmer-penguins

   $ wget -q https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/README.md -O README.md
   $ datalad save -m "Add better description of dataset contents"

Afterwards, we can publish the dataset without file contents::

   $ git remote add public-empty https://hub.datalad.org/edu/penguins-empty.git
   $ datalad push --to public-empty --data nothing

.. find-out-more:: Check if everything works as expected

   It is a good idea to test if your dataset keeps everything private as expected.
   Let's clone the dataset and confirm that dataset contents can not be retrieved:

   .. runrecord:: _examples/remote-analysis-115
      :language: console
      :workdir: usecases/remote-analysis/palmer-penguins
      :exitcode: 1

      $ cd ..
      $ datalad clone https://hub.datalad.org/edu/penguins-empty.git
      $ cd penguins-empty
      $ datalad get .

**Publishing a mock dataset**

If you want to generate artificial data in place of sensitive content, you need to do that prior to publishing your dataset.

How to do this will depend on your data, and not always will this be easy.
While it may be easy to generate good-enough artificial tabular data [#f5]_, it can be near impossible for more complex, multidimensional data.
In the latter cases, it may be easier to add example files that follow the naming scheme of the dataset but are fine to share openly (e.g., public data, phantom/test data, ...).

In our example, we can create artificial mock data in place of the tables.
This way, a data provider would not need to extensively document variable names or coding schemes.
A `short script <https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/mock-data.py>`_ will do the job, which we record reproducibly and transparently with :dlcmd:`run`::

   $ wget -q https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/mock-data.py -O code/mock-data.py
   $ datalad save -m "add script to create mock data"
   # running the script requires numpy and pandas
   $ datalad run -m "create artificial data" -o '*/*table*.csv' 'python code/mock-data.py'
   [INFO] == Command start (output follows) =====
   [INFO] == Command exit (modification check follows) =====
   unlock(ok): adelie/table_219.csv (file)
   unlock(ok): chinstrap/table_221.csv (file)
   unlock(ok): gentoo/table_220.csv (file)
   run(ok): /home/me/usecases/remote-analysis/palmer-penguins (dataset) [python code/mock-data.py]
   add(ok): adelie/table_219.csv (file) [Copied metadata from old version of adelie/table_219.csv to new version. If you don't want this copied metadata, run: git annex metadata --remove-all adelie/table_219.csv]
   add(ok): chinstrap/table_221.csv (file) [Copied metadata from old version of chinstrap/table_221.csv to new version. If you don't want this copied metadata, run: git annex metadata --remove-all chinstrap/table_221.csv]
   add(ok): gentoo/table_220.csv (file) [Copied metadata from old version of gentoo/table_220.csv to new version. If you don't want this copied metadata, run: git annex metadata --remove-all gentoo/table_220.csv]
   save(ok): . (dataset)

The three tables now have gotten their "sensitive" content replaced with random data.
We can publish this dataset with the artificial contents of these three files, using :dlcmd:`push` with a simple path specification [#f6]_::

   $ git remote add public-mock https://hub.datalad.org/edu/penguins-mock.git
   $ datalad push --to public-mock */*table*.csv

Note that this does *not* publish the previous, sensitive version of file contents, but only the most recent version with mock data.
And as the recorded special remotes were declared "dead", past versions of the content can't be retrieved.

2. Perspective: Prepare a remote analysis as a collaborator
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

You are an expert on jellyfish, and currently on a scientific exploration in the Ocean.
The population of jellyfish you study hangs out with a group of penguins - a sensational finding.
Sadly, you have no idea at all about penguins, and do not even know their species.
Rather than giving up, you measure a few of their characteristics and hope that you can determine the species with the help of the external "penguin" dataset:
You plan to

- train a model to predict species based on body features - using the external dataset;
- and then use the model to predict the species in your own samples.

Start by creating a DataLad dataset for your analysis (e.g., using the YODA configuration (see also :ref:`chapter_yoda`)):

.. runrecord:: _examples/remote-analysis-101
   :language: console
   :workdir: usecases/remote-analysis

   $ datalad create -c yoda penguin-jelly

Save your own measurements into it:

.. runrecord:: _examples/remote-analysis-102
   :language: console
   :workdir: usecases/remote-analysis

   $ cd penguin-jelly
   $ mkdir data
   $ wget -q https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/local-samples.csv -O data/local-samples.csv
   $ datalad save -m "add own measurements"

Next, clone the access-restricted dataset as a subdataset of your analysis.
To explore how different variations of remote analyses feel, you can either:

- clone the empty dataset, which provides file names, but where file contents can't be retrieved: https://hub.datalad.org/edu/penguins-empty.git
- or clone the dataset with simulated file contents: https://hub.datalad.org/edu/penguins-mock.git.

.. runrecord:: _examples/remote-analysis-103
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad clone -d . https://hub.datalad.org/edu/penguins-mock.git inputs

Afterwards, it is time to "develop" your analysis.
In this toy example, you can download a demo analysis, but its also a good exercise to take a look at the available information in the shared dataset and write a script to compute something simple from it - like for example an arithmetic mean.


.. runrecord:: _examples/remote-analysis-104
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ wget -q https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/predict.py -O code/predict.py
   $ datalad save -m "Write a remote analysis script"

.. find-out-more:: What does the script do?

   The first part is an import of necessary libraries and functions, as is custom in Python:

   .. code-block::

      import argparse
      import pandas as pd
      import seaborn as sns

      from glob import glob
      from pathlib import Path

      from sklearn.model_selection import cross_validate
      from sklearn.linear_model import LogisticRegression
      from sklearn.pipeline import make_pipeline
      from sklearn.preprocessing import StandardScaler

   Next, a simple command line interface is defined, so that three arguments can be given to the script: ``--input``, ``--measurements``, and ``--output``.

   .. code-block::

      # simple command line interface
      parser = argparse.ArgumentParser(
               description='''
                   This script fits a regression model on external input
                   data from penguin beak measurements and uses the model
                   to predict Species membership of own measurements. ''')
      parser.add_argument('-i', '--input',
               type=str,
               default='inputs/',
               help='''
                   Path to an input dataset with penguin data. The dataset
                   should contain csv tables with the columns "Culmen Length
                    (mm)" and "Culmen Depth (mm)".''')
      parser.add_argument('-m', '--measurements',
               default='data/local-samples.csv',
               help='''
                   Path to a csv file with own beak measurements. Should
                   contain columns "Culmen Length (mm)" and "Culmen Depth (mm)".''')
      parser.add_argument('-o', '--output',
               default='predictions.csv',
               help='''
                   Path where results shall be saved as a csv file.''')
      args = parser.parse_args()
      # extract commandline arguments:
      measurements = Path(args.measurements)
      inputs = Path(args.input)

   Thanks to this, running the script with ``--help`` prints the following::

		$ python code/predict.py --help
		usage: predict.py [-h] [-i INPUT] [-m MEASUREMENTS] [-o OUTPUT]

		This script fits a regression model on external input data from penguin beak
		measurements and uses the model to predict Species membership of own
		measurements.

		options:
		  -h, --help            show this help message and exit
		  -i, --input INPUT     Path to an input dataset with penguin data. The
					dataset should contain csv tables with the columns
					"Culmen Length (mm)" and "Culmen Depth (mm)".
		  -m, --measurements MEASUREMENTS
						Path to a csv file with own beak measurements. Should
						contain columns "Culmen Length (mm)" and "Culmen Depth
						(mm) ".
		  -o, --output OUTPUT   Path where results shall be saved as a csv file.

   The actual data wrangling starts here.
   The script finds all files that match ``*/*table*.csv`` within the input dataset and reads them into a single data frame.
   It also reads in the "local samples".

   .. code-block::

      # find all tables
      files = sorted(inputs.glob('*/*table*.csv'))

      # combine the data into a single DataFrame
      dfs = []
      for file in files:
          df = pd.read_csv(file)
          dfs.append(df)

      combined_data = pd.concat(dfs, ignore_index=True)

      # read local samples
      local_samples = pd.read_csv(measurements,
								usecols=['Culmen Length (mm)', 'Culmen Depth (mm)'])

   Next, it builds the model using variable names from the spreadsheet:
   "Culmen Length (mm)" and "Culmen Depth (mm)" are used as features to predict the "Species".
   The model performance is evaluated in a cross-validation, and the script prints the average accuracy.

   .. code-block::

      # define features and targets, build a smaller dataset
      penguins = combined_data[["Culmen Length (mm)", "Culmen Depth (mm)", "Species"]]
      penguins = penguins.dropna()
      data, target = penguins.drop(columns="Species"), penguins["Species"]


      # build a pipeline with a Logistic Regression
      model = make_pipeline(StandardScaler(), LogisticRegression())
      # evaluate the model using cross-validation
      cv_result = cross_validate(model, data, target, cv=3)
      print(f'average model accuracy is {cv_result["test_score"].mean():.3f}')

   Finally, the trained model is used to predict the penguin species of your own samples, and writes it to a file.

   .. code-block::

      # fit the model on data; predict Species of own data points
      model.fit(data, target)
      res = model.predict(local_samples)
      local_samples['prediction'] = res
      # save the prediction
      local_samples.to_csv(args.output)


To make things easier for the data provider, you can add a software container that includes all required software, using the ``datalad-containers`` extension.

.. runrecord:: _examples/remote-analysis-105
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad containers-add software --url shub://adswa/resources:2

Let's run the script on mock data in the software container.
The results will not be correct because the data is only simulated, but it generates a run record that the data provider can very easily rerun - sparing you the need for detailed instructions in an email or a README file.
Keep in mind to properly define inputs and outputs, so that the analysis can easily be rerun.

.. runrecord:: _examples/remote-analysis-106
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad containers-run -n software -m "run analysis on mock data" -i 'inputs/*/*table*.csv' -o "predictions.csv" "python3 code/predict.py"

Note how bad the model performs - this accuracy will likely improve on the real data.
We can tag the dataset state to make rerunning easier:

.. runrecord:: _examples/remote-analysis-107
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ git tag runme

At this point, you will want to share your analysis dataset with the data provider.
You could, for example, publish it and share a URL that can be cloned.

3. Perspective: Execute the remote analysis
"""""""""""""""""""""""""""""""""""""""""""

The question is: How does this look on the real data?
A data provider would clone the external collaborator's dataset and replace the subdataset with the actual sensitive dataset.

We can pretend to do this:

.. runrecord:: _examples/remote-analysis-108
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad drop --what datasets inputs
   $ datalad clone -d . https://hub.datalad.org/edu/penguins.git inputs


Then, the data provider would rerun the analysis:

.. runrecord:: _examples/remote-analysis-109
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad rerun runme

Note how much better the model performs on the real data, and how the contents in ``predictions.csv`` change.
The data provider would then share the resulting outputs back to the external collaborator - and not the sensitive input data.
Thus, the analysis was conducted verifiably on specified sensitive input data in a transparently recorded version, but without sharing the sensitive file contents.


.. rubric:: Footnotes

.. [#f1] When would it be useful to have simulated data? For example for variable names or data ranges in tabular data. This way, external collaborators know that their scripts need to extract the columns "``age``", "``cortisol_morning``" and "``cortisol_evening``", and that a value of "``-2``" denotes missing data that should be filtered out.

.. [#f2] The section :ref:`config2` contains information on the possible configuration mechanisms to achieve this.

.. [#f3] You could also very aggressively clean the Git history (see e.g., :ref:`cleanup` for a few glimpses into that). But this is a technically complex task in which you can very easily lose data or provenance you did not intend to lose.

.. [#f4] For example, you can configure a "public" dataset sibling (in the code below identified with the sibling name ``public-org``) to "not want" any annexed files::

   $ git annex wanted public-org "exclude=*"

   Such a configuration would be honored automatically when you use :dlcmd:`push`. Find out more at `git-annex.branchable.com/git-annex-wanted <https://git-annex.branchable.com/git-annex-wanted/>`_.


.. [#f5] The script that was used for mock penguin data is in `hub.datalad.org/edu/penguins-mock/src/branch/main/code/mock-data.py <https://hub.datalad.org/edu/penguins-mock/src/branch/main/code/mock-data.py>`_

.. [#f6] Hint: If you ever accidentally pushed more than you wanted to push, you can ``git annex drop -f <sibling-name>``.