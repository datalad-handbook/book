.. _mpiberlin:

An introduction to DataLad at the MPI Berlin
--------------------------------------------

This code contains code-along snippets to copy and paste into your own terminal, as well as additional references to useful chapters if you want to read up about a specific command elsewhere in the DataLad Handbook.

Introduction & set-up
^^^^^^^^^^^^^^^^^^^^^

In order to code along, you should have a recent DataLad version, e.g., ``0.13.5``, installed.
Installation instructions are in section :ref:`install`.
You can check which version of DataLad you have installed with the following command::

   datalad --version

You should also have a configured :term:`Git` identity. Here is how you set it::

   git config --global --add user.name "Bob McBobFace"
   git config --global --add user.email "bob@example.com"

How to use DataLad
^^^^^^^^^^^^^^^^^^

DataLad is a command line tool and it has a Python API.
Whenever used, it is thus operated it in a :term:`terminal` using the command line (as done above), or used it in scripts such as shell scripts, Python scripts, Jupyter Notebooks, and so forth.
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

Creating a dataset is done with the ``datalad create`` command.
This command only needs a name, and it will subsequently create a new directory under this name and instruct DataLad to manage it.
Here, the command also has an additional option, the ``-c yoda`` option.
With the -c option, datasets can be configured in a certain way at the time of creation.
You can find out about the details of the yoda configuration in the datalad handbook in sections :ref:`procedures`, but in general this configuration is a very useful standard configuration for datasets for data analysis, as it preconfigures a dataset according to the :ref:`yoda principles <yoda>`::

   datalad create -c yoda myanalysis

After creating it, the dataset is a new directory, and you can "change directories" (``cd``) inside it::

   cd myanalysis

Here is how the directory looks at the moment::

   tree       # lists the file structure

The YODA procedure pre-created a useful directory structure and added some placeholder ``README`` files.
If you list all of the hidden files with ``ls -a`` as well, you can see that tools such as :term:`Git` and DataLad operate in the background, with hidden directories and files::

   ls -a      # show also hidden files


Version control
^^^^^^^^^^^^^^^

Version controlling a file means to record its changes over time, associate those changes with an author, date, and identifier, creating a lineage of file content, and being able to revert changes or restore previous file versions.
DataLad datasets use two established version control tools: :term:`Git` and :term:`git-annex`.
Thanks to those tools, datasets can version control their contents, regardless of size.
Let's see what happens when we delete placeholders in the ``README``::

   echo " " >| README.md       # this overwrites existing contents

:command:`datalad status` can report on the state of a dataset.
As we modified a version controlled file, this file shows up as being "modified"::

   datalad status

What has changed compared to the files last known version state?
The :command:`git diff` can tell us::

   git diff

Let's also replace the contents of the other README::

   echo " " >| code/README.md
   git diff

In order to save a modification one needs to use the :command:`datalad save` command.
:command:`datalad save` will save the current status of your dataset: It will save both modifications to known files and yet untracked files.
The ``-m/--message`` option lets you attach a concise summary of your change.
Such a :term:`commit message` makes it easier for others and your later self to understand a dataset's history::

   datalad save -m "Replace placeholder in README"

Note that ``datalad save`` will save **all** modifications in a dataset at once!
If you have several modified files, you can supply a path to the file or files you want to save::

   # make some more edits to the file
   nano README.md

Here is what you changed::

   git diff

Let's make another change to the dataset, by adding a new file (a webcomic, downloaded via `wget <https://en.wikipedia.org/wiki/Wget>`_)::

   wget https://imgs.xkcd.com/comics/compiling.png

.. windows-wit:: Windows users may not have wget

   If the ``wget`` command above fails for you, you could

   * Install a Windows version of wget
   * Use the following ``curl`` command: ``curl https://imgs.xkcd.com/comics/compiling.png --output compiling.png`` (recent Windows 10 builds include ``curl`` natively)
   * Download and save the image from your web browser

With this change, there are two modifications in your dataset, a modified file and an untracked file::

   datalad status

