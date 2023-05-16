OHBM Brainhack TrainTrack: DataLad
----------------------------------

This code belongs to the 2020 OHBM Brainhack Traintrack session on DataLad. Copy-paste
them into your terminal to follow along.

Introduction & set-up
^^^^^^^^^^^^^^^^^^^^^

DataLad is a command line tool and it has a Python API. Whenever I use it,
I thus operate it in a terminal using the command line, or I use it in scripts
such as shell scripts, Python scripts, Jupyter Notebooks, and so forth.
In the command line, this always starts with the general ``datalad`` command::

   datalad

For example, I can type ``datalad --help`` to find out more about
the available commands.

To use its python interface, I import the ``datalad.api as dl``::

   ipython
   import datalad.api as dl
   exit

You can find more details about how to install DataLad and its dependencies on
all operating systems in the DataLad handbook, in the section :ref:`install`.
It also details how to install DataLad on shared machines that
you don't have administrative privileges (sudo rights) on, such as high
performance compute clusters.
If you already have datalad installed,
**make sure that it is a recent version, at least 0.12 or higher**::

   datalad --version


The very first thing to do if you haven't done so yet is to configure your Git
identity. Don't worry if you have never used Git. The identity you are
configuring consists of your name and email-adress so that the changes that you
do to a project can be associated with you as an author of the changes::

   git config --global --add user.name "Adina Wagner"
   git config --global --add user.email "adina.wagner@t-online.de"

Creating a dataset is done with the ``datalad create`` command. This command only needs a name, and
it will subsequently create a new directory under this name and instruct DataLad
to manage it. Here, the command also has an additional option, the -c text2git
option. With the -c option, datasets can be configured in a certain way at the
time of creation. You can find out about the details of the text2git configuration
in the datalad handbook in sections :ref:`procedures`, but in general this configuration is a very useful
standard configuration for datasets::

   datalad create -c text2git DataLad-101

Right after dataset creation, there is a new directory on the computer called
``DataLad-101``::

   cd DataLad-101
   ls # ls does not show any output, because the dataset is empty

Datasets have the exciting features that they can record
everything that is done inside of them, version control all content given to
Datalad, regardless of the size of this content, and have a complete history that
you can interact with. This history is already present, although it is very
short at this point in time. Let's check it out nevertheless.

This history exists thanks to Git. Therefore, you can access the history of a
dataset with any tool that shows you git
history. We'll stay basic and just use gits built-in ``git log`` command, but you
could also use tools with graphical user interfaces if you want to, for example
:term:`tig`::

   git log

Version control workflows
^^^^^^^^^^^^^^^^^^^^^^^^^

I'll start by creating a books directory with the mkdir command, and then I will download two books
from the internet. Here, I'm using the command line tool wget to do this in
order to do everything from the commandline. But you can also just download the
book manually and save it into the dataset with a file manager if you are more
comfortable doing it this way. Remember, a dataset is just a directory on your
computer::

   mkdir books
   cd books && wget -nv https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf && wget -nv https://edisciplinas.usp.br/pluginfile.php/3252353/mod_resource/content/1/b_Swaroop_Byte_of_python.pdf -O byte-of-python.pdf && cd ../

The tree command can visualize the directory hierarchy::

   tree

Use the datalad status command to find out what happened in the dataset. This
command is very helpful and reports on the current state of your dataset. Any
content that is new or changed will be highlighted. If nothing has changed, a
datalad status will report what is called a clean dataset state. And in general
it is very useful to always have a clean dataset state::

   datalad status

Any content that
we want DataLad to manage needs to be explicitly given to DataLad, it is not
enough to simply put it inside of the dataset. To give new or changed content to
DataLad, we need to save it using datalad save. This is the first time that we
need to specify a commit message, and this is done with the -m option of the
command::

   datalad save -m "add books on Python and Unix to read later"

With git log -n 1 you can take a look at the most recent commit in the history::

   git log -p -n 1

