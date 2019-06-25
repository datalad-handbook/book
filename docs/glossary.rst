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

   git
      A version control system. (TODO: add references)

   git-annex
      TODO

   gitk
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

   tig
      A tool to display git histories (TODO: improve this)

   version control
      TODO
