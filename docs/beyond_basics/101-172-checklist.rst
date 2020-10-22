.. _inm7checklist:

Checklist for the impatient: Preprocess a DataLad dataset with fMRIprep
-----------------------------------------------------------------------

Let's say you have a BIDS-structured DataLad dataset with input data that you want to preprocess with `fMRIprep <https://fmriprep.readthedocs.io/>`_ using HTCondor, but you can't be bothered to read and understand more than a few pages of user documentation.
Here is a step-by-step bullet point instruction that may get you to where you want to be, but doesn't enforce any learning upon you.
It will only work if the data you want to preprocess is already a DataLad dataset and in a BIDS-compliant structure.

.. admonition:: Placeholders

   Throughout the checklist, the following placeholders need to be replaced with whatever applies to your project:

   - ``projectfolder``: This is your 1TB project folder under ``/data/project/`` on juseless
   - ``processed``: This is an arbitrary name that you call the folder to hold preprocessing results
   - ``BIDS``: This is your BIDS-compliant input data in a DataLad dataset

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

   $ mkdir ../logs

2. Install your BIDS compliant input dataset as a subdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go into your newly created dataset::

   $ cd <processed>

Install your BIDS-compliant input dataset as a subdataset.
We call the subdataset ``sourcedata``.
If you decide to go for a different name you will need to exchange the word "sourcedata" in all other scripts with whatever else you decided to call the dataset.

.. code-block:: bash

   $ datalad clone -d . path/to/<BIDS> sourcedata

3. Install an fMRIprep container dataset as a subdataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a preconfigured container dataset with fMRIprep available on juseless.
You should install it as a subdataset.

.. code-block:: bash

   $ datalad clone -d . TODO code/pipelines

You can find out how to create such a container dataset and its configuration in paragraph :ref:`pipelineenki` of the previous section.

4. Build a workflow script
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

For small datasets (200k files or less)
"""""""""""""""""""""""""""""""""""""""

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
      find sourcedata -mindepth 2 -name '*.json' -a ! -wholename "$1"/'*' -delete

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

Save the addition of this workflow file::

   $ datalad save -m "added fmriprep preprocessing workflow" code/fmriprep_participant_job

For large datasets
""""""""""""""""""

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
      find sourcedata -mindepth 2 -name '*.json' -a ! -wholename "$1"/'*' -delete

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

Save the addition of this workflow file::

   $ datalad save -m "added fmriprep preprocessing workflow" code/fmriprep_participant_job

5. Build a HTCondor submit file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

6. Submit the job
^^^^^^^^^^^^^^^^^

In the root of your dataset, run

.. code-block:: bash

   condor_submit code/fmriprep_all_participants.submit

7.