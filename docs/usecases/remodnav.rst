.. _remodnav:

****************************
Writing a reproducible paper
****************************
.. todo::
   This title should be changed to something more catchy


Summary
^^^^^^^
This use case demonstrates how to use nested DataLad datasets to create a fully
reproducible paper by linking

#. (different) DataLad dataset sources with
#. the code needed to compute results and
#. LaTeX files to compile the resulting paper.

The different components each exist in individual DataLad datasets and are
aggregated into a single :term:`DataLad superdataset`. The resulting superdataset can be publicly
shared, data can effortlessly be obtained on demand by anyone that has the superdataset,
and results and paper can be generated and recomputed everywhere on demand.


The Problem Space
^^^^^^^^^^^^^^^^^
Over the past year, Steve worked on the implementation of an algorithm as a software package.
For testing purposes, he used one of his own data collections, and later also included a publicly shared
data collection. After completion, he continued to work on validation analyses to
prove the functionality and usefulness of his software. Next to a directory in which he developed
his code, and directories with data he tested his code on, he now also has other directories
with different data sources used for validation analyses.
"This can't take too long!" Steve thinks optimistically when he finally sits down to write up a paper.


His scripts run his algorithm on the different data collections, create derivates of his raw data,
pretty figures, and impressive tables.
Just after he hand-copies and checks the last decimal of the final result in the very
last table of his manuscript, he realizes that the script specified the wrong parameter
values, and all of the results need to be recomputed - and obviously updated in his manuscript.
When writing the discussion, he finds a paper that reports an error in the publicly shared
data collection he uses. After many more days of updating tables and fixing data columns
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


The DataLad World
^^^^^^^^^^^^^^^^^
Steve sets up a DataLad dataset and calls it ``algorithm-paper``. In this
dataset, he creates several subdirectories to collate everything that is relevant for
the manuscript: Data, code, a manuscript backbone without results.
``code/`` contains a Python script that he uses for validation analyses, and
prior to computing results, the script
attempts to download the data should the files need to be obtained using DataLads Python API.
``data/`` contains a seperate DataLad subdataset for every dataset he uses. An
``algorithm/`` directory is a DataLad dataset containing a clone of his software repository,
and within it, in the directory ``test/data/``, are additional DataLad subdatasets that
contain the data he used for testing.
Lastly, the DataLad superdataset contains a ``LaTeX`` ``.tex`` file with the text of the manuscript.
When everything is set up, a single command line call triggers (optional) data retrieval
from Github repositories of the datasets, computation of
results and figures, automatic embedding of results and figures into his manuscript
upon computation, and PDF compiling.
When he notices the error in his script, his manuscript is recompiled and updated
with a single command line call in under
five minutes, and when he learns about the data error, he updates the respective DataLad dataset
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
   DataLad world described above.


Step-by-Step
^^^^^^^^^^^^

``datalad create`` a DataLad dataset (in this example, it is named "algorithm-paper"):

.. code-block:: bash

   $ datalad create algorithm-paper

   [INFO   ] Creating a new annex repo at /home/adina/repos/testing/algorithm-paper
   create(ok): /home/adina/repos/testing/algorithm-paper (dataset)

Enter this newly created directory and
create subdirectories (``code/`` and ``data/``) to give your dataset a comprehensible structure:

.. code-block:: bash

   $ cd algorithm-paper
   $ mkdir code data

   # You can checkout the directory structure with the tree command

   $ tree
   algorithm-paper
   ├── code
   └── data

All of your analyses scripts should live in the ``code/`` directory, and all data should
live in the ``data/`` directory.

To populate the DataLad dataset, add all the
data collections you want to perform analyses on as individual DataLad subdatasets within
``data/``.
In this example, all data collections are already DataLad datasets or git repositories and hosted on Github.
``datalad install`` therefore installs them as subdatasets:

