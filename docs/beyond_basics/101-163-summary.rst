.. _gobigsummary:

Summary
-------

If you want to go big, DataLad is a suitable tool and can overcome shortcomings
of Git and git-annex, if used correctly. Scaling up involves
some thought, and in some instances compromise, though.

- The general mechanism that allows scaling up is nesting datasets. This process
  can be done by hand or programmatically. Recursive operations ease working
  across a hierarchy of datasets and create a monorepo-like experience
- Beware of accidentally placing to many (even small) files into Git's version
  control in a single dataset!
  ``.gitignore`` files can keep irrelevant files out of version control, the
  ``explicit`` option :command:`datalad run` may be helpful, and
  custom largefile rules in ``.gitattributes`` may be necessary to override
  dataset configurations such as ``text2git``.
- Don't consider only the limits of version control software, but also the
  limits of your file system. Too many files in single directories can become
  problematic even without version control.
- If things go wrong, it's not all lost. There are ways to clean up your dataset
  if it ever gets clogged, although they are the software equivalent of a
  blowtorch and should be handled with care.


Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Go big, if you want to. :ref:`Distribute 80TB of files <usecase_HCP_dataset>`
or `more <https://github.com/datalad/datalad-ukbiobank>`_, or version control
large analyses with minimized performance loss of your version control tools.