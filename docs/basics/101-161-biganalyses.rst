.. _big_analysis:

Calculate in greater numbers
----------------------------

When creating and populating datasets yourself it may be easy to introduce
subdatasets whenever and where ever necessary. It may not be as straightforward
when you are not population datasets yourself, but when *software* or
analyses scripts suddenly dump vast amounts of output.
Certain analysis software can create myriads of files. A standard
`FEAT analysis <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide>`_ [#f1]_
in `FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_, for example, can easily output
several dozens of directories and up to hundreds of result files per subject.
If this software runs on a substantially sized input dataset, the results may be
overwhelming.

This section demonstrates some tips on how to prevent swamping your datasets
with files. Note: If you accidentally got stuck with an overflowing dataset,
first checkout section :ref:`cleanup`.

Solution: Subdatasets
^^^^^^^^^^^^^^^^^^^^^

To stick to the example of FEAT, here is a quick overview on what this software
does: It is modelling neuroimaging data based on general linear modelling (GLM),
and creates web page analyses reports, color activation images, time-course plots
of data and model, preprocessed intermediated data, images with filtered data,
statistical output images, colour rendered output images, log files, and many more.
Plenty of these outputs are text-based, but there are also many sizable files.
Depending on the type of analyses that is run, not all types of outputs
will be relevant. At the end of the analysis, one usually has subject-specific
directories with many subdirectories filled with result files, log files,
intermediate and preprocessed files, and "higher-level" group directories that
aggregate results over subjects.

With such a setup, the output directories (subjects, grouplevel) can be

Solutions without creating subdatasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to scale up without going through the complexities of
creating several subdatasets. It involves compromising, though.
The following section highlights a few caveats to bear in mind if you attempt
a big analyses in single-level datasets, and outlines solutions that do not
involve subdatasets. If you have something to add, please
`get in touch <https://github.com/datalad-handbook/book/issues/new/>`_.

Too many files
""""""""""""""

**Caveat**: Drown a dataset with too many files.

**Examples**: The FSL FEAT analysis mentioned in the introduction produces
several 100k files, but not all of these files are important.
``tsplot/``, for example, is a directory that contains time series plots for
various data and results, and may be of little interested for many analyses once
general quality control is done.

**Solutions**:

- Don't put irrelevant files under version control at all: Consider creating
  a *.gitignore* file with patterns that match files or directories that are of no
  relevance to you. These files will not be version controlled or saved to your
  dataset. Section :ref:`gitignore` can tell you more about this. Be mindful, though:
  Having too many files in a single directory can still be problematic for your
  file system. A concrete example: Consider your analyses create logfiles that
  are not precious enough to be version controlled. Adding ``logs/*`` to your
  ``.gitignore`` file and saving this change will keep these files out of
  version control.

- Similarly, you can instruct :command:`datalad run` to save only specific directories
  or files by specifying them with the ``--output`` option and executing the command
  with the ``--explicit`` flag. This may be more suitable an approach if you know
  what you want to keep rather than what is irrelevant.

Too many files in Git
"""""""""""""""""""""

**Caveat**: Drown Git because of configurations.

**Example**: If your dataset is configured with a configuration such as ``text2git`` or if
you have modified your ``.gitattributes`` file [#f2]_ to store files below a certain
size of certain types in :term:`Git` instead of :term:`git-annex`, an
excess of sudden text files can still be overwhelming in terms of total file size.
Several thousand, or tens of thousand, text files may still add up to several GB
in size even if they are each small in size.

**Solutions**:

- Add files to git-annex instead of Git: Consider creating custom ``largefile``
  rules for directories that you generate these files in or for patterns that
  match file names that do not need to be in Git. This way, these files will be
  put under git-annex's version control. A concrete example: Consider that your
  analyses output a few thousand textfiles into all ``sub-*/correlations/``
  directories in your dataset. Appending
  ``sub-*/correlations/* annex.largefiles=anything`` to ``.gitattributes`` and
  saving this change will store all of in the dataset's annex instead of in Git.
- Don't put irrelevant files under version control at all: Consider creating
  a *.gitignore* file with patterns that match files or directories that are of no
  relevance to you. These files will not be version controlled or saved to your
  dataset. Section :ref:`gitignore` can tell you more about this. Be mindful, though:
  Having too many files in a single directory can still be problematic for your
  file system. A concrete example: Consider your analyses create logfiles that
  are not precious enough to be version controlled. Adding ``logs/*`` to your
  ``.gitignore`` file and saving this change will keep these files out of
  version control.













.. rubric:: Footnotes

.. [#f1] FEAT is a software tool for model-based fMRI data analysis and part of of
         `FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_.

.. [#f2] Read up on these configurations in the chapter :ref:`chapter_config`.