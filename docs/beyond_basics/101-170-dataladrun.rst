.. _runhpc:

DataLad-centric analysis with job scheduling and parallel computing
-------------------------------------------------------------------

.. importantnote:: This workflow has an update!

   The workflow below is valid and working, but over many months and a few very large scale projects we have improved it with a more flexible and scalable setup.
   Currently, this work can be found as a comprehensive tutorial and bootstrapping script on GitHub (`github.com/psychoinformatics-de/fairly-big-processing-workflow <https://github.com/psychoinformatics-de/fairly-big-processing-workflow>`_), and a corresponding show case implementation with fMRIprep (`github.com/psychoinformatics-de/fairly-big-processing-workflow-tutorial <https://github.com/psychoinformatics-de/fairly-big-processing-workflow-tutorial>`_).
   Also, there is an accompanying preprint with more high-level descriptions of the workflow at `www.biorxiv.org/content/10.1101/2021.10.12.464122v1 <https://www.biorxiv.org/content/10.1101/2021.10.12.464122v1>`_.
   Its main advantages over the workflow below lie in a distributed (and thus independent) setup of all involved dataset locations; built-in support for two kinds of job schedulers (HTCondor, SLURM); enhanced scalability (tested on 42k datasets of the `UK Biobank dataset <https://www.ukbiobank.ac.uk/>`_; and use of :term:`Remote Indexed Archive (RIA) store`\s that provide support for additional security or technical features.
   It is advised to use the updated workflow over the one below.
   In the future, this chapter will be updated with an implementation of the updated workflow.

There are data analyses that consist of running a handful of scripts on a handful of files.
Those analyses can be done in a couple of minutes or hours on your private computer.
But there are also analyses that are so large -- either in terms of computations, or with regard to the amount of data that they are run on -- that it would takes days or even weeks to complete them.
The latter type of analyses typically requires a compute cluster, a job scheduler, and parallelization.
The question is: How can they become as reproducible and provenance tracked as the simplistic, singular analysis that were showcased in the handbook so far, and that comfortably fitted on a private computer?

.. importantnote:: Reading prerequisite for distributed computing

   It is advised to read the previous chapter :ref:`chapter_gobig` prior to this one

This section is a write-up of how DataLad can be used on a scientific computational cluster with a job scheduler for reproducible and FAIR data analyses at scale.
It showcases the general principles behind parallel processing of DataLad-centric workflows with containerized pipelines.
While this chapter demonstrates specific containerized pipelines and job schedulers, the general setup is generic and could be used with any containerized pipeline and any job scheduling system.

This section lays the groundwork to the next section, a walk-through through a real life example of containerized `fMRIprep <https://fmriprep.readthedocs.io/>`_ preprocessing on the `eNKI <http://fcon_1000.projects.nitrc.org/indi/enhanced/>`_ neuroimaging dataset, scheduled with `HTCondor <https://research.cs.wisc.edu/htcondor/>`_.

Why job scheduling?
^^^^^^^^^^^^^^^^^^^

On scientific compute clusters, job scheduling systems such as `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ or `slurm <https://slurm.schedmd.com/overview.html>`_ are used to distribute computational jobs across the available computing infrastructure and manage the overall workload of the cluster.
This allows for efficient and fair use of available resources across a group of users, and it brings the potential for highly parallelized computations of jobs and thus vastly faster analyses.

Consider one common way to use a job scheduler: processing all subjects of a dataset independently and as parallel as the current workload of the compute cluster allows -- instead of serially "one after the other".
In such a setup, each subject-specific analysis becomes a single job, and the job scheduler fits as many jobs as it can on available :term:`compute node`\s.
If a large analysis can be split into many independent jobs, using a job scheduler to run them in parallel thus yields great performance advantages in addition to fair compute resource distribution across all users.

.. find-out-more:: How is a job scheduler used?

   Depending on the job scheduler your system is using, the looks of your typical job scheduling differ, but the general principle is the same.

   Typically, a job scheduler is used *non-interactively*, and a *job* (i.e., any command or series of commands you want run) is *submitted* to the scheduler.
   This submission starts with a "submit" command of the given job scheduler (such as ``condor_submit`` for HTCondor or ``sbatch`` for slurm) followed by a command, script, or *batch/submit-file* that contains job definitions and (potentially) compute resource requirements.

   The job scheduler takes the submitted jobs, *queues* them up in a central queue, and monitors the available compute resources (i.e., :term:`compute node`\s) of the cluster.
   As soon as a computational resource is free, it matches a job from the queue to the available resource and computes the job on this node.
   Usually, a single submission queues up multiple (dozens, hundreds, or thousands of) jobs.
   If you are interested in a tutorial for HTCondor, checkout the `INM-7 HTCondor Tutorial <https://jugit.fz-juelich.de/inm7/training/htcondor>`_.

Where are the difficulties in parallel computing with DataLad?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to capture as much provenance as possible, analyses are best ran with a :command:`datalad run` or :command:`datalad containers-run` command, as these commands can capture and link all relevant components of an analysis, starting from code and results to input data and computational environment.
Tip: Make use of ``datalad run``'s ``--dry-run`` option to craft your run-command (see :ref:`dryrun`)!

But in order to compute parallel jobs with provenance capture, *each individual job* needs to be wrapped in a ``run`` command, not only the submission of the jobs to the job scheduler.
This requires multiple parallel ``run`` commands on the same dataset.
But: Multiple simultaneous ``datalad (containers-)run`` invocations in the same dataset are problematic.

- Operations carried out during one :command:`run` command can lead to modifications that prevent a second, slightly later ``run`` command from being started
- The :command:`datalad save` command at the end of :command:`datalad run` could save modifications that originate from a different job, leading to mis-associated provenance
- A number of *concurrency issues*, unwanted interactions of processes when they run simultaneously, can arise and lead to internal command failures

Some of these problems can be averted by invoking the ``(containers-)run`` command with the ``--explicit`` [#f1]_ flag.
This doesn't solve all of the above problems, though, and may not be applicable to the computation at hand -- for example because all jobs write to a similar file or the result files are not known beforehand.
Below, you can find a complete, largely platform and scheduling-system agnostic containerized analysis workflow that addressed the outlined problems.

Processing FAIRly *and* in parallel -- General workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. importantnote:: FAIR and parallel: more than one way to do it

    FAIR *and* parallel processing requires out-of-the-box thinking, and many creative approaches can lead to success.
    Here is **one** approach that leads to a provenance-tracked, computationally reproducible, and parallel preprocessing workflow, but many more can work.
    `We are eager to hear about yours <https://github.com/datalad-handbook/book/issues/new/>`_.

**General setup**: The overall setup consists of a data analysis with a containerized pipeline (i.e., a software container that performs a single or a set of analyses).
Results will be aggregated into a top-level analysis dataset while the input dataset and a "pipeline" dataset (with a configured software container) exist as subdatasets.
The analysis is carried out on a computational cluster that uses a job scheduling system to distribute compute jobs.

The "creative" bits involved in this parallelized processing workflow boil down to the following tricks:

- Individual jobs (for example subject-specific analyses) are computed in **throw-away dataset clones** to avoid unwanted interactions between parallel jobs.
- Beyond computing in job-specific, temporary locations, individual job results are also saved into uniquely identified :term:`branch`\es to enable simple **pushing back of the results** into the target dataset.
- The jobs constitute a complete DataLad-centric workflow in the form of a simple **bash script**, including dataset build-up and tear-down routines in a throw-away location, result computation, and result publication back to the target dataset.
  Thus, instead of submitting a ``datalad run`` command to the job scheduler, **the job submission is a single script**, and this submission is easily adapted to various job scheduling call formats.
- Right after successful completion of all jobs, the target dataset contains as many :term:`branch`\es as jobs, with each branch containing the results of one job.
  A manual :term:`merge` aggregates all results into the :term:`master` branch of the dataset.

The keys to the success of this workflow lie in

- creating it completely *job-scheduling* and *platform agnostic*, such that the workflow can be deployed as a subject/...-specific job anywhere, with any job scheduling system, and ...
- instead of computing job results in the same dataset over all jobs, temporary clones are created to hold individual, job-specific results, and those results are pushed back into the target dataset in the end ...
- while all dataset components (input data, containerized pipeline) are reusable and the results completely provenance-tracked.

Step-by-Step
""""""""""""

To get an idea of the general setup of parallel provenance-tracked computations, consider a :ref:`YODA-compliant <yoda>` data analysis dataset...

.. code-block:: bash

    $ datalad create parallel_analysis
    [INFO   ] Creating a new annex repo at /tmp/parallel_analysis
    [INFO   ] Scanning for unlocked files (this may take some time)
    create(ok): /tmp/parallel_analysis (dataset)
    $ cd parallel_analysis

... with input data as a subdataset ...

.. code-block:: bash

    $ datalad clone -d . /path/to/my/rawdata
    [INFO   ] Scanning for unlocked files (this may take some time)
    install(ok): /tmp/parallel_analysis/rawdata (dataset)
    add(ok): /tmp/parallel_analysis/rawdata (file)
    add(ok): /tmp/parallel_analysis/.gitmodules (file)
    save(ok): /tmp/parallel_analysis (dataset)
    action summary:
      add (ok: 2)
      install (ok: 1)
      save (ok: 1)

... and a dataset with a containerized pipeline (for example from the `ReproNim container-collection <https://github.com/repronim/containers>`_ [#f2]_) as another subdataset:

.. code-block::

   $ datalad clone -d . https://github.com/ReproNim/containers.git
    [INFO   ] Scanning for unlocked files (this may take some time)
    install(ok): /tmp/parallel_analysis/containers (dataset)
    add(ok): /tmp/parallel_analysis/containers (file)
    add(ok): /tmp/parallel_analysis/.gitmodules (file)
    save(ok): /tmp/parallel_analysis (dataset)
    action summary:
      add (ok: 2)
      install (ok: 1)
      save (ok: 1)

.. find-out-more:: Why do I add the pipeline as a subdataset?

   You could also add and configure the container using ``datalad containers-add`` to the top-most dataset.
   This solution makes the container less usable, though.
   If you have more than one application for a container, keeping it as a standalone dataset can guarantee easier reuse.
   For an example on how to create such a dataset yourself, please checkout the Findoutmore in  :ref:`pipelineenki` in the real-life walk-through in the next section.


The analysis aims to process the ``rawdata`` with a pipeline from ``containers`` and collect the outcomes in the toplevel ``parallel_analysis`` dataset -- FAIRly and in parallel, using ``datalad containers-run``.

One way to conceptualize the workflow is by taking the perspective of a single compute job.
This job consists of whatever you may want to parallelize over.
For an arbitrary example, say your raw data contains continuous moisture measurements in the Arctic, taken over the course of 10 years.
Each file in your dataset contains the data of a single day.
You are interested in a daily aggregate, and are therefore parallelizing across files -- each compute job will run an analysis pipeline on one datafile.

.. find-out-more:: What are common analysis types to parallelize over?

   The key to using a job scheduler and parallelization is to break down an analysis into smaller, loosely coupled computing tasks that can be distributed across a compute cluster.
   Among common analysis setups that are suitable for parallelization are computations that can be split into several analysis that each run on one subset of the data -- such as one (or some) out of many subjects, acquisitions, or files.
   The large computation "preprocess 200 subjects" can be split into 200 times the job "preprocess 1 subject", for example.
   In simulation studies, a commonly parallelized task concerns analyses that need to be ran with a range of different parameters, where each parameter configuration can constitute one job.

What you will submit as a job with a job scheduler is not a ``datalad containers-run`` call, but a shell script that contains all relevant data analysis steps.
Using `shell <https://en.wikipedia.org/wiki/Shell_script>`_ as the language for this script is a straight-forward choice as it allows you to script the DataLad workflow just as you would type it into your terminal.
Other languages (e.g., using :ref:`DataLad's Python API <python>` or system calls in languages such as Matlab) would work as well, though.

**Building the job**:

``datalad (containers-)run`` does not support concurrent execution in the *same* dataset clone.
The solution is as easy as it is stubborn: We simply create one throw-away dataset clone for each job.

.. find-out-more:: how does one create throw-away clones?

    One way to do this are :term:`ephemeral clone`\s, an alternative is to make :term:`git-annex` disregard the datasets annex completely using ``git annex dead here``.
    The latter is more appropriate for this context -- we could use an ephemeral clone, but that might deposit data of failed jobs at the origin location, if the job runs on a shared filesystem.

Using throw-away clones involves a build-up, result-push, and tear-down routine for each job.
It sounds complex and tedious, but this actually works well since datasets are by nature made for such decentralized, collaborative workflows.
We treat cluster compute nodes like contributors to the analyses: They clone the analysis dataset hierarchy into a temporary location, run the computation, push the results, and remove their temporary dataset again [#f3]_.
The complete routine is done in a single script, which will be submitted as a job.
Here, we build the general structure of this script, piece by piece.

The compute job clones the dataset to a unique place, so that it can run a ``containers-run`` command inside it without interfering with any other job.
The first part of the script is therefore to navigate to a unique location, and clone the analysis dataset to it.

.. find-out-more:: How can I get a unique location?

   On common HTCondor setups, ``/tmp`` directories in individual jobs are a job-specific local Filesystem that are not shared between jobs -- i.e., unique locations!
   An alternative is to create a unique temporary directory, e.g., with the ``mktemp -d`` command on Unix systems.

.. code-block:: bash

   # go into unique location
   $ cd /tmp
   # clone the analysis dataset
   $ datalad clone /path/to/parallel_analysis ds
   $ cd ds

This dataset clone is *temporary*: It will exist over the course of one analysis/job only, but before it is being purged, all of the results it computed will be pushed to the original dataset.
This requires a safe-guard: If the original dataset receives the results from the dataset clone, it knows about the clone and its state.
In order to protect the results from someone accidentally synchronizing (updating) the dataset from its linked dataset after is has been deleted, the clone should be created as a "trow-away clone" right from the start.
By running ``git annex dead here``, :term:`git-annex` disregards the clone, preventing the deletion of data in the clone to affect the original dataset.

.. code-block:: bash

   $ git annex dead here

The ``datalad push`` to the original clone location of a dataset needs to be prepared carefully.
The job computes *one* result (out of of many results) and saves it, thus creating new data and a new entry with the run-record in the dataset history.
But each job is unaware of the results and :term:`commit`\s produced by other branches.
Should all jobs push back the results to the original place (the :term:`master` :term:`branch` of the original dataset), the individual jobs would conflict with each other or, worse, overwrite each other (if you don't have the default push configuration of Git).

The general procedure and standard :term:`Git` workflow for collaboration, therefore, is to create a change on a different, unique :term:`branch`, push this different branch, and integrate the changes into the original master branch via a :term:`merge` in the original dataset [#f4]_.

In order to do this, prior to executing the analysis, the script will *checkout* a unique new branch in the analysis dataset.
The most convenient name for the branch is the Job-ID, an identifier under which the job scheduler runs an individual job.
This makes it easy to associate a result (via its branch) with the log, error, or output files that the job scheduler produces [#f5]_, and the real-life example will demonstrate these advantages more concretely.

.. code-block:: bash

   # git checkout -b <name> creates a new branch and checks it out
   $ git checkout -b "job-$JOBID"

Importantly, the ``$JOB-ID`` isn't hardcoded into the script but it can be given to the script as an environment or input variable at the time of job submission.
The code snippet above uses a bash :term:`environment variable` (``$JOBID``, as indicated by the all-upper-case variable name with a leading ``$``).
It will be defined in the job submission -- this is shown and explained in detail in the respective paragraph below.

Next, its time for the :command:`containers-run` command.
The invocation will depend on the container and dataset configuration (both of which are demonstrated in the real-life example in the next section), and below, we pretend that the container invocation only needs an input file and an output file.
These input file is specified via a bash variables (``$inputfile``) that will be defined in the script and provided at the time of job submission via command line argument from the job scheduler, and the output file name is based on the input file name.

.. code-block:: bash

   $ datalad containers-run \
      -m "Computing results for $inputfile" \
      --explicit \
      --output "aggregate_${inputfile}" \
      --input "rawdata/$inputfile" \
      -n code/containers/mycontainer \
      '{inputs}' '{outputs}'

After the ``containers-run`` execution in the script, the results can be pushed back to the dataset :term:`sibling` ``origin`` [#f6]_::

   $ datalad push --to origin


Pending a few yet missing safe guards against concurrency issues and the definition of job-specific (environment) variables, such a script can be submitted to any job scheduler with identifiers for input files, output files, and a job ID as identifiers for the branch names.
This workflow sketch takes care of everything that needs to be done apart from combining all computed results afterwards.

.. find-out-more:: Fine-tuning: Safe-guard concurrency issues

   An important fine-tuning is missing:
   Cloning and pushing *can* still run into concurrency issues in the case when one job clones the original dataset while another job is currently pushing its results into this dataset.
   Therefore, a trick can make sure that no two clone or push commands are executed at *exactly* the same time.
   This trick uses `file locking <https://en.wikipedia.org/wiki/File_locking>`_, in particular the tool `flock <https://www.tutorialspoint.com/unix_system_calls/flock.htm>`_, to prevent exactly concurrent processes.
   This is done by prepending ``clone`` and ``push`` commands with ``flock --verbose $DSLOCKFILE``, where ``$DSLOCKFILE`` is a text file placed into ``.git/`` at the time of job submission, provided via environment variable (see below and the paragraph "Job submission").
   This is a non-trivial process, but luckily, you don't need to understand file locking or ``flock`` in order to follow along -- just make sure that you copy the usage of ``$DSLOCKFILE`` in the script and in the job submission.

.. find-out-more:: Variable definition

   There are two ways to define variables that a script can use:
   The first is by defining :term:`environment variable`\s, and passing this environment to the compute job.
   This can be done in the job submission file.
   To set and pass down the job-ID and a lock file in HTCondor, one can supply the following line in the job submission file::

      environment = "JOBID=$(Cluster).$(Process) DSLOCKFILE=$ENV(PWD)/.git/datalad_lock"

   The second way is via shell script command line arguments.
   Everything that is given as a command line argument to the script can be accessed in the script in the order of their appearance via ``$``.
   A script invoked with ``bash myscript.sh <inputfile> <parameter> <argument>`` can access ``inputfile`` with ``$1``, ``parameter`` with ``$2``, and ``<argument>`` with ``$3``.
   If the job scheduler takes care of iterating through input file names, the relevant input variable for the simplistic example could thus be defined in the script as follows::

      inputfile=$1

With fine tuning and variable definitions in place, the only things missing are a :term:`shebang` at the top of the script, and some shell settings for robust scripting with verbose log files (``set -e -u -x``).
Here's how the full general script looks like.

.. code-block:: bash

    #!/bin/bash

    # fail whenever something is fishy, use -x to get verbose logfiles
    set -e -u -x

    # we pass arbitrary arguments via job scheduler and can use them as variables
    fileid=$1
    ...

    # go into unique location
    cd /tmp
    # clone the analysis dataset. flock makes sure that this does not interfere
    # with another job finishing and pushing results back at the same time
    flock --verbose $DSLOCKFILE datalad clone /path/to/parallel_analysis ds
    cd ds
    # announce the clone to be temporary
    git annex dead here
    # checkout a unique branch
    git checkout -b "job-$JOBID"
    # run the job
    datalad containers-run \
      -m "Computing data $inputfile" \
      --explicit \
      --output "aggregate_${inputfile}" \
      --input "rawdata/$inputfile" \
      -n code/containers/mycontainer \
      '{inputs}' '{outputs}'
    # push, with filelocking as a safe-guard
    flock --verbose $DSLOCKFILE datalad push --to origin

    # Done - job handler should clean up workspace

Its a short script that encapsulates a complete workflow.
Think of it as the sequence of necessary DataLad commands you would need to do in order to compute a job.
You can save this script into your analysis dataset, e.g., as ``code/analysis_job.sh``, and make it executable (such that it is executed automatically by the program specified in the :term:`shebang`)using ``chmod +x code/analysis_job.sh``.

**Job submission**:

Job submission now only boils down to invoking the script for each participant with the relevant command line arguments (e.g., input files for our artificial example) and the necessary environment variables (e.g., the job ID that determines the branch name that is created, and one that points to a lockfile created beforehand once in ``.git``).
Job scheduler such as HTCondor can typically do this with automatic variables.
They for example have syntax that can identify subject IDs or consecutive file numbers from consistently named directory structure, access the job ID, loop through a predefined list of values or parameters, or use various forms of pattern matching.
Examples of this are demonstrated `here <https://jugit.fz-juelich.de/inm7/training/htcondor/-/blob/master/03_define_jobs.md>`_.
Thus, the submit file takes care of defining hundreds or thousands of variables, but can still be lean even though it queues up hundreds or thousands of jobs.
Here is a submit file that could be employed:

.. find-out-more:: HTCondor submit file

   .. code-block:: bash

      universe       = vanilla
      get_env        = True
      # resource requirements for each job, determined by
      # investigating the demands of a single test job
      request_cpus   = 1
      request_memory = 20G
      request_disk   = 210G

      executable     = $ENV(PWD)/code/analysis_job.sh

      # the job expects to environment variables for labeling and synchronization
      environment = "JOBID=$(Cluster).$(Process) DSLOCKFILE=$ENV(PWD)/.git/datalad_lock"
      log    = $ENV(PWD)/../logs/$(Cluster).$(Process).log
      output = $ENV(PWD)/../logs/$(Cluster).$(Process).out
      error  = $ENV(PWD)/../logs/$(Cluster).$(Process).err
      arguments = $(inputfile)
      # find all input data, based on the file names in the source dataset.
      # The pattern matching below finds all *files* that match the path
      # "rawdata/acquisition_*.txt".
      # Each relative path to such a file name will become the value of `inputfile`,
      # the argument given to the executable (the shell script).
      # This will queue as many jobs as file names match the pattern
      queue inputfile matching files rawdata/acquisition_*_.txt

   How would the first few jobs look like that this submit file queues up?
   It would send out the commands

   .. code-block:: bash

      ./code/analysis_job.sh rawdata/acquisition_day1year1_.txt
      ./code/analysis_job.sh rawdata/acquisition_day2year1_.txt
      [...]

   and each of them are send to a compute node with at least 1 CPU, 20GB of RAM and 210GB of disk space.
   The log, output, and error files are saved under a HTCondor-specific Process and Cluster ID in a log file directory (which would need to be created for HTCondor!).
   Two environment variables, ``JOBID`` (defined from HTCondor-specific Process and Cluster IDs) and ``DSLOCKFILE`` (for file locking), will be defined on the compute node.

All it takes to submit is a single ``condor_submit <submit_file>``.


**Merging results**:
Once all jobs are finished, the results lie in individual branches of the original dataset.
The only thing left to do now is merging all of these branches into :term:`master` -- and potentially solve any merge conflicts that arise.
Usually, merging branches is done using the ``git merge`` command with a branch specification.
For example, in order to merge one job branch into the :term:`master` :term:`branch`, one would need to be on ``master`` and run ``git merge <job branch name>``.
Given that the parallel job execution could have created thousands of branches, and that each ``merge`` would lead to a commit, in order to not inflate the history of the dataset with hundreds of :term:`merge` commits, one can do a single `Octopus merges <https://git-scm.com/docs/git-merge#Documentation/git-merge.txt-octopus>`_ of all branches at once.

.. find-out-more:: What is an octopus merge?

   Usually a commit that arises from a merge has two *parent* commits: The *first parent* is the branch the merge is being performed from, in the example above, ``master``. The *second parent* is the branch that was merged into the first.

   However, ``git merge`` is capable of merging more than two branches simultaneously if more than a single branch name is given to the command.
   The resulting merge commit has as many parent as were involved in the merge.
   If a commit has more than two parents, if is affectionately called an "Octopus" merge.

   Octopus merges require merge-conflict-free situations, and will not be carried out whenever manual resolution of conflicts is needed.

The merge command can be assembled quickly.
If all result branches were named ``job-<JOBID>``, a complete list of branches is obtained with the following command::

   $ git branch -l | grep 'job-' | tr -d ' '

This command line call translates to: "list all branches. Of those branches, show me those that contain ``job-``, and remove (``tr -d``) all whitespace."
This call can be given to ``git merge`` as in

.. code-block:: bash

   $ git merge -m "Merge results from job cluster XY" $(git branch -l | grep 'job-' | tr -d ' ')

Voilà -- the results of all provenance-tracked job executions merged into the original dataset.
If you are interested in seeing this workflow applied in a real analysis, read on into the next section, :ref:`hcpenki`.

.. rubric:: Footnotes

.. [#f1] To re-read about :command:`datalad run`'s ``--explicit`` option, take a look into the section :ref:`run5`.

.. [#f2] The `ReproNim container-collection <https://github.com/repronim/containers>`_ is a DataLad dataset that contains a range of preconfigured containers for neuroimaging.

.. [#f3] Clean-up routines can, in the case of common job schedulers, be taken care of by performing everything in compute node specific ``/tmp`` directories that are wiped clean after job termination.

.. [#f4] For an analogy, consider a group of software developers: Instead of adding code changes to the main :term:`branch` of a repository, they develop in their own repository clones and on dedicated, individual feature branches. This allows them to integrate their changes back into the original repository with as little conflict as possible. To find out why a different branch is required to enable easy pushing back to the original dataset, please checkout the explanation on :ref:`pushing to non-bare repositories <nonbarepush>` in the section on :ref:`help`.

.. [#f5] Job schedulers can commonly produce log, error, and output files and it is advisable to save them for each job. Usually, job schedulers make it convenient to save them with a job-ID as an identifier. An example of this for HTCondor is shown in the Findoutmore in :ref:`jobsubmit`.

.. [#f6] When a dataset is cloned from any location, this original location is by default known as the :term:`sibling`/:term:`remote` ``origin`` to the clone.