.. code-block:: bash

   $ cd data
   # install existing git repositories with data (-s specifies the source, in this case, Github repositories)
   datalad install -s https://github.com/psychoinformatics-de/studyforrest-data-phase2.git

   [INFO   ] Cloning https://github.com/psychoinformatics-de/studyforrest-data-phase2.git [1 other candidates] into '/home/adina/repos/testing/algorithm-paper/data/raw_eyegaze'
   install(ok): /home/adina/repos/testing/algorithm-paper/data/raw_eyegaze (dataset)

   $ datalad install -s git@github.com:psychoinformatics-de/studyforrest-data-eyemovementlabels.git

   [INFO   ] Cloning git@github.com:psychoinformatics-de/studyforrest-data-eyemovementlabels.git into '/home/adina/repos/testing/algorithm-paper/data/studyforrest-data-eyemovementlabels'
   Cloning (compressing objects):  45% 1.80k/4.00k [00:01<00:01, 1.29k objects/s
   [...]

Any script we need for the analysis should live inside ``code/``. During script writing, save any changes
to you want to record in your history with ``datalad save``.

The eventual outcome of this work is a Github repository that anyone can use to get the data
and recompute all results
when running the script after cloning and setting up the necessary software.
This requires minor preparation:

* The final analysis should be able to run on anyone's filesystem. It is therefore important to reference datafiles with the scripts in ``code/`` as a :term:`relative path` instead of hard-coding absolute paths.

* After cloning the ``algorithm-paper`` repository, data files are not yet present locally. To spare users the work of a manual ``datalad get``, you can have your script take care of data retrieval

These two preparations can be seen in this excerpt from the Python script:

.. code-block:: python

   # import Datalads API
   from datalad.api import get

   # note that the datapath is relative
   datapath = op.join('data',
                      'studyforrest-data-eyemovementlabels',
                      'sub*',
                      '*run-2*.tsv')
   data = sorted(glob(datapath))

   # this will get the data if it is not yet retrieved
   get(dataset='.', path=data)


Lastly, ``datalad install`` the software repository as a subdataset in the root of the superdataset.

.. code-block:: bash

   # in the root of ``algorithm-paper`` run
   $ datalad install -s git@github.com:psychoinformatics-de/remodnav.git

This repository has also subdatasets in which the datasets used for testing live (``tests/data/``):

.. code-block:: bash

   $ tree
   [...]

   |   ├── remodnav
   │   ├── clf.py
   │   ├── __init__.py
   │   ├── __main__.py
   │   └── tests
   │       ├── data
   │       │   ├── anderson_etal
   │       │   └── studyforrest


At this stage, a public ``algorithm-paper`` repository shares code and data, and changes to any
dataset can easily be handled by updating the respective subdataset.

.. todo::

   The non-Datalad part is very unrelated to DataLad and also not trivial. Nevertheless,
   I bet that this is a very exciting part for anyone who compiled the paper, and at least
   useful to include with some sort of disclaimer that this is an "add-on" and requires
   some understanding of LaTeX, Python, Makefiles, ...

To go beyond that and include freshly computed results in a manuscript on the fly does not
require DataLad anymore, only some ``LaTeX`` and Makefiles. As with most things,
its a surprisingly simple challenge if one has just seen how to do it once.
The main advantage of this method as opposed to for example Jupyter Notebooks
is that the result will be a PDF, and thus a standard format for paper submission.
In principle, the challenge boils down to:

* have the script output results (only requires ``print()`` statements)

* capture these results automatically (done with a single line of Unix commands)

* embed the captured results in the PDF (done with one line in the ``.tex`` file and some clever referencing)

* automate as much as possible to keep it as simple as possible (done with a Makefile)

Lets start by revealing how this magic trick works. Everything relies on printing
the results in the form of user-defined ``LaTeX`` definitions (the so called
``\newcommand``), referencing those definitions in your manuscript where the
results should end up, and bind the ``\newcommands`` as ``\input{}`` to your ``.tex``
file. But lets get there in small steps.

First, if you want to read up on the ``\newcommand``, please see
`the documentation <https://en.wikibooks.org/wiki/LaTeX/Macros>`_.
The command syntax looks like this:

``\newcommand{\name}[num]{definition}``

What we want to do, expressed in the most human-readable form, is this:

``\newcommand{\Table1Cell1Row1}{0.67}``

where ``0.67`` would be a single result computed by your script.
This requires ``print()`` statements that look like this in the most simple
form (excerpt from script):

.. code-block:: python

   print('\\newcommand{\\maxmclf}{max_mclf}')

where ``max_mclf`` is a variable that stores the value of one computation.

Tables and references to results within the ``.tex`` files then do not contain the
specific value ``0.67`` (this value would change if the data changes, or other parameters),
but ``\maxmclf`` (and similar, unique names for other results).
For full tables, one can come up with naming schemes that make it easy
to fill tables with unique names with minimal work, for example like this:

.. code-block:: tex

   \begin{table}[tbp]
     % table caption is above the table
     \caption{Cohen's Kappa reliability between human coders (MN, RA), and \remodnav\ (AL)
     with each of the human coders.
     }
     \label{tab:kappa}       % Give a unique label
     % For LaTeX tables use
     \begin{tabular*}{0.5\textwidth}{c @{\extracolsep{\fill}}llll}
       \textbf {Fixations}                   &                  &                   &                    \\
       \hline\noalign{\smallskip}
       Comparison                            & Images           & Dots              & Videos             \\
       \noalign{\smallskip}\hline\noalign{\smallskip}
       MN versus RA                          & \kappaRAMNimgFix & \kappaRAMNdotsFix & \kappaRAMNvideoFix \\
       AL versus RA                          & \kappaALRAimgFix & \kappaALRAdotsFix & \kappaALRAvideoFix \\
       AL versus MN                          & \kappaALMNimgFix & \kappaALMNdotsFix & \kappaALMNvideoFix \\
       \noalign{\smallskip}
       \textbf{Saccades}                     &                  &                   &                    \\
       \hline\noalign{\smallskip}
       Comparison                            & Images           & Dots              & Videos             \\
       \noalign{\smallskip}\hline\noalign{\smallskip}
       MN versus RA                          & \kappaRAMNimgSac & \kappaRAMNdotsSac & \kappaRAMNvideoSac \\
       AL versus RA                          & \kappaALRAimgSac & \kappaALRAdotsSac & \kappaALRAvideoSac \\
       AL versus MN                          & \kappaALMNimgSac & \kappaALMNdotsSac & \kappaALMNvideoSac \\
       \noalign{\smallskip}
       \textbf{PSOs}                         &                  &                   &                    \\
       \hline\noalign{\smallskip}
       Comparison                            & Images           & Dots              & Videos             \\
       \noalign{\smallskip}\hline\noalign{\smallskip}
       MN versus RA                          & \kappaRAMNimgPSO & \kappaRAMNdotsPSO & \kappaRAMNvideoPSO \\
       AL versus RA                          & \kappaALRAimgPSO & \kappaALRAdotsPSO & \kappaALRAvideoPSO \\
       AL versus MN                          & \kappaALMNimgPSO & \kappaALMNdotsPSO & \kappaALMNvideoPSO \\
       \noalign{\smallskip}\hline
     \end{tabular*}
   \end{table}

``print()`` statements to fill those tables can utilize Pythons string concatenation methods
loops to keep them within a few lines for a full table, such as

.. code-block:: python

   for stim in ['img', 'dots', 'video']:
      for ev in ['Fix', 'Sac', 'PSO']:

      [...]

         for rating, comb in [('RAMN', [RA_res_flat, MN_res_flat]),
                           ('ALRA', [RA_res_flat, AL_res_flat]),
                           ('ALMN', [MN_res_flat, AL_res_flat])]:
            kappa = cohen_kappa_score(comb[0], comb[1])
            label = 'kappa{}{}{}'.format(rating, stim, ev)
            print('\\newcommand{\\%s}{%s}' % (label, '%.2f' % kappa))


Running the python script hence will print plenty of LaTeX commands to your screen (try it out,
if you want!). Those statements just need to be captured, and bound to the ``.tex`` file of your
script.

The `tee <https://en.wikipedia.org/wiki/Tee_(command)>`_ command can write all of the output to
a file (called ``results_def.tex``):

.. code-block:: python

   code/mk_figuresnstats.py -s | tee results_def.tex

One can include this file as an input source into the ``.tex`` file with

.. code-block:: tex

   \begin{document}
   \input{results_def.tex}

Upon compilation of the ``.tex`` file into a PDF, the results of the computations captured with
``\newcommand`` definitions are inserted into the respective part of the manuscript.

To automate this process, `Makefiles <https://en.wikipedia.org/wiki/Make_(software)>`_ can help.

tbc...
