.. index:: ! 3-001
.. _3-001:
.. _usecase_datastore:

Building a scalable data storage for scientific computing
---------------------------------------------------------

.. index:: ! Usecase; Remote Indexed Archive (RIA) store

Research can require enormous amounts of data. Such data needs to be accessed by
multiple people at the same time, and is used across a diverse range of
computations or research questions.
The size of the dataset, the need for simultaneous access and transformation
of this data by multiple people, and the subsequent storing of multiple copies
or derivatives of the data constitutes a challenge for computational clusters
and requires state-of-the-art data management solutions.
This use case details a model implementation for a scalable data storage
solution, suitable to serve the computational and logistic demands of data
science in big (scientific) institutions, while keeping workflows for users
as simple as possible. It elaborates on

#. How to implement a scalable :term:`Remote Indexed Archive (RIA) store` to flexibly
   store large amounts of DataLad datasets, potentially remote to lower storage
   strains on computing infrastructure,
#. How disk-space aware computing can be eased by DataLad based workflows and
   enforced by infrastructural incentives and limitations, and
#. How to reduce technical complexities for users and encourage reproducible,
   version-controlled, and scalable scientific workflows.

.. note::

   This usecase is technical in nature and aimed at IT/data management
   personnel seeking insights into the technical implementation and
   configuration of a RIA store or into its workflows. In particular, it
   describes the RIA data storage and workflow implementation as done in INM-7,
   research centre Juelich, Germany.

   **Note further**: Building a RIA store requires **DataLad version 0.13.0**
   or higher.


The Challenge
^^^^^^^^^^^^^

The data science institute XYZ consists of dozens of people: Principle
investigators, PhD students, general research staff, system administration,
and IT support. It does research on important global issues, and prides
itself with ground-breaking insights obtained from elaborate and complex
computations run on a large scientific computing cluster.
The datasets used in the institute are big both in size and number of files,
and expensive to collect.
Therefore, datasets are used for various different research questions, by
multiple researchers. Every member of the institute has an account on an expensive
and large compute cluster, and all of the data exists in dedicated directories
on this server. However, researchers struggle with the technical overhead of
data management *and* data science.
In order to work on their research questions without modifying
original data, every user creates their own copies of the full data in their
user account on the cluster -- even if it contains many files that are not
necessary for their analysis. In addition, as version control is not a standard
skill, they add all computed derivatives and outputs, even old versions, out of
fear of losing work that may become relevant again. Thus, an excess of (unorganized)
data copies and derivatives exists in addition to the already substantial
amount of original data. At the same time, the compute cluster is both the
data storage and the analysis playground for the institute. With data
directories of several TB in size, *and* computationally heavy analyses, the
compute cluster is quickly brought to its knees: Insufficient memory and
IOPS starvation make computations painstakingly slow, and hinder scientific
progress. Despite the elaborate and expensive cluster setup, exciting datasets
can not be stored or processed, as there just doesn't seem to be enough disk
space.

Therefore, the challenge is two-fold: On an infrastructural level, institute XYZ
needs a scalable, flexible, and maintainable data storage solution for their
growing collection of large datasets.
On the level of human behavior, researchers not formerly trained in data
management need to apply and adhere to advanced data management principles.

The DataLad approach
^^^^^^^^^^^^^^^^^^^^

The compute cluster is refurbished to a state-of-the-art data management
system.
For a scalable and flexible dataset storage, the data store is a
:term:`Remote Indexed Archive (RIA) store` -- an extendable, file-system based
storage solution for DataLad datasets that aligns well with the requirements of
scientific computing (infrastructure).
The RIA store is configured as a git-annex ORA-remote ("optional remote archive")
special remote for access to annexed keys in the store and so that full
datasets can be (compressed) 7-zip archives.
The latter is especially useful in case of filesystem inode
limitations, such as on HPC storage systems: Regardless of a dataset's number of
files and size, (compressed) 7zipped datasets use only few inodes, but retain the
ability to query available files.
Unlike traditional solutions, both because of the size of the large
amounts of data, and for more efficient use of compute power for
calculations instead of data storage, the RIA store is set up *remote*: Data is
stored on a different machine than the one the scientific analyses are computed
on. While unconventional, it is convenient, and perfectly possible with DataLad.