You can add a path to make sure only modifications in the specified file are saved::

   datalad save -m "Add project information to README" README.md

And perform a second ``datalad save`` to save remaining changes, i.e., the yet untracked comic::

   datalad save -m "Add a motivational webcomic"

Your dataset has now started to grow a log of everything that was done.
You can view this history with the command :command:`git log`, or any tool that can display :term:`Git` history, such as :term:`tig`.
You can even ask a specific file what has been done to it::

   git log README.md

While you can add and save any file into your dataset, it is often useful to know where files came from.
If you add a file from a web-source into your dataset, you can use the command ``datalad download-url`` in order to download the file, save it together with a commit message into the dataset, and record its origin internally.
Soon it will become clear why this is a useful feature.
Here, we add a comic as a little `Easter egg <https://imgs.xkcd.com/comics/fuck_grapefruit.png>`_ (because we save it as a hidden dotfile called ``.easteregg``) into the dataset::

   datalad download-url -m "add motivational comic to my dataset"  \
      -O .easteregg  \
      https://imgs.xkcd.com/comics/fuck_grapefruit.png
   # open the comic
   xdg-open .easteregg

The very first chapter of the handbook, :ref:`chapter_datasets` will show you even more details about version controlling files in datasets.


Data consumption & transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Datasets can be installed from local paths or remote URLs using :command:`datalad clone`.
Cloning is a fast operation, and the resulting dataset typically takes up only a fraction of the total size of the data that it tracks::

   cd ../
   datalad clone git@github.com:datalad-datasets/machinelearning-books.git

After installations, the directory tree can be browsed, but most files in datasets will not yet contain file content.
This makes cloning fast and datasets lightweight::

   cd machinelearning-books
   ls
   # print the size of the directory in human readable sizes
   du -sh

The dataset can have a lot of file contents though.
``datalad status`` can report on how much data actually is accessible with the ``--annex`` and ``--annex all`` options::

   datalad status --annex

On demand, content for files, directories, or the complete dataset can be downloaded using :command:`datalad get`.
The snippet below uses :term:`globbing` to get the content of all books that start with a "D", but you could also get a full directory, a single file, all files, etc.::

    datalad get D*

This works because DataLad datasets track where file contents are available from.
If the origin of a file (such as a web source) is known, you can drop file *content* to free up disk space, but you retain access via :command:`datalad get`::

   datalad drop D.C.C.MacKay-Information_Theory_Inference_and_Learning_Algorithms.pdf

This, too, works for files saved with :command:`datalad download-url`::

   cd ../myanalysis
   datalad drop .easteregg

but DataLad will refuse to drop files that it doesn't know how to reobtain unless you use ``--nocheck``::

   datalad drop compiling.png

Afterward dropping files, only "metadata" about file content and file availability stays behind, and you can't open the file anymore::

   xdg-open .easteregg    # its gone :(!

But because the origin of the file is known, it can be reobtained using the :command:`datalad get`::

   datalad get .easteregg

Opening the comic works again, afterwards::

   xdg-open .easteregg

This mechanism gives you access to data without the necessity to store all of the data locally.
As long as there is one location that data is available from (a dataset on a shared cluster, a web source, cloud storage, a USB-stick, ...) and this source is known, there is no need for storing data when it is not in use.
If you want to try it with large amounts of data, checkout `datasets.datalad.org <http://datasets.datalad.org/>`_, a collection of more than 200TB of open data.


Dataset nesting
^^^^^^^^^^^^^^^

Datasets can be nested in superdataset-subdataset hierarchies.
This helps to link datasets together.
It is especially helpful to do this to link input data to an analysis dataset -- it helps to reuse data in multiple analysis, to link input data in a precise version, and to create an intuitively structured dataset layout.

.. figure:: ../artwork/src/linkage_subds.svg

We will start a data analysis in the ``myanalysis`` dataset
First, let's install input data (a small dataset from GitHub) as a subdataset.
This is done with the ``-d/--dataset`` option of :command:`datalad clone`::

   datalad clone -d . git@github.com:datalad-handbook/iris_data.git input/

