.. _inm7checklistfmriprep_:

Checklists for the impatient: Preprocess a DataLad dataset with fMRIprep
------------------------------------------------------------------------

Let's say you have a BIDS-structured DataLad dataset with input data that you want to preprocess with `fMRIprep <https://fmriprep.readthedocs.io/>`_ using HTCondor.
Here is a step-by-step bullet point instruction that contains all required steps -- in the case of a fully-standard-no-special-cases analysis setup, with all necessary preparations, e.g., input dataset creation and BIDS validation, being done already.
It may get you to where you want to be, but is doomed to fail when your analysis does not align completely with the set up that this example work with, and it will in all likelihood not enable you to understand and solve the task that you are facing yourself if need be.

.. admonition:: Requirements and implicit assumptions

   The following must be true about your data analysis. Else, adjustments are necessary:

   - The data that you want to preprocess (i.e., your ``sourcedata``) is a DataLad dataset.
     If not, read the first three chapters of the Basics and the section :ref:`dataladdening`, and turn it into a dataset.
   - You want to preprocess the data with `fMRIprep <https://fmriprep.readthedocs.io/>`_.
   - ``sourcedata`` is BIDS-compliant, at least BIDS-compliant enough that fMRIprep is able to run with no fatal errors.
     If not, go the `BIDS starterkit <https://github.com/bids-standard/bids-starter-kit>`_ to read about it, contact the INM-7 data management people, and provide information about what you need -- they can help you get started.
   - The scripts assume that your project is in a `project folder <https://docs.inm7.de/cluster/data/>`_ (e.g., ``/data/project/fancyproject/fmripreppreprocessinganalyis`` where ``fancyproject`` is your `project folder <https://docs.inm7.de/cluster/data/>`_ and ``fmripreppreprocessinganalysis`` is the data analysis that you will create.
     If your data analysis is somewhere else (e.g., some subdirectories down in the project folder), you need to adjust absolute paths that point to it in the workflow script.


.. findoutmore:: How much do I need to learn in order to understand everything that is going?

   A lot.
   That is not to say that it is an inhumane and needlessly complicated effort.
   We're scientists, trying to do a complicated task not only somewhat, but also well.
   The goal is that an analysis of yours can be discovered in a decade by someone who does not know you and has no means of reaching you, ever, but that this person is able to understand and hopefully even recompute what you have done in a matter of minutes, from information that your analysis privides on its own.
   `While this is be the way science should function, this task is yet something to be commonly accomplished <https://www.nature.com/articles/d41586-020-02462-7>`_.
   DataLad can help with this complex task.
   But it comes at the expense of learning to use the tool.
   If you want to learn, there are enough resources.
   Read the :ref:`basics-intro` of the handbook, understand as much as you can, ask about things you don't understand.

To adjust the commands in the checklist to your own data analysis endeavour, please replace any place holder (enclosed in ``<`` and ``>``) with your own information.


.. admonition:: Placeholders

   Throughout the checklist, the following placeholders need to be replaced with whatever applies to your project:

   - ``projectfolder``: This is your 1TB project folder under ``/data/project/`` on juseless
   - ``processed``: This is an arbitrary name that you call the folder to hold preprocessing results
   - ``BIDS``: This is your BIDS-compliant input data in a DataLad dataset
   - ``cluster``: This is the cluster ID HTCondor assigns to your jobs (you will see it once your jobs are submitted)

1. Create an analysis dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to your project folder on juseless::

   $ cd /data/project/<projectfolder>

Create a new dataset, using the YODA-procedure.
This dataset should not be a subdataset of anything at this point.

.. code-block:: bash

   $ datalad create -c yoda <processed>

It will contain the outputs of fMRIprep (fMRIprep will write its output into two folders it creates, ``fmriprep`` and ``freesurfer``), and scripts related to HTCondor job creation and submission.
Input data and fMRIprep container will be subdatasets.

Finally, create a new directory ``logs`` outside of the analysis dataset -- this is where HTCondor's log files will be stored.

.. code-block:: bash

   $ mkdir logs

Install your BIDS compliant input dataset as a subdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go into your newly created dataset::

   $ cd <processed>

Install your BIDS-compliant input dataset as a subdataset.
We call the subdataset ``sourcedata``.
If you decide to go for a different name you will need to exchange the word "sourcedata" in all other scripts with whatever else you decided to call the dataset.

.. code-block:: bash

   $ datalad clone -d . path/to/<BIDS> sourcedata

Install an fMRIprep container dataset as a subdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a preconfigured container dataset with fMRIprep available on juseless.
You should install it as a subdataset.

.. code-block:: bash

   $ datalad clone -d . TODO code/pipelines

You can find out how to create such a container dataset and its configuration in paragraph :ref:`pipelineenki` of the previous section.

Build a workflow script
^^^^^^^^^^^^^^^^^^^^^^^

Due to concurrency issues, parallel execution can't happen in the same dataset.
Therefore, you need to create a workflow script that handles individual job execution in a temporary location on the compute node and push its results back to your dataset.
This workflow is defined in a workflow script, and this workflow script is defined below.

Depending on how many files you (roughly) expect to produce, pick either "For small datasets (200k files or less)" or "For large datasets (200k files or more)" below.
It is important to estimate the amount of result files (not including files in fMRIpreps working directory) and pick the correct section -- too many files can make datasets slow or dysfunctional, and the workflow file needs to be adjusted to overcome this.

A conservative estimate for the amount of files a fMRIprep invocation produces is between 500 and 700 files.
As this amount is dependent on the data structure (the types of acquisitions and amount of files), you could run fMRIprep on a single subject of your dataset, check the amount of produced files, and  extrapolate beforehand.
If you don't want to do this, here are a few benchmarks:

- freesurfer generally produces ~350 files
- eNKI processing (previous section) results in about 500 files per subject
- preprocessing of ``HCP_structural_preprocessed`` data results in about 400 files per subject
- UKBiobank preprocessing leads to about 450 files per subject

.. findoutmore:: For small datasets (200k files or less)

    If you expect fewer than 200k output files, take the workflow script below, replace the placeholders with the required information, and save it as ``fmriprep_participant_job`` into the ``code/`` directory.

    .. code-block:: bash

          #!/bin/bash
          set -e -u -x

          subid=$(basename $1)

          cd /tmp
          flock --verbose $DSLOCKFILE datalad clone /data/project/<projectfolder>/<processed> ds

          cd ds
          datalad get -n -r -R1 .
          git annex dead here

          git checkout -b "job-$JOBID"

          mkdir -p .git/tmp/wdir
          find sourcedata -mindepth 2 -name '*.json' -a ! -wholename "$1"'*' -delete

          # add your required fMRIprep parametrization
          datalad containers-run \
            -m "fMRIprep $subid" \
            --explicit \
            -o freesurfer -o fmriprep \
            -i "$1" \
            -n code/pipelines/fmriprep \
            sourcedata . participant \
            --n_cpus 1 \
            --skip-bids-validation \
            -w .git/tmp/wdir \
            --participant-label "$subid" \
            --random-seed 12345 \
            --skull-strip-fixed-seed \
            --md-only-boilerplate \
            --output-spaces MNI152NLin6Asym \
            --use-aroma \
            --cifti-output
          # selectively push outputs only
          # ignore root dataset, despite recorded changes, needs coordinated
          # merge at receiving end
          flock --verbose $DSLOCKFILE datalad push --to origin


.. findoutmore:: For large datasets

    If you expect more than 200k result files, first create two subdatasets::

        $ datalad create -d . fmriprep
        $ datalad create -d . freesurfer

    If you run ``datalad subdatasets`` afterwards in the root of your dataset you should see four subdatasets listed.
    Then, take the workflow script below, replace the placeholders with the required information, and save it as ``fmriprep_participant_job`` into the ``code/`` directory.

    .. code-block:: bash

          #!/bin/bash
          set -e -u -x

          subid=$(basename $1)

          cd /tmp
          flock --verbose $DSLOCKFILE datalad clone /data/project/<projectfolder>/<processed> ds

          cd ds
          datalad get -n -r -R1 .
          git submodule foreach --recursive git annex dead here

          git -C fmriprep checkout -b "job-$JOBID"
          git -C freesurfer checkout -b "job-$JOBID"

          mkdir -p .git/tmp/wdir
          find sourcedata -mindepth 2 -name '*.json' -a ! -wholename "$1"'*' -delete

          (cd fmriprep && rm -rf logs "$subid" "$subid.html" dataset_description.json desc-*.tsv)
          (cd freesurfer && rm -rf fsaverage "$subid")

          # add your required fMRIprep parametrization
          datalad containers-run \
            -m "fMRIprep $subid" \
            --explicit \
            -o freesurfer -o fmriprep \
            -i "$1" \
            -n code/pipelines/fmriprep \
            sourcedata . participant \
            --n_cpus 1 \
            --skip-bids-validation \
            -w .git/tmp/wdir \
            --participant-label "$subid" \
            --random-seed 12345 \
            --skull-strip-fixed-seed \
            --md-only-boilerplate \
            --output-spaces MNI152NLin6Asym \
            --use-aroma \
            --cifti-output

          flock --verbose $DSLOCKFILE datalad push -d fmriprep --to origin
          flock --verbose $DSLOCKFILE datalad push -d freesurfer --to origin

Then, make the script executable::

   $ chmod +x code/fmriprep_participant_job

Save the addition of this workflow file::

   $ datalad save -m "added fmriprep preprocessing workflow" code/fmriprep_participant_job

Build a HTCondor submit file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To be able to submit the jobs, create a file called ``code/fmriprep_all_participants.submit`` with the following contents:

.. code-block:: bash


      universe       = vanilla
      get_env        = True
      # resource requirements for each job, determined by
      # investigating the demands of a single test job
      request_cpus   = 1
      request_memory = 20G
      request_disk   = 210G

      executable     = $ENV(PWD)/code/fmriprep_participant_job

      # the job expects to environment variables for labeling and synchronization
      environment = "JOBID=$(Cluster).$(Process) DSLOCKFILE=$ENV(PWD)/.git/datalad_lock"
      log    = $ENV(PWD)/../logs/$(Cluster).$(Process).log
      output = $ENV(PWD)/../logs/$(Cluster).$(Process).out
      error  = $ENV(PWD)/../logs/$(Cluster).$(Process).err
      arguments = $(subid)
      # find all participants, based on the subdirectory names in the source dataset
      # each relative path to such a subdirectory with become the value of `subid`
      # and another job is queued. Will queue a total number of jobs matching the
      # number of matching subdirectories
      queue subid matching dirs sourcedata/sub-*

Save the addition of this submit file::

   $ datalad save -m "added fmriprep preprocessing workflow" code/fmriprep_all_participants.submit

Submit the job
^^^^^^^^^^^^^^

In the root of your dataset, run

.. code-block:: bash

   condor_submit code/fmriprep_all_participants.submit

Monitor the job
^^^^^^^^^^^^^^^

Use `standard HTCondor commands <https://docs.inm7.de/htcondor/commands/>`_ to monitor your job.
Your jobs should be listed as either "idle" (awaiting to be ran), or "run"::


    -- Schedd: head1.htc.inm7.de : <10.0.8.10:9618?... @ 11/03/20 10:07:19
    OWNER BATCH_NAME    SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
    adina ID: 323991  11/3  08:16      _   151     303   454  323991.0

If they are being ``held``, you should check on them (see the `INM-7 docs <https://docs.inm7.de/htcondor/commands/>`_ for info and commands).

HTCondor will also write log files into your project directory in ``/data/project/<projectfolder>/logs``.
You should examine the contents of those files to monitor jobs and troubleshoot problems.
The Findoutmores below detail what type of content can be expected in each file.

.. findoutmore:: What kind of content can I expect in log files?

   ``*.log`` files will contain no DataLad-related output, only information from HTCondor

.. findoutmore:: What kind of content can I expect in out files?

   ``out`` files contain messages such as successful datalad operation result summaries (``get(ok)``, ``install(ok)``, ...) and workflow output from fmriprep. Here is an example::

        install(ok): /tmp/ds (dataset)
        flock: getting lock took 3.562222 seconds
        flock: executing datalad
        update(ok):../../ /tmp/ds/code/pipelines (dataset)
        configure-sibling(ok):../../ /tmp/ds/code/pipelines (sibling)
        install(ok): /tmp/ds/code/pipelines (dataset)
        update(ok):../ /tmp/ds/sourcedata (dataset)
        configure-sibling(ok):../ /tmp/ds/sourcedata (sibling)
        install(ok): /tmp/ds/sourcedata (dataset)
        action summary:
          configure-sibling (ok: 2)
          install (ok: 2)
          update (ok: 2)
        dead here ok
        (recording state in git...)
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/anat/sub-A00010893_ses-DS2_T1w.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/dwi/sub-A00010893_ses-DS2_dwi.bval (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/dwi/sub-A00010893_ses-DS2_dwi.bvec (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/dwi/sub-A00010893_ses-DS2_dwi.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-breathhold_acq-1400_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-checkerboard_acq-1400_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-checkerboard_acq-645_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-rest_acq-1400_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-rest_acq-645_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893/ses-DS2/func/sub-A00010893_ses-DS2_task-rest_acq-cap_bold.nii.gz (file) [from inm7-storage...]
        get(ok): /tmp/ds/sourcedata/sub-A00010893 (directory)
        get(ok): /tmp/ds/code/pipelines/.datalad/environments/fmriprep/image (file) [from origin-2...]
        201023-12:36:57,535 nipype.workflow IMPORTANT:

            Running fMRIPREP version 20.1.1:
              * BIDS dataset path: /tmp/ds/sourcedata.
              * Participant list: ['A00010893'].
              * Run identifier: 20201023-123648_216eb011-9b7f-4f2b-8d43-482bf4795041.
              * Output spaces: MNI152NLin6Asym:res-native.
              * Pre-run FreeSurfer's SUBJECTS_DIR: /tmp/ds/freesurfer.
        201023-12:37:33,593 nipype.workflow INFO:
        [...]

.. findoutmore:: What kind of content can I expect in err files?

   ``*.err`` files will contain any message that is sent to the `"stderr" output stream <https://en.wikipedia.org/wiki/Standard_streams#Standard_error_(stderr)>`_.
   With the setup detailed in this checklist, there are three different things that could end up in those files:

       - fMRIprep tracebacks. Those are actual, troublesome errors that require action
       - log messages from DataLad. In most cases, those message are fine and do not require action.
       - log messages from the script. In most cases, those message are fine and do not require action.

   fMRIprep will send Python tracebacks into this file.
   If this happens, the pipeline has crashed, and you should investigate the error.
   Here is an example::

        You are using fMRIPrep-20.1.1, and a newer version of fMRIPrep is available: 20.2.0.
        Please check out our documentation about how and when to upgrade:
        https://fmriprep.readthedocs.io/en/latest/faq.html#upgrading
        Process Process-2:
        Traceback (most recent call last):
          File "/usr/local/miniconda/lib/python3.7/multiprocessing/process.py", line 297, in _bootstrap
            self.run()
          File "/usr/local/miniconda/lib/python3.7/multiprocessing/process.py", line 99, in run
            self._target(*self._args, **self._kwargs)
          File "/usr/local/miniconda/lib/python3.7/site-packages/fmriprep/cli/workflow.py", line 84, in build_workflow
            retval["workflow"] = init_fmriprep_wf()
          File "/usr/local/miniconda/lib/python3.7/site-packages/fmriprep/workflows/base.py", line 64, in init_fmriprep_wf
            single_subject_wf = init_single_subject_wf(subject_id)
          File "/usr/local/miniconda/lib/python3.7/site-packages/fmriprep/workflows/base.py", line 292, in init_single_subject_wf
            func_preproc_wf = init_func_preproc_wf(bold_file)
          File "/usr/local/miniconda/lib/python3.7/site-packages/fmriprep/workflows/bold/base.py", line 261, in init_func_preproc_wf
            tr=metadata.get("RepetitionTime")),
          File "/usr/local/miniconda/lib/python3.7/site-packages/nipype/interfaces/base/core.py", line 611, in __init__
            from_file=from_file, resource_monitor=resource_monitor, **inputs
          File "/usr/local/miniconda/lib/python3.7/site-packages/nipype/interfaces/base/core.py", line 183, in __init__
            self.inputs = self.input_spec(**inputs)
          File "/usr/local/miniconda/lib/python3.7/site-packages/nipype/interfaces/base/specs.py", line 66, in __init__
            super(BaseTraitedSpec, self).__init__(**kwargs)
          File "/usr/local/miniconda/lib/python3.7/site-packages/traits/trait_handlers.py", line 172, in error
            value )
        traits.trait_errors.TraitError: The 'tr' trait of a FunctionalSummaryInputSpec instance must be a float, but a value of None <class 'NoneType'> was specified.

   DataLad will send all of its logging messages, i.e., messages that start with ``[INFO]``, ``[WARNING]``, or ``[ERROR]`` into this file.
   Unless it is an error message, the presence of DataLad log messages in the ``*.err`` files is not worrisome, but only a byproduct of how Unix systems handle input and output communication.
   In most cases, you will see ``[INFO]`` messages that state the progress of the task at hand.
   Note that there is also one ``ConnectionOpenFailedError`` included as an INFO message -- while this looks like trouble, its only an information that using first of several clone targets has not worked out::

        [INFO] Cloning dataset to Dataset(/tmp/ds)
        [INFO] Attempting to clone from /data/project/enki/processed to /tmp/ds
        [INFO] Completed clone attempts for Dataset(/tmp/ds)
        + cd ds
        + datalad get -n -r -R1 .
        [INFO] Installing Dataset(/tmp/ds) to get /tmp/ds recursively
        [INFO] Cloning dataset to Dataset(/tmp/ds/code/pipelines)
        [INFO] Attempting to clone from /data/project/enki/processed/code/pipelines to /tmp/ds/code/pipelines
        [INFO] Completed clone attempts for Dataset(/tmp/ds/code/pipelines)
        [INFO] Cloning dataset to Dataset(/tmp/ds/fmriprep)
        [INFO] Attempting to clone from /data/project/enki/processed/fmriprep to /tmp/ds/fmriprep
        [INFO] Completed clone attempts for Dataset(/tmp/ds/fmriprep)
        [INFO] Cloning dataset to Dataset(/tmp/ds/freesurfer)
        [INFO] Attempting to clone from /data/project/enki/processed/freesurfer to /tmp/ds/freesurfer
        [INFO] Completed clone attempts for Dataset(/tmp/ds/freesurfer)
        [INFO] Cloning dataset to Dataset(/tmp/ds/sourcedata)
        [INFO] Attempting to clone from /data/project/enki/processed/sourcedata to /tmp/ds/sourcedata
        [INFO] Start check out things
        [INFO] Completed clone attempts for Dataset(/tmp/ds/sourcedata)
        [INFO] hanke4@judac.fz-juelich.de: Permission denied (publickey).
        [INFO] ConnectionOpenFailedError: 'ssh -fN -o ControlMaster=auto -o ControlPersist=15m -o ControlPath=/home/mih/.cache/datalad/sockets/64c612f8 judac.fz-juelich.de' failed with exitcode 255 [Failed to open SSH connection (could not start ControlMaster process)]
        + git submodule foreach --recursive git annex dead here
        + git -C fmriprep checkout -b job-107890.1168
        Switched to a new branch 'job-107890.1168'
        + git -C freesurfer checkout -b job-107890.1168
        Switched to a new branch 'job-107890.1168'
        + mkdir -p .git/tmp/wdir
        + find sourcedata -mindepth 2 -name '*.json' -a '!' -wholename 'sourcedata/sub-A00081239/*' -delete
        + cd fmriprep
        + rm -rf logs sub-A00081239 sub-A00081239.html dataset_description.json desc-aparcaseg_dseg.tsv desc-aseg_dseg.tsv
        + cd freesurfer
        + rm -rf fsaverage sub-A00081239
        + datalad containers-run -m 'fMRIprep sub-A00081239' --explicit -o freesurfer -o fmriprep -i sourcedata/sub-A00081239/ -n code/pipelines/fmriprep sourcedata . participant --n_cpus 1 --skip-bids-validation -w .git/tmp/wdir --participant-label sub-A00081239 --random-seed 12345 --skull-strip-fixed-seed --md-only-boilerplate --output-spaces MNI152NLin6Asym --use-aroma --cifti-output
        [INFO] Making sure inputs are available (this may take some time)
        [INFO] == Command start (output follows) =====
        [INFO] == Command exit (modification check follows) =====
        + flock --verbose /data/project/enki/processed/.git/datalad_lock datalad push -d fmriprep --to origin
        [INFO] Determine push target
        [INFO] Push refspecs
        [INFO] Start enumerating objects
        [INFO] Start counting objects
        [INFO] Start compressing objects
        [INFO] Start writing objects
        [INFO] Start resolving deltas
        [INFO] Finished
        [INFO] Transfer data
        [INFO] Start annex operation
        [INFO] sub-A00081239.html
        [INFO] sub-A00081239/anat/sub-A00081239_desc-aparcaseg_dseg.nii.gz
        [...]

   Note that the ``fmriprep_participant_job`` script's log messages are also included in the script.
   Those are the lines that start with a ``+`` and simply log which line of workflow script is presently executed.



Merge the results
^^^^^^^^^^^^^^^^^

fMRIprep writes out a ``CITATION.md`` file in each job.
These files contain a general summary, such as the number of sessions that have been processed.
If those differ between subjects, a straight :term:`merge` will fail.
You can safely try it out first, though (the command would abort if it can't perform the operation)::

   git merge -m "Merge results from job cluster <cluster>" $(git branch -l | grep 'job-' | tr -d ' ')

If this fails, copy the contents of one ``CITATION.md`` file into the :term:`master` branch::

    TODO - catfile command

Afterwards, delete the ``CITATION.md`` files in all branches with the following command::

   for b in $(git branch -l | grep 'job-' | tr -d ' ');
     do ( git checkout -b m$b $b && git rm logs/CITATION.md && git commit --amend --no-edit ) ;
   done

Lastly, repeat the merge command from above::

   git merge -m "Merge results from job cluster <cluster>" $(git branch -l | grep 'job-' | tr -d ' ')
