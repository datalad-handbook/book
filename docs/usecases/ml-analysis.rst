.. _usecase_ML:

DataLad for reproducible machine-learning analyses
--------------------------------------------------

.. index:: ! Usecase; Machine Learning Analysis

This use case demonstrates an automatically and computationally reproducible analyses in the context of a machine learning (ML) project.
It demonstrates on an example image classification analysis project how one can

- link data, models, parametrization, software and results using ``datalad containers-run``
- keep track of results and compare them across models or parametrizations
- stay computationally reproducible, transparent, and importantly, intuitive and clear


The Challenge
^^^^^^^^^^^^^

Chad is a recent college graduate and has just started in a wicked start-up that prides itself with using "AI and ML for individualized medicine" in the Bay area.
Even though he's extraordinarily motivated, the fast pace and pressure to deliver at his job are still stressful.
For his first project, he's tasked with training a machine learning model to detect cancerous tissue in `computer tomography (CT) <https://en.wikipedia.org/wiki/CT_scan>`_ images.
Excited and eager to impress, he builds his first image classification ML model with state of the art Python libraries and a `stochastic gradient descent (SGD) <https://en.wikipedia.org/wiki/Stochastic_gradient_descent>`_ classifier.
"Not too bad", he thinks, when he shares the classification accuracy with his team lead, "way higher than chance level!"
"Fantastic, Chad, but listen, we really need a higher accuracy than this.
Our customers deserve that. Turn up the number of iterations. Also, try a random forest classification instead. And also, I need that done by tomorrow morning latest, Chad.
Take a bag of organic sea-weed-kale crisps from the kitchen, oh, and also, you're coming to our next project pitch at the roof-top bar on Sunday?"

Hastily, Chad pulls an all-nighter to adjust his models by dawn.
Increase iterations here, switch classifier there, oh no, did this increase or decrease the overall accuracy? Tune some parameters here and there, re-do that previous one just one more time just to be sure.
A quick two-hour nap on the office couch, and he is ready for the `daily scrum <https://en.wikipedia.org/wiki/Scrum_(software_development)#Daily_scrum>`_ in the morning.
"Shit, what accuracy belonged to which parametrization again?", he thinks to himself as he pitches his analysis and presents his results.
But everyone rushes to the next project already.

A week later, when a senior colleague is tasked with checking his analyses, Chad needs to spend a few hours with them to them guide through his chaotic analysis directory full of jupyter notebooks.
They struggle to figure out which Python libraries to install on the colleagues computer, have to adjust hard-code :term:`absolute path`\s, and fail to reproduce the results that he presented.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Machine learning analyses are complex: Beyond data preparation and general scripting, they typically consist of training and optimizing several different machine learning models and comparing them based on performance metrics.
This complexity can jeopardize reproducibility – it is hard to remember or figure out which model was trained on which version of what data and which has been the ideal optimization.
But just like any data analysis project, machine learning projects can become easier to understand and reproduce if they are intuitively structured, appropriately version controlled, and if analysis executions are captured with enough (ideally machine-readable and re-executable) provenance.

DataLad has many concepts and tools that assist in creating transparent and computationally and automatically reproducible analyses.
From general principles on how to structure analyses projects to linking and versioning software and data alongside to code or capturing analysis execution as re-executable run-records.
To make a machine-learning project intuitively structured and transparent, Chad applies DataLad's YODA principles to his work.
He keeps the training and testing data a reusable, standalone component, installed as a subdataset, and keeps his analysis dataset completely self-contained with :term:`relative path`\s in all his scripts.
Later, he can share his dataset without the need to adjust paths.
Chad also attaches a software container to his dataset, so that others don't need to recreate his Python environment.
And lastly, he wraps every command that he executes in a ``datalad containers-run`` call, such that others don't need to rely on his brain to understand the analysis, but can have a computer recompute every analysis step in the correct software environment.
Using concise commit messages and :term:`tag`\s, Chad creates a transparent and intuitive dataset history.
With these measures in place, he can experiment flexibly with various models and data, and does not only have means to compare his models, but can also set his dataset to the state in which his most preferred model is ready to be used.

Step-by-Step
^^^^^^^^^^^^