This dataset has been linked in a precise version to the dataset, and it has preserved its complete history.


Reproducible analyses
^^^^^^^^^^^^^^^^^^^^^

Not only can DataLad version control, consume, and share data, it can also help to create datasets with data analyses in a way that your future self and others can easily and automatically recompute what was done.
In this part of the tutorial, we start with a small analysis to introduce core commands and concepts for reproducible execution.
Later, during a more elaborate ML-themed analysis, these commands and concepts will reappear.

For the first small analysis, we start by adding some code for a data analysis (copy paste from ``cat`` to the final ``EOT`` to paste the code into a file ``scripty.py`` in your ``code/`` directory, or use an editor of your choice and copy paste the script)::

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
   plot = sns.pairplot(df, hue='class', palette='muted')
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

This script highlights an important key point from the YODA principles:
:term:`relative path`\s instead of :term:`absolute path`\s make the dataset self-contained and portable.
It also demonstrates how DataLad's Python API can be used with a :command:`dl.get()` function in the script.

Running the above code block created a new file in the dataset::

   datalad status

Let's save it with a datalad save command.
DataLad save can in addition also attach an identifier in the form of a :term:`tag` with the ``--version-tag`` flag::

   datalad save -m "add script for kNN classification and plotting" \
     --version-tag ready4analysis code/script.py

The :command:`datalad run` command can run this script in a way that links the script to the results it produces and the data it was computed from.
In principle, the command is simple: Execute any command, save the resulting changes in the dataset, and associate them as well as all other optional information provided.
Because each :command:`datalad run` ends with a :command:`datalad save`, its recommended to start with a clean dataset (see :ref:`chapter_run` for details on how to use it in unclean datasets)::

   datalad status

Then, give the command you would execute to datalad run, in this case ``python code/script.py``.
Datalad will take the command, run it, and save all of the changes in the dataset that this leads this to under the commit message specified with the -m option.
Thus, it associates the script (or any command execution) with the results it generates.
But the command can become even more helpful.
Below, we also specify the input data the command needs - DataLad will make sure to :command:`get` the data beforehand.
And we also specify the output of the command.
This is not in order to identify outputs (DataLad would do that on its own), but to specify files that should be :command:`unlock`\ed and potentially updated if the command is reran -- but more on this later.
To understand fully what ``--output`` does, please read chapters :ref:`chapter_run` and :ref:`chapter_gitannex`::

   datalad run -m "analyze iris data with classification analysis" \
    --input "input/iris.csv" \
    --output "prediction_report.csv" \
    --output "pairwise_relationships.png" \
    "python3 code/script.py"

.. admonition:: software note

   In order to execute the above script successfully you will need to run it in an environment that has the Python packages pandas, scikit-learn, datalad, and seaborn installed.
   If you're thinking "WTF, it is SO inconvenient that I have to create the software environment to make this run", wait until the next section.

Datalad creates a commit in the dataset history.
This commit has the commit message as a human readable summary of what was done, it contains the produced output, and it has a machine readable record that contains information on the
input data, the results, and the command that was run to create this result::

   # take a look at the most recent entry in git log
   git log -n 1

This machine readable record is particularly helpful, because one can now instruct datalad to ``rerun`` this command so that you don't have to memorize what had been done, and people you share the dataset with don't need to ask you how this result was produced, by can simply let DataLad tell them.

This is done with the ``datalad rerun`` command.
For this demonstration, there is a published analysis dataset that resembles the one created here fully at `github.com/adswa/my_analysis <https://github.com/adswa/myanalysis>`_.
This dataset can be cloned, and the analysis within it can be automatically rerun::

   cd ../
   datalad clone git@github.com:adswa/myanalysis.git analysis_clone


