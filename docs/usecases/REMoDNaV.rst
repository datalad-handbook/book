****************************
Writing a reproducible paper
****************************
.. todo::
   This title should be changed to something more catchy


Summary
^^^^^^^
This use case demonstrates how to use nested Datalad datasets to create a fully
reproducible paper by linking

#. (different) data sources with
#. the code needed to compute results and
#. LaTeX files to compile the resulting paper.

The different components each exist in individual Datalad datasets and are
aggregated into a single :term:`Datalad superdataset`. The resulting superdataset can be publicly
shared, data can effortlessly be obtained on demand by anyone that has the superdataset,
and results and paper can be generated and recomputed everywhere on demand.


The Problem Space
^^^^^^^^^^^^^^^^^
Over the past year, Steve worked on the implementation of an algorithm as a software package.
For testing purposes, he used one of his own data sets, and later also included a publicly shared
data set. After completion, he continued to work on validation analyses to
prove the functionality and usefulness of his software. Next to a directory in which he developed
his code, and directories with data he tested his code on, he now also has other directories
with different data sources used for validation analyses.
"This can't take too long!" Steve thinks optimistically when he finally sits down to write up a paper.

His scripts run his algorithm on the different data sets, create derivates of his raw data,
pretty figures, and impressive tables.
Just after he hand-copies and checks the last decimal of the final result in the very
last table of his manuscript, he realizes that the script specified the wrong parameter
values, and all of the results need to be recomputed - and obviously updated in his manuscript.
When writing the discussion, he finds a paper that reports an error in the publicly shared
data set he uses. After many more days of updating tables and fixing data columns
by hand, he finally submits the paper. Trying to stand with his values of
open and reproducibile science, he struggles to bundle all scripts, algorithm code, and data
he used in a shareable form, and frankly, with all the extra time this manuscript took
him so far, he lacks motivation and time. In the end, he writes a three page long README
file in his Github code repository, includes his email for data requests, and
secretly hopes that no-one will want to recompute his results, because by now even he
himself forgot which script ran on which dataset and what data was fixed in which way,
or whether he was careful enough to copy all of the results correctly. In the review process,
reviewer 2 demands that the figures his software produces need to get a new color scheme,
which requires updates in his software package, and more recomputations.


The Datalad World
^^^^^^^^^^^^^^^^^
Steve sets up a datalad dataset and calls it ``algorithm-paper``. In this
dataset, he creates several subdirectories to collate everything that is relevant for
the manuscript: Data, code, a manuscript backbone without results.
``code/`` contains a Python script that he uses for validation analyses, and
prior to computing results, the script
attempts to download the data should the files need to be obtained using Datalads Python API.
``data/`` contains a seperate datalad subdataset for every dataset he uses. An
``algorithm/`` directory is a datalad dataset containing a clone of his software repository,
and within it, in the directory ``test/data``, are additional datalad subdatasets that
contain the data he used for testing.
Lastly, the Datalad superdataset contains a ``LaTeX`` ``.tex`` file with the text of the manuscript.
When everything is set up, a single command line call triggers (optional) data retrieval
from Github repositories the data sets were published to, computation of
results and figures, automatic embedding of results and figures into his manuscript
upon computation, and PDF compiling.
When he notices the error in his script, his manuscript is recompiled and updated in under
five minutes, and when he learns about the data error, he updates the respective datalad dataset
to the fixed state while preserving the history of the data repository.


He makes his superdataset a public repository on Github, and anyone who clones it can obtain the
data automatically and recompute and recompile the full manuscript with all results.
Steve never had more confidence in his research results and proudly submits his manuscript.
During review, the color scheme update in his algorithm sourcecode is integrated with a simple
update of the ``algorithm/`` subdataset, and upon command-line invocation his manuscript updates
itself with the new figures.


.. note::
   The actual manuscript this use case is based on can be found
   `here <https://github.com/psychoinformatics-de/paper-remodnav/>`_:
   https://github.com/psychoinformatics-de/paper-remodnav/. ``datalad install``
   the repository and follow the few instructions in the README to experience the
   Datalad world described above.


Step-by-Step
^^^^^^^^^^^^

``datalad create`` a Datalad dataset (in this example, it is named "algorithm-paper"):

.. code-block:: bash

   % datalad create algorithm-paper

   [INFO   ] Creating a new annex repo at /home/adina/repos/testing/algorithm-paper
   create(ok): /home/adina/repos/testing/algorithm-paper (dataset)

