.. _extensions_intro:

DataLad extensions
------------------

.. index:: ! extensions

DataLad's commands cover a broad range of domain-agnostic use cases.  However,
there are extension packages that can add specialized functionality with
additional commands. :numref:`table-datalad-extensions` lists a number of
such extensions.

DataLad extensions are shipped as separate Python packages, and are *not*
included in DataLad itself. Instead, users needing a particular extension can
install the extension package -- either on top of DataLad, if already
installed, or on its own. In the latter case, the extension will then pull in
DataLad core automatically, with no need to first or simultaneously install
DataLad itself explicitly. The installation is done with standard Python
package managers, such as :term:`pip`, and beyond installation of the package,
no additional setup is required.

DataLad extensions listed here are of various maturity levels. Check out their
documentation and the sections or chapters associated with an extension to
find out more about them.

.. todo::
   We are working on content to describe each of the
   extensions, but this is not a high priority at the given time.
   Contributions of sections, chapters, or demonstrations for extensions
   that do not yet have one in the handbook are highly welcomed.

.. tabularcolumns:: \Y{.2}\Y{.8}
.. list-table:: Selection of available DataLad extensions. A more up-to-date list can be found on `PyPi <https://pypi.org/search/?q=datalad>`__
   :name: table-datalad-extensions
   :widths: 50 100
   :header-rows: 1

   * - Name
     - Description

   * - `container <http://docs.datalad.org/projects/container>`_
     - Equips DataLad's :command:`run`/:command:`rerun` functionality with
       the ability to transparently execute commands in containerized
       computational environments. The section :ref:`containersrun` demonstrates
       how this extension can be used, as well as the usecase :ref:`usecase_reproduce_neuroimg`.

   * - `crawler <http://docs.datalad.org/projects/crawler>`_
     - One of the initial goals behind DataLad was to provide access
       to already existing data resources. With
       :command:`crawl-init`/:command:`crawl` commands, this extension
       allows to automate creation of DataLad datasets from resources
       available online, and efficiently keep them
       up-to-date. The majority of datasets in :term:`the DataLad superdataset ///`
       on `datasets.datalad.org <http://datasets.datalad.org/>`_ are created and
       updated using this extension functionality.

   * - `htcondor <https://github.com/datalad/datalad-htcondor>`__
     - Enhances DataLad with the ability for remote execution via the job
       scheduler `HTCondor <https://research.cs.wisc.edu/htcondor/>`_.

   * - `metalad <http://docs.datalad.org/projects/metalad>`_
     - Equips DataLad with an alternative command suite and advanced tooling
       for metadata handling (extraction, aggregation, reporting).

   * - `mihextras <https://datalad-mihextras.readthedocs.io>`_
     - Special-interest commands and previews for future DataLad additions.

   * - `neuroimaging <https://datalad-neuroimaging.readthedocs.io>`_
     - Metadata extraction support for a range of standards common to
       neuroimaging data. The usecase :ref:`usecase_reproduce_neuroimg` demonstrates
       how this extension can be used.

   * - `osf <http://docs.datalad.org/projects/osf>`_
     - Enables DataLad to interface and work with the `Open Science Framework
       <https://osf.io/>`_. Use it to publish your dataset's data to an OSF
       project, thus utilizing the OSF for dataset storage and sharing.

   * - `rclone-remote <https://github.com/datalad/git-remote-rclone>`_
     - Enables DataLad to push and pull to all third party providers with no native Git
       support that are supported by `rclone <https://rclone.org/>`_.

   * - `ukbiobank <https://github.com/datalad/datalad-ukbiobank>`__
     - Equips DataLad with a set of commands to obtain and monitor imaging data
       releases of the `UKBiobank <https://www.ukbiobank.ac.uk//>`_.
       An introduction can be found in chapter

   * - `xnat <https://github.com/datalad/datalad-xnat>`__
     - Equips DataLad with a set of commands to track
       `XNAT <https://www.xnat.org/>`_ projects.
       An alternative, more basic method to retrieve data from an XNAT server is
       outlined in section :ref:`providers`.


.. todo::

  contribute a section or a demo, e.g. based on `existing one <http://docs.datalad.org/projects/crawler/en/latest/demos/track_data_from_webpage.html>`__

.. todo::

  link hirni chapter once done


.. todo::

  once section on metadata is done, link it here

.. todo::

  link UKB chapter once done

.. todo::

  Rewrite Third Party chapter to use this helper

.. todo::

  Contribute a usecase or a demo when done.


To install a DataLad extension, use

.. code-block:: bash

   $ pip install <extension-name>

such as in

.. code-block:: bash

   $ pip install datalad-container

Afterwards, the new DataLad functionality the extension provides is
readily available.

Some extensions could also be available from the software distribution (e.g.,
NeuroDebian or conda) you used to install DataLad itself.  Visit
`github.com/datalad/datalad-extensions/
<https://github.com/datalad/datalad-extensions/>`_ to review available versions
and their status.
