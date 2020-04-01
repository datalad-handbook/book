.. _big_analysis:

Calculate in greater numbers
----------------------------

When creating and populating datasets yourself it may be easy to monitor the
overall size of the dataset and its file number, and introduce
subdatasets whenever and where ever necessary. It may not be as straightforward
when you are not population datasets yourself, but when *software* or
analyses scripts suddenly dump vast amounts of output.
Certain analysis software can create myriads of files. A standard
`FEAT analysis <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FEAT/UserGuide>`_ [#f1]_
in `FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_, for example, can easily output
several dozens of directories and up to thousands of result files per subject.
Maybe your own custom scripts are writing out many files as outputs, too.
Regardless of *why* a lot of files are produced by an analyses, if the analysis
or software in question runs on a substantially sized input dataset, the results
may overwhelm the capacities of a single dataset.

This section demonstrates some tips on how to prevent swamping your datasets
with files. If you already accidentally got stuck with an overflowing dataset,
checkout section :ref:`cleanup` first.

Solution: Subdatasets
^^^^^^^^^^^^^^^^^^^^^

To stick to the example of FEAT, here is a quick overview on what this software
does: It is modelling neuroimaging data based on general linear modelling (GLM),
and creates web page analyses reports, color activation images, time-course plots
of data and model, preprocessed intermediate data, images with filtered data,
statistical output images, colour rendered output images, log files, and many more
-- in short: A LOT of files.
Plenty of these outputs are text-based, but there are also many sizable files.
Depending on the type of analyses that is run, not all types of outputs
will be relevant. At the end of the analysis, one usually has session-,
subject-specific, or aggregated "group" directories with many subdirectories
filled with log files, intermediate and preprocessed files, and results for all
levels of the analysis.

In such a setup, the output directories (be it on a session/run, subject, or group
level) are predictably named, or custom nameable. In order to not flood a single
dataset, therefore, one can pre-create appropriate subdatasets of the necessary
granularity and have them filled by their analyses.
This approach is by no means limited to analyses with certain software, and
can be automated. For scripting languages other than Python or shell, standard
system calls can create output directories as DataLad subdatasets right away,
Python scripts can even use DataLad's Python API [#f2]_.
Thus, you can create scripts that take care of subdataset creation, or, if you
write analysis scripts yourself, you can take care of subdataset creation right
in the scripts that are computing and saving your results.

As it is easy to link datasets and operate (e.g., save, clone) across dataset
hierarchies, splitting datasets into a hierarchy of datasets
does not have many downsides. One substantial disadvantage, though, is that
on their own, results in subdirectories don't have meaningful provenance
attached. The information about what script or software created them is attached
to the superdataset. Should only the subdataset be cloned or inspected, the information
on how it was generated is not found.

Solutions without creating subdatasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is also possible to scale up without going through the complexities of
creating several subdatasets, or tuning your scaling beyond the creation of
subdatasets. It involves more thought, or compromising, though.
The following section highlights a few caveats to bear in mind if you attempt
a big analyses in single-level datasets, and outlines solutions that may not
need to involve subdatasets. If you have something to add, please
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
you have modified your ``.gitattributes`` file [#f3]_ to store files below a certain
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

.. todo::

   Add more caveats and examples


.. rubric:: Footnotes

.. [#f1] FEAT is a software tool for model-based fMRI data analysis and part of of
         `FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_.

.. [#f2] Read more about DataLad's Python API in the first hidden section in
         :ref:`yoda_project`.

.. [#f3] Read up on these configurations in the chapter :ref:`chapter_config`.