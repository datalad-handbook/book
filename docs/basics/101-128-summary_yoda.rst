.. _summary_yoda:

Summary: YODA principles
------------------------

The YODA principles are a small set of guidelines that can make a huge
difference towards reproducibility, comprehensibility, and transparency
in a data analysis project.

These standards are not complex -- quite the opposite, they are very
intuitive. They structure essential components of a data analysis project --
data, code, computational environments, and lastly also the results --
in a modular and practical way, and use basic principles and commands
of DataLad you are already familiar with.

There are many advantages to this organization of contents.

- Having input data as independent dataset(s) that are not influenced (only
  consumed) by an analysis allows for a modular reuse of pure data datasets,
  and does not conflate the data of an analysis with the results or the code.

- Keeping code within an independent, version-controlled directory, but as a part
  of the analysis dataset, makes sharing code easy and transparent, and helps
  to keep directories neat and organized. Moreover,
  with the data as subdatasets, data and code can be automatically shared together.

- Including the computational environment into an analysis dataset encapsulates
  software and software versions, and thus prevents re-computation failures
  (or sudden differences in the results) once
  software is updated, and software conflicts arising on different machines
  than the one the analysis was originally conducted on.

- Having all of these components as part of a DataLad dataset allows version
  controlling all pieces within the analysis regardless of their size, and
  generates provenance for everything, especially if you make use of the tools
  that DataLad provides.

- The yoda procedure is a good starting point to build your next data analysis
  project up on.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Using tools that DataLad provides you are able to make the most out of
your data analysis project. The YODA principles are a guide to accompany
you on your path to reproducibility.

What should have become clear in this section is that you are already
equipped with enough DataLad tools and knowledge that complying to these
standards will feel completely natural and effortless in your next analysis
project.
The next section will add to your existing skills by demonstrating how to
use DataLad also within Python scripts.