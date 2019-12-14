.. _summary_yoda:

Summary
-------

The YODA principles are a small set of guidelines that can make a huge
difference towards reproducibility, comprehensibility, and transparency
in a data analysis project. By applying them in your own midterm analysis
project, you have experienced their immediate benefits.

You also noticed that these standards are not complex -- quite the opposite,
they are very intuitive.
They structure essential components of a data analysis project --
data, code, potentially computational environments, and lastly also the results --
in a modular and practical way, and use basic principles and commands
of DataLad you are already familiar with.

There are many advantages to this organization of contents.

- Having input data as independent dataset(s) that are not influenced (only
  consumed) by an analysis allows for a modular reuse of pure data datasets,
  and does not conflate the data of an analysis with the results or the code.
  You have experienced this with the ``iris_data`` subdataset.

- Keeping code within an independent, version-controlled directory, but as a part
  of the analysis dataset, makes sharing code easy and transparent, and helps
  to keep directories neat and organized. Moreover,
  with the data as subdatasets, data and code can be automatically shared together.
  By complying to this principle, you were able to submit both code and data
  in a single superdataset.

- Keeping an analysis dataset fully self-contained with relative instead of
  absolute paths in scripts is critical to ensure that an analysis reproduces
  easily on a different computer.

- DataLad's Python API makes all of DataLad's functionality available in
  Python, either as standalone functions that are exposed via ``datalad.api``,
  or as methods of the ``Dataset`` class.
  This provides an alternative to the command line, but it also opens up the
  possibility of performing DataLad commands directly inside of scripts.

- Including the computational environment into an analysis dataset encapsulates
  software and software versions, and thus prevents re-computation failures
  (or sudden differences in the results) once
  software is updated, and software conflicts arising on different machines
  than the one the analysis was originally conducted on. You have not yet
  experienced how to do this first-hand, but you will in a later section.

- Having all of these components as part of a DataLad dataset allows version
  controlling all pieces within the analysis regardless of their size, and
  generates provenance for everything, especially if you make use of the tools
  that DataLad provides. This way, anyone can understand and even reproduce
  your analysis without much knowledge about your project.

- The yoda procedure is a good starting point to build your next data analysis
  project up on.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using tools that DataLad provides you are able to make the most out of
your data analysis project. The YODA principles are a guide to accompany
you on your path to reproducibility and provenance-tracking.

What should have become clear in this section is that you are already
equipped with enough DataLad tools and knowledge that complying to these
standards felt completely natural and effortless in your midterm analysis
project.