Enter this newly created directory:

.. code-block:: bash

   % cd algorithm-paper

Create subdirectories (``code/`` and ``data/``) to give your dataset a comprehensible structure:

.. code-block:: bash

   % mkdir code data

You can checkout the directory structure with the tree command

.. code-block:: bash

   % tree
   algorithm-paper
   ├── code
   └── data

All of your analyses scripts should live in the ``code/`` directory, and all data should
live in the ``data/`` directory. It is important to reference datafiles with the scripts in
``code/`` as a :term:`relative path` to ensure that the scripts also run on somebody elses
file system.

Lets start to populate our Datalad dataset. Add all the
data sets you want to perform analyses on as individual :term:`datalad subdataset` within
``data/``.
Data sets that are already git repositories (for example if they are hosted on Github)
can be ``datalad install``-ed:

.. code-block:: bash

   % cd data
   # install existing git repositories with data (-s specifies the source, in this case, Github repositories)
   datalad install -s https://github.com/richardandersson/EyeMovementDetectorEvaluation.git

   [INFO   ] Cloning https://github.com/richardandersson/EyeMovementDetectorEvaluation.git [1 other candidates] into '/home/adina/repos/testing/algorithm-paper/data/EyeMovementDetectorEvaluation'
   install(ok): /home/adina/repos/testing/algorithm-paper/data/EyeMovementDetectorEvaluation (dataset)

   % datalad install -s git@github.com:psychoinformatics-de/studyforrest-data-eyemovementlabels.git

   [INFO   ] Cloning git@github.com:psychoinformatics-de/studyforrest-data-eyemovementlabels.git into '/home/adina/repos/testing/algorithm-paper/data/studyforrest-data-eyemovementlabels'
   Cloning (compressing objects):  45%|▍| 1.80k/4.00k [00:01<00:01, 1.29k objects/s
   [...]

For data sets that are not (yet) git repositories, one can simply create Datalad subdatasets,
add the data, and ``datalad save`` this subdataset:

.. code-block:: bash

   # for data that does not yet live in a git repository, create a new dataset and add the data to it
   % datalad create additional_data
   # copy your data into this dataset ("cp -r" copies a directories recursively)
   % cp -r /home/adina/data/mystudy additional_data
   # enter the subdataset and save its current state. Make sure to give it an informative commit message with -m
   % cd additional_data
   % datalad save . -m "added the data from my study on xyz"


Each of these datasets now has their own history, and the superdataset only records the states the
subdatasets are in. If you navigate into any of these subdatasets, a log-tool of your choice (``git log``,
:term:`tig`, :term:`gitk`, ...) can display this Datalad datasets history:

.. code-block:: bash

   # navigate into the specific subdataset
   % cd data/studyforrest-data-eyemovementlabels
   # display history, e.g. with git log
   % git log
   commit 92279db3850ee4282d97001a3f650fc55cb64b4e (HEAD, medusa/synced/master)
   Author: Adina Wagner <adina.wagner@t-online.de>
   Date:   Tue Apr 23 15:03:21 2019 +0200

      update remodnav to release v0.2

   commit a5a75ff673dfe091345ed0a734bdb417e64eb96e
   Author: Adina Wagner <adina.wagner@t-online.de>
   Date:   Tue Apr 23 15:02:34 2019 +0200

      minor cleanup: delete obsolete figures


Any script we need for the analysis should live inside ``code/``. The changes to these files you want
to record in your history can be ``datalad save`` -d

.. code-block:: bash

   # lets say you fixed a bug in your script. Datalad status can tell you if modifications are present
   % datalad status
   modified: code/mk_figuresnstats.py

   # save these changes to your history with datalad save and a meaningful message
   % datalad save code/mk_figuresnstats.py -m "Bugfix: make path relative"

Whats missing still is the software repository. This already lives on Github, and can hence also be
``datalad install`` -ed in the root of the subdataset.

.. code-block:: bash

   % datalad install -s git@github.com:psychoinformatics-de/remodnav.git

This repository has also subdatasets in which the datasets used for testing live (``tests/data/``):

.. code-block:: bash

       ├── remodnav
   │   ├── clf.py
   │   ├── __init__.py
   │   ├── __main__.py
   │   └── tests
   │       ├── data
   │       │   ├── anderson_etal
   │       │   └── studyforrest


This ``algorithm-paper`` superdataset is already making research life easy.

tbc...

