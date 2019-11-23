.. _inm7usecase_hammerpants:

Using the INM-7 Hammerpants data store
--------------------------------------

This usecase is a step-by-step instruction on how to work with the distributed
data store ``HAMMERPANTS`` at INM-7, Research Centre Juelich. It details how to

- Create an analysis dataset with an appropriate configuration
- Install datasets from ``HAMMERPANTS`` and obtain file content
- Publish results back to the data store for archival and back-up, and
- House-keep within datasets and work disk-space-aware

.. findoutmore:: Why is it called HAMMERPANTS?

   Because the data store is maintained, backed-up, and managed by data curators and system
   administrators -- not users.

   .. only:: html

        .. figure:: https://media1.tenor.com/images/35ee8a604228fc32fec3fa5007570e61/tenor.gif
           :alt: McHammer

           You indeed can't touch this.


The Challenge
^^^^^^^^^^^^^

INM-7 is a prestigious institute and well-known in neuroscience and beyond for
the high-impact studies on large cohorts and patient groups its researchers conduct.
With increasing numbers of people working in the institute, and increasing
data set sizes for their analyses, the expensive compute cluster of the
institute is slowly but steadily brought to its knees: Data sets of many TB in size
exist as multiple duplicates in various versions or processing stages in many
locations, analysis directories overflow with results recomputed again and again
whenever analysis scripts were updated, and even abandoned work-in-progress datasets
kept because of a lack of documentation on what needs to be kept inflate the disk
usage of the compute cluster.