Among other ways, run records can be identified via their commit hash.
If given to ``datalad rerun <hash>``, DataLad will read the machine readable record of what was done, get required data, unlock to-be-modified files, and recompute the exact same thing::

   cd analysis_clone
   datalad rerun 71cb8c5

This allows others to very easily rerun computations, but it also spares yourself the need to remember how a script was executed, and results can simply be asked where they came from::

   git log pairwise_relationships.png

Computational reproducibility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Its fantastic to have means to recompute a command automatically, but the ability to re-execute a command is often not enough.
If you don't have the required Python packages available, or in a wrong version, running the script and computing the results will fail.
In order to be *computationally* reproducible the run record does not only need to link code, command, and data, but also encapsulate the *software* that is necessary for a computation::

   cd ../myanalysis

The way this can be done is with a :term:`DataLad extension` called ``datalad container``.
You can install this extension with :term:`pip` by running ``pip install datalad-container``.
This extension allows to attach :term:`software container`\s such as :term:`Singularity` or :term:`Docker` :term:`container image`\s to the dataset and execute commands inside of these containers.
Thus, the dataset can share share data, code, code execution, and software.

Here is how this works: First, attach a software container to the dataset using ``datalad containers-add``.
This command needs a name for the container (here it is called ``software``, but you can go for any name -- how about "take-this-one-mom"?), and a URL or path where to find the container.
Here, it is a URL that points to :term:`Singularity-hub` (but :term:`Docker-Hub`, with a ``docker://<user>/<container>:<version>`` URL, would work fine, too).
This records a pre-created software environment with the required Python packages in the dataset::

   datalad containers-add software --url shub://adswa/resources:2

Note: You need to have `singularity <https://sylabs.io/guides/3.5/user-guide/>`_ installed to run this!

.. find-out-more:: Why Singularity and not Docker?

   :term:`Singularity`, unlike :term:`Docker`, can be deployed on shared compute infrastructure such as computational clusters as it does not require or grant `superuser privileges <https://en.wikipedia.org/wiki/Superuser>`_ ("sudo rights") to users that use a container.
   Docker is not deployed on HPC systems is because it grants users those sudo rights, and on multi-user systems users should not have those privileges, as it would enable them to tamper with other's or shared data and resources, posing a severe security threat.
   Singularity is capable of working with both Docker and Singularity containers, though.

Afterwards, rerun the analysis in the software container with the ``datalad containers-run`` command.
This container works just as the run command before, with the additional ``-n/--name`` option that is needed to specify the container name.
If you were to rerun such an analysis, DataLad would not only retrieve the input data but also the software container::

   datalad containers-run -m "rerun analysis in container" \
   --container-name software \
   --input "input/iris.csv" \
   --output "prediction_report.csv" \
   --output "pairwise_relationships.png" \
   "python3 code/script.py"

You can read more about this command and containers in general in the section :ref:`containersrun`.


An ML-themed example
^^^^^^^^^^^^^^^^^^^^

Typically, ML analysis aren't as straightforward as the example above.
The following workflow demonstrates a more realistic analysis path in machine learning projects.
The example in this workflow is an image classification task on the `Imagenette dataset <https://github.com/fastai/imagenette>`_, a smaller subset of the `Imagenet dataset <http://www.image-net.org/>`_, one of the most widely used large scale dataset for bench-marking Image Classification algorithms.
It consists of the following steps:

* Create a stand-alone input dataset with data from the Imagenette dataset
* Set up a data analysis dataset, and install the input data as a subdataset
* Prepare a subset of the data by creating training and validation labels
* Train, evaluate, and compare different kinds of classifiers
* Update the input data and redo the analysis

The workflow will demonstrate how re-executable run records and DataLad's linking and updating mechanisms can be used to repeat more complex and multistepped analyses than the previous example that include evolving input datasets.
Beyond DataLad commands, it makes use of some :term:`Git` concepts (:term:`tag`\s, :term:`branch`\es) to create transparent analysis logs.

Create an input dataset
"""""""""""""""""""""""

First of all, we create a new dataset from scratch to put the Imagenette data inside::

   cd ../
   datalad create imagenette

Afterwards, we can download the Imagenette data and save it in the dataset.
It is made available as a tarball via an Amazon S3 bucket.
A very convenient way of downloading such an archive is with the :command:`datalad download-url --archive` command -- this command does not only download and save data and its origin, but it also unpacks the archive and keeps an archive as an internal backup.
Thus, you could drop the unpacked data, and a :command:`datalad get` would re-extract it from a local archive.
Only if the local archive is dropped as well the data is re-downloaded from the S3 bucket::

   cd imagenette
   # 0.12.2 <= datalad < 0.13.4  needs the configuration option -c datalad.runtime.use-patool=1 to handle .tgz
   datalad -c datalad.runtime.use-patool=1 download-url \
     --archive \
     --message "Download Imagenette dataset" \
     'https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz'

Afterwards, ``tree -d`` shows the directory hierarchy of the dataset::

   tree -d

It is split in a train and validation set, and within each subdirectory, one directory exists per image class (ten categories: tenches (a type of fish), English springer (a type of dog), cassette players, chain saws, churches, French horns, garbage trucks, gas pumps, golf balls, and parachutes).

Create an analysis dataset
""""""""""""""""""""""""""

Next, we set up and configure a dataset for the analysis.
Given that code is frequently modified and should be easily editable, and would be useful to share right away if desired, it makes sense to keep it stored in Git.
Thus, we preconfigure and prestructure the dataset with a few configurations:

.. code-block:: bash

   cd ../
   datalad create -c text2git -c yoda ml-project

It can also be useful to add use case specific ``.gitignore`` files to datasets.
``.gitignore`` files can keep files from being version controlled by any tool, which is helpful in keeping a clean dataset state even though certain tools create temporary or useless files (such as ``.DSStore`` under macos, ``.$ICON`` files under Windows, ``.idea/`` directories when using PyCharm, ``__pycache__`` files, and so forth).
The chapter :ref:`gitignore` has more insights on how these files work.
Thankfully, there are thousands of useful premade templates for various applications, and below we're downloading a comprehensive ``.gitignore`` file for Python projects::

   datalad download-url -m "Add Python project .gitignore template" \
     https://raw.githubusercontent.com/toptal/gitignore/master/templates/Python.gitignore \
     -O .gitignore

Next, the input dataset is installed as a subdataset from the local path::

   cd ml-project
   mkdir -p data
   # install the dataset into data/
   datalad clone -d . ../imagenette data/raw


Here's how it looks like in the dataset now::

   # show the directory hierarchy
   tree -d

In order to link the correct software environment to the data we add a prepared software container with the correct Python libraries for the analysis::

   datalad containers-add software --url shub://adswa/python-ml:1

Prepare the data
""""""""""""""""

This workflow uses a script to create labeled sets of training and validation data -- for the sake of this example, only two categories of ten are labeled.
The script will read out file names from the input data, and create CSV files that map file names to image categories::

   cat << EOT > code/prepare.py
   #!/usr/bin/env python3

   from pathlib import Path

   FOLDERS_TO_LABELS = {"n03445777": "golf ball",
                        "n03888257": "parachute"}


   def files2labels(source, label, out):
       for image_path in source.rglob("*.JPEG"):
           out.write('{},{}\n'.format(image_path, label))


   if __name__ == "__main__":
       data_path = Path('data')
       fileheader = 'filename,label\n'
       for part, labelfname in (('train', 'train.csv'),
                                ('val', 'test.csv')):
           with Path('data', labelfname).open('w') as labelfile:
               labelfile.write(fileheader)
               for imgfolder, label in FOLDERS_TO_LABELS.items():
                   files2labels(
                       Path('data', 'raw', 'imagenette2-160', part, imgfolder),
                       label,
                       labelfile)
   EOT

This yields a new, untracked file::

   datalad status

And we can save it, optionally with a version tag::

   datalad save -m "Add script for data preparation for 2 categories" \
      --version-tag "ready4prepping" code/prepare.py


We prepare the data using :command:`datalad containers-run` to ensure that all relevant Python libraries are installed.
To keep execution time in this example short, we only specify the subset of the data that the above script uses as an input, and we use the ``datalad.runtime.max-annex-jobs`` configuration to parallelize execution::


   datalad -c datalad.runtime.max-annex-jobs=5 containers-run -n software \
     -m "Prepare the data for categories golf balls and parachutes" \
     --input 'data/raw/imagenette2-160/train/n03445777' \
     --input 'data/raw/imagenette2-160/val/n03445777' \
     --input 'data/raw/imagenette2-160/train/n03888257' \
     --input 'data/raw/imagenette2-160/val/n03888257' \
     --output 'data/train.csv' \
     --output 'data/test.csv' \
     "python3 code/prepare.py"


Train and evaluate an ML model
""""""""""""""""""""""""""""""

The next two scripts are used for training and evaluation.
The training script below will use a stochastic gradient descent classifier and train it on the training set.
Afterwards, it will dump the trained classifier as a joblib object -- this allows to transparently cache the classifier as a Python object to disk.
Later, `the cached model can be applied to various data with the need to retrain the classifier <https://scikit-learn.org/stable/modules/model_persistence.html>`_.
The code below creates the first script::

   cat << EOT > code/train.py
   #!/usr/bin/env python3

   from joblib import dump
   from pathlib import Path

   import numpy as np
   import pandas as pd
   from skimage.io import imread_collection
   from skimage.transform import resize
   from sklearn.linear_model import SGDClassifier


   def load_images(data_frame, column_name):
       filelist = data_frame[column_name].to_list()
       image_list = imread_collection(filelist)
       return image_list


   def load_labels(data_frame, column_name):
       label_list = data_frame[column_name].to_list()
       return label_list


   def preprocess(image):
       resized = resize(image, (100, 100, 3))
       reshaped = resized.reshape((1, 30000))
       return reshaped


   def load_data(data_path):
       df = pd.read_csv(data_path)
       labels = load_labels(data_frame=df, column_name="label")
       raw_images = load_images(data_frame=df, column_name="filename")
       processed_images = [preprocess(image) for image in raw_images]
       data = np.concatenate(processed_images, axis=0)
       return data, labels


   def main(repo_path):
       train_csv_path = repo_path / "data/train.csv"
       train_data, labels = load_data(train_csv_path)
       clf = SGDClassifier(max_iter=10)
       trained_model = clf.fit(train_data, labels)
       dump(trained_model, repo_path / "model.joblib")


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT

Let's save it::

   datalad save -m "Add SGD classification script" code/train.py

The next script loads the trained classifier from disk and evaluates it on the validation data.
To evaluate the model performance, it calculates the accuracy of the prediction, i.e., the proportion of correctly labeled images, prints it to the terminal, and saves it into a JSON file in the superdataset::

   cat << EOT > code/evaluate.py

   #!/usr/bin/env python3

   from joblib import load
   import json
   from pathlib import Path

   from sklearn.metrics import accuracy_score

   from train import load_data


   def main(repo_path):
       test_csv_path = repo_path / "data/test.csv"
       test_data, labels = load_data(test_csv_path)
       model = load(repo_path / "model.joblib")
       predictions = model.predict(test_data)
       accuracy = accuracy_score(labels, predictions)
       metrics = {"accuracy": accuracy}
       print(metrics)
       accuracy_path = repo_path / "accuracy.json"
       accuracy_path.write_text(json.dumps(metrics))


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT

Let's save the script.
Because we're "ready for analysis" with this last piece, we can set a tag::

   datalad save -m "Add script to evaluate model performance" --version-tag "ready4analysis" code/evaluate.py


And now, we can execute the scripts.
First, train the model::

   datalad containers-run -n software \
     -m "Train an SGD classifier on the data" \
     --input 'data/raw/imagenette2-160/train/n03445777' \
     --input 'data/raw/imagenette2-160/train/n03888257' \
     --output 'model.joblib' \
     "python3 code/train.py"


Then, evaluate performance::

   datalad containers-run -n software \
     -m "Evaluate SGD classifier on test data" \
     --input 'data/raw/imagenette2-160/val/n03888257' \
     --input 'data/raw/imagenette2-160/val/n03445777' \
     --output 'accuracy.json' \
     "python3 code/evaluate.py"

Repeat after tuning!
""""""""""""""""""""

We can now demonstrate how the run records come in handy when we change an aspect of the analysis.
Let's increase the number of iterations turing training from 10 to 100 (here done via the stream editor :term:`sed`)::

   sed -i 's/SGDClassifier(max_iter=10)/SGDClassifier(max_iter=100)/g' code/train.py

Here is what changed::

   git diff

First, we save this change, and mark it with a tag::

   datalad save -m "Increase the amount of iterations to 100" --version-tag "SGD-100" code/train.py


And then we can rerun all run records in the dataset history between two states (identified with the version tags provided in this example, but commit hashes are an equally possible alternative)::

   datalad rerun -m "Recompute classification with more iterations" ready4analysis..SGD-100

If this did not yet lead to a fully satisfactory performance, we could switch classifiers.
The code block below changes the script to use a random forest instead of stochastic gradient descent::

   sed -i 's/linear_model import SGDClassifier/ensemble import RandomForestClassifier/g' code/train.py
   sed -i 's/SGDClassifier(max_iter=100)/RandomForestClassifier()/g' code/train.py

Here is what has changed::

   git diff

Let's save the new script version and tag it::

   datalad save -m "Switch to random forest classification" --version-tag "random-forest" code/train.py


To easily compare the two models, SGD and random forest, we can rerun training and classification with the random forest script on a new branch.
This uses a built-in feature of :command:`datalad rerun`, and is useful as one can very fast and easily switch between the new and the old branch (of which each has the trained model and its accuracy evaluation readily available)::

   datalad rerun --branch="randomforest" -m "Recompute classification with random forest classifier" ready4analysis..SGD-100


A ``git diff`` between the two branches in the ``accuracy.json`` file can give an overview of how the models compare::

   git diff master -- accuracy.json

A ``git checkout`` will get you back to the previous branch with the trained SGD model and results.
Should you decide that a model is not worth keeping in the revision history, you can selectively drop data from those branches.
The run records you kept could always be used to recompute a dropped ``model.joblib`` file, though::

   git checkout master
   cat accuracy.json

Repeat on changed data!
"""""""""""""""""""""""

Let's say you're training on an evolving set of images and your input dataset is changing.
We can simulate this by removing a file from the input data and pretending its faulty (we would have added a file, but couldn't find a nice one).
Importantly, we're applying the change in the original dataset::

   cd ../imagenette
   rm imagenette2-160/train/n03445777/ILSVRC2012_val_00002314.JPEG

Afterwards, :command:`datalad status` reports the file to be deleted::

   datalad status

(Side-note: While the file is deleted in the most recent dataset state, it can be brought back to life as it still exists in the datasets history.
You can find out more about this and also how to remove also past copies of a file in the section :ref:`filesystem`)

The deletion of a file must be saved::

    datalad save -m "remove faulty image"

This change can be brought into all clones of the dataset by updating them.
Here is how that looks like::

   cd ../ml-project/data/raw
   datalad update --merge

This has integrated the changes in the original dataset::

   git log

In the superdataset, the subdataset is now reported as having changed from its originally linked state::

   cd ../../
   datalad status

To make the changed input data transparent in your analysis, you can save the updated subdataset state::

   datalad save -m "Update input data - we removed a file"

To now recompute the complete workflow with the updated data, we rerun a larger range of run-records than before to also redo the data preparation stage::

   datalad rerun -m "Recompute classification with fewer data" ready4prepping..SGD-100

Done!
This extensive walk-through has hopefully provided you with a good idea of DataLad and how it can be used in the context of machine-learning analysis.
