.. _extensions_intro:

DataLad's extensions
--------------------

The commands DataLad provides cover a broad range of domain-agnostic use cases.
However, there is a vast supply of extension packages that can add
(domain-specific) functionality and new commands.

Such extensions are shipped as proper Python packages, and are *not* included in
DataLad itself. Instead, users with the need for a particular extension can
install the extension package on top of DataLad. The installation is done with
standard Python package managers, such as :term:`pip`, and beyond installation
of the package, no additional setup is required.

The following DataLad extensions are currently available:

.. todo::

   Which extensions do you want to see mentioned (and which not)?

.. list-table::
   :widths: 50 100
   :header-rows: 1

   * - Extension name
     - Description
   * - `DataLad Container <http://docs.datalad.org/projects/container/en/latest/>`_
     - Equips DataLad's :command:`run`/:command:`rerun` functionality with
       the ability to transparently execute commands in containerized
       computational environments.
   * - `DataLad Neuroimaging <https://datalad-neuroimaging.readthedocs.io/en/latest/>`_
     - Metadata extraction support for a range of standards common to
       neuroimaging data.
   * - `DataLad Metalad <http://docs.datalad.org/projects/metalad/en/latest/>`_
     - Equips DataLad with an alternative command suite for metadata handling
       (extraction, aggregation, reporting).
   * - `DataLad Webapp <https://github.com/datalad/datalad-webapp>`_
     - DataLad extension for exposing a REST API of selected functionality.
   * - `DataLad Crawler <http://docs.datalad.org/projects/crawler/en/latest/basics.html>`_
     - Datalad for crawling web resources and automated data distributions.
   * - `DataLad HTCondor <https://github.com/datalad/datalad-htcondor>`_
     - Remote code execution for DataLad via HTCondor.


To install a DataLad extension, use

.. code-block:: bash

   $ pip install <extension-name>

such as in

.. code-block:: bash

   $ pip install datalad-container

Afterwards, the new DataLad functionality the extension provides is readily available.