With less and less disk space available, the cluster aches under the
additional load of large computing jobs. Analyses run slower and slower because of
insufficient memory. Moreover, because no job scheduler [#f1]_ exists on the cluster
that would incentivize reasonably sized partial analyses steps, analyses can be
large chunks that run for days or weeks. With this, important analyses often sit
idle for weeks, and important computations are delayed.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

A new cluster is build, but beyond this, a new concept for data storage and management
is implemented as well. The changes in infrastructure and workflows not only improve
the efficiency and scalability of the institute's computations, but also the
reproducibility and audibility of individual research projects.

Instead of storing data in random locations on the cluster,
a remote data store, ``HAMMERPANTS``, is set up. This data store holds all of
the institute's large data sets as DataLad datasets, is sufficiently backed-up, and
managed by experienced system administrators and data curators.

Users set up their analyses in DataLad datasets, configured with an institute-specific
run-procedure.
In these analysis datasets, data from the data store can be installed as subdatasets.
Given that not all file contents in a dataset will be relevant for all analysis,
users can obtain the precise required content on demand, instead of all of the dataset
contents.
Simple local version control workflows help researchers to keep track of file modifications
regardless of file size, and best practices and standards for structuring
data analyses datasets contribute to making analysis projects intuitively organized
and reproducible.
Upon analysis completion, results can be published to the datastore to ensure archival
and backup that complies to funding requirements.

Other than data retrieval and storage, computational analysis workflows are improved by
incentivizing computational best-practices and preventing computational catastrophes.
Users' ``$HOME`` directories are limited to a maximum of 100 GB in size - this allows
researchers to explore data and test their scripts as they wish, but prevents uncontrolled
clutter and data piling up. In order to scale and compute analysis on large datasets,
computations have to run on the compute nodes of the cluster, managed by the job
scheduler `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ to ensure optimal
resource usage and fair job allocation. The use of the job scheduler further incentivizes
small-chunked, partial analysis-steps, that can run fast and in parallel, making
computations more efficient.

Because researchers work more disk-space aware than before, and because the remote
``HAMMERPANTS`` data store ensures data is sufficiently backed up and easily
available again, input datasets from the data store are dropped to save disk space
once an analysis is finished.

.. todo::

   Add how the cluster aids computing jobs at the JSC


Step-by-Step
^^^^^^^^^^^^

Once the ``HAMMERPANTS`` storage is set up, only experienced, specialized data
curation, system administration, and maintenance personnel has write access to
it. This ensure that organizational and file name standards are kept, prevents
accidental changes or deletion of data, rules out that multiple duplicates of
datasets exist, and leads to standardized workflows for applications for datasets
and their download.

On the level of users ``$HOME`` directories and the compute cluster, sensible
limits and rules prevent blatant misuse of computational infrastructure and
compute resources without restricting researchers. Users' ``$HOME`` directories are
limited to 100GB in size. This is sufficient to explore and visualize data,
develop analysis scripts, test analysis workflows, and conduct small-sized
analyses, but it would be insufficient to host large-scale computation projects.
This ensures that the clusters head node is not taken hostage by single user's
computations. Instead, large analyses have to be computed on the dedicated compute
nodes. Access to such nodes is only possible via the job scheduler HTCondor.
The job scheduler ensures that computational resources are distributed fairly
among all users, and that all jobs are distributed across the cluster in the
most efficient way possible [#f1]_.


.. figure:: ../artwork/src/ephemeral_infra.svg
   :alt: A simple, local version control workflow with datalad.
   :figwidth: 80%

   Trinity of research data handling: The data store (``$DATA``) is managed and
   backed-up. The compute cluster (``$COMPUTE``) has an analysis-appropriate structure
   with adequate resources, but just as users workstations/laptops (``$HOME``),
   it is not concerned with data hosting.

When working on projects and interacting with the data store, technical overhead
for users is kept minimal. A basic set of DataLad commands suffices.
Any new analysis is set up as a DataLad dataset, using the ``cfg_inm7``
run-procedure [#f2]_::

   $ datalad create -c inm7 mynewproject

This procedure takes care of all the relevant set up. It configures a complete
linkage to ``HAMMERPANTS``: Both on the institutes GitLab instance and on
``HAMMERPANTS``, a sibling-project is automatically created and linked.
Afterwards, datasets from the datastore can be installed with
:command:`datalad install` [#f3]_::

   $ datalad install --dataset mynewdataset \
   --source <ID/URL> \
   mynewdataset/inputs/...

Datasets are identified through their ID or a URL

.. todo::

   - How do people get to know these IDs? This needs an example.
   - At which point does Alex create projects for people?

Installing the datasets as subdatasets into the analysis project dataset establishes
a link between the datasets, and ensures modularity.

File content from the subdatasets can be retrieved on demand, either with
:command:`datalad get` calls from the command line or within scripts (using DataLad's
Python API, or standard system calls in any other programming language [#f4]_)
or by appropriate ``--input`` specification in a :command:`datalad run` command [#f5]_.

After creation & configuration of a dataset and installation of input datasets
from ``HAMMERPANTS`` researchers can use their standard workflows to develop and
script their analysis. Once the analysis is set up, a HTCondor submit file needs
to be written. This file takes care of handing the computational job for management
and fair, efficient distribution to HTCondor. While this sounds scary to users that
are unfamiliar with HTCondor, the process is intuitive and fast, and there documentation
and tutorials are available [#f1]_.

The results computed from the analyses need to be backed-up and archived. To do this,
users :command:`datalad publish` their results back to ``HAMMERPANTS`` for longterm-storage::

   $ datalad publish --to inm7

.. todo::

   mention how this makes it easier to be FAIR, link researchers to their data and
   results, and ensures legal compliance to funding requirements or the requirements
   that journals have after publication of a manuscript.

Data analyses projects comply to the YODA principles [#f6]_. The projects are build up
from separate, but linked modular entities. Once analyses are finished, contents of the linked
subdatasets from the ``HAMMERPANTS`` data store can be removed with :command:`datalad drop` [#f7]_.
This is best practice and saves disk space by removing local copies of datasets
that are stored in ``HAMMERPANTS``. By using :command:`datalad drop`, the input
data content is removed (saving disk space), but the linkage to the input dataset
is kept, so that it can be re-obtained automatically.

.. todo::

   summarize how easy the workflow is.


.. rubric:: Footnotes

.. [#f1] A job scheduler is a computer application for managing computational workload
         on a cluster by controlling unattended background program execution of jobs.
         This is commonly called *batch scheduling*. Job schedulers such as
         `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ queue jobs for
         execution on high-throughput computing infrastructure, monitor the state
         of the jobs, and allocate jobs to available compute resources (cluster nodes).
         You can find documentation and tutorials on using HTCondor in the
         `INM7 docs <https://docs.inm7.de/cluster/htcondor/>`_ and on
         `JuGit <https://jugit.fz-juelich.de/inm7/training/htcondor>`_.

.. [#f2] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on Gitlab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_
         if you are interested.
         To re-read about creating datasets, start with the first chapter on the
         Basics of DataLad datasets starting at section :ref:`createDS`.

.. [#f3] To re-read about installing datasets and how to interact with installed
         datasets, as well as basic concepts on dataset nesting, check out the
         sections starting from :ref:`installds`.

.. [#f4] A general example analysis that makes use of DataLad functions within scripts is in
         section :ref:`yodaproject`.

.. [#f5] To re-read about the :command:`datalad run` command, checkout the chapter
         "DataLad, Run!", starting with section :ref:`run`.

.. [#f6] To re-read about the YODA principles, checkout section :ref:`yoda`.

.. [#f7] Find out how drop works in section :ref:`filesystem`. See it in action
         in the use case

         .. todo::

            link updated neuroimaging use case once in the book.