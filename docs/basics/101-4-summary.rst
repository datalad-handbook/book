Starting from scratch: Summary
------------------------------

In the last few pages, we have discovered the basics of starting a DataLad dataset from scratch,
and making simple modifications *locally*:

* An empty dataset can be created with the ``datalad create`` command. Its useful to add a description
  to the dataset and use the ``-c text2git`` configuration, but we will see later why.
  Command structure: ``datalad create --description "here is a description" -c text2git PATH``

* Thanks to :term:`Git` and :term:`Git-annex`, the dataset has a history to track files and their
  modifications. Build in Git tools (``git log``) or external tools (such as ``tig``) allow to explore
  the history.

* The ``datalad save`` command records the current state of the dataset to the history. Make it a habit
  of specifying a concise commit message to summarize the change, and do not forget to specify the
  path to the file (change) that should be saved to history! Remember, if you run a ``datalad save`` without
  specifying a path, all untracked files and all file changes will be committed to the history together!
  Command structure: ``datalad save -m "here is a commit message" PATH``

* The typical local workflow consists of an initial ``datalad save -m "Add file XY" PATH`` to instruct
  DataLad to track the file and its content. Afterwards, one *modifies* the file, and then *saves* the
  changes to the history (and repeats these two steps).

.. todo::

   make a graphic of this workflow

* ``datalad status`` reports the current state of the dataset. Its a very helpful command you should
  run frequently to check for untracked or modified content.


Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simple local workflows allow you to version control changing small files, for example your CV, your code,
or a book that you are working on.
Additionally, you can add very large files to your datasets history.

Currently, this is more of "best-practice building" than seeing DataLad magic. You can already explore
the history, but for now, its been only informative, and hasn't been used for anything more fancy.
The next lectures in ``DataLad-101`` will focus on utilizing the history in order to undo mistakes,
changes to large content (as opposed to small content we have been modifying so far), and consuming
existing datasets.