"datalad save" saved all untracked contents to the
dataset. Sometimes this is inconvenient. One great advantage of a datasets
history is that it allows you to revert changes you are not happy with, but this
is only easily possible in the units of single commits. So if one save commits
several unrelated files or changes, they are hard to disentangle if you ever
want to revert some of those changes. But if you for example provide a path to
the file you want to save you can specify more precisely what will be saved
together::

   cd books && wget -nv https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf && cd ../
   datalad status

Attach a path to the next ``datalad save`` command::

   datalad save -m "add reference book about git" books/progit.pdf

Let's take a look at files that are
frequently modified such as code or text. To try this, I will create a file
and modify it. I do this with a `here doc <https://en.wikipedia.org/wiki/Here_document>`_,
but you can also write the note with an editor of your choice. If you execute this
code snippet, make sure you copy-paste everything, starting with ``cat`` and ending
with the second ``EOT``::

   cat << EOT > notes.txt
   One can create a new dataset with '"'"'datalad create PATH'"'"'.
   The dataset is created empty


   EOT

Datalad status will, as expected, say that there is a new untracked file in the
dataset::

   datalad status

We can save it with datalad save command and a helpful commit message. As
its the only change in the dataset, there is no need to provide a path::

   datalad save -m "Add notes on datalad create"

Let's now add another note to modify this file::

   cat << EOT >> notes.txt
   The command "datalad save [-m] PATH" saves the file
   (modifications) to history. Note to self:
   Always use informative, concise commit messages.

   EOT

A datalad status reports the file not to be untracked, but because it
differs now from the state it was saved under it is reported to be modified::

   datalad status

Let's save this::

   datalad save -m "add note on datalad save"

If you take a look at the history of this file with git log, the history
neatly summarizes all of the changes that have been done::

   git log -p -n 2


Dataset consumption and nesting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, create a new subdirectory to be organized::

   mkdir recordings

Afterwards, I'll install the dataset I am interested in, either from a path or
a URL. The dataset I want to install lives on GitHub, so in order to get it, I
will provide its URL to the datalad clone command. I'm also attaching a path to
where I want to have it installed to this call. Importantly I am installing this
dataset as a subdataset of DataLad-101, in other words I will nest the two
datasets inside of each other. This is done with the --dataset flag::


   datalad clone --dataset . \
   https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow

There are new directories in my DataLad/101 dataset, and in these new directories, there are
hundreds of mp3 files::

   tree -d # we limit the output to directories
   cd recordings/longnow/Long_Now__Seminars_About_Long_term_Thinking
   ls

here is the crucial and incredibly
handy feature of DataLad datasets: At this point, after cloning, the dataset
has small files, for example the README, but larger files in it don't have any
file content yet. It only retrieved what we in a simplified way call file
availability metadata and shows that as the file hierarchy in the dataset. So
while I can read the file names and find out what the dataset contains, I don't
have the file contents yet. If I would try to play one of the recordings with the
vlc player, this would fail::

   vlc Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

This is a curious behavior, but there are many advantages to this. One is speed, and
another one is small disk usage. Here is the total size of this dataset::

   cd ../ # in longnow/
   du -sh  # Unix command to show the size of contents

It's tiny! But we can also find out how large the dataset would be if we had all
of its contents with datalad status and the --annex flag. In total, there are
more than 15GB of podcasts you now have access to::

   datalad status --annex

You can get individual or groups of files,
directories, or datasets with the datalad get command. This command retrieves
the content for you::

   datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

Content that is already present is not re-retrieved::

   datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3  \Long_Now__Seminars_About_Long_term_Thinking/2003_12_13__Peter_Schwartz__The_Art_Of_The_Really_Long_View.mp3  \Long_Now__Seminars_About_Long_term_Thinking/2004_01_10__George_Dyson__There_s_Plenty_of_Room_at_the_Top__Long_term_Thinking_About_Large_scale_Computing.mp3

If you don't need the data locally anymore you can
drop the content from your dataset to save disk space::

   datalad drop Long_Now__Seminars_About_Long_term_Thinking/2003_12_13__Peter_Schwartz__The_Art_Of_The_Really_Long_View.mp3

Afterwards, as long as DataLad knows where a file came from, its content can be retrieved
again::

   datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_12_13__Peter_Schwartz__The_Art_Of_The_Really_Long_View.mp3

