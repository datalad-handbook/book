.. _runhpc:

DataLad-centric analysis with job scheduling and parallel computing
-------------------------------------------------------------------

.. note::

   It is advised to read the previous chapter :ref:`chapter_gobig` prior to this one

This section is a write-up of how DataLad can be used on a scientific computational cluster with a job scheduler for reproducible and FAIR data analyses at scale.
More concretely, it shows an example of containerized `fMRIprep <https://fmriprep.readthedocs.io/>`_ preprocessing on the `eNKI <http://fcon_1000.projects.nitrc.org/indi/enhanced/>`_ neuroimaging dataset, scheduled with `HTCondor <https://research.cs.wisc.edu/htcondor/>`_.
While the choice of containerized pipeline and job scheduler are specific in this example, the general setup is generic and could be used with any containerized pipeline and any job scheduling system.

Why job scheduling?
^^^^^^^^^^^^^^^^^^^

On scientific compute clusters, job scheduling systems such as `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ or `slurm <https://slurm.schedmd.com/overview.html>`_ are used to distribute computational jobs across the available computing infrastructure and manage the overall workload of the cluster.
This allows for efficient and fair use of available resources across a group of users, and it brings the potential for highly parallelized computations of jobs and thus vastly faster analyses.

Consider one common way to use a job scheduler: processing all subjects of a dataset independently and as parallel as the current workload of the compute cluster allows instead of serially (i.e., "one after the other").
In such a setup, each subject-specific analysis becomes a single job, and the job scheduler fits as many jobs as it can on available :term:`compute node`\s.
If a large analysis can be split into many independent jobs, using a job scheduler to run them in parallel thus yields great performance advantages in addition to fair compute resource distribution across all users.

.. findoutmore:: How is a job scheduler used?

   Depending on the job scheduler your system is using, the looks of your typical job scheduling differ, but the general principle is the same.

   Typically, a job scheduler is used *non-interactively*, and a *job* (i.e., any command or series of commands you want run) is *submitted* to the scheduler.
   This submission starts with a "submit" command of the given job scheduler (such as ``condor_submit`` for HTCondor or ``sbatch`` for slurm) followed by a command, script, or *batch/submit-file* that contains job definitions and (potentially) compute resource requirements.

   The job scheduler takes the submitted jobs, *queues* them up in a central queue, and monitors the available compute resources (i.e., :term:`compute node`\s) of the cluster.
   As soon as a computational resource is free, it matches a job from the queue to the available resource and computes the job on this node.
   Usually, a single submission queues up multiple (dozens, hundreds, or thousands of) jobs.

Where are the difficulties in parallel computing with DataLad?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to capture as much provenance as possible, analyses are best ran with a :command:`datalad run` or :command:`datalad containers-run` command, as these commands can capture and link all relevant components of an analysis, starting from code and results to input data and computational environment.

Note, though, that when parallelizing jobs and computing them with provenance capture, *each individual job* needs to be wrapped in a ``run`` command, and not only the submission of the jobs to the job scheduler -- and this requires multiple parallel ``run`` commands on the same dataset.
Multiple simultaneous ``datalad (containers-)run`` invocations in the same dataset are, however, problematic:

- Operations carried out during one :command:`run` command can lead to modifications that prevent a second, slightly later ``run`` command from being started
- The :command:`datalad save` command at the end of of :command:`datalad run` could save modifications that originate from a different job, leading to mis-associated provenance
- A number of *concurrency issues*, unwanted interactions of processes when they run simultaneously, can arise and lead to internal command failures

