.. _usecase_external_collaboration:

Collaborations on sensitive data with remote analyses
-----------------------------------------------------

This usecase is based on a common problem:
An external collaborator would like to perform an analysis on a dataset that contains personal information of participants and thus can't be shared outside of the lab.
With DataLad, the collaboration can succeed:

#. A mock dataset with the same structure (organization, file names, potentially mock-content) but without (access to) the actual problematic data is shared or made publicly available instead of the original dataset.
#. This mock dataset can assist others to develop their code, without disclosing personal information.
#. External collaborators create a new dataset for their analysis code, with the mock dataset as a subdataset.
#. The collaborator submits their dataset back to the lab that has all of the data. After code review, the code is executed on the actual data, its results are captured in the submitted dataset, and only results are pushed back to the external collaborators.

The Challenge
^^^^^^^^^^^^^

The ABC-Lab collected data from patients for one of their studies.
After publication, a Post-doc from the XYZ-Lab reaches out and proposes and interesting analysis of the same data on a new research question.
Everyone involved is excited about this collaboration:
The XYZ-Lab is happy that such a valuable dataset exists and is eager to give credit and co-authorship to collaborators in the ABC-Lab.
The ABC-Lab is happy that someone else is interested in using their data and appreciates the possibility of another publication with lab-members as co-authors.

However, the legal department in ABC's institutes steps in: The data can not be shared with anyone outside as this would be a privacy violation.
The data contains potentially identifying or personal information of the patients it was collected from.

With such legal problems, the promising collaboration ceases before it even started, the data remains disclosed but also unused, and an interesting research question remains unanswered.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Scientists take their participant's privacy very seriously, and everyone is well aware that certain data can not leave the institute's computational premises.
Nevertheless, valuable data should not remain accessible to only selected few.
To enable data analysis by others without disclosing private information researchers can make use of DataLad.