The infrastructural changes are accompanied by changes in the mindset and
workflows of the researchers that perform analyses on the cluster.
By using a RIA store, the institute's work routines are adjusted around
DataLad datasets. Simple configurations, distributed system-wide with DataLad's
run-procedures, or basic data management principles improve the efficiency and
reproducibility of research projects:
Analyses are set-up inside of DataLad datasets, and for every
analysis, an associated ``project`` is created under the namespace of the
institute on the institute's :term:`GitLab` instance automatically. This does
not only lead to vastly simplified version control workflows, but also to
simplified access to projects and research logs for collaborators and supervisors.
Input data gets installed as subdatasets from the RIA store. This automatically
links analyses projects to data sets, and allows for fine-grained access of up
to individual file level. With only precisely needed data, analyses datasets are
already much leaner than with previous complete dataset copies, but as data can
be re-obtained on-demand from the store, original input files or files that are
easily recomputed can safely be dropped to save even more disk-space.
Beyond this, upon creation of an analysis project, the associated GitLab project
is automatically configured as a remote with a publication dependency on the
data store, thus enabling vastly simplified data publication routines and
backups of pristine results: After computing their results, a
:command:`datalad push` is all it takes to backup and share ones scientific
insights. Thus, even with a complex setup of data store, compute infrastructure,
and repository hosting, configurations adjusted to the compute infrastructure
can be distributed and used to mitigate any potential remaining technical overhead.
Finally, with all datasets stored in a RIA store and in a single place, any remaining
maintenance and query tasks in the datasets can be performed by data management
personnel without requiring domain knowledge about dataset contents.


Step-by-step
^^^^^^^^^^^^

The following section will elaborate on the details of the technical
implementation of a RIA store, and the workflow requirements and incentives for
researchers. Both of them are aimed at making scientific analyses on a
compute cluster scale and can be viewed as complimentary but independent.

.. note::

   Some hardware-specific implementation details are unique to the real-world
   example this usecase is based on, and are not a requirement. In this particular
   case of application, for example, a *remote* setup for a RIA store made sense:
   Parts of an old compute cluster and of the super computer at the Juelich
   supercomputing centre (JSC) instead of the institutes compute cluster are used
   to host the data store. This may be an unconventional storage location,
   but it is convenient: The data does not strain the compute cluster, and with
   DataLad, it is irrelevant where the RIA store is located. The next subsection
   introduces the general layout of the compute infrastructure and some
   DataLad-unrelated incentives and restrictions.

Incentives and imperatives for disk-space aware computing
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

On a high level, the layout and relationships of the relevant computational
infrastructure in this usecase are as follows:
Every researcher has a workstation that they can access the compute cluster with.
On the compute clusters' head node, every user account has their own
home directory. These are the private spaces of researchers and are referred to
as ``$HOME`` in :numref:`fig_store`.
Analyses should be conducted on the cluster's compute nodes (``$COMPUTE``).
``$HOME`` and ``$COMPUTE`` are not managed or trusted by data management personnel,
and are seen as *ephemeral* (short-lived).
The RIA store (``$DATA``) can be accessed both from ``$HOME`` and ``$COMPUTE``,
in both directions: Researchers can pull datasets from the store, push new
datasets to it, or update (certain) existing datasets. ``$DATA`` is the one location
in which experienced data management personnel ensures back-up and archival, performs
house-keeping, and handles :term:`permissions`, and is thus were pristine raw
data is stored or analysis code or results from ``$COMPUTE`` and ``$HOME`` should
end up in. This aids organization, and allows a central management of back-ups
and archival, potentially by data stewards or similar data management personnel
with no domain knowledge about data contents.

.. _fig_store:

.. figure:: ../artwork/src/ephemeral_infra.svg
   :alt: A simple, local version control workflow with datalad.
   :figwidth: 80%

   Trinity of research data handling: The data store (``$DATA``) is managed and
   backed-up. The compute cluster (``$COMPUTE``) has an analysis-appropriate structure
   with adequate resources, but just as users workstations/laptops (``$HOME``),
   it is not concerned with data hosting.

One aspect of the problem are disk-space unaware computing workflows. Researchers
make and keep numerous copies of data in their home directory and perform
computationally expensive analyses on the headnode of a compute cluster because
they do not know better, and/or want to do it in the easiest way possible.
A general change for the better can be achieved by imposing sensible limitations
and restrictions on what can be done at which scale:
Data from the RIA store (``$DATA``) is accessible to researchers for exploration
and computation, but the scale of the operations they want to perform can require
different approaches.
In their ``$HOME``, researchers are free to do whatever they want as long as it
is within the limits of their machines or their user accounts (100GB). Thus,
researchers can explore data, test and develop code, or visualize results,
but they can not create complete dataset copies or afford to keep an excess of
unused data around.
Only ``$COMPUTE`` has the necessary hardware requirements for expensive computations.
Thus, within ``$HOME``, researchers are free to explore data
as they wish, but scaling requires them to use ``$COMPUTE``. By using a job
scheduler, compute jobs of multiple researchers are distributed fairly across
the available compute infrastructure. Version controlled (and potentially
reproducible) research logs and the results of the analyses can be pushed from
``COMPUTE`` to ``$DATA`` for back-up and archival, and hence anything that is
relevant for a research project is tracked, backed-up, and stored, all without
straining available disk-space on the cluster afterwards. While the imposed
limitations are independent of DataLad, DataLad can make sure that the necessary
workflows are simple enough for researchers of any seniority, background, or
skill level.

