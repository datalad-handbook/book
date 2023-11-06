.. _sharethirdparty:

Beyond shared infrastructure
----------------------------

Data sharing potentially involves a number of different elements:

.. figure:: ../artwork/src/publishing/startingpoint.svg
   :width: 60%

   An overview of all elements potentially included in a publication workflow.

Users on a common, shared computational infrastructure such as an :term:`SSH server`
can share datasets via simple installations with paths, without any involvement of third party storage providers or repository hosting services:

.. figure:: ../artwork/src/publishing/clone_combined.svg

But at some point in a dataset's life, you may want to share it with people that
can't access the computer or server your dataset lives on, store it on other infrastructure
to save diskspace, or create a backup.
When this happens, you will want to publish your dataset to repository hosting
services (for example :term:`GitHub`, :term:`GitLab`, or :term:`Gin`)
and/or third party storage providers (such as Dropbox_, Google_,
`Amazon S3 buckets <https://aws.amazon.com/s3>`_,
the `Open Science Framework`_ (OSF), and many others).

This chapter tackles different aspects of dataset publishing.
The remainder of this section talks about general aspects of dataset publishing, and
illustrates the idea of using third party services as :term:`special remote`\s from
which annexed file contents can be retrieved via :dlcmd:`get`.

The upcoming section :ref:`gin` shows you one of the most easy ways to publish your
dataset publicly or for selected collaborators and friends.
If you don't want to dive in to all the details on dataset sharing, it is safe to
directly skip ahead to this section, and have your dataset published in only a few minutes.

Other sections in this chapter will showcase a variety of ways to publish datasets
and their contents to different services:
The section :ref:`share_hostingservice` demonstrates how to publish datasets to any
kind of Git repository hosting service.
The sections :ref:`s3` and :ref:`dropbox` are concrete examples of sharing datasets
publicly or with selected others via different cloud services.
The section :ref:`gitlfs` talks about using the centralized, for-pay service
`Git LFS`_ for sharing dataset content on GitHub, and the
section :ref:`figshare` shows built-in dataset export to services such as
`figshare.com <https://figshare.com>`__.

Leveraging third party infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways to make datasets available for others:

- You can **publish your dataset to a repository with annex support** such as :term:`Gin` or the OSF_ [#f1]_. This is the easiest way to share datasets and all their contents. Read on in the section :ref:`gin` or consult the tutorials of the `datalad-osf extension`_ to learn how to do this.

- You can **publish your dataset to a repository hosting service**, and **configure an external resource that stores your annexed data**. Such a resource can be a private web server, but also a third party services cloud storage such as Dropbox_, Google_, `Amazon S3 buckets <https://aws.amazon.com/s3>`_, `Box.com <https://www.box.com>`_, `owncloud <https://owncloud.com>`_, `sciebo <https://hochschulcloud.nrw>`_, or many more.

- You can **export your dataset statically** as a snapshot to a service such as  `Figshare <https://figshare.com>`__ or the OSF_ [#f1]_.

- You can **publish your dataset to a repository hosting service** and ensure that
  all dataset contents are either available from pre-existing public sources or can be recomputed from a :term:`run record`.

Dataset contents and third party services influence sharing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because DataLad datasets are :term:`Git` repositories, it is possible to
:dlcmd:`push` datasets to any Git repository hosting service, such as
:term:`GitHub`, :term:`GitLab`, :term:`Gin`, :term:`Bitbucket`, `Gogs <https://gogs.io>`_,
or Gitea_.
You have already done this in section :ref:`yoda_project` when you shared your ``midterm_project`` dataset via :term:`GitHub`.

However, most Git repository hosting services do not support hosting the file content
of the files managed by :term:`git-annex`.
For example, the the results of the analysis in section :ref:`yoda_project`,
``pairwise_comparisons.png`` and ``prediction_report.csv``, were not published to
GitHub: There was meta data about their file availability, but if a friend cloned
this dataset and ran a :dlcmd:`get` command, content retrieval would fail
because their only known location is your private computer to which only you have access.
Instead, they would need to be recomputed from the :term:`run record` in the dataset.

When you are sharing DataLad datasets with other people or third party services,
an important distinction thus lies in *annexed* versus *not-annexed* content, i.e.,
files that stored in your dataset's :term:`annex` versus files that are committed
into :term:`Git`.
The third-party service of your choice may have support for both annexed and non-annexed files, or only one them.

.. figure:: ../artwork/src/publishing/publishing_network_publishparts2.svg
   :width: 80%

   Schematic difference between the Git and git-annex aspect of your dataset, and where each part *usually* gets published to.


The common case: Repository hosting without annex support and special remotes
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Because DataLad datasets are :term:`Git` repositories, it is possible to
:dlcmd:`push` datasets to any Git repository hosting service, such as
:term:`GitHub`, :term:`GitLab`, :term:`Gin`, :term:`Bitbucket`, `Gogs <https://gogs.io>`_,
or Gitea_.
But while anything that is managed by Git is accessible in repository hosting services, they usually don't support storing annexed data [#f2]_.

When you want to publish a dataset to a Git repository hosting service to allow others to easily find and clone it, but you also want others to be able to retrieve annexed files in this dataset via :dlcmd:`get`, annexed contents need to be pushed to additional storage hosting services.
The hosting services can be all kinds of private, institutional, or commercial services, and their location will be registered in the dataset under the concept of a :term:`special remote`.

.. index::
   pair: special remote; git-annex concept
.. find-out-more:: What is a special remote

   A special-remote is an extension to Git’s concept of remotes, and can
   enable :term:`git-annex` to transfer data from and possibly to places that are not Git
   repositories (e.g., cloud services or external machines such as an HPC
   system). For example, an *s3* special remote uploads and downloads content
   to AWS S3, a *web* special remote downloads files from the web, and *datalad-archive*
   extracts files from the annexed archives, etc. Don’t envision a special-remote
   as merely a physical place or location – a special-remote is a protocol that
   defines the underlying transport of your files to and/or from a specific location.

To register a special remote in your dataset and use it for file storage, you need to configure the service of your choice and *publish* the annexed contents to it. Afterwards, the published dataset (e.g., via :term:`GitHub` or :term:`GitLab`) stores the information about where to obtain annexed file contents from such that
:dlcmd:`get` works.
Once you have configured the service of your choice, you can push your datasets Git history to the repository hosting service and the annexed contents to the special remote. DataLad also makes it easy to push these different dataset contents exactly where they need to be automatically via a :term:`publication dependency`.

Exemplary walk-throughs for Dropbox_, `Amazon S3 buckets <https://aws.amazon.com/s3>`_, and `Git LFS`_ can be found in the upcoming sections in this chapter.
But the general workflow looks as follows:

From your perspective (as someone who wants to share data), you will
need to

- (potentially) install/setup the relevant *special-remote*,
- create a dataset sibling on GitHub/GitLab/... for others to install from,
- set up a *publication dependency* between repository hosting and special remote, so that annexed contents are automatically pushed to the special remote when ever you update the sibling on the Git repository hosting site,
- publish your dataset.

This gives you the freedom to decide where your data lives and
who can have access to it. Once this set up is complete, updating and
accessing a published dataset and its data is almost as easy as if it would
lie on your own machine.

From the perspective of a consumer (as someone who wants to obtain your dataset),
they will need to

- (potentially) install the relevant *special-remote* (dependent on the third-party service you chose) and
- perform the standard :dlcmd:`clone` and :dlcmd:`get` commands
  as necessary.

Thus, from a collaborator's perspective, with the exception of potentially
installing/setting up the relevant *special-remote*, obtaining your dataset and its
data is as easy as with any public DataLad dataset.
While you have to invest some setup effort in the beginning, once this
is done, the workflows of yours and others are the same that you are already
very familiar with.

.. figure:: ../artwork/src/publishing/clone_url.svg
   :width: 60%


If you are interested in learning how to set up different services as special remotes, you can take a look at the sections :ref:`s3`, :ref:`dropbox` or :ref:`gitlfs` for concrete examples with DataLad datasets, and the general section :ref:`share_hostingservice` on setting up dataset siblings.
In addition, there are step-by-step walk-throughs in the documentation of git-annex for services such as `S3 <https://git-annex.branchable.com/tips/public_Amazon_S3_remote>`_, `Google Cloud Storage <https://git-annex.branchable.com/tips/using_Google_Cloud_Storage>`_,
`Box.com <https://git-annex.branchable.com/tips/using_box.com_as_a_special_remote>`__,
`Amazon Glacier <https://git-annex.branchable.com/tips/using_Amazon_Glacier>`_,
`OwnCloud <https://git-annex.branchable.com/tips/owncloudannex>`__, and many more.
Here is the complete list: `git-annex.branchable.com/special_remotes <https://git-annex.branchable.com/special_remotes>`_.



The easy case: Repository hosting with annex support
""""""""""""""""""""""""""""""""""""""""""""""""""""

There are a few Git repository hosting services with support for annexed contents.
One of them is :term:`Gin`.
What makes them extremely convenient is that there is no need to configure a special remote -- creating a :term:`sibling` and running :dlcmd:`push` is enough.

.. figure:: ../artwork/src/publishing/publishing_network_publishgin.svg
   :width: 80%

Read the section :ref:`gin` for a walk-through.

The uncommon case: Special remotes with repository hosting support
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Typically, storage hosting services such as cloud storage providers do not provide
the ability to host Git repositories.
Therefore, it is typically not possible to :dlcmd:`clone` from a cloud storage.
However, a number of :term:`datalad extension`\s have been created that equip cloud storage providers with the ability to also host Git repositories.
While they do not get the ability to display repositories the same way that pure
Git repository hosting services like GitHub do, they do get the super power of becoming clonable.

One example for this is the Open Science Framework, which can become the home of datasets by using the `datalad-osf extension`_.
As long as you and your collaborators have the extension installed, annexed dataset
contents and the Git repository part of your dataset can be pushed or cloned in one go.

.. figure:: ../artwork/src/publishing/publishing_network_publishosf.svg
   :width: 80%

Please take a look at the documentation and tutorials of the `datalad-osf extension`_ for examples and more information.

The creative case: Ensuring availability using only repository hosting
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

When you only want to use pure Git repository hosting services without annex support, you can still allow others to obtain (some) file contents with some creativity:

For one, you can use commands such as :dlcmd:`download-url` or :dlcmd:`addurls`  to retrieve files from web sources and register their location automatically.
The first Chapter :ref:`chapter_datasets` demonstrates :dlcmd:`download-url`.

Other than this, you can rely on digital provenance in the form of :term:`run record`\s that allow consumers of your dataset to recompute a result instead of :dlcmd:`get`\ing it.
The midterm-project example in section :ref:`yoda_project` has been an example for this.


The static case: Exporting dataset snapshots
""""""""""""""""""""""""""""""""""""""""""""

While DataLad datasets have the great advantage that they carry a history with all kinds of useful digital provenance and previous versions of files, it may not in all cases be necessary to make use of this advantage.
Sometimes, you may just want to share or archive the most recent state of the dataset as a snapshot.

DataLad provides the ability to do this out of the box to arbitrary locations, and support for specific services such as `Figshare <https://figshare.com>`__.
Find out more information on this in the section :ref:`figshare`.
Other than that, some :term:`datalad extension`\s allow an export to additional services such as the Open Science Framework.

General information on publishing datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beyond concrete examples of publishing datasets, some general information may be useful in addition:
The section :ref:`push` illustrates the DataLad command :dlcmd:`push`, a command that handles every publication operation, regardless of the type of published content or its destination.
In addition to this, the section :ref:`privacy` contains tips and strategies on publishing datasets without leaking potentially private contents or information.

.. _dropbox: https://www.dropbox.com
.. _google: https://www.google.com
.. _gitea: https://about.gitea.com
.. _git lfs: https://git-lfs.com
.. _Open Science Framework: https://osf.io
.. _OSF: https://osf.io
.. _datalad-osf extension: https://docs.datalad.org/projects/osf

.. rubric:: Footnotes

.. [#f1] Requires the `datalad-osf extension`_.

.. [#f2] In addition to not storing annexed data, most Git repository hosting services also have a size limit for files kept in Git. So while you could *theoretically* commit a sizable file into Git, this would not only negatively impact the performance of your dataset as Git doesn't handle large files well, but it would also `prevent your dataset to be published to a Git repository hosting service like GitHub <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>`_.

.. [#f5] Old versions of :term:`GitLab`, on the other hand, provide a git-annex configuration. It
         is disabled by default, and to enable it you would need to have administrative
         access to the server and client side of your GitLab instance.
         Alternatively, GitHub can integrate with
         `Git LFS`_, a non-free, centralized service
         that allows to store large file contents. :ref:`gitlfs` shows an example on how to use their free trial version.
