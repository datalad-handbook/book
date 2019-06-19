********
Glossary
********


.. glossary::

   absolute path
      The complete path from the root of the file system. Absolute paths always start with ``/``.
      Example: ``/home/user/studyforrest-phase-2/sub-02``. See also :term:`relative path`.

   Datalad dataset
      A DataLad dataset is a Git repository that may or may not have a data annex that is used to
      manage data referenced in a dataset. In practice, most DataLad datasets will come with an annex.

   Datalad subdataset
      A datalad dataset contained within a different datalad dataset (the parent or :term:`Datalad superdataset`)

   Datalad superdataset
      A datalad dataset that contains one or more levels of other datalad datasets (:term:`Datalad subdataset`)

   git
      A version control system. (TODO: add references)

   git-annex
      TODO

   gitk
      TODO

   relative path
      A path related to the present working directory. Relative paths never start with ``/``.
      Example: ``../data/studyforrest-phase-2/sub-02``. See also :term:`absolute path`.

   tig
      A tool to display git histories (TODO: improve this)