Remote indexed archive (RIA) stores
"""""""""""""""""""""""""""""""""""

A RIA store is a storage solution for DataLad datasets that can be flexibly
extended with new datasets, independent of static file names or directory
hierarchies, and that can be (automatically) maintained or queried without
requiring expert or domain knowledge about the data. At its core, it is a flat,
file-system based repository representation of any number of datasets, limited
only by disk-space constrains of the machine it lies on.

Put simply, a RIA store is a dataset storage location that allows for access to
and collaboration on DataLad datasets.
The high-level workflow overview is as follows: Create a dataset,
use the :command:`datalad create-sibling-ria` command to establish a connection
to an either pre-existing or not-yet-existing RIA store, publish dataset contents
with :command:`datalad push`, (let others) clone the dataset from the
RIA store, and (let others) publish and pull updates. In the
case of large, institute-wide datasets, a RIA store (or multiple RIA stores)
can serve as a central storage location that enables fine-grained data access to
everyone who needs it, and as a storage and back-up location for all analyses datasets.
Beyond constituting central storage locations, RIA stores also ease dataset
maintenance and queries:
If all datasets of an institute are kept in a single RIA store, questions such
as "Which projects use this data as their input?", "In which projects was the
student with this Git identity involved?", "Give me a complete research log
of what was done for this publication", or "Which datasets weren't used in the
last 5 years?" can be answered automatically with Git tools, without requiring
expert knowledge about the contents of any of the datasets, or access to the
original creators of the dataset.
To find out more about RIA stores, check out section :ref:`riastore`.

.. todo::

   Add a paragraph on the setup in INM-7 once it exists (bulk nodes, project-wise
   RIA stores, stores in home directories, etc.

RIA store workflows
"""""""""""""""""""

.. todo::

   Sketch a RIA store workflow from a user's perspective

**Configurations can hide the technical layers**

Setting up a RIA store and appropriate siblings is fairly easy -- it requires
only the :command:`datalad create-sibling-ria` command.
However, in the institute this usecase describes, in order to spare users
knowing about RIA stores, custom configurations are distributed via DataLad's
run-procedures to simplify workflows further and hide the technical layers of
the RIA setup:

A `custom procedure <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_
performs the relevant sibling setup with a fully configured link to the RIA store,
and, on top of it, also creates an associated repository with a publication
dependency on the RIA store to an institute's GitLab instance [#f1]_.
With a procedure like this in place system-wide, an individual researcher only
needs to call the procedure right at the time of dataset creation, and has a
fully configured and set up analysis dataset afterwards:

.. code-block:: bash

   $ datalad create -c inm7 <PATH>

Working in this dataset will require only :command:`datalad save` and
:command:`datalad push` commands, and configurations ensure that the projects
history and results are published where they need to be: The RIA store, for storing
and archiving the project including data, and GitLab, for exposing the projects
progress to the outside and ease collaboration or supervision. Users do not need
to know the location of the store, its layout, or how it works -- they can go
about doing their science, while DataLad handles publications routines.

In order to get input data from datasets hosted in the datastore without requiring
users to know about dataset IDs or construct ``ria+`` URLs, superdatasets
get a :term:`sibling` on :term:`GitLab` or :term:`GitHub` with a human readable
name. Users can clone the superdatasets from the web hosting service, and obtain data
via :command:`datalad get`. A concrete example for this is described in
the usecase :ref:`usecase_HCP_dataset`. While :command:`datalad get` will retrieve file
or subdataset contents from the RIA store, users will not need to bother where
the data actually comes from.

Summary
"""""""

The infrastructural and workflow changes around DataLad datasets in RIA stores
improve the efficiency of the institute:

With easy local version control workflows and DataLad-based data management routines,
researchers are able to focus on science and face barely any technical overhead for
data management. As file content for analyses is obtained *on demand*
via :command:`datalad get`, researchers selectively obtain only those data they
need instead of having complete copies of datasets as before, and thus save disk
space. Upon :command:`datalad push`, computed results and project histories
can be pushed to the data store and the institute's GitLab instance, and be thus
backed-up and accessible for collaborators or supervisors. Easy-to-reobtain input
data can safely be dropped to free disk space on the compute cluster. Sensible
incentives for computing and limitations on disk space prevent unmanaged clutter.
With a RIA store full of bare git repositories, it is easily maintainable by data
stewards or system administrators. Common compression or cleaning operations of
Git and git-annex are performed without requiring knowledge about the data
inside of the store, as are queries on interesting aspects of datasets, potentially
across all of the datasets of the institute.
With a remote data store setup, the compute cluster is efficiently used for
computations instead of data storage. Researchers can not only compute their
analyses faster and on larger datasets than before, but with DataLad's version
control capabilities their work also becomes more transparent, open, and
reproducible.


.. rubric:: Footnotes

.. [#f1] To re-read about DataLad's run-procedures, check out section
         :ref:`procedures`. You can find the source code of the procedure
         `on GitLab <https://jugit.fz-juelich.de/inm7/infrastructure/inm7-datalad/blob/master/inm7_datalad/resources/procedures/cfg_inm7.py>`_.

