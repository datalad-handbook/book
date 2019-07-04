
********
Glossary
********


.. glossary::

   absolute path
      The complete path from the root of the file system. Absolute paths always start with ``/``.
      Example: ``/home/user/studyforrest-phase-2/sub-02``. See also :term:`relative path`.

   commit message
      A consise summary of changes you should attach to a ``datalad save`` command. This summary will
      show up in your :term:`Datalad dataset` history.

   DataLad dataset
      A DataLad dataset is a Git repository that may or may not have a data annex that is used to
      manage data referenced in a dataset. In practice, most DataLad datasets will come with an annex.

   DataLad subdataset
      A DataLad dataset contained within a different DataLad dataset (the parent or :term:`DataLad superdataset`)

   DataLad superdataset
      A DataLad dataset that contains one or more levels of other DataLad datasets (:term:`DataLad subdataset`)

   Git
      A version control system to track changes made to small-sized files over time. You can find out
      more about git in `this (free) book <https://git-scm.com/book/en/v2>`_
      or `these interactive Git tutorials <https://try.github.io/>`_ on :term:`Github`

   Git-annex
      TODO

   Github
      GitHub is an online platform where one can store and share version controlled projects
      using Git (and thus also DataLad project).

   Gitk
      TODO

   metadata
      "Data about data": Information about one or more aspects of data used to summmarize
      basic information, for example means of create of the data, creator or author, size,
      or purpose of the data. For example, a digital image may include metadata that
      describes how large the picture is, the color depth, the image resolution, when the image
      was created, the shutter speed, and other data.

   provenance
      A record that describes entities and processes that were involved in producinng or influencing
      a digital resource. It provides a critical foundation for assessing authenticity, enables trust,
      and allows reproducibility.

   relative path
      A path related to the present working directory. Relative paths never start with ``/``.
      Example: ``../data/studyforrest-phase-2/sub-02``. See also :term:`absolute path`.

   symlink
      TODO

   tig
      A text-mode interface for git that allows you to easily browse through your commit history.
      It is not part of git and needs to be installed. Find out more `here <https://jonas.github.io/tig/>`_.

   version control
      The management of changes to documents or other collections of information
