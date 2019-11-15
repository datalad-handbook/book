.. _usecase_reproduce_neuroimg:

An automatically reproducible analysis of public neuroimaging data
------------------------------------------------------------------

This use case sketches the basics of an analysis that can be
automatically reproduced by anyone:

#. Public open data stems from :term:`the DataLad superdataset ///`.
#. Automatic data retrieval can be ensured by using DataLad's
   commands in the analysis scripts, or the ``--input`` specification of
   :command:`datalad run`,
#. Analyses are executed using :command:`datalad run` and
   :command:`datalad rerun` commands to capture everything relevant to
   reproduce the analysis.
#. The final dataset can be kept as lightweight as possible by dropping input
   that can be easily re-obtained.
#. A complete reproduction of the computation (including input retrieval),
   is possible with a single :command:`datalad rerun` command.

This use case is a specialization of :ref:`usecase_reproducible_paper`:
It is a data analysis that requires and creates large data files,
uses specialized analysis software, and is fully automated using solely
DataLad commands and tools.
While exact data types, analysis methods, and software mentioned
in this use case belong to the scientific field of neuroimaging, the
basic workflow is domain-agnostic.


The Challenge
^^^^^^^^^^^^^

Creating reproducible (scientific) analyses seems to require so much:
One needs to share data, scripts, results, and instructions on how to
use data and scripts to obtain the results.
A researcher at any stage of their career can struggle to remember
which script needs to be run in which order,
or to create comprehensible instructions for others
on where and how to obtain data and how to run which script
at what point in time.
This leads to failed replications, a loss of confidence in results,
and major time requirements for anyone trying to reproduce others
or even their own analyses.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Scientific studies should be reproducible, and with the increasing accessibility
of data, there is not much excuse for a lack of reproducibility anymore.
DataLad can help with the technical aspects of reproducible science.

For neuroscientific studies, :term:`the DataLad superdataset ///` provides unified
access to a large amount of data. Using it to install datasets into an
analysis-superdataset makes it easy to share this data together with the analysis.
By ensuring that all relevant data is downloaded via :command:`datalad get`
via DataLad's command line tools in the analysis scripts, or ``--input`` specifications
in a :command:`datalad run`, an analysis can retrieve all required
inputs fully automatically during execution.
Recording executed commands with :command:`datalad run` allows to rerun
complete analysis workflows with a single command, even if input data does not exist
locally. Combining these three steps allows to share fully automatically reproducible
analyses as lightweight datasets.

Step-by-Step
^^^^^^^^^^^^

It always starts with a dataset:

.. runrecord:: _examples/repro-101
   :language: console
   :workdir: usecases/repro

   $ datalad create -c yoda demo

For this demo we are using two public brain imaging datasets that were published on
`OpenFMRI.org <https://legacy.openfmri.org/>`_, and are available from
:term:`the DataLad superdataset ///` (datasets.datalad.org). When installing datasets
from this superdataset, we can use its abbreviation ``///``.
The two datasets, `ds000001 <https://legacy.openfmri.org/dataset/ds000001/>`_ and
`ds000002 <https://legacy.openfmri.org/dataset/ds000002/>`_, are installed into the
subdirectory ``inputs/``.

.. runrecord:: _examples/repro-102
   :language: console
   :workdir: usecases/repro

   $ cd demo
   $ datalad install -d . -s ///openfmri/ds000001 inputs/ds000001

.. runrecord:: _examples/repro-103
   :language: console
   :workdir: usecases/repro

   $ cd demo
   $ datalad install -d . -s ///openfmri/ds000002 inputs/ds000002

Both datasets are now registered as subdatasets, and their precise versions
(e.g. in the form of the commit shasum of the lastest commit) are on record:

.. runrecord:: _examples/repro-104
   :language: console
   :workdir: usecases/repro/demo

   $ datalad --output-format '{path}: {gitshasum}' subdatasets

DataLad datasets are fairly lightweight in size, they only contain
pointers to data and history information in their minimal form.
Thus, so far very little data were actually downloaded:

.. runrecord:: _examples/repro-105
   :language: console
   :workdir: usecases/repro/demo

   $ du -sh inputs/

Both datasets would actually be several gigabytes in size, once the
dataset content gets downloaded:

.. runrecord:: _examples/repro-106
   :language: console
   :workdir: usecases/repro/demo

   $ datalad -C inputs/ds000001 status --annex
   $ datalad -C inputs/ds000002 status --annex

Both datasets contain brain imaging data, and are compliant with the
`BIDS standard <https://bids.neuroimaging.io/>`_.
This makes it really easy to locate particular images
and perform analysis across datasets.

Here we will use a small script that performs ‘brain extraction’ using
`FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSL>`_ as a stand-in for
a full analysis pipeline. The script will be stored inside of the
``code/`` directory that the yoda-procedure created that at the time of
dataset-creation.