In order to *develop* analysis scripts that can analyze the data, the actual sensitive data is not needed.
A mock dataset that has the same structural layout and the same file names as the original dataset can already be sufficient information to create a working script.
Therefore, the ABC-lab shares a mock dataset with its collaborators that does not contain sensitive information.
In the simplest case, this can be achieved by not making the annexed data available and thus providing only file names and availability information without content.
If certain properties of the data are relevant to develop analyses (for example because they don't follow a common standard or can't be anticipated otherwise for the external collaborators [#f1]_), simulated data with relevant properties can replace the actual file content.

Collaborators can install this dataset as a subdataset in their own analysis datasets, and develop their code against the layout and potentially mock-content.
This ensures that the script is adjusted to the actual file names and works "out-of-the-box".

Afterwards, this dataset is given back to the ABC-lab.
They can review the provided code and exchange the mock dataset with the original, sensitive data.
With this, they can run the code provided by the collaborator such that sensitive data stays within their institute.
All results computed from this are aggregated into their collaborator's dataset.
Upon completion, only the results, not the sensitive input data, are pushed back.


.. find-out-more:: Advice for the holder of sensitive data

   When providing data in a remote analysis, the data holder should make an effort for external collaborators' computations to succeed in their own interest: In an ideal, smooth case, the data holder only reviews and runs the code, and doesn't need to spent time debugging.
   For this, the following pieces of advice can help:

   * If you can, make use of applicable organizational standards in your field. The more predictable your data layout, the easier it is to develop code against it.
   * Document relevant information about the data. This could be variable names and data ranges in tabular files, values used to denote missing data or other special cases, etc. Use your own analyses scripts for insights: Is there anything you adjust for? Maybe you can even share own scripts for guidance.
   * Document relevant information about the compute environment. What would the external collaborator need to pay attention to? Is there specific architecture the code needs to be compatible with (e.g., GPUs?).


.. find-out-more:: Advice for the external collaborator

   When providing code in a remote analysis, the external collaborator should make the execution as easy as possible for the data holder.
   For this, the following pieces of advice can help:

   * Write clean and well-documented code to make a pre-execution review simple.
   * Write your code as generic as you can: If the data follows data organization standards, make use of existing tools that understand the standard (e.g., for data ingestion).
   * Provide detailed information about the required software, or, even better, provide a :term:`software container` that contains it. See the chapter :ref:`chapter_containersrun` on why and how.
   * Make your code portable: Use relative paths instead of absolute paths, define all necessary environment variables in your code, and test your code and software on a different computer to rule out that anything on your particular system is required for the code execution to succeed.

Toy Example
^^^^^^^^^^^

Let's play this through from start to end with a toy example.
You can decide whether you would like to take the collaborators' perspective, or the data holders' perspective - or both.

The dataset we will be working with is `The Palmer Penguins <https://hub.datalad.org/edu/penguins>`_ dataset, which contains data from several penguin species.
It is not sensitive data, but for the sake of the example, let us pretend it is.

Central to the dataset are ``.csv`` files, i.e., tabular data.
As a collaborator, you will want to script an analysis that makes use of this tabular data.
As a data provider, you will want to keep the true file contents of the tables private, but nevertheless provide enough information about them for collaborators to write successfully executable scripts.

The collaborators perspective
"""""""""""""""""""""""""""""

You are an expert on jelly fish, and currently on a scientific exploration in the Ocean.
The population of jelly fish you study hangs out with a group of penguins - a sensational finding.
Sadly, you have no idea at all about penguins, and do not even know their species.
Rather than giving up, you measure a few of their characteristics and hope that you can determine the species with the help of the external "penguin" dataset:
You plan to

- train a model to predict species based on body features - using the external dataset;
- and then use the model to predict the species in your own samples

Start by creating a DataLad Dataset for your analysis (e.g., using the YODA configuration):

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

- clone an empty dataset, which provides file names, but where file contents can't be retrieved: https://hub.datalad.org/edu/penguins-empty.git
- or clone a dataset with simulated file contents: https://hub.datalad.org/edu/penguins-mock.git

.. runrecord:: _examples/remote-analysis-103
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad clone -d . https://hub.datalad.org/edu/penguins-mock.git inputs

Afterwards, it is time to "develop" your analysis.
In this toy example, you can download it, but its also a good exercise to take a look at the available information in the shared dataset and write a script to compute something simple from it - like for example a mean.


.. runrecord:: _examples/remote-analysis-104
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ wget https://hub.datalad.org/edu/scripts/raw/branch/main/remote-analysis/predict.py -O code/predict.py
   $ datalad save -m "Write a remote analysis script"

.. find-out-more:: What does the script do?

   TODO

To make things easier for the data provider, you can add a software container that includes all required software, using the ``datalad-containers`` extension.

.. runrecord:: _examples/remote-analysis-105
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad containers-add software --url shub://adswa/resources:2

Let's run the script on mock data in the software container.
Keep in mind to properly define inputs and outputs, so that the analysis can easily be rerun.

.. runrecord:: _examples/remote-analysis-106
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad containers-run -n software -m "run analysis on mock data" -i 'inputs/*/*table*.csv' -o "predictions.csv" "python3 code/predict.py"

We can tag the dataset state to make rerunning easier:

.. runrecord:: _examples/remote-analysis-107
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ git tag runme

The question is: How does this look like on the real data?
A data provider would clone your dataset and replace the subdataset with the actual sensitive dataset.

We can pretend to do this:

.. runrecord:: _examples/remote-analysis-108
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad drop --what datasets inputs
   $ datalad clone -d . https://hub.datalad.org/edu/penguins.git inputs


Then, we rerun the analysis:

.. runrecord:: _examples/remote-analysis-109
   :language: console
   :workdir: usecases/remote-analysis/penguin-jelly

   $ datalad rerun runme




The data providers perspective
""""""""""""""""""""""""""""""



Step-by-Step
^^^^^^^^^^^^

Creating a dataset
""""""""""""""""""

The first step is likely the initial creation of a DataLad dataset.
To be able to keep all or selected file contents private, data providers should make sure that

* any sensitive files are annexed
* file names do not contain sensitive information, regardless if there annexed or in :term:`Git`

The section :ref:`config2` contains information on the possible configuration mechanisms to achieve this.


Configuring public siblings
"""""""""""""""""""""""""""

External collaborators need to be able to access a dataset to script their analyses against.
This "public" dataset must not contain any sensitive file content.
This can be achieved in several ways.
One is to publish the dataset to a place that doesn't support hosting annexed files such as :term:`GitHub` or :term:`GitLab`.
If you are using annex-aware services like :term:`forgejo-aneksajo` or :term:`Gin`, make sure that annexed file contents are not pushed there.
This could be done "manually" using the ``--data nothing`` option of :dlcmd:`push`, or with an ``annex wanted`` configuration.
For example, you can configure your "public" dataset to "not want" any annexed files::

   $ git annex wanted public-org "exclude=*"

Such a configuration would be honored automatically when you use :dlcmd:`push`.

.. importantnote:: Beware of autoenabled special remotes!

   DataLad Datasets are made for decentralization.
   As such, the availability information of their files can span an arbitrarily large network.
   Be mindful that the dataset you are sharing does not "accidentally" make file contents available with an autoenabled special remote that is accessible (to some).
   Before publishing a "public" dataset, consider running ``git annex dead [remote-name]`` for any special remotes that you want to hide.



.. rubric:: Footnotes

.. [#f1] When would it be useful to have simulated data? For example for variable names or data ranges in tabular data. This way, external collaborators know that their scripts need to extract the columns "``age``", "``cortisol_morning``" and "``cortisol_evening``", and that a value of "``-2``" denotes missing data that should be filtered out.
