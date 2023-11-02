.. _hpc:

DataLad on High Throughput or High Performance Compute Clusters
---------------------------------------------------------------

For efficient computing of large analysis, to comply to best computing practices, or to fulfil the requirements that `responsible system administrators <https://xkcd.com/705>`_ impose, users may turn to computational clusters such as :term:`high-performance computing (HPC)` or :term:`high-throughput computing (HTC)` infrastructure for data analysis, back-up, or storage.

This chapter is a collection of useful resources and examples that aims to help you get started with DataLad-centric workflows on clusters.
We hope to grow this chapter further, so please `get in touch <https://github.com/datalad-handbook/book/issues/new>`_ if you want to share your use case or seek more advice.

Pointers to content in other chapters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To find out more about centralized storage solutions, you may want to checkout the use case :ref:`usecase_datastore` or the section :ref:`riastore`.

DataLad installation on a cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users of a compute cluster generally do not have administrative privileges (sudo rights) and thus can not install software as easily as on their own, private machine.
In order to get DataLad and its underlying tools installed, you can either `bribe (kindly ask) your system administrator <https://hsto.org/getpro/habr/post_images/02e/e3b/369/02ee3b369a0326760a160004aca631dc.jpg>`_ [#f1]_ or install everything for your own user only following the instructions in the paragraph :ref:`norootinstall` of the :ref:`installation page <install>`.


.. rubric:: Footnotes

.. [#f1] You may not need to bribe your system administrator if you are kind to them. Consider frequent gestures of appreciation, or send a geeky T-Shirt for `SysAdminDay <https://en.wikipedia.org/wiki/System_Administrator_Appreciation_Day>`_ (the last Friday in July) -- Sysadmins do amazing work!
