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

A new cluster is build, but beyond this a new concept for data storage and management
is implemented as well. The changes in infrastructure and workflows not only improve
the efficiency and scalability of the institute's computations, but also the
reproducibility and audibility of individual research projects.

Instead of storing data in random locations on the cluster,
a distributed data store, ``HAMMERPANTS``, is set up. This data store holds all of
the institute's large data sets as DataLad datasets, is sufficiently backed-up, and
managed by experienced system administrators.

Users set up their analyses in DataLad datasets, configured with an institute-specific
run-procedure.
In these analysis datasets, data from the data store can be installed as subdatasets.
Given that not all file contents in a dataset will be relevant for all analysis,
users can obtain the precise required content on demand.
Simple local version control workflows help researchers to keep track of file modifications
regardless of file size, and best practices and standards for structuring
data analyses datasets contribute to making analysis projects intuitively organized
and reproducible.
Upon analysis completion, results can be published to the datastore to ensure archival
and backup.

Users' ``$HOME`` directories are limited to a maximum of 100GB in size - this allows
any researchers to explore data and test their scripts as they wish, but prevents uncontrolled
clutter and data piles. In order to scale and compute analysis on large datasets,
computations have to run on the compute nodes of the cluster, managed by the job
scheduler `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ to ensure optimal
resource usage and fair job allocation. The use of the job scheduler further incentivizes
small-chunked, partial analysis-steps, that can run fast and in parallel.
Once an analysis has been performed, input datasets from the data store can be
dropped to save disk space on the cluster.

.. figure:: ../artwork/src/ephemeral_infra.svg
   :alt: A simple, local version control workflow with datalad.
   :figwidth: 80%

   Trinity of research data handling: The data store (``$DATA``) is managed and
   backed-up. The compute cluster (``$COMPUTE``) has an analysis-appropriate structure
   with adequate resources, but just as users workstations/laptops (``$HOME``),
   it is not concerned with data hosting.


Step-by-Step
^^^^^^^^^^^^

Any new analysis is set up as a DataLad dataset, using the ``cfg_inm7`` run-procedure [#f2]_::

   $ datalad create -c inm7 mynewproject

This procedure takes care of all the relevant set up. Afterwards, a dataset from the
datastore can be installed with :command:`datalad install` [#f3]_::

   $ datalad install --dataset mynewdataset \
   --source <ID/URL> \
   mynewdataset/inputs/...

Datasets are identified through their ID or a URL

.. todo::

   How do people get to know these IDs?

Installing the datasets as subdatasets into the analysis project dataset establishes
a link between the datasets, and ensures modularity.

File content from the subdatasets can be retrieved on demand, either with
:command:`datalad get` calls from the command line or within scripts (using DataLad's
Python API)

.. todo::

   finish and link this section

or by appropriate ``--input`` specification in a :command:`datalad run` command [#f4]_.

.. rubric:: Footnotes

.. [#f1] A job scheduler is a computer application for managing computational workload
         on a cluster by controlling unattended background program execution of jobs.
         This is commonly called *batch scheduling*. Job schedulers such as
         `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ queue jobs for
         execution on high-throughput computing infrastructure, monitor the state
         of the jobs, and allocate jobs to available compute resources (cluster nodes).

.. [#f2] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on Gitlab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_
         if you are interested.
         To re-read about creating datasets, start with the first chapter on the
         Basics of DataLad datasets starting at section :ref:`createDS`.

.. [#f3] To re-read about installing datasets and how to interact with installed
         datasets, as well as basic concepts on dataset nesting, check out the
         sections starting from :ref:`installds`.

.. [#f4] To re-read about the :command:`datalad run` command, checkout the chapter
         "DataLad, Run!", starting with section :ref:`run`