.. runrecord:: _examples/repro-107
   :language: console
   :workdir: usecases/repro/demo
   :emphasize-lines: 6

   $ cat << EOT > code/brain_extraction.sh
   # enable FSL
   . /etc/fsl/5.0/fsl.sh

   # obtain all inputs
   datalad get \$@
   # perform brain extraction
   count=1
   for nifti in \$@; do
      subdir="sub-\$(printf %03d \$count)"
      mkdir -p \$subdir
      echo "Processing \$nifti"
      bet \$nifti \$subdir/anat -m
      count=\$((count + 1))
   done
   EOT

Note that this script uses the :command:`datalad get` command which automatically
obtains the required files from their remote source – we will see this in
action shortly.

We are saving this script in the dataset. This way, we will know exactly
which code was used for the analysis. Everything inside of ``code/``
is tracked with Git thanks to the yoda-procedure, so we can see more easily
how it was edited over time. In addition, we will “tag” this state of the
dataset with the tag ``setup_done`` to mark the repository state at which the
analysis script was completed. This is optional, but it can help to identify
important milestones more easily.

.. runrecord:: _examples/repro-108
   :language: console
   :workdir: usecases/repro/demo

   $ datalad save --version-tag setup_done -m "Brain extraction script" code/brain_extraction.sh

Now we can run our analysis code to produce results. However, instead of
running it directly, we will run it with DataLad – this will automatically
create a record of exactly how this script was executed.

For this demo we will just run it on the structural images (T1w) of the first
subject (sub-01) from each dataset.
The uniform structure of the datasets makes this very easy.
Of course we could run it on all subjects; we are simply saving some time for
this demo. While the command runs, you should notice a few things:

1) We run this command with ‘bash -e’ to stop at any failure that may occur

2) You’ll see the required data files being obtained as they are needed – and
   only those that are actually required will be downloaded (because of the
   appropriate ``--input`` specification of the :command:`datalad run` -- but
   as a :command:`datalad get` is also included in the bash script, forgetting
   an ``--input`` specification would not be problem).

.. runrecord:: _examples/repro-109
   :language: console
   :workdir: usecases/repro/demo

   $ datalad run -m "run brain extract workflow" \
     --input "inputs/ds*/sub-01/anat/sub-01_T1w.nii.gz" \
     --output "sub-*/anat" \
     bash -e code/brain_extraction.sh inputs/ds*/sub-01/anat/sub-01_T1w.nii.gz



The analysis step is done, all generated results were saved in the dataset.
All changes, including the command that caused them are on record:

.. runrecord:: _examples/repro-110
   :language: console
   :workdir: usecases/repro/demo

   $ git show --stat

DataLad has enough information stored to be able to re-run a command.

On command exit, it will inspect the results and save them again, but
only if they are different.
In our case, the re-run yields bit-identical results, hence nothing
new is saved.

.. runrecord:: _examples/repro-111
   :language: console
   :workdir: usecases/repro/demo

   $ datalad rerun

Now that we are done, and have checked that we can reproduce the results
ourselves, we can clean up. DataLad can easily verify if any part of our
input dataset was modified since we configured our analysis, using
:command:`datalad diff` and the tag we provided:

.. runrecord:: _examples/repro-112
   :language: console
   :workdir: usecases/repro/demo

   $ datalad diff setup_done inputs

Nothing was changed.

With DataLad with don’t have to keep those inputs around – without losing
the ability to reproduce an analysis.
Let’s uninstall them, and check the size on disk before and after.

.. runrecord:: _examples/repro-113
   :language: console
   :workdir: usecases/repro/demo

   $ du -sh

.. runrecord:: _examples/repro-114
   :language: console
   :workdir: usecases/repro/demo

   $ datalad uninstall inputs/*

.. runrecord:: _examples/repro-115
   :language: console
   :workdir: usecases/repro/demo

   $ du -sh

The dataset is substantially smaller as all inputs are gone…

.. runrecord:: _examples/repro-116
   :language: console
   :workdir: usecases/repro/demo

   $ ls inputs/*

But as these inputs were registered in the dataset when we installed
them, getting them back is very easy.
Only the remaining data (our code and the results) need to be kept and
require a backup for long term archival. Everything else can be
re-obtained as needed, when needed.

As DataLad knows everything needed about the inputs, including where
to get the right version, we can re-run the analysis with a single command.
Watch how DataLad re-obtains all required data, re-runs the code, and checks
that none of the results changed and need saving.

.. runrecord:: _examples/repro-117
   :language: console
   :workdir: usecases/repro/demo

   $ datalad rerun

Reproduced!

This dataset could now be published and shared as a lightweight yet fully
reproducible resource and enable anyone to replicate the exact
same analysis -- with a single command.
Public data and reproducible execution for the win!