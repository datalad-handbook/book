.. _usecase_collab:

A typical collaborative data management workflow
------------------------------------------------

This use case sketches the basics of a common, collaborative
data management workflow for an analysis:

#. A 3rd party dataset is obtained to serve as input for an analysis.
#. Data processing is collaboratively performed by two colleagues.
#. Upon completion, the results are published alongside the original data
   for further consumption.

The data types and methods mentioned in this usecase belong to the scientific
field of neuroimaging, but the basic workflow is domain-agnostic.

The Challenge
^^^^^^^^^^^^^

Bob is a new PhD student and about to work on his first analysis.
He wants to use an open dataset as the input for his analysis, so he asks
a friend who has worked with the same dataset for the data and gets it
on a hard drive.
Later, he's stuck with his analysis. Luckily, Alice, a senior grad
student in the same lab, offers to help him. He sends his script to
her via email and hopes she finds the solution to his problem. She
responds a week later with the fixed script, but in the meantime
Bob already performed some miscellaneous changes to his script as well.
Identifying and integrating her fix into his slightly changed script
takes him half a day. When he finally finishes his analysis, he wants to
publish code and data online, but can not find a way to share his data
together with his code.


The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Bob creates his analysis project as a DataLad dataset. Complying with
the `YODA principles <http://handbook.datalad.org/en/latest/basics/101-123-yoda.html>`_,
he creates his scripts in a dedicated
``code/`` directory, and installs the open dataset as a standalone
DataLad subdataset within a dedicated subdirectory.
To collaborate with his senior grad
student Alice, he shares the dataset on the lab's SSH server, and they
can collaborate on the version controlled dataset almost in real time
with no need for Bob to spend much time integrating the fix that Alice
provides him with. Afterwards, Bob can execute his scripts in a way that captures
all provenance for this results with a :command:`datalad run` command.
Bob can share his whole project after completion by creating a sibling
on a webserver, and pushing all of his dataset, including the input data,
to this sibling, for everyone to access and recompute.

Step-by-Step
^^^^^^^^^^^^

Bob creates a DataLad dataset for his analysis project to live in.
Because he knows about the YODA principles, he configures the dataset
to be a YODA dataset right at the time of creation:

.. runrecord:: _examples/collab-101
   :workdir: usecases/collab
   :language: console

   $ datalad create -c yoda --description "my 1st phd project on work computer" myanalysis

After creation, there already is a ``code/`` directory, and all of its
inputs are version-controlled by :term:`Git` instead of :term:`Git-annex`
thanks to the yoda procedure:

.. runrecord:: _examples/collab-102
   :workdir: usecases/collab
   :language: console

   $ cd myanalysis
   $ tree

Bob knows that a DataLad dataset can contain other datasets. He also knows that
as any content of a dataset is tracked and its precise state is recorded,
this is a powerful method to specify and later resolve data dependencies,
and that including the dataset as a standalone data component will it also
make it easier to keep his analysis organized and share it later.
The dataset that Bob wants to work with is structural brain imaging data from the
`studyforrest project <http://studyforrest.org/>`_, a public
data resource that the original authors share as a DataLad dataset through
:term:`Github`. This means that Bob can simply install the relevant dataset from this
service and into his own dataset. To do that, he installs it as a subdataset
into a directory he calls ``src/`` as he wants to make it obvious which parts
of his analysis steps and code require 3rd party data:

.. runrecord:: _examples/collab-103
   :workdir: usecases/collab/myanalysis
   :language: console

   $ datalad install -d . --source https://github.com/psychoinformatics-de/studyforrest-data-structural.git src/forrest_structural

Now that he executed this command, Bob has access to the entire dataset
content, and the precise version of the dataset got linked to his top-level dataset
``myanalysis``. However, no data was actually downloaded (yet). Bob very much
appreciates that DataLad datasets primarily contain information on a dataset’s
content and where to obtain it: the installation above was done rather
quickly, and will still be relatively lean even for a dataset that contains
several hundred GBs of data. He knows that his script can obtain the
relevant data he needs on demand if he wraps it into a :command:`datalad run`
command and therefore does not need to care about getting the data yet. Instead,
he focuses to write his script ``code/run_analysis.sh``.
To save this progress, he runs frequent :command:`datalad save` commands:

.. runrecord:: _examples/collab-104
   :workdir: usecases/collab/myanalysis
   :language: console
   :realcommand: echo "#! /usr/bin/env python" > code/run_analysis.py && datalad save -m "First steps: start analysis script" code/run_analysis.py

   $ datalad save -m "First steps: start analysis script" code/run_analysis.py

Once Bob's analysis is finished, he can wrap it into :command:`datalad run`.
To ease execution, he first makes his script executable by adding a :term:`shebang`
that specifies Python as an interpreter at the start of his script, and giving it
executable permissions:

.. runrecord:: _examples/collab-105
   :workdir: usecases/collab/myanalysis
   :language: console

   $ chmod +x code/run_analysis.py
   $ datalad save -m "make script executable"

Importantly, prior to a :command:`datalad run`, he specifies the necessary
inputs such that DataLad can take care of the data retrieval for him:

.. runrecord:: _examples/collab-106
   :workdir: usecases/collab/myanalysis
   :language: console
   :realcommand: datalad run -m "run first part of analysis workflow" --input "src/forrest_structural/sub-01/anat/sub-01_T1w.nii.gz" --output results.txt "code/run_analysis.py"

   $ datalad run -m "run first part of analysis workflow" \
     --input "src/forrest_structural" \
     --output results.txt \
     "code/run_analysis.py"

This will take care of retrieving the data, running Bobs script, and
saving all outputs.

Some time later, Bob needs help with his analysis. He turns to his senior
grad student Alice for help. Alice and Bob both work on the same computing server.
Bob has told Alice in which directory he keeps his analysis dataset, and
the directory is configured to have permissions that allow for
read-access for all lab-members, so Alice can obtain Bob’s work directly
from his home directory:

.. runrecord:: _examples/collab-107
   :workdir: usecases/collab
   :language: console
   :realcommand: echo "$ datalad install -r --source "$BOBS_HOME/myanalysis" bobs_analysis" && datalad install -r --source "myanalysis" bobs_analysis

.. runrecord:: _examples/collab-108
   :workdir: usecases/collab
   :language: console
   :realcommand: cd bobs_analysis && echo "some contribution" >> code/run_analysis.py && datalad save

   $ cd bobs_analysis
   # ... make contributions, and save them
   $ [...]
   $ datalad save -m "your welcome, bob"


Alice can get the studyforrest data Bob used as an input as well as the
result file, but she can also rerun his analysis by using :command:`datalad rerun`.
She goes ahead and fixes Bobs script, and saves the changes. To integrate her
changes into his dataset, Bob registers Alice's dataset as a sibling:

.. runrecord:: _examples/collab-109
   :workdir: usecases/collab/myanalysis
   :language: console
   :realcommand: echo "$ datalad siblings add -s alice --url '$ALICES_HOME/bobs_analysis'" && datalad siblings add -s alice --url '../bobs_analysis'

   #in Bobs home directory

Afterwards, he can get her changes with a :command:`datalad update --merge`
command:


.. runrecord:: _examples/collab-110
   :workdir: usecases/collab/myanalysis
   :language: console

   $ datalad update -s alice --merge


Finally, when Bob is ready to share his results with the world or a remote
collaborator, he makes his dataset available by uploading them to a webserver
via SSH. Bob does so by creating a sibling for the dataset on the server, to
which the dataset can be published and later also updated.

.. code-block:: bash

    # this generated sibling for the dataset and all subdatasets
    $ datalad create-sibling --recursive -s public "$SERVER_URL"

Once the remote sibling is created and registered under the name “public”,
Bob can publish his version to it.

.. code-block:: bash

    $ datalad publish -r --to public .

This workflow allowed Bob to obtain data, collaborate with Alice, and publish
or share his dataset with others easily -- he cannot wait for his next project,
given that this workflow made his life so simple.
