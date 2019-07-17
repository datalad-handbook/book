.. _philo:

A brief overview of DataLad
---------------------------

There can be numerous reasons why you ended up with this handbook in front of
you -- We don't know who you are, or why you are here.
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
**not only making sharing, retrieving and linking (meta-)data easy**,
but it assists with the combination of all things
necessary in the digitial workflow of data and science.

As built-in, but *optional* features, DataLad yields FAIR resources -- for example
:term:`metadata` and :term:`provenance` -- and anything (or everything)
can be easily shared *should the user want this*.


The DataLad Philosophy
^^^^^^^^^^^^^^^^^^^^^^

DataLad is built up on a handful of principles. It is this underlying philosophy
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
   `share one of the largest whole brain MRI images in the world <https://www.nature.com/articles/sdata201732>`_,
   organize your private music library, keep track of all
   `cat memes <https://www.diabloii.net/gallery/data/500/medium/moar6-cat.jpg>`_
   on the internet, or `anything else <https://media.giphy.com/media/3o6YfXCehdioMXYbcs/giphy.gif>`_.

#. **A dataset is a Git repository**. If you know the :term:`version control` system
   :term:`Git`, and what you can use it for,
   then take notice that everything you can use Git for also applies to everything managed
   by DataLad -- plus much more. If you don't know Git,
   (which is completely fine), rest assured that this is a good feature.
   You will experience much of Git working its
   magic underneath the hood when you use DataLad. Do also rest assured that there
   is no need to panic if you don't know Git -- there is no necessity
   to learn Git to follow along in learning and using DataLad.

#. **A DataLad dataset can take care of managing and version controlling arbitrarily large data**.
   To do this, it has an optional *annex* for (large) file content:
   Thanks to this annex, DataLad can easily track files that are many TB or PB in size
   (something that git couldn't do, and that allows you to restore previous versions of data,
   transform and work with it while capturing all :term:`provenance`,
   or share it with whomever you want). At the same time, DataLad does all of the magic
   necessary to get this awesome feature to work quietly in the background.
   The annex is set-up automatically, and the tool :term:`Git-annex`
   (https://git-annex.branchable.com) manages it all underneath the hood. Worry-free
   large-content data management? Check!

#. Deep in the core of DataLad lies the social principle to
   **minimize custom procedures and data structures**. DataLad will not transform
   your files into something that only DataLad or a specialized tool can read.
   A PDF file (or any other type of
   file) stays a PDF file (or whatever other type of file it was)
   whether it is managed by DataLad or not. This guarantees that users will not loose
   data or data access if DataLad would vanish from their system, or even when DataLad
   would vanish from the face of Earth. Using DataLad thus does not require or generate
   datastructures that can only be used or read with DataLad -- DataLad doesn't
   tie you down, it liberates you.

#. Furthermore, DataLad is developed for **complete decentralization**.
   There is no required central server or service necessary to use DataLad. In this
   way, no central infrastructure needs to be maintained (or paid for) --
   your own laptop is the perfect place to live for your DataLad project, as is your
   institutions webserver, or any other common computational infrastructure you
   might be using.

#. Simultaneously, though, DataLad aims to
   **maximize the (re-)use of existing 3rd-party data resources and infrastructure**.
   Users *can* use existing central infrastructure should they want to.
   DataLad works with any infrastructure from :term:`Github` to
   Dropbox, Figshare or institutional
   repositories, enabling users to harvest all of the advantages of their preferred
   infrastructure without tying anyone down to central services.

These principles hopefully gave you some idea of what to expect from DataLad,
cleared some worries that you might have had, and highlighted what DataLad is and what
it is not.

Additionally, as some last key facts about DataLad, it comes with a
command line interface enabling usage from within a terminal, and a Python API
to use its features within your software and scripts. And while being a general,
multi-purpose tool, it comes with plenty of extensions that provide helpful,
domain specific features that may very well fit your precise use case.

But enough of the abstract talking.
You came here to learn, and the handbook will not waste your time further by
requiring you to only read -- let's start to *use* DataLad.
