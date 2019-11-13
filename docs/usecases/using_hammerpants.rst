.. _hammerpants:

Using the INM-7 Hammerpants data store
--------------------------------------

This usecase is a step-by-step instruction on how to work with the distributed
data store ``HAMMERPANTS`` at INM-7, Research Centre Juelich. It details how to

- Create an analysis dataset with an appropriate configuration
- Install datasets from ``HAMMERPANTS`` and obtain file content
- Publish results back to the data store for archival and back-up
- House-keep within datasets and work disk-space-aware

.. findoutmore:: Why is it called HAMMERPANTS?

   Stop! Hammertime!

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

With fewer and fewer available disk space available, the cluster aches under the
additional load of large computing jobs. Analyses run slower and slower because of
insufficient memory. Moreover, because no job scheduler [#f1]_ exists on the cluster
that would incentivize reasonably sized partial analyses steps, analyses can be
large chunks that run for days or weeks. With this, important analyses often sit
idle for weeks, and important computations are delayed.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

A new cluster is build, but beyond this a new concept for data storage and management
is implemented as well. Instead of storing data in random locations on the cluster,
a distributed data store, ``HAMMERPANTS``, is set up. This data store holds all of
the institutes large data sets as DataLad datasets, is sufficiently backed-up, and
managed by experienced system administrators.

Analyses are set up in specifically configured DataLad datasets. In these, data
from the data store can be installed as subdatasets, and the precise required
content can be obtained on demand.
Simple local version control workflows help researchers to keep track of file modifications
regardless of file size, and best practices and standards for structuring
data analyses datasets contribute to making analysis projects intuitively organized.
Upon analysis completion, results can be published to the datastore to ensure archival
and backup.

Users ``$HOME`` directories are limited to a maximum of 100GB in size - this allows
any researchers to explore data and test their scripts, but prevents uncontrolled
clutter and data piles. In order to scale and compute analysis on large datasets,
computations have to ran on the compute nodes of the cluster, managed by the job
scheduler `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ to ensure optimal
resource usage and fair job allocation.

Once an analysis has been performed, input datasets from the data store can be
dropped to save disk space on the cluster.

Step-by-Step
^^^^^^^^^^^^

.. rubric:: Footnotes

.. [#f1] A job scheduler is a computer application for managing computational workload
         on a cluster by controlling unattended background program execution of jobs.
         This is commonly called *batch scheduling*. Job schedulers such as
         `HTCondor <https://research.cs.wisc.edu/htcondor/>`_ queue jobs for
         execution on high-throughput computing infrastructure, monitor the state
         of the jobs, and allocate jobs to available compute resources (cluster nodes).