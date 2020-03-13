.. _extensions_intro:

DataLad's extensions
--------------------

.. index:: ! extensions

The commands DataLad provides cover a broad range of domain-agnostic use cases.
However, there are extension packages that can add (domain-specific)
functionality and new commands.

Such extensions are shipped as separate Python packages, and are *not* included in
DataLad itself. Instead, users with the need for a particular extension can
install the extension package -- either on top of DataLad if DataLad is already
installed, or on its own (the extension will then pull in DataLad core
automatically, with no need to first or simultaneously install DataLad itself
explicitly). The installation is done with
standard Python package managers, such as :term:`pip`, and beyond installation
of the package, no additional setup is required.

Among others (a full list can be found on `PyPi <https://pypi.org/search/?q=datalad>`_),
the following DataLad extensions are available:

.. list-table::
   :widths: 50 100
   :header-rows: 1

   * - Extension name
     - Description
   * - `DataLad Container <http://docs.datalad.org/projects/container/en/latest/>`_
     - Equips DataLad's :command:`run`/:command:`rerun` functionality with
       the ability to transparently execute commands in containerized
       computational environments. The section :ref:`containersrun` demonstrates
       how this extension can be used, as well as the usecase :ref:`usecase_reproduce_neuroimg`.
   * - `DataLad Crawler <http://docs.datalad.org/projects/crawler/en/latest/>`_
     - One of the initial goals behind DataLad was to provide access
       to already existing data resources. With
       :command:`crawl-init`/:command:`crawl` commands, this extension
       allows to automate creation of DataLad datasets from resources
       available online, and efficiently keep them
       up-to-date. The majority of datasets in :term:`the DataLad superdataset ///`
       on `datasets.datalad.org <http://datasets.datalad.org/>`_ are created and
       updated using this extension functionality.

       .. todo::

          contribute a section or a demo, e.g. based on `existing one <http://docs.datalad.org/projects/crawler/en/latest/demos/track_data_from_webpage.html>`__

   * - `DataLad Neuroimaging <https://datalad-neuroimaging.readthedocs.io/en/latest/>`_
     - Metadata extraction support for a range of standards common to
       neuroimaging data. The usecase :ref:`usecase_reproduce_neuroimg` demonstrates
       how this extension can be used.
   * - `DataLad Metalad <http://docs.datalad.org/projects/metalad/en/latest/>`_
     - Equips DataLad with an alternative command suite and advanced tooling
       for metadata handling (extraction, aggregation, reporting).

       .. todo::

          once section on metadata is done, link it here

To install a DataLad extension, use

.. code-block:: bash

   $ pip install <extension-name>

such as in

.. code-block:: bash

   $ pip install datalad-container

Afterwards, the new DataLad functionality the extension provides is
readily available.

Some extensions could also be available from the
software distribution (e.g., NeuroDebian or conda) you used to install
DataLad itself.  Visit `github.com/datalad/datalad-extensions/
<https://github.com/datalad/datalad-extensions/>`_ to review available
versions and their status.
