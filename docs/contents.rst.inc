################
**Introduction**
################

.. toctree::
   :maxdepth: 1
   :caption: What DataLad and the handbook are all about

   intro/philosophy
   intro/narrative
   intro/installation
   intro/howto
   intro/executive_summary

.. only:: latex

   ##########
   **Basics**
   ##########

.. only:: html

   .. figure:: artwork/src/basics.svg
      :width: 60%
      :target: http://handbook.datalad.org/en/latest/basics/intro.html

################################
**Basics 1** -- DataLad datasets
################################

.. only:: html

   .. toctree::
      :hidden:

      basics/intro.rst

.. toctree::
   :maxdepth: 1
   :caption: Exploring DataLad's core data structure

   basics/101-101-create
   basics/101-102-populate
   basics/101-103-modify
   basics/101-105-install
   basics/101-106-nesting
   basics/101-107-summary


#############################
**Basics 2** -- Datalad, Run!
#############################

.. toctree::
   :maxdepth: 1
   :caption: How DataLad records provenance of dataset modifications

   basics/101-108-run
   basics/101-109-rerun
   basics/101-110-run2
   basics/101-112-run4
   basics/101-113-summary


#########################################
**Basics 3** -- Under the hood: git-annex
#########################################

.. toctree::
   :maxdepth: 1
   :caption: A closer look at how and why things work

   basics/101-114-txt2git
   basics/101-115-symlinks

#############################
**Basics 4** -- Collaboration
#############################

.. toctree::
   :maxdepth: 1
   :caption: Sharing on shared file systems

   basics/101-116-sharelocal
   basics/101-117-sharelocal2
   basics/101-118-sharelocal3
   basics/101-119-sharelocal4
   basics/101-121-siblings
   basics/101-120-summary

#############################################
**Basics 5** -- Tuning datasets to your needs
#############################################

.. toctree::
   :maxdepth: 1
   :caption: Various types and methods for dataset configurations

   basics/101-122-config
   basics/101-123-config2
   basics/101-124-procedures
   basics/101-125-summary


#############################################
**Basics 6** -- Make the most out of datasets
#############################################

.. toctree::
   :maxdepth: 1
   :caption: Organizational principles and best practices for reproducible data analyses

   basics/101-126-intro
   basics/101-127-yoda
   basics/101-130-yodaproject
   basics/101-128-summary_yoda


################################
**Basics 7** -- One step further
################################

.. toctree::
   :maxdepth: 1
   :caption: Advanced nesting and "extended" reproducibility

   basics/101-132-advancednesting
   basics/101-133-containersrun
   basics/101-134-summary


#############################
**Basics 8** -- Help yourself
#############################

.. toctree::
   :maxdepth: 1
   :caption: Dealing with problems, filesystems, and version histories

   basics/101-135-intro
   basics/101-136-filesystem
   basics/101-137-history
   basics/101-135-help


##########################################
**Basics 9** -- Third party infrastructure
##########################################

.. toctree::
   :maxdepth: 1
   :caption: Leverage third party services to share datasets

   basics/101-138-sharethirdparty
   basics/101-139-gin
   basics/101-140-summary


################################
**Basics 10** -- Further options
################################

.. toctree::
   :maxdepth: 1
   :caption: Small pieces of advice and helpful additional options

   basics/101-179-gitignore
   basics/101-144-intro_extensions
   basics/101-145-hooks

.. only:: latex

   #############
   **Use cases**
   #############

.. only:: html

   .. figure:: artwork/src/usecases.svg
      :width: 60%
      :target: http://handbook.datalad.org/en/latest/usecases/intro.html


###############################
**Use case I** -- Collaboration
###############################

.. only:: html

   .. toctree::
      :hidden:
      :maxdepth: 1
      :caption: Hands-on real-world applications with step-by-step recipes...

      usecases/intro

.. toctree::
   :maxdepth: 1
   :caption: Bob uses public data for a data analysis project and collaborates with Alice to develop his analysis scripts.

   usecases/collaborative_data_management


#############################
**Use case II** -- Provenance
#############################

.. toctree::
   :maxdepth: 1
   :caption: Track provenance of dataset contents: From their origin from websources to scripts or commands that used, modified, or produced them.

   usecases/provenance_tracking


#################################################
**Use case III** -- Reproducible Research Objects
#################################################

.. toctree::
   :maxdepth: 1
   :caption: Share code, data, and computational workflows of your science, and allow others to not only recompute your results, but also build a PDF manuscript from scratch.

   usecases/reproducible-paper


##############################
**Use case IV** -- Supervision
##############################

.. toctree::
   :maxdepth: 1
   :caption: Use DataLad in a supervision setup and benefit from easy data management workflows and automatic log keeping.

   usecases/supervision


#######################################
**Use case V** -- Reproducible Analysis
#######################################

.. toctree::
   :maxdepth: 1
   :caption: A thorough demonstration of data management and data analysis practices to create reproducible (neuro-)science.

   usecases/reproducible_neuroimaging_analysis


#################################
**Use case VI** -- Infrastructure
#################################

.. toctree::
   :maxdepth: 1
   :caption: An implementation of a domain-agnostic data store to enable scalability of scientific computing.

   usecases/datastorage_for_institutions

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

* :ref:`genindex`
* :ref:`search`

..
  stuff that we do not need or show at the moment

.. toctree::
   :hidden:

   usecases/datasets
