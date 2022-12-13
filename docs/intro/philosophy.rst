.. _philo:

A brief overview of DataLad
---------------------------

There can be numerous reasons why you ended up with this handbook in front of
you -- We do not know who you are, or why you are here.
You could have any background, any amount of previous experience with
DataLad, any individual application to use it for,
any level of maturity in your own mental concept of what DataLad
is, and any motivational strength to dig into this software.

All this brief section tries to do is to provide a minimal, abstract explanation
of what DataLad is, to give you, whoever you may be, some idea of what kind of
tool you will learn to master in this handbook, and to combat some prejudices
or presumptions about DataLad one could have.

To make it short, DataLad is a software tool developed to aid with everything
related to the evolution of digital objects.

It is **not only keeping track of code**, it is
**not only keeping track of data**, it is
**not only making sharing, retrieving and linking data (and metadata) easy**,
but it assists with the combination of all things
necessary in the digital workflow of data and science.

As built-in, but *optional* features, DataLad yields FAIR resources -- for example
:term:`metadata` and :term:`provenance` -- and anything (or everything)
can be easily shared *should the user want this*.


On Data
^^^^^^^

Everyone uses data. But once it exists, it does not suffice for most data
to simply reside unchanged in a single location for eternity.

Most **data need to be shared** -- may it be a digital collection of family
photos, a genomic database between researchers around the world, or inventory
lists of one company division to another. Some data are public and should be
accessible to everyone.  Other data should circulate only among a select few.
There are various ways to distribute data, from emailing files to sending
physical storage media, from pointers to data locations on shared file systems
to using cloud computing or file hosting services. But what if there was an
easy, **generic way of sharing and obtaining data**?


Most **data changes and evolves**. A scientist extends a data collection or
performs computations on it. When applying for a new job, you update your
personal CV.  The documents required for an audit need to comply to a new
version of a common naming standard and the data files are thus renamed.  It may
be easy to change data, but it can be difficult to revert a change, get
information on previous states of this data, or even simply find out how a piece
of data came into existence. This latter aspect, the :term:`provenance` of data
-- information on its lineage and *how* it came to be in its current state -- is
often key to understanding or establishing trust in data.  In collaborative
fields that work with small-sized data such as Wikipedia pages or software
development, :term:`version control` tools are established and indispensable. These
tools allow users to keep track of changes, view previous states, or restore
older versions.  How about a **version control system for data**?


If data are shared as a copy *of one state* of its history, **keeping all shared
copies of this data up-to-date** once the original data changes or evolves is at
best tedious, but likely impossible. What about ways to easily **update data and
its shared copies**?


The world is full of data. The public and private sector make use of it to
understand, improve, and innovate the complex world we live in.  Currently, this
process is far from optimal.  In order for society to get the most out of public
data collections, public **data need to be** `FAIR <https://www.go-fair.org/>`_: Findable,
Accessible, Interoperable, and Reusable. Apart from easy ways to share or update
shared copies of data, extensive **metadata** is required to identify data, link
data collections together, and make them findable and searchable in a
standardized way. Can we also easily **attach metadata to our data and its
evolution**?


**DataLad** is a general purpose tool for managing everything involved in the
digital workflow of using data -- regardless of the data's type, content, size,
location, generation, or development.  It provides functionality to share,
search, obtain, and version control data in a distributed fashion, and it aids
managing the evolution of digital objects in a way that fulfills the `FAIR <https://www.go-fair.org/>`_
principles.


The DataLad Philosophy
^^^^^^^^^^^^^^^^^^^^^^
From a software point of view, DataLad is a command line tool, with an additional
Python API to use its features within your software and scripts.
While being a general, multi-purpose tool, there are also plenty of extensions
that provide helpful, domain specific features that may very well fit your precise use case.

But beyond software facts, DataLad is built up on a handful of principles. It is this underlying philosophy
that captures the spirit of what DataLad is, and here is a brief overview on it.

#. **DataLad only cares (knows) about two things: Datasets and files.**
   A DataLad dataset is a collection of files in folders.
   And a file is the smallest unit any dataset can contain. Thus, a DataLad
   dataset has the same structure as any directory on your computer, and
   DataLad itself can be conceptualized as a content-management system that operates
   on the units of files. As most people
   in any field work with files on their computer, at its core,
   **DataLad is a completely domain-agnostic, general-purpose tool to manage data**.
   You can use it whether you have a PhD in Neuroscience and want to
   `share one of the largest whole brain MRI images in the world <https://github.com/datalad-datasets/bmmr-t1w-250um>`_,
   organize your private music library, keep track of all
   `cat memes <https://pbs.twimg.com/profile_images/897468832910004224/tJYwYsf3.jpg>`_
   on the internet, or `anything else <https://media.giphy.com/media/3o6YfXCehdioMXYbcs/giphy.gif>`_.

#. **A dataset is a Git repository**. 
   All features of the :term:`version control` system :term:`Git`
   also apply to everything managed by DataLad – plus many more.
   If you do not know or use Git yet, there is no need to panic – there is no necessity to 
   learn all of Git to follow along in learning and using DataLad. You will 
   experience much of Git working its magic underneath the hood when you use DataLad, 
   and will soon start to appreciate its features. Later, you may want to know more
   on how DataLad uses Git as a fundamental layer and learn some of Git.

#. **A DataLad dataset can take care of managing and version controlling arbitrarily large data**.
   To do this, it has an optional *annex* for (large) file content.
   Thanks to this :term:`annex`, DataLad can easily track files that are many TB or PB in size
   (something that Git could not do, and allows you to transform, work with, and restore previous 
   versions of data, while capturing all :term:`provenance`,
   or share it with whomever you want). At the same time, DataLad does all of the magic
   necessary to get this awesome feature to work quietly in the background.
   The annex is set-up automatically, and the tool :term:`git-annex`
   (https://git-annex.branchable.com) manages it all underneath the hood. Worry-free
   large-content data management? Check!

#. Deep in the core of DataLad lies the social principle to
   **minimize custom procedures and data structures**. DataLad will not transform
   your files into something that only DataLad or a specialized tool can read.
   A PDF file (or any other type of
   file) stays a PDF file (or whatever other type of file it was)
   whether it is managed by DataLad or not. This guarantees that users will not lose
   data or access if DataLad would vanish from their system (or from the face of the 
   Earth). Using DataLad thus does not require or generate
   data structures that can only be used or read with DataLad -- DataLad does not
   tie you down, it liberates you.

#. Furthermore, DataLad is developed for **complete decentralization**.
   There is no required central server or service necessary to use DataLad. In this
   way, no central infrastructure needs to be maintained (or paid for).
   Your own laptop is the perfect place for your DataLad project to live, as is your
   institution's webserver, or any other common computational infrastructure you
   might be using.

#. Simultaneously, though, DataLad aims to
   **maximize the (re-)use of existing 3rd-party data resources and infrastructure**.
   Users *can* use existing central infrastructures should they want to.
   DataLad works with any infrastructure from :term:`GitHub` to
   `Dropbox <https://www.dropbox.com>`_, `Figshare <https://figshare.com/>`_
   or institutional repositories,
   enabling users to harvest all of the advantages of their preferred
   infrastructure without tying anyone down to central services.

These principles hopefully gave you some idea of what to expect from DataLad,
cleared some worries that you might have had, and highlighted what DataLad is and what
it is not. The section :ref:`executive_summary` will give you a one-page summary
of the functionality and commands you will learn with this handbook. But before we
get there, let's get ready to *use* DataLad. For this, the next
section will show you how to use the handbook.

