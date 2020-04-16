.. _usecaseJSC:

Computing at the JSC
--------------------

This document details how to run computations on the JSC. It is a collection of
useful advice and best-practices that will grow over time as we get more and
more experience.

Please refer to the section :ref:`install` for installation instructions for
DataLad and its requirements on the JSC's supercomputers.

Getting access to singularity on JURECA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Loading singularity is done by executing the following steps on JURECA:

.. code-block:: bash

   module use $OTHERSTAGES
   module load Stages/Devel-2019a
   module load Singularity/3