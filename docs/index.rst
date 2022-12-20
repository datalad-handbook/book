:orphan:

.. meta::
   :description: The home of the DataLad handbook

.. image:: artwork/src/img/datalad-animated.gif
   :scale: 100%
   :alt: Animated DataLad logo

============
The Handbook
============

**Welcome!**

This handbook is a living resource about why and -- more importantly -- *how* to
use DataLad. It aims to provide novices and advanced users of all backgrounds
with both the basics of DataLad and start-to-end use cases of specific
applications. If you want to get hands-on experience and learn DataLad, the *Basics*
part of this book will teach you. If you want to know what is possible, the
*use cases* will show you. And if you want to help others to get started with DataLad,
the `companion repository <https://github.com/datalad-handbook/course>`_ provides
:ref:`free and open source teaching material <teach>` tailored to the handbook.

Before you read on, please note that the handbook is based on **at least** DataLad version **0.12**, and the higher your version of DataLad is, the better.
The section :ref:`install` will set you up with what you need if you currently do not have DataLad 0.12 or higher installed.

If you're new here, please start the handbook :ref:`here <philo>`.
Alternatively, try to identify with one of several user-types in this
:ref:`user specific guide to the handbook <usertypes>`.

.. importantnote:: The handbook is currently in beta stage.

   If you would be willing to provide feedback on its contents, please
   `get in touch <https://github.com/datalad-handbook/book/issues/new>`_.


.. image:: artwork/src/enter.svg
   :width: 60%
   :align: center

.. toctree::
   :maxdepth: 2
   :caption: What this is all about

   intro/intro

.. image:: artwork/src/basics.svg
   :width: 60%
   :align: center

.. toctree::
   :maxdepth: 3
   :caption: The fundamentals of DataLad

   basics/intro

.. image:: artwork/src/advanced.svg
   :width: 60%
   :align: center

.. toctree::
   :maxdepth: 3
   :caption: Beyond the Basics

   beyond_basics/intro.rst

.. image:: artwork/src/usecases.svg
   :width: 60%
   :align: center

.. toctree::
   :maxdepth: 2
   :caption: Hands-on real-world applications with step-by-step recipes

   usecases/intro

########
Appendix
########

.. toctree::
   :maxdepth: 1
   :caption: Further information and references

   glossary
   basics/101-180-FAQ
   basics/101-136-cheatsheet
   contributing
   teaching
   acknowledgements
   intro/user_types
   OHBMposter
   usecases/openneuro
   intro/windows
   intro/filenaming

########################
Code lists from chapters
########################

.. toctree::
   :maxdepth: 1
   :caption: Easy access to copy-paste snippets for workshops

   code_from_chapters/intro
   code_from_chapters/01_dataset_basics_code
   code_from_chapters/02_reproducible_execution_code
   code_from_chapters/10_yoda_code
   code_from_chapters/OHBM
   code_from_chapters/OHBM_OSR.rst
   code_from_chapters/usecase_ml_code
   code_from_chapters/MPI_code
   code_from_chapters/DLBasicsMPI
   code_from_chapters/ABCD
   code_from_chapters/yale
   code_from_chapters/dgpa
   code_from_chapters/neurohackademy
..
  stuff that we do not need or show at the moment

.. only:: adminmode

    .. toctree::
       :hidden:

       usecases/datasets
       r