Some of these problems can be averted by invoking the ``(containers-)run`` command with the ``--explicit`` [#f1]_ flag.
This doesn't solve all of the above problems, though, and may not be applicable to the computation at hand -- for example because all jobs write to a similar file or the result files are not known beforehand.
Below, a complete, largely platform and scheduling-system agnostic containerized analysis workflow is outlined that addressed the outlined problems.

Processing FAIRly *and* in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    FAIR *and* parallel processing requires out-of-the-box thinking, and many creative approaches can lead to success.
    Here is **one** approach that led to a provenance-tracked, computationally reproducible, and parallel preprocessing workflow, but many more can work.
    `We are eager to hear about yours <https://github.com/datalad-handbook/book/issues/new/>`_.

**General background**: We need to preprocess data from 1300 participants with a containerized pipeline.
All data lies in a single dataset.
The preprocessing results will encompass several TB and about half a million files, and will therefore need to be split into two result datasets.

The keys to the success of this workflow lie in

- creating it completely *job-scheduling* and *platform agnostic*, such that the workflow can be deployed as a subject-specific job anywhere, with any job scheduling system, and ...
- instead of computing job results in the same dataset over all jobs, temporary, :term:`ephemeral clone`\s are created to hold individual, subject-specific results, and those results are pushed back into the target dataset in the end.

The "creative" bits involved in this parallelized processing workflow boiled down to the following tricks:

- Individual jobs (in this case, subject-specific analyses) are computed in throw-away dataset clones to avoid unwanted interactions between ``save`` commands.
- Moreover, beyond computing in job-specific, temporary locations, individual job results are also saved into uniquely identified :term:`branch`\es to enable simple pushing back of the results into the target dataset [#f6]_.
- The jobs constitute a complete DataLad-centric workflow in the form of a simple bash script, including dataset build-up and tear-down routines in a throw-away location, result computation, and result publication back to the target dataset. Thus, instead of submitting a ``datalad run`` command to the job scheduler, the job submission is a single script, and this submission is easily adapted to various job scheduling call formats.
- Right after successful job termination, the target dataset contains as many :term:`branch`\es as jobs, with each branch containing the results of one job. A manual :term:`merge` aggregates all results into the :term:`master` branch of the dataset.

Walkthrough
^^^^^^^^^^^

The goal of the following analysis was standard preprocessing using `fMRIprep <https://fmriprep.readthedocs.io/>`_ on neuroimaging data of 1300 subjects in the `eNKI <http://fcon_1000.projects.nitrc.org/indi/enhanced/>`_ dataset.
In order to associate input data, containerized pipeline, and outputs, the analysis was carried out in a DataLad dataset and with the :command:`datalad containers-run` command.
Here's a walkthrough of what was done and how.

Starting point: Datasets for software and input data
""""""""""""""""""""""""""""""""""""""""""""""""""""

At the beginning of this endeavour, two important analysis components already exist as DataLad datasets:

1. The input data
2. The containerized pipeline

Following the :ref:`YODA principles <yoda>`, each of these components is a standalone dataset.
While the input dataset creation is straightforwards, some thinking went into the creation of containerized pipeline dataset to set it up in a way that allows it to be installed as a subdataset and invoked from the superdataset.
If you are interested in this, find the details in the findoutmore below.

.. findoutmore:: pipeline dataset creation

   We start with a dataset (called ``pipelines`` in this example)::

       $ datalad create pipelines
         [INFO   ] Creating a new annex repo at /data/projects/enki/pipelines
         create(ok): /data/projects/enki/pipelines (dataset)
       $ cd pipelines

   As one of tools used in the pipeline, `freesurfer <https://surfer.nmr.mgh.harvard.edu/>`_, requires a license file, this license file needs to be added into the dataset.
   Only then can this dataset be moved around flexibly and also to different machines.
   In order to have the license file available right away, it is saved ``--to-git`` and not annexed [#f2]_::

       $ cp <location/to/fs-license.txt> .
       $ datalad save --to-git -m "add freesurfer license file" fs-license.txt

   Finally, we add a container with the pipeline to the dataset using :command:`datalad containers-add` [#f3]_.
   The important part is the configuration of the container -- it has to be done in a way that makes the container usable in any superdataset the pipeline dataset.

   Depending on how the container/pipeline needs to be called, the configuration differs.
   In the case of an fMRIprep run, we want to be able to invoke the container from a superdataset.
   The superdataset contains input data and ``pipelines`` dataset as subdatasets, and will collect all of the results.
   Thus, these are arguments we want to supply the invocation with (following `fMRIprep's documentation <https://fmriprep.org/en/stable/usage.html>`_) during a ``containers-run`` command::

        $ datalad containers-run \
        [...]
        <BIDS_dir> <output_dir> <analysis_level> \
        --n_cpus <N> \
        --participant-label <ID> \
        [...]

   Note how this list does not include bind-mounts of the necessary directories or of the freesurfer license -- this makes the container invocation convenient and easy for any user.
   Starting an fMRIprep run requires only a ``datalad containers-run`` with all of the desired fMRIprep options.

   This convenience for the user requires that all of the bind-mounts should be taken care of -- in a generic way -- in the container call specification, though.
   Here is how this is done::

       $ datalad containers-add fmriprep \
         --url TODO \
         --call-fmt singularity run --cleanenv -B "$PWD" {img} {cmd} --fs-license-file "$PWD/{img_dspath}/freesurfer_license.txt"

   During a :command:`datalad containers-run` command, the ``--call-fmt`` specification will be used to call the container.
   The placeholders ``{img}`` and ``{cmd}`` will be replaced with the container (``{img}``) and the command given to ``datalad containers-run`` (``{cmd}``).
   Thus, the ``--cleanenv`` flag (`recommended by fMRIprep <https://fmriprep.org/en/stable/singularity.html#handling-environment-variables>`_) as well as bind-mounts are handled prior to the container invocation, and the ``--fs-license-file`` option with a path to the license file within the container is appended to the command.
   Bind-mounting the working directory (``-B "$PWD"``) makes sure to bind mount the directory from which the container is being called, which should be the superdataset that contains input data and ``pipelines`` subdataset.
   With these bind-mounts, input data and the freesurfer license file within ``pipelines`` are available in the container.

   With such a setup, the ``pipelines`` dataset can be installed in any dataset and will work out of the box.

Analysis dataset setup
""""""""""""""""""""""

An analysis dataset consists of the following components:

- input data as a subdataset
- ``pipelines`` container dataset as a subdataset
- subdatasets to hold the results

Following the benchmarks and tips in the chapter :ref:`chapter_gobig`, the amount of files produced by fMRIprep on 1300 subjects requires two datasets to hold them.
In this particular computation, following the naming scheme and structure of fMRIpreps output directories, one subdataset is created for the `freesurfer <https://surfer.nmr.mgh.harvard.edu/>`_ results of fMRIprep in a subdataset called ``freesurfer``, and one for the minimally preprocessed input data in a subdataset called ``fmriprep``.

Here is an overview of the directory structure in the superdataset::

    superds
    ├── code                # directory
    │   └── pipelines       # subdataset with fMRIprep
    ├── fmriprep            # subdataset for results
    ├── freesurfer          # subdataset for results
    └── sourcedata          # subdataset with BIDS-formatted data
        ├── sourcedata      # subdataset with raw data
        ├── sub-A00008326   # directory
        ├── sub-...


Workflow script
"""""""""""""""

The general complexity of concurrent ``datalad (containers-)run`` commands arises when they are carried out in the same dataset.
Therefore, the strategy is to create throw-away dataset clone for all jobs.

.. findoutmore:: how does one create throw-away clones?

    One way to do this are :term:`ephemeral clone`\s, an alternative is to make :term:`git-annex` disregard the datasets annex completely using ``git annex dead here``.

Using throw-away clones involves a build-up and tear-down routine for each job: Clone the analysis dataset hierarchy into a temporary location, run the computation, push the results, remove temporary dataset [#f4]_.
All of this is done in a single script, which will be submitted as a job.

To give you a first idea, a sketch of this is below in a :term:`bash` (shell) script.
Using `shell <https://en.wikipedia.org/wiki/Shell_script>`_ as the language for this script is a straight-forward choice as it allows you to script the DataLad workflow just as you would type it into your terminal, but other languages (e.g., using :ref:`DataLad's Python API <python>` or system calls in languages such as Matlab) would work as well.
Fine-tuning and the complete script are shown in the findoutmore afterwards::

   # everything is running under /tmp inside a compute job, /tmp is a performant local filesystem
   $ cd /tmp

   # clone the superdataset
   $ datalad clone /data/project/enki/superds ds
   $ cd ds

   # get first-level subdatasets (-R1 = --recursion-limit 1)
   $ datalad get -n -r -R1 .

   # make git-annex disregard the clones - they are meant to be thrown away
   $ git submodule foreach --recursive git annex dead here

   # checkout unique branches (names derived from job IDs) in both subdatasets
   # to enable pushing the results without interference from other jobs
   $ git -C fmriprep checkout -b "job-$JOBID"
   $ git -C freesurfer checkout -b "job-$JOBID"

   # call fmriprep with datalad containers-run. Use all relevant fMRIprep
   # arguments for your usecase
   $ datalad containers-run \
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

   # push back the results
   $ datalad push -d fmriprep --to origin
   $ datalad push -d freesurfer --to origin
   # job handler should clean up workspace

Pending a few yet missing safe guards against concurrency issues and to enable re-running computations, such a script can be submitted to any job scheduler with a subject ID and a job ID as identifiers for the fMRIprep run and branch names.
The concrete calling/submission of this script is shown in the paragraph :ref:`jobsubmit`, but on a procedural level, this workflow sketch takes care

.. findoutmore:: Fine-tuning: Enable re-running and safe-guard concurrency issues

   Two important fine-tunings are missing:
   For one, cloning and pushing *can* still run into concurrency issues in the case when one job clones the original dataset while another job is currently pushing into this dataset.
   Therefore, a trick can make sure that no two clone or push commands are executed at the same time.
   This trick uses `file locking <https://en.wikipedia.org/wiki/File_locking>`_, in particular the tool `flock <https://www.tutorialspoint.com/unix_system_calls/flock.htm>`_, to prevent exactly concurrent processes.
   This is done by prepending ``clone`` and ``push`` commands with ``flock --verbose $DSLOCKFILE``, where ``$DSLOCKFILE`` is a textfile placed into ``.git/`` at the time of job submission (further details in the submit file in the next section)

   The second issue concerns the ability to rerun a computation quickly:
   If fMRIprep finds preexisting results, it will fail to run.
   Therefore, all outputs of a job are attempted to be removed before the jobs is started [#f5]_::

        (cd fmriprep && rm -rf logs "$subid" "$subid.html" dataset_description.json desc-*.tsv)
        (cd freesurfer && rm -rf fsaverage "$subid")

   With this in place, the only things missing are a :term:`shebang` at the top of the script, and some shell settings for robust scripting with verbose log files (``set -e -u -x``).
   You can find the full script with rich comments in the next findoutmore.

.. findoutmore:: See the complete bash script

   This script is placed in ``code/fmriprep_participant_job``:

   .. code-block:: bash

        #!/bin/bash

        # fail whenever something is fishy, use -x to get verbose logfiles
        set -e -u -x

        # we pass in "sourcedata/sub-...", extract subject id from it
        subid=$(basename $1)

        # this is all running under /tmp inside a compute job, /tmp is a performant
        # local filesystem
        cd /tmp
        # get the output dataset, which includes the inputs as well
        # flock makes sure that this does not interfere with another job
        # finishing at the same time, and pushing its results back
        # importantly, we clone from the location that we want to push the
        # results too
        flock --verbose $DSLOCKFILE \
            datalad clone /data/project/enki/super ds

        # all following actions are performed in the context of the superdataset
        cd ds
        # obtain all first-level subdatasets:
        # dataset with fmriprep singularity container and pre-configured
        # pipeline call; also get the output dataset to prep them for output
        # consumption, we need to tune them for this particular job, sourcedata
        # important: because we will push additions to the result datasets back
        # at the end of the job, the installation of these result datasets
        # must happen from the location we want to push back too
        datalad get -n -r -R1 .
        # let git-annex know that we do not want to remember any of these clones
        # (we could have used an --ephemeral clone, but that might deposite data
        # of failed jobs at the origin location, if the job runs on a shared
        # filesystem -- let's stay self-contained)
        git submodule foreach --recursive git annex dead here

        # checkout new branches in both subdatasets
        # this enables us to store the results of this job, and push them back
        # without interference from other jobs
        git -C fmriprep checkout -b "job-$JOBID"
        git -C freesurfer checkout -b "job-$JOBID"
        # create workdir for fmriprep inside to simplify singularity call
        # PWD will be available in the container
        mkdir -p .git/tmp/wdir
        # pybids (inside fmriprep) gets angry when it sees dangling symlinks
        # of .json files -- wipe them out, spare only those that belong to
        # the participant we want to process in this job
        find sourcedata -mindepth 2 -name '*.json' -a ! -wholename "$1"/'*' -delete

        # next one is important to get job-reruns correct. We remove all anticipated
        # output, such that fmriprep isn't confused by the presence of stale
        # symlinks. Otherwise we would need to obtain and unlock file content.
        # But that takes some time, for no reason other than being discarded
        # at the end
        (cd fmriprep && rm -rf logs "$subid" "$subid.html" dataset_description.json desc-*.tsv)
        (cd freesurfer && rm -rf fsaverage "$subid")

        # the meat of the matter, add actual parameterization after --participant-label
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
        flock --verbose $DSLOCKFILE datalad push -d fmriprep --to origin
        flock --verbose $DSLOCKFILE datalad push -d freesurfer --to origin

        # job handler should clean up workspace

.. _jobsubmit:

Job submission
""""""""""""""

With this script set up, job submission boils down to invoking the script for each participant with a participant identifier that determines on which subject the job runs, and setting two environment variables - one the job ID that determines the branch name that is created, and one that points to a lockfile created beforehand once in ``.git``.
Job scheduler such as HTCondor have syntax that can identify subject IDs from consistently named directories, for example, and the submit file is thus lean.

You can find the submit file used in this analyses in the findoutmore below.

.. findoutmore:: HTCondor submit file fmriprep_all_participants.submit

   .. code-block:: bash

      universe       = vanilla
      # this is currently necessary, because otherwise the
      # bundles git in git-annex-standalone breaks
      # but it should be removed eventually
      get_env        = True
      # resource requirements for each job
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

All it takes to submit is a single ``condor_submit fmriprep_all_participants.submit``.

Merging results
"""""""""""""""

Once all jobs have finished, the results lie in individual branches of the output datasets.
In this concrete example, the subdatasets ``fmriprep`` and ``freesurfer`` will each have 1300 branches that hold individual job results.
The only thing left to do now is merging all of these branches into :term:`master` -- and potentially solve any merge conflicts that arise.

TODO - need to ask mih how he did it and how merge conflicts were solved.

Recomputing results
"""""""""""""""""""

TODO


.. rubric:: Footnotes

.. [#f1] To re-read about :command:`datalad run`'s ``--explicit`` option, take a look into the section :ref:`run5`.

.. [#f2] If the distinction between annexed and unannexed files is new to you, please read section :ref:`symlink`

.. [#f3] Note that this requires the ``datalad containers`` extension. Find an overview of all datalad extensions in :ref:`extensions_intro`.

.. [#f4] Clean-up routines can, in the case of common job schedulers, be taken care of by performing everything in compute node specific ``/tmp`` directories that are wiped clean after job termination.

.. [#f5]  The brackets around the commands are called *command grouping* in bash, and yield a subshell environment: `www.gnu.org/software/bash/manual/html_node/Command-Grouping.html <https://www.gnu.org/software/bash/manual/html_node/Command-Grouping.html>`_.

.. [#f6] To find out why a different branch is required to enable easy pushing back to the original dataset, please checkout the explanation on :ref:`pushing to non-bare repositories <nonbarepush>` in the section on :ref:`help`.