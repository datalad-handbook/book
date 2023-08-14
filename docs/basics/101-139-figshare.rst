.. _figshare:

Built-in data export
^^^^^^^^^^^^^^^^^^^^

Apart from flexibly configurable special remotes that allow publishing
annexed content to a variety of third party infrastructure, DataLad also has
some built-in support for "exporting" data to other services.
This usually means that a static snapshot of your dataset and its files are shared
in archives or collections of files.
While an export of a dataset looses some of the advantages that a DataLad dataset has, for example a transparent version history, it can be a fast and simple way to make the most recent version of your dataset available or archived.

One example is the command :dlcmd:`export-archive`.
Running this command creates a ``.tar.gz`` file with the content of your dataset.
This compressed archive can be uploaded to any data hosting portal manually.
This moves data out of version control and decentralized tracking, and essentially "throws it over the wall" - while your data (also the annexed data) will be available for download from where you share it, none of the special features a DataLad dataset provides will be available, such as its history or configurations.

Another example is :dlcmd:`export-to-figshare`.
`Figshare <https://figshare.com>`__ is an online open access repository where researchers can preserve and share their research outputs, including figures, datasets, or images - and thus everything that could potentially be managed in a Datalad dataset.
Running :dlcmd:`export-to-figshare` allows you to publish the dataset as a snapshot.
Note that this requires a free account on Figshare, and the generation of an `access token <https://figshare.com/account/applications>`_ for authentication.
An interactive prompt will ask you to supply authentication credentials, and guide you through the process of creating a new article.

.. code-block:: bash
   :emphasize-lines: 5

   $ datalad export-to-figshare
	[INFO   ] Exporting current tree as an archive under /home/me/DataLad-101 since figshare does not support directories
	[INFO   ] Uploading /home/me/datalad_b1cbbaa9-dd5c-473e-8092-e911021f33cb.zip to figshare
	Article
	Would you like to create a new article to upload to?  If not - we will list existing articles (choices: yes, no): yes

	New article
	Please enter the title (must be at least 3 characters long). [abcd#b1cbbaa9-dd5c-473e-8092-e911021f33cb]: my-cool-dataset

	[INFO   ] Created a new (private) article 16676764 at https://figshare.com/account/articles/16676764. Please visit it, enter additional meta-data and make public
	[INFO   ] 'Registering' /home/me/datalad_b1cbbaa9-dd5c-473e-8092-e911021f33cb.zip within annex
	[INFO   ] Adding URL https://ndownloader.figshare.com/files/30876682 for it
	[INFO   ] Registering links back for the content of the archive
	[INFO   ] Adding content of the archive /home/me/datalad_b1cbbaa9-dd5c-473e-8092-e911021f33cb.zip into annex AnnexRepo(/home/me/DataLad-101)
	[INFO   ] Initiating special remote datalad-archives
	[INFO   ] Finished adding /home/me/datalad_b1cbbaa9-dd5c-473e-8092-e911021f33cb.zip: Files processed: 4, removed: 4, +git: 2, +annex: 2
	[INFO   ] Removing generated and now registered in annex archive
	export_to_figshare(ok): Dataset(/home/me/DataLad-101) [Published archive https://ndownloader.figshare.com/files/30876682]



The screenshot below shows how the ``DataLad-101`` dataset looks like in exported form:

.. figure:: ../artwork/src/figshare_screenshot.png
   :width: 50%

You could then extend the dataset with metadata, obtain a `DOI <https://www.doi.org/driven_by_DOI.html>`_ for it and make it citable, and point others to it in order to download it as an archive of files.

Beyond this, as the command :dlcmd:`export-archive` is used by it to prepare content for upload to Figshare, annexed files also will be annotated as available from the archive on Figshare using ``datalad-archive`` special remote.
As a result, if you publish your Figshare dataset and share your DataLad dataset on a repository hosting service without support for annexed files, users will still be able to fetch content from the tarball shared on Figshare.

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: datalad-archives(+) [datalad-archives]
