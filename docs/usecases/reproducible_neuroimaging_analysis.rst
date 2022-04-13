.. _usecase_reproduce_neuroimg:

An automatically and computationally reproducible neuroimaging analysis from scratch
------------------------------------------------------------------------------------

.. index:: ! Usecase; Reproducible Neuroimaging

This use case sketches the basics of a portable analysis that can be
automatically computationally reproduced, starting from the
acquisition of a neuroimaging dataset with a magnetic resonance imaging (MRI)
scanner up to complete data analysis results:

#. Two extension packages, `datalad-container <https://github.com/datalad/datalad-container>`_
   and `datalad-neuroimaging <https://github.com/datalad/datalad-neuroimaging>`_
   extend DataLad's functionality with the ability to work with computational
   containers and neuroimaging data workflows.
#. The analysis is conducted in a way that leaves comprehensive provenance
   (including software environments) all the way from the raw data, and
   structures study components in a way that facilitates reuse.
#. It starts with preparing a raw data (dicom) dataset, and subsequently uses
   the prepared data for a general linear model (GLM) based analysis.
#. After completion, data and results are archived, and disk usage of the
   dataset is maximally reduced.

This use case is adapted from the
`ReproIn/DataLad tutorial <http://www.repronim.org/ohbm2018-training/03-01-reproin/>`_
by Michael Hanke and Yaroslav Halchenko, given at the 2018 OHBM training course
ran by `ReproNim <https://www.repronim.org/>`_.

The Challenge
^^^^^^^^^^^^^

Allan is an exemplary neuroscientist and researcher. He has spent countless
hours diligently learning not only the statistical methods for his research
questions and the software tools for his computations, but also taught
himself about version control and data standards in neuroimaging, such as
the brain imaging data structure (`BIDS <https://bids.neuroimaging.io/>`_).
For his final PhD project, he patiently acquires functional MRI data of many
participants, and prepares it according to the BIDS standard afterwards.
It takes him a full week of time and two failed attempts, but he
eventually has a `BIDS-compliant <http://bids-standard.github.io/bids-validator/>`_
dataset.

When he writes his analysis scripts he takes extra care to responsibly
version control every change. He happily notices how much cleaner his
directories are, and how he and others can transparently see how his code
evolved. Once everything is set up, he runs his analysis using large and
complex neuroscientific software packages that he installed on his computer a
few years back. Finally, he writes a paper and publishes his findings in a
prestigious peer-reviewed journal. His data and code can be accessed by
others easily, as he makes them publicly available. Colleagues and
supervisors admire him for his wonderful contribution to open science.

However, a few months after publication, Allan starts to get
emails by that report that his scripts do not produce the same
results as the ones reported in the publication. Startled and confused he
investigates what may be the issue. After many sleepless nights he realizes:
The software he used was fairly old! More recent versions of the same
software compute results slightly different, changed function's names, or
fixed discovered bugs in the underlying source code. Shocked, he realizes that
his scripts are even incompatible with the most recent release of the software
package he used and throw an error. Luckily, he can quickly fix this by
adding information about the required software versions to the ``README`` of his
project, and he is grateful for colleagues and other scientists that provide
adjusted versions of his code for more recent software releases. In the end,
his results prove to be robust regardless of software version. But while
Allen shared code and data, not including any information about his *software*
environment prevented his analysis from becoming *computationally*
reproducible.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Even if an analysis workflow is fully captured and version-controlled, and
data and code are being linked, an analysis may not reproduce. Comprehensive
*computational* reproducibility requires that also the *software* involved
in an analysis and its precise versions need to be known.
DataLad can help with this. Using the ``datalad-containers`` extension,
complete software environments can be captured in computational containers,
added to (and thus shared together with) datasets, and linked with commands
and outputs they were used for.

Step-by-Step
^^^^^^^^^^^^

The first part of this Step-by-Step guide details how to computationally
reproducibly and automatically reproducibly perform data preparation from raw
`DICOM <https://www.dicomstandard.org/>`_ files to BIDS-compliant
`NIfTI <https://nifti.nimh.nih.gov/>`_ images. The actual analysis, a
first-level GLM for a localization task, is performed in the second part. A
final paragraph shows how to prepare the dataset for the afterlife.

For this use case, two DataLad extensions are required:

- `datalad-container <https://github.com/datalad/datalad-container>`_ and
- `datalad-neuroimaging <https://github.com/datalad/datalad-neuroimaging>`_

You can install them via ``pip`` like this::

   $ pip install datalad-neuroimaging datalad-container

