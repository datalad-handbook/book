.. _philo:

######################
The DataLad Philosophy
######################

DataLad is a software tool developed to aid with everything related to the
evolution of digital objects. It is not only keeping track of code, and it is not
only keeping track of data, but it assists with the combination of all things
necessary in the digitial workflow of science.
As built-in, but *optional* features, DataLad yields FAIR resources - for example
:term:`metadata` and :term:`provenance` - and everything can be easily shared
*should the user want this*.

DataLad is built up on a handful of principles.

#. **DataLad only cares (knows) about two things: Datasets and files.**
   A dataset is a collection of files and folders (see the upcoming section on :ref:`datasets`),
   and a file is the smallest unit any dataset can contain. Therefore, DataLad is a
   content-management system that operates on the units of files, and, as most people
   in any field work with files on their computer, DataLad at its core is completey
   domain-agnostic, general-purpose tool.

#. **A dataset is a Git repository**. If you know :term:`git`, and what you can use it for:
   This applies to everything managed by DataLad as well. If you don't know git
   (which is completely fine): You will experience many git features working their
   magic underneath the hood when you use DataLad, with no necessity to learn any git at all.

#. **A dataset can have an optional annex for (large) file content tracking**:
   Thanks to this annex, DataLad can track TB or PB in file size (something that git
   couldn't do). The annex is set-up automatically, and :term:`git-annex`
   (https://git-annex.branchable.com) manages it all underneath the hood.

#. Deep in the core of DataLad is the social principle of
   **minimizing custom procedures and data structures: Users must not loose data or data access, if DataLad would vanish**
   Using DataLad does not require or generate datastructures that can only be
   used or read with DataLad.

#. Furthermore, DataLad is developed for
   **complete decentralization, with no required central server or service**.
   This way, no central infrastructure anyone would need to pay for needs to be maintained -
   your own laptop is the perfect place to live for your DataLad project for example.
   ...

#. ... but simultanteously, DataLad aims to
   **maximize use of existing 3rd-party data resources and infrastructure re-use**
   Users *can* use existing central infrastructure should they want to.
   DataLad works with any infrastructure from Github to Figshare or institutional
   repositories, enabling users to harvest all of the advantages of their preferred
   infrastructure, without tying anyone down to central services.



.. todo::

   Command line interface and Python API
   Elaborate on Provenance capture and linkage between datasets
   Maybe also include more on FAIR and metadata
   Talk about other projects or services that use datalad: HeudiConv, OpenNeuro
   Talk briefly about extensions (that they exist)