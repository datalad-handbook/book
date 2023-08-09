:orphan:

====================
The DataLad Handbook
====================

.. raw:: latex

  % page header setup
  % page numbers at the outer edges
  % chapter and section names at the inner edges,
  % such that an open double-page reads: chapter...section
   \fancyhead[LE]{\small\thepage}
   \fancyhead[RO]{\small\thepage}
   \fancyhead[RE]{\small\nouppercase{\leftmark}}
   \fancyhead[LO]{\small\nouppercase{\rightmark}}
   \fancyfoot{}
   \fancyfoot[LE]{}
   \renewcommand*{\footrule}{}%


.. toctree::

   intro/philosophy
   intro/narrative
   intro/installation
   intro/howto
   intro/executive_summary
   basics/basics-datasets
   basics/basics-run
   basics/basics-annex
   basics/basics-collaboration
   basics/basics-configuration
   basics/basics-yoda
   basics/basics-containers
   basics/basics-thirdparty
   basics/basics-help

..
   beyond_basics/intro.rst
   usecases/intro

.. raw:: latex

   \appendix

.. toctree::

   book_appendix