Dataset nesting
^^^^^^^^^^^^^^^

Let's take a look into the history of the longnow subdataset:
We can see that it has preserved its history completely. This means that the data we
retrieved preserved all of its provenance::

   git log --reverse

How does this look in the top-level dataset? If we query DataLad-101s history,
there will be no commit about mp3 files or any of the commits we have seen in
the subdataset. Instead, we can see that the super dataset recorded
the recordings|longnow dataset as a subdataset. This means that it recorded where this dataset
came from and what version it is in::

  cd ../../
  git log -p -n 1

The subproject commit registered the most recent commit of the subdataset, and thus
the subdataset version::

   cd recordings/longnow
   git log --oneline
   cd ../../

More on data versioning, nesting, and a glimpse into reproducible paper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We'll clone a repository for a paper that shares the manuscript, code, and data::

   cd ../
   datalad clone git@github.com:psychoinformatics-de/paper-remodnav.git

The top-level dataset has many subdatasets. One of it, remodnav, is a dataset that contains the source code for a Python
package called remodnav used in eye tracking analyses::

   cd paper-remodnav
   datalad subdatasets

After cloning a dataset, its subdatasets will be known, but just as content is
not yet retrieved for files in datasets, subdatasets of datasets are not yet
installed. If I navigate into an uninstalled subdataset it will appear like an
empty directory::

   cd remodnav
   ls

In order to install a subdataset, I use datalad get::

  datalad get --recursive --recursion-limit 2 -n .
  ls

This command doesn't only retrieve file contents, but it also installs
subdatasets. So if you want to be really lazy, just run datalad get --recursive
-n in the root of a dataset to install all subdatasets that are available.
The -n option prevents get from downloading any data, so that only subdataset
are installed, but no data is downloaded. Here, the depth of recursion is limited.
For one, it would take a while to install all subdatasets, but the very raw eye tracking
dataset contains subject IDs that should not be shared, and therefore, this subdataset
is not accessible - if you try to install all subdatasets, the source eyetracking
data will throw an error, because it is not made publicly available.

Afterwards, you can see that the remodnav subdataset also contains further
subdatasets. In this case, these subdatasets contain data that is used for
testing and validating software performance::

   datalad subdatasets

One of the validation
data subdatasets came form another lab that shared their data. After I was
almost finished with my paper, I found another paper that reported a mistake in
this data. The mistake was still present in the data I was using, though. So by
inspecting the history of this dataset you can see that at one point, I
contributed a fix that changed the data::

   cd remodnav/tests/data/anderson_etal
   git log -n 3

But because I can link subdatasets in precise version I can
consciously decide and openly record which version of the data I am using or
even test how much my results change by resetting the subdataset to an earlier
state or updating the dataset to a more recent version.

Reproducible analyses
^^^^^^^^^^^^^^^^^^^^^

Not only can I version control data and consume data with datalad, I
can also create datasets with data analyses in a way that my future self
and others can easily and automatically recompute what was done::

   cd ../../../../ # get out of the paper repository

First, create a new dataset, in this case with the yoda configuration::

   datalad create -c yoda myanalysis

This sets up a helpful structure for my dataset with a code directory and some README files,
and applies helpful configurations::

   cd myanalysis
   tree

Read up more about the YODA principles and the yoda configuration in the section
:ref:`yoda`.

Next, install input data as a subdataset. For this, I created a
dataset with the Iris data and published it on Github. Here, we're installing it
into a directory ``input``::

   datalad clone -d . git@github.com:datalad-handbook/iris_data.git input/


The last thing is code to run on the data and produce results. For this, here is a
k-means classification analysis script written in Python. You can find this analysis
in more detail in the section :ref:`yoda_project`::

   cat << EOT > code/script.py

   import pandas as pd
   import seaborn as sns
   import datalad.api as dl
   from sklearn import model_selection
   from sklearn.neighbors import KNeighborsClassifier
   from sklearn.metrics import classification_report

   data = "input/iris.csv"

   # make sure that the data are obtained (get will also install linked sub-ds!):
   dl.get(data)

   # prepare the data as a pandas dataframe
   df = pd.read_csv(data)
   attributes = ["sepal_length", "sepal_width", "petal_length","petal_width", "class"]
   df.columns = attributes

   # create a pairplot to plot pairwise relationships in the dataset
   plot = sns.pairplot(df, hue='"'"'class'"'"', palette='"'"'muted'"'"')
   plot.savefig('"'"'pairwise_relationships.png'"'"')

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
   df_report = pd.DataFrame(report).transpose().to_csv('"'"'prediction_report.csv'"'"')

   EOT