Data Preparation
""""""""""""""""

We start by creating a home for the raw data:

.. runrecord:: _examples/repro2-101
   :language: console
   :workdir: usecases/repro2

   $ datalad create localizer_scans
   $ cd localizer_scans

For this example, we use a number of publicly available DICOM files. Luckily,
at the time of data acquisition, these DICOMs were already equipped with the
relevant metadata: Their headers contain all necessary information to
identify the purpose of individual scans and encode essential properties to
create a BIDS compliant dataset from them. The DICOMs are stored on Github
(as a Git repository [#f1]_), so they can be installed as a subdataset. As
they are the raw inputs of the analysis, we store them in a directory we call
``inputs/raw``.

.. runrecord:: _examples/repro2-102
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad clone --dataset . \
    https://github.com/datalad/example-dicom-functional.git  \
    inputs/rawdata

The :command:`datalad subdatasets` reports the installed dataset to be indeed
a subdataset of the superdataset ``localizer_scans``:

.. runrecord:: _examples/repro2-103
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad subdatasets

Given that we have obtained *raw* data, this data is not yet ready for data
analysis. Prior to performing actual computations, the data needs to be
transformed into appropriate formats and standardized to an intuitive layout.
For neuroimaging, a useful transformation is a transformation from
DICOMs into the NIfTI format, a format specifically designed for scientific
analyses of brain images. An intuitive layout is the BIDS standard.
Performing these transformations and standardizations, however, requires
software. For the task at hand, `HeudiConv <https://heudiconv.readthedocs.io/en/latest/>`_,
a DICOM converter, is our software of choice. Beyond converting DICOMs, it
also provides assistance in converting a raw data set to the BIDS standard,
and it integrates with DataLad to place converted and original data under
Git/Git-annex version control, while automatically annotating files with
sensitive information (e.g., non-defaced anatomicals, etc).

To take extra care to know exactly what software is used both to be
able to go back to it at a later stage should we have the
need to investigate an issue, and to capture *full* provenance of the
transformation process, we are using a software container that contains the
relevant software setup.
A ready-made `singularity <http://singularity.lbl.gov/>`_ container is
available from `singularity-hub <https://singularity-hub.org/>`_ at
`shub://ReproNim/ohbm2018-training:heudiconvn <shub://ReproNim/ohbm2018-training:heudiconvn>`_.

Using the :command:`datalad containers-add` command we can add this container
to the ``localizer_scans`` superdataset. We are giving it the name
``heudiconv``.

.. runrecord:: _examples/repro2-104
   :language: console
   :workdir: usecases/repro2/localizer_scans
   :realcommand: datalad containers-add heudiconv --call-fmt 'singularity exec -B {{pwd}} {img} {cmd}'  --url shub://ReproNim/ohbm2018-training:heudiconvn

   $ datalad containers-add heudiconv --url shub://ReproNim/ohbm2018-training:heudiconvn

The command :command:`datalad containers-list` can verify that this worked:

.. runrecord:: _examples/repro2-105
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad containers-list

Great. The dataset now tracks all of the input data *and* the computational
environment for the DICOM conversion. Thus far, we have a complete record of
all components. Let's stay transparent, but also automatically reproducible
in the actual data conversion by wrapping the necessary ``heudiconv`` command
seen below::

   $ heudiconv -f reproin -s 02 -c dcm2niix -b -l "" --minmeta -a . \
    -o /tmp/heudiconv.sub-02 --files inputs/rawdata/dicoms

within a :command:`datalad containers-run` command.
To save time, we will only transfer one subjects data (``sub-02``, hence the
subject identifier ``-s 02`` in the command). Note that the output below is
how it indeed should look like -- the software we are using in this example
produces very wordy output.

.. runrecord:: _examples/repro2-106
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad containers-run -m "Convert sub-02 DICOMs into BIDS" \
     --container-name heudiconv \
     'heudiconv -f reproin -s 02 -c dcm2niix -b -l "" --minmeta -a . -o /tmp/heudiconv.sub-02 --files inputs/rawdata/dicoms'

Find out what changed after this command by comparing the most recent commit
by DataLad (i.e., ``HEAD``) to the previous one (i.e., ``HEAD~1``) with
:command:`datalad diff`:

.. runrecord:: _examples/repro2-107
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad diff -f HEAD~1

As expected, DICOM files of one subject were converted into NIfTI files,
**and** the outputs follow the BIDS standard's layout and naming conventions!
But what's even better is that this action and the relevant software
environment was fully recorded.

There is only one thing missing before the functional imaging data can be
analyzed: A stimulation protocol, so that we know what stimulation was done
at which point during the scan.
Thankfully, the data was collected using an implementation that exported
this information directly in the BIDS events.tsv format. The file came with
our DICOM dataset and can be found at ``inputs/rawdata/events.tsv``. All we need
to do is copy it to the right location under the BIDS-mandated name. To keep
track of where this file came from, we will also wrap the copying into a
:command:`datalad run` command. The ``{inputs}`` and ``{outputs}``
placeholders can help to avoid duplication in the command call:

.. runrecord:: _examples/repro2-108
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ datalad run -m "Import stimulation events" \
     --input inputs/rawdata/events.tsv \
     --output sub-02/func/sub-02_task-oneback_run-01_events.tsv \
     cp {inputs} {outputs}

``git log`` shows what information DataLad captured about this command's
execution:

.. runrecord:: _examples/repro2-109
   :language: console
   :workdir: usecases/repro2/localizer_scans

   $ git log -n 1


Analysis execution
""""""""""""""""""

Since the raw data are reproducibly prepared in BIDS standard we can now go
further and conduct an analysis. For this example, we will implement a very
basic first-level GLM analysis using `FSL <http://fsl.fmrib.ox.ac.uk/>`__
that takes only a few minutes to run. As before, we will capture all provenance:
inputs, computational environments, code, and outputs.

Following the YODA principles [#f2]_, the analysis is set up in a new
dataset, with the input dataset ``localizer_scans`` as a subdataset:

.. runrecord:: _examples/repro2-110
   :language: console
   :workdir: usecases/repro2/localizer_scans

   # get out of localizer_scans
   $ cd ../

   $ datalad create glm_analysis
   $ cd glm_analysis

We install ``localizer_scans`` by providing its path as a ``--source`` to
:command:`datalad install`:

.. runrecord:: _examples/repro2-111
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad clone -d . \
     ../localizer_scans \
     inputs/rawdata

:command:`datalad subdatasets` reports the number of installed subdatasets
again:

.. runrecord:: _examples/repro2-112
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad subdatasets

We almost forgot something really useful: Structuring the dataset with
the help of DataLad! Luckily, procedures such as ``yoda`` can not only be
applied upon creating of a dataset (as in :ref:`createDS`), but also with the
:command:`run-procedure` command (as in :ref:`procedures`)

.. runrecord:: _examples/repro2-113
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad run-procedure cfg_yoda


The analysis obviously needs custom code. For the simple GLM analysis with
FSL we use:

#. A small script to convert BIDS-formatted ``events.tsv`` files into the
   ``EV3`` format FSL understands, available at
   `https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/events2ev3.sh <https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/events2ev3.sh>`_

#. An FSL analysis configuration template script, available at
   `https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/ffa_design.fsf <https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/ffa_design.fsf>`_

These script should be stored and tracked inside the dataset within ``code/``.
The :command:`datalad download-url` command downloads these scripts *and*
records where they were obtained from:

.. runrecord:: _examples/repro2-114
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad download-url  --path code/ \
     https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/events2ev3.sh \
     https://raw.githubusercontent.com/myyoda/ohbm2018-training/master/section23/scripts/ffa_design.fsf

The commit message that DataLad created shows the URL where each script has
been downloaded from:

.. runrecord:: _examples/repro2-115
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ git log -n 1

Prior to the actual analysis, we need to run the ``events2ev3.sh`` script to
transform inputs into the format that FSL expects. The :command:`datalad run`
makes this maximally reproducible and easy, as the files given as
``--inputs`` and ``--outputs`` are automatically managed by DataLad.

.. runrecord:: _examples/repro2-116
   :workdir: usecases/repro2/glm_analysis
   :language: console

   $ datalad run -m 'Build FSL EV3 design files' \
     --input inputs/rawdata/sub-02/func/sub-02_task-oneback_run-01_events.tsv \
     --output 'sub-02/onsets' \
     bash code/events2ev3.sh sub-02 {inputs}

The dataset now contains and manages all of the required inputs, and we're
ready for FSL. Since FSL is not a simple program, we make sure to record the
precise software environment for the analysis with
:command:`datalad containers-run`. First, we get a container with FSL in the
version we require:


.. runrecord:: _examples/repro2-117
   :workdir: usecases/repro2/glm_analysis
   :language: console
   :realcommand: datalad containers-add fsl --call-fmt 'singularity exec -B {{pwd}} {img} {cmd}'  --url shub://mih/ohbm2018-training:fsl

   $ datalad containers-add fsl --url shub://mih/ohbm2018-training:fsl

As the analysis setup is now complete, let's label this state of the dataset:

.. runrecord:: _examples/repro2-118
   :workdir: usecases/repro2/glm_analysis
   :language: console

   $ datalad save --version-tag ready4analysis

All we have left is to configure the desired first-level GLM analysis with
FSL. At this point, the template contains placeholders for the ``basepath``
and the subject ID, and they need to be replaced.
The following command uses the arcane, yet powerful :term:`sed` editor to do
this. We will again use :command:`datalad run` to invoke our command so that
we store in the history how this template was generated (so that we may
audit, alter, or regenerate this file in the future — fearlessly).

.. runrecord:: _examples/repro2-119
   :workdir: usecases/repro2/glm_analysis
   :language: console

   $ datalad run \
    -m "FSL FEAT analysis config script" \
    --output sub-02/1stlvl_design.fsf \
    bash -c 'sed -e "s,##BASEPATH##,{pwd},g" -e "s,##SUB##,sub-02,g" \
    code/ffa_design.fsf > {outputs}'

To compute the analysis, a simple ``feat sub-02/1stlvl_design.fsf`` command
is wrapped into a ``datalad containers-run`` command with appropriate
``--input`` and ``--output`` specification:

.. runrecord:: _examples/repro2-120
   :language: console
   :workdir: usecases/repro2/glm_analysis
   :lines: 1-12, 356-

   $ datalad containers-run --container-name fsl -m "sub-02 1st-level GLM" \
     --input sub-02/1stlvl_design.fsf \
     --input sub-02/onsets \
     --input inputs/rawdata/sub-02/func/sub-02_task-oneback_run-01_bold.nii.gz \
     --output sub-02/1stlvl_glm.feat \
     feat {inputs[0]}

Once this command finishes, DataLad will have captured the entire FSL output,
and the dataset will contain a complete record all the way from the input BIDS
dataset to the GLM results. The BIDS subdataset in turn has a
complete record of all processing down from the raw DICOMs onwards.

.. importantnote:: Many files need more planning

   See how many files were created and added in this computation of a single
   participant? If your study has many participants, analyses like the one above
   could inflate your dataset. Please check out the chapter :ref:`chapter_gobig`.
   in particular the section :ref:`big_analysis` for tips and tricks on how to
   create analyses datasets that scale.


Archive data and results
""""""""""""""""""""""""

After study completion it is important to properly archive data and results,
for example for future inquiries by reviewers or readers of the associated
publication. Thanks to the modularity of the study units, this tasks is easy
and avoids needless duplication.

The raw data is tracked in its own dataset (``localizer_scans``) that only
needs to be archived once, regardless of how many analysis are using it as
input. This means that we can “throw away” this subdataset copy within this
analysis dataset. DataLad can re-obtain the correct version at any point in
the future, as long as the recorded location remains accessible.

To make sure we're not deleting information we are not aware of,
:command:`datalad diff` and :command:`git log` can help to verify that the
subdataset is in the same state as when it was initially added:

.. runrecord:: _examples/repro2-121
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad diff -- inputs

The command does not show any output, thus indicating that there is indeed no
difference. ``git log`` confirms that the only action that was performed on
``inputs/`` was the addition of it as a subdataset:

.. runrecord:: _examples/repro2-122
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ git log -- inputs

Since the state of the subdataset is exactly the state of the original
``localizer_scans`` dataset it is safe to uninstall it.

.. runrecord:: _examples/repro2-123
   :language: console
   :workdir: usecases/repro2/glm_analysis

   $ datalad uninstall --dataset . inputs --recursive

Prior to archiving the results, we can go one step further and verify their
computational reproducibility. DataLad's ``rerun`` command is
capable of “replaying” any recorded command. The following command
re-executes the FSL analysis by re-running everything since the dataset was
tagged as ``ready4analysis``). It will record the recomputed results in a
separate Git branch named ``verify``. Afterwards, we can automatically
compare these new results to the original ones in the ``master`` branch. We
will see that all outputs can be reproduced in bit-identical form. The only
changes are observed in log files that contain volatile information, such as
time steps.

.. runrecord:: _examples/repro2-124
   :language: console
   :workdir: usecases/repro2/glm_analysis
   :lines: 1-17, 362-

   $ datalad rerun --branch verify --onto ready4analysis --since ready4analysis

.. runrecord:: _examples/repro2-125
   :language: console
   :workdir: usecases/repro2/glm_analysis

   # check that we are now on the new `verify` branch
   $ git branch

.. runrecord:: _examples/repro2-126
   :language: console
   :workdir: usecases/repro2/glm_analysis

   # compare which files have changes with respect to the original results
   $ git diff master --stat


.. runrecord:: _examples/repro2-127
   :language: console
   :workdir: usecases/repro2/glm_analysis

   # switch back to the master branch and remove the `verify` branch
   $ git checkout master
   $ git branch -D verify

The outcome of this usecase can be found as a dataset on Github
`here <https://github.com/myyoda/demo-dataset-glmanalysis>`_.


.. rubric:: Footnotes

.. [#f1] "Why can such data exist as a Git repository, shouldn't large files
         be always stored outside of Git?" you may ask. The DICOMs exist in a
         Git-repository for a number of reasons: First, it makes them easily
         available for demonstrations and tutorials without involving DataLad
         at all. Second, the DICOMs are *comparatively* small: 21K per file.
         Importantly, the repository is not meant to version control those
         files *and* future states or derivatives and results obtained from
         them -- this would bring a Git repositories to its knees.

.. [#f2] To re-read everything about the YODA principles, checkout out section
         :ref:`yoda`.