.. admonition:: Required software

   The analysis requires the Python packages `scikit-learn <https://scikit-learn.org/stable/>`_, `scikit-image <https://scikit-image.org/>`_, `pandas <https://pandas.pydata.org/>`_, and `numpy <https://numpy.org/>`_.
   We have build a :term:`Singularity` :term:`software container` with all relevant software, and the code below will use the ``datalad-containers`` extension [#f1]_ to download the container from :term:`Singularity-Hub` and execute all analysis in this software environment.
   If you do not want to install the ``datalad-containers`` extension or Singularity, you can also create a :term:`virtual environment` with all necessary software if you prefer [#f2]_, and exchange the ``datalad containers-run`` commands below with ``datalad run`` commands.

Let's start with an overview of the analysis plans:
We're aiming for an image classification analysis.
In this type of ML analysis, a `classifier` is trained on a subset of data, the `training set`, and is then used for predictions on a previously unseen subset of data, the `test set`.
Its task is to label the test data with one of several class attributes it is trained to classify, such as `"cancerous" or "non-cancerous" with medical data <https://www.nature.com/articles/d41586-020-00847-2>`_, `"cat" or "dog" <https://www.kaggle.com/c/dogs-vs-cats>`_ with your pictures of pets, or "spam" versus "not spam" in your emails.
In most cases, classification analyses are `supervised` learning methods: The correct class attributes are known, and the classifier is tested on a `labeled` set of training data.
Its classification accuracy is calculated from comparing its performance on the unlabeled testing set with its correct labels.
As a first analysis step, train and testing data therefore need to be labeled -- both to allow model training and model evaluation.
In a second step, a classifier needs to be trained on the labeled test data.
It learns which features are to be associated with which class attribute.
In a final step, the trained classifier classifies the test data, and its results are evaluated against the true labels.

Below, we will go through a image classification analysis on a few categories in the `Imagenette dataset <https://github.com/fastai/imagenette>`_, a smaller subset of the `Imagenet dataset <http://www.image-net.org/>`_, one of the most widely used large scale dataset for bench-marking Image Classification algorithms. It contains images from ten categories (tench (a type of fish), English springer (a type of dog), cassette player, chain saw, church, French horn, garbage truck, gas pump, golf ball, parachute).
We will prepare a subset of the data, and train and evaluate different types of classifier.
The analysis is based on `this tutorial <https://realpython.com/python-data-version-control/>`_.

First, let's create an input data dataset.
Later, this dataset will be installed as a subdataset of the analysis.
This complies to the :ref:`YODA principles <yoda>` and helps to keep the input data modular, reusable, and transparent.

.. runrecord:: _examples/ml-101
   :language: console
   :cast: usecase_ml
   :workdir: usecases

   $ datalad create imagenette

The original Imagenette dataset contains 10 image categories can be downloaded as an archive from Amazon (`s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz <https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz>`_), but for this tutorial we're using a subset of this dataset with only two categories.
It is available as an archive from the :term:`Open Science Framework (OSF)`.
The :command:`datalad download-url --archive` not only extracts and saves the data, but also registers the datasets origin such that it can re-retrieved on demand from its original location.

.. runrecord:: _examples/ml-102
   :language: console
   :cast: usecase_ml
   :workdir: usecases
   :realcommand: cd imagenette && datalad download-url --archive --message "Download Imagenette dataset" 'https://osf.io/d6qbz/download' | grep -v '^\(copy\|get\|drop\|add\|delete\)(ok):.*(file)$' && sleep 15

   $ cd imagenette
   # 0.12.2 <= datalad < 0.13.4  needs the configuration option -c datalad.runtime.use-patool=1 to handle .tgz
   $ datalad download-url \
     --archive \
     --message "Download Imagenette dataset" \
     'https://osf.io/d6qbz/download'

Next, let's create an analysis dataset.
For a pre-structured and pre-configured starting point, the dataset can be created with the ``yoda`` and ``text2git`` :term:`run procedure`\s [#f3]_.
These configurations create a ``code/`` directory, place some place-holding ``README`` files in appropriate places, and make sure that all text files, e.g. scripts or evaluation results, are kept in :term:`Git` to allow for easier modifications.

.. windows-wit:: Note for Windows-Users

   Hey there!
   If you are using **Windows 10** (not `Windows Subsystem for Linux (WSL) <https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux>`_) **without the custom-built git-annex** installer mentioned in the installation section, you need a work-around.

   Instead of running ``datalad create -c text2git -c yoda ml-project``, please remove the configuration ``-c text2git`` from the command and run only ``datalad create -c yoda  ml-project``::

      $ datalad create -c yoda ml-project
      [INFO] Creating a new annex repo at C:\Users\mih\ml-project
      [INFO] Detected a filesystem without fifo support.
      [INFO] Disabling ssh connection caching.
      [INFO] Detected a crippled filesystem.
      [INFO] Scanning for unlocked files (this may take some time)
      [INFO] Entering an adjusted branch where files are unlocked as this filesystem does not support locked files.
      [INFO] Switched to branch 'adjusted/master(unlocked)'
      [INFO] Running procedure cfg_yoda
      [INFO] == Command start (output follows) =====
      [INFO] == Command exit (modification check follows) =====
      create(ok): C:\Users\mih\ml-project (dataset)

   Instead of the ``text2git`` configuration, you need to create a configuration by hand by pasting the following lines of text into the (hidden) ``.gitattributes`` file in your newly created dataset.
   :ref:`chapter_config` can explain the details of this procedure.

   Here are lines that need to be appended to the existing lines in ``.gitattributes`` and will mimic the configuration ``-c text2git`` would apply::

     *.json annex.largefiles=nothing

   You can achieve this by copy-pasting the following code snippets into your terminal (but you can also add them using a text editor of your choice):

   .. code-block::

      $ echo\ >> .gitattributes && echo *.json annex.largefiles=nothing >> .gitattributes

   Afterwards, these should be the contents of ``.gitattributes``:

   .. code-block::

      $ cat .gitattributes
        * annex.backend=MD5E
        **/.git* annex.largefiles=nothing
        CHANGELOG.md annex.largefiles=nothing
        README.md annex.largefiles=nothing
        *.json annex.largefiles=nothing

   Lastly, run this piece of code to save your changes:

   .. code-block:: bash

      $ datalad save -m "Windows-workaround: custom config to place text into Git" .gitattributes


.. runrecord:: _examples/ml-103
   :language: console
   :cast: usecase_ml
   :workdir: usecases/imagenette

   $ cd ../
   $ datalad create -c text2git -c yoda ml-project

Afterwards, the input dataset can be installed from a local path as a subdataset, using :command:`datalad clone` with the ``-d``/``--dataset`` flag and a ``.`` to denote the current dataset:

.. runrecord:: _examples/ml-104
   :language: console
   :cast: usecase_ml
   :workdir: usecases

   $ cd ml-project
   $ mkdir -p data
   # install the dataset into data/
   $ datalad clone -d . ../imagenette data/raw

Here are the dataset contents up to now:

.. runrecord:: _examples/ml-105
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   # show the directory hierarchy
   $ tree -d

Next, let's add the necessary software to the dataset.
This is done using the ``datalad containers`` extension and the :command:`datalad container-add` command. This command takes an arbitrary name and a path or url to a :term:`software container`, registers the containers origin, and adds it under the specified name to the dataset.
If used with a public url, for example to :term:`Singularity-Hub`, others that you share your dataset with can retrieve the container as well [#f1]_.

.. runrecord:: _examples/ml-106
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project
   :realcommand: datalad containers-add software --call-fmt 'singularity exec -B {{pwd}} --cleanenv {img} {cmd}' --url shub://adswa/python-ml:1

   $ datalad containers-add software --url shub://adswa/python-ml:1

At this point, with input data and software set-up, we can start with the first step: Dataset preparation.
The imagenette dataset is structured in ``train/`` and ``val/`` folder, and each folder contains one sub-folder per image category.
To prepare the dataset for training and testing a classifier, we create a mapping between file names and image categories.

In this example we only use two categories, "golf balls" (subdirectory ``n03445777``) and "parachutes" (subdirectory ``n03888257``).
The following script creates two files, ``data/train.csv`` and ``data/test.csv`` from the input data.
Each contains file names and category associations for the files in those subdirectories.
Note how, in accordance to the :ref:`YODA principles <yoda>`, the script only contains :term:`relative path`\s to make the dataset portable.

.. runrecord:: _examples/ml-107
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ cat << EOT > code/prepare.py
   #!/usr/bin/env python3

   import pandas as pd
   from pathlib import Path

   FOLDERS_TO_LABELS = {"n03445777": "golf ball",
                        "n03888257": "parachute"}


   def get_files_and_labels(source_path):
       images = []
       labels = []
       for image_path in source_path.rglob("*/*.JPEG"):
           filename = image_path
           folder = image_path.parent.name
           if folder in FOLDERS_TO_LABELS:
               images.append(filename)
               label = FOLDERS_TO_LABELS[folder]
               labels.append(label)
       return images, labels


   def save_as_csv(filenames, labels, destination):
       data_dictionary = {"filename": filenames, "label": labels}
       data_frame = pd.DataFrame(data_dictionary)
       data_frame.to_csv(destination)


   def main(repo_path):
       data_path = repo_path / "data"
       train_path = data_path / "raw/train"
       test_path = data_path / "raw/val"
       train_files, train_labels = get_files_and_labels(train_path)
       test_files, test_labels = get_files_and_labels(test_path)
       save_as_csv(train_files, train_labels, data_path / "train.csv")
       save_as_csv(test_files, test_labels, data_path / "test.csv")


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT

Executing the `here document <https://en.wikipedia.org/wiki/Here_document>`_ in the code block above has created a script ``code/prepare.py``:

.. runrecord:: _examples/ml-108
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ datalad status

We add it to the dataset using :command:`datalad save`:

.. runrecord:: _examples/ml-109
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ datalad save -m "Add script for data preparation for 2 categories" code/prepare.py

This script can now be used to prepare the data.
Note how it, in accordance to the :ref:`YODA principles <yoda>`, saves the files into the superdataset, and leaves the input dataset untouched.
When ran, it will create files with the following structure::

   ,filename,label
   0,data/raw/imagenette2-160/val/n03445777/n03445777_20061.JPEG,golf ball
   1,data/raw/imagenette2-160/val/n03445777/n03445777_9740.JPEG,golf ball
   2,data/raw/imagenette2-160/val/n03445777/n03445777_3900.JPEG,golf ball
   3,data/raw/imagenette2-160/val/n03445777/n03445777_5862.JPEG,golf ball
   4,data/raw/imagenette2-160/val/n03445777/n03445777_4172.JPEG,golf ball
   5,data/raw/imagenette2-160/val/n03445777/n03445777_14301.JPEG,golf ball
   6,data/raw/imagenette2-160/val/n03445777/n03445777_2951.JPEG,golf ball
   7,data/raw/imagenette2-160/val/n03445777/n03445777_8732.JPEG,golf ball
   8,data/raw/imagenette2-160/val/n03445777/n03445777_5810.JPEG,golf ball
   9,data/raw/imagenette2-160/val/n03445777/n03445777_3132.JPEG,golf ball
   [...]

To capture all provenance and perform the computation in the correct software environment, this is best done in a :command:`datalad containers-run` command:

.. runrecord:: _examples/ml-110
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project
   :realcommand: datalad containers-run -n software -m "Prepare the data for categories golf balls and parachutes" --input 'data/raw/train/n03445777' --input 'data/raw/val/n03445777' --input 'data/raw/train/n03888257'     --input 'data/raw/val/n03888257' --output 'data/train.csv' --output 'data/test.csv' "python3 code/prepare.py" | grep -v '^\(copy\|get\|drop\|add\|delete\)(ok):.*(file)'

   $ datalad containers-run -n software \
     -m "Prepare the data for categories golf balls and parachutes" \
     --input 'data/raw/train/n03445777' \
     --input 'data/raw/val/n03445777' \
     --input 'data/raw/train/n03888257' \
     --input 'data/raw/val/n03888257' \
     --output 'data/train.csv' \
     --output 'data/test.csv' \
     "python3 code/prepare.py"

Beyond the script execution and container name (``-n/--container-name``), this command can take a human readable commit message to summarize the operation (``-m/--message``) and input and output specifications (``-i/--input``, ``-o/--output``).
DataLad will make sure to retrieve everything labeled as ``--input`` prior to running the command, and specifying ``--output`` ensures that the files can be updated should the command be reran at a later point [#f4]_.
It saves the results of this command together with a machine-readable run-record into the dataset history.

Next, the first model can be trained.


.. runrecord:: _examples/ml-111
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ cat << EOT > code/train.py
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
       sgd = SGDClassifier(max_iter=10)
       trained_model = sgd.fit(train_data, labels)
       dump(trained_model, repo_path / "model.joblib")


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT

This script trains a stochastic gradient descent classifier on the training data.
The files in the ``train.csv`` file a read, preprocessed into the same shape, and an SGD model is fitted to the predict the image labels from the data.
The trained model is then saved into a ``model.joblib`` file -- this allows to transparently cache the classifier as a Python object to disk.
Later, `the cached model can be applied to various data with the need to retrain the classifier <https://scikit-learn.org/stable/modules/model_persistence.html>`_.
Let's save the script.

.. runrecord:: _examples/ml-112
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ datalad save -m "Add SGD classification script" code/train.py

The last analysis step needs to test the trained classifier.
We will use the following script for this:

.. runrecord:: _examples/ml-113
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ cat << EOT > code/evaluate.py

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

It will load the trained and dumped model and use it to test its prediction performance on the yet unseen test data.
To evaluate the model performance, it calculates the accuracy of the prediction, i.e., the proportion of correctly labeled images, prints it to the terminal, and saves it into a json file in the superdataset.
As this script constitutes the last analysis step, let's save it with a :term:`tag`.
Its entirely optional to do this, but just as commit messages are an easier way for humans to get an overview of a commits contents, a tag is an easier way for humans to identify a change than a commit hash.
With this script set up, we're ready for analysis, and thus can tag this state ``ready4analysis`` to identify it more easily later.

.. runrecord:: _examples/ml-114
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ datalad save -m "Add script to evaluate model performance" --version-tag "ready4analysis" code/evaluate.py

Afterwards, we can train the first model:

.. runrecord:: _examples/ml-115
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project
   :realcommand: datalad containers-run -n software -m "Train an SGD classifier on the data" --input 'data/raw/train/n03445777' --input 'data/raw/train/n03888257' --output 'model.joblib'  "python3 code/train.py" | grep -v '^\(copy\|get\|drop\|add\|delete\)(ok):.*(file)$'

   $ datalad containers-run -n software \
     -m "Train an SGD classifier on the data" \
     --input 'data/raw/train/n03445777' \
     --input 'data/raw/train/n03888257' \
     --output 'model.joblib' \
     "python3 code/train.py"

And finally, we're ready to find out how well the model did and run the last script:

.. runrecord:: _examples/ml-116
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project
   :realcommand:  datalad containers-run -n software -m "Evaluate SGD classifier on test data" --input 'data/raw/val/n03445777' --input 'data/raw/val/n03888257' --output 'accuracy.json' "python3 code/evaluate.py" | grep -v '^\(copy\|get\|drop\|add\|delete\)(ok):.*(file)$'

   $ datalad containers-run -n software \
     -m "Evaluate SGD classifier on test data" \
     --input 'data/raw/val/n03445777' \
     --input 'data/raw/val/n03888257' \
     --output 'accuracy.json' \
     "python3 code/evaluate.py"

Now this initial accuracy isn't yet fully satisfying.
What could have gone wrong?
The model would probably benefit from a few more training iterations for a start.
Instead of 10, the patch below increases the number of iterations to 100.
Note that the code block below does this change with the stream editor :term:`sed` for the sake of automatically executed code in the handbook, but you could also apply this change with a text editor "by hand".

.. runrecord:: _examples/ml-117
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ sed -i 's/SGDClassifier(max_iter=10)/SGDClassifier(max_iter=100)/g' code/train.py

Here's what has changed:

.. runrecord:: _examples/ml-118
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ git diff

Let's save the change...

.. runrecord:: _examples/ml-119
   :language: console
   :cast: usecase_ml
   :workdir: usecases/ml-project

   $ datalad save -m "Increase the amount of iterations to 100" --version-tag "SGD-100" code/train.py

... and try again.

As we need to retrain the classifier and re-evaluate its performance, we rerun every run-record between the point in time we created the ``SGD`` tag and now.
This will update both the ``model.joblib`` and the ``accuracy.json`` files, but their past versions are still in the dataset history.
One was to do this is to specify a range between the two tags, but likewise, commit hashes would work, or a specification using ``--since`` [#f5]_.

.. runrecord:: _examples/ml-130
   :workdir: usecases/ml-project
   :cast: usecase_ml
   :language: console

   $ datalad rerun -m "Recompute classification with more iterations" ready4analysis..SGD-100

Any better? Mhh, not so much. Maybe a different classifier does the job better.
Let's switch from SGD to a `random forest classification <https://en.wikipedia.org/wiki/Random_forest>`_.
The code block below writes the relevant changes (highlighted) into the script.

.. runrecord:: _examples/ml-131
   :workdir: usecases/ml-project
   :language: console
   :cast: usecase_ml
   :emphasize-lines: 11, 39-40

   $ cat << EOT >| code/train.py
   #!/usr/bin/env python3

   from joblib import dump
   from pathlib import Path

   import numpy as np
   import pandas as pd
   from skimage.io import imread_collection
   from skimage.transform import resize
   from sklearn.ensemble import RandomForestClassifier

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
       rf = RandomForestClassifier()
       trained_model = rf.fit(train_data, labels)
       dump(trained_model, repo_path / "model.joblib")

   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT

We need to save this change:

.. runrecord:: _examples/ml-132
   :workdir: usecases/ml-project
   :cast: usecase_ml
   :language: console

   $ datalad save -m "Switch to random forest classification" --version-tag "random-forest" code/train.py

And now we can retrain and reevaluate again.
This time, in order to have very easy access to the trained models and results of the evaluation, we're rerunning the sequence of run-records in a new :term:`branch` [#f6]_.
This way, we have access to a trained random-forest model or a trained SGD model or their respective results by simply switching branches.

.. runrecord:: _examples/ml-133
   :workdir: usecases/ml-project
   :cast: usecase_ml
   :language: console

   $ datalad rerun --branch="randomforest" -m "Recompute classification with random forest classifier" ready4analysis..SGD-100

This updated the model.joblib file to a trained random forest classifier, and also updated ``accuracy.json`` with the current models' evaluation.
The difference in accuracy between models could now for example be compared with a ``git diff`` of the contents of ``accuracy.json`` to the :term:`master` :term:`branch`:

.. runrecord:: _examples/ml-134
   :workdir: usecases/ml-project
   :cast: usecase_ml
   :language: console

   $ git diff master -- accuracy.json

And if you decide to rather do more work on the SGD classier, you can go back to the previous :term:`master` :term:`branch`:

.. runrecord:: _examples/ml-135
   :workdir: usecases/ml-project
   :cast: usecase_ml
   :language: console

   $ git checkout master
   $ cat accuracy.json

Your Git history becomes a log of everything you did as well as the chance to go back to and forth between analysis states.
And this is not only useful for yourself, but it makes your analyses and results also transparent to others that you share your dataset with.
If you cache your trained models, there is no need to retrain them when traveling to past states of your dataset.
And if any aspect of your dataset changes -- from changes to the input data to changes to your trained model or code -- you can rerun these analysis stages automatically.
The attached software container makes sure that your analysis will always be rerun in the correct software environment, even if the dataset is shared with collaborators with systems that lack a Python installation.


References
^^^^^^^^^^

The analysis is adapted from the chapter :ref:`dvc`, which in turn is based on `this tutorial at RealPython.org <https://realpython.com/python-data-version-control/>`_.

.. rubric:: Footnotes

.. [#f1] You can install the ``datalad-containers`` extension from :term:`pip` via ``pip install datalad-container``. You can find out more about extensions in general in the section :ref:`extensions_intro`, and you can more computationally reproducible analysis using ``datalad container`` in the chapter :ref:`containersrun` and the usecase :ref:`usecase_reproduce_neuroimg`.

.. [#f2] Unsure how to create a :term:`virtual environment`? You can find a tutorial using :term:`pip` and the ``virtualenv`` module `in the Python docs <https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/>`_.

.. [#f3] To re-read about :term:`run procedure`\s, check out section :ref:`procedures`.

.. [#f4] The chapter :ref:`chapter_run` introduces the options of ``datalad run`` and demonstrates their use. Note that ``--output``\s don't need to be individual files, but could also be directories or :term:`globbing` terms.

.. [#f5] In order to re-execute any run-record in the last five commits, you could use ``--since=HEAD~5``, for example. You could also, however, rerun the previous run commands sequentially, with ``datalad rerun <commit-hash>``.

.. [#f6] Rerunning on a different :term:`branch` is optional but handy. Alternatively, you could checkout a previous state in the datasets history to get access to a previous version of a file, reset the dataset to a previous state, or use commands like :command:`git cat-file` to read out a non-checked-out file. The section :ref:`history` summarizes a number of common Git operations to interact with the dataset history.