So far the script is untracked::

   datalad status

Let's save it with a datalad save command and also attach an identifier with the
``--version-tag`` flag::

   datalad save -m "add script for kNN classification and plotting" --version-tag ready4analysis code/script.py

The challenge DataLad helps me to accomplish is running this script in a way
that links the script to the results it produces and the data it was computed
from. I can do this with the datalad run command. In principle, it is simple.
You start with a clean dataset::

   datalad status

Then, give the command you would execute to datalad run, in this case ``python code/script.py``.
Datalad will take the command, run it, and save all of the changes in the
dataset that leads it to under the commit message specified with
the -m option. Thus, it associates the script with the results.
But it can be even more helpful. Here, we also specify the input data the command
needs and datalad will get the data beforehand. And we also specify the output
of the command. To understand fully what this does, please read chapters
:ref:`chapter_run` and :ref:`chapter_gitannex`, but specifying the outputs will allow me later to rerun
the command and let me update outdated results::

   datalad run -m "analyze iris data with classification analysis" \
   --input "input/iris.csv" \
   --output "prediction_report.csv" \
   --output "pairwise_relationships.png" \
   "python3 code/script.py"

Datalad creates a commit in my history. This commit has my commit
message as a human readable summary of what was done, it contains the produced
output, and it has a machine readable record that contains information on the
input data, the results, and the command that was ran to create this result::

   git log -n 1

This machine readable record is particularly helpful, because I can now instruct
datalad to rerun this command so that I don't have to memorize what I had done
and people I share my dataset with don't need to ask me how this result was
produced, by can simply let DataLad tell them.

This is done with the ``datalad rerun`` command. For this demonstration, I have
prepared this analysis dataset and published it to GitHub at
`github.com/adswa/my_analysis <https://github.com/adswa/myanalysis>`_::

   cd ../
   git clone git@github.com:adswa/myanalysis.git analysis_clone

I can clone this repository and give for example the checksum of the run command
to the ``datalad rerun`` command. DataLad will read the machine readable record of
what was done and recompute the exact same thing::

   datalad rerun 71cb8c5

This allows others to very easily rerun my computations, but it also spares me
the need to remember how I executed my script, and I can ask for results where they
came from::

   git log pairwise_relationships.png


Computational reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't have the required python packages available, running the script and
computing the results will fail. In order to be computationally reproducible
I need to attach the software that is necessary for computation to this
execution record::

   cd ../myanalysis

And the way I can do this is with a datalad extension called datalad containers.
You can install this extension with pip by running
``pip install datalad-containers``.
This extension allows attaching software containers such as singularity
images to my dataset and execute my commands inside of these containers. Thus, I
can share data, code, code execution, and software.

Here is how this works: First, I attach a software container to my dataset using
``datalad containers-add`` with a name of the container (here I call it ``software``)
and a url or path where to find this container, here it is singularity hub. This
records the software in the dataset::

   datalad containers-add software --url shub://adswa/resources:2

Note: You need to have `singularity <https://sylabs.io/guides/3.5/user-guide/>`_
installed to run this!

Afterwards, rerun the analysis in the software container with the
``datalad containers-run`` command. This container works just as the run command before, I
only need to specify the container name. If you were to rerun such an analysis,
datalad would not only retrieve the input data but also the software container::

   datalad containers-run -m "rerun analysis in container" \
   --container-name software \
   --input "input/iris.csv" \
   --output "prediction_report.csv" \
   --output "pairwise_relationships.png" \
   "python3 code/script.py"

Read more about this in the section :ref:`containersrun`.


**Done! Thanks for coding along!**