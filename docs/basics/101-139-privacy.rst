.. _privacy:

Keeping (some) dataset contents private
---------------------------------------

Datasets can contain information that you don't want to share with others.
Maybe the collection of pictures from your team-building event also contains those after-hour photos where you drunkenly kidnapped a tram.
Or you are handling data with strict privacy requirements, such as patient data or
medical imaging files.
Whatever it may be, this short section summarizes strategies that help you to ensure
to private information is not leaked, even when you publicly share datasets that contain it.

Strategy 1: Never save private information to Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most important strategy to keep in mind in handling datasets with potentially sensitive information is to **never save sensitive information into Git**. **NEVER**.
Saving sensitive information into a dataset or Git repository that you intend to share is the equivalent of including your account password as an attachment to every email you write -- you don't necessarily point out that there is private information, but it lies around for everyone to accidentally find.
Once a file with sensitive contents has been saved in the version history, sharing this dataset may accidentally expose the sensitive information even if it has been removed in the most recent version -- the transparent revision history of a dataset allows to simply restore the file.

Thus, make sure to always manage sensitive files with :term:`git-annex`, even if the file is just a small text file.
Having the file annexed allows you to specifically not share its contents, even when you make your dataset publicly available.
However, it is highly important to realize that while annexed file's *contents* are not saved into Git, annex file's *names* are.
If private information such as a medical patients non-anonymized ID or other potentially identifying information becomes a part of the file name, this information is exposed in the Git history of the dataset.
Keep in mind that this applies even if you renamed the file.

.. find-out-more:: Help! I accidentally saved sensitive information to Git!

	The only lasting way to remove contents from the dataset history completely is to substantially rewrite the dataset's history via tools such as ``git-filter-repo`` or ``git filter-branch``, two very dangerous and potentially destructive operations.
	If you ever need to go there, the advanced section :ref:`cleanup` contains a paragraph on "Getting contents out of Git".

Strategy 2: Restrict access via third party service or file system permissions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you have a dataset and only authorized actors should be allowed to access it,
it is possible to set access restrictions simply via choice of (third party) storage permissions.
When it is an access restricted dataset on shared infrastructure, for example a scientific dataset that only researchers who signed a data usage agreement should have access to, it could suffice to create specific `Unix groups <https://en.wikipedia.org/wiki/Group_identifier>`_ with authorized users, and give only those groups the necessary permissions.
Depending on what permissions are set, unauthorized actors would not be able to retrieve file contents, or be able to clone the dataset at all.

The ability of repository hosting services to make datasets private and only allow select collaborators access is yet another method of keeping complete datasets as private as necessary, even though you should think twice on whether or not you should host sensitive repositories at all on these services.

One method to exert potentially fine-grained access control over file contents is via choice of (third party) hosting service for some or all annexed file contents.
If you chose a service only selected people have access to, and publish annexed contents exclusively there, then only those selected people can perform a successful :command:`datalad get`.
For example, when it is a dataset with content hosted on third party cloud storage such as S3 buckets, permission settings in the storage locations would allow data providers to specify or limit who is able to retrieve the file contents.
An example for this is the usecase :ref:`usecase_hcp_dataset`, where file contents from the human connectome project can only be retrieved when a user has obtained the necessary credentials first.


Strategy 3: Selective publishing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If it is individual files that you do not want to share, you can selectively publish the contents of all files you want others to have, and withhold the data of the files you do not want to share.
This can be done by providing paths to the data that should be published, or a `git-annex-wanted <https://git-annex.branchable.com/git-annex-wanted/>`_ configuration and the ``--data auto`` option.

Let's say you have a dataset with three files:

- ``experiment.txt``
- ``subject_1.dat``
- ``subject_2.data``

Consider that all of these files are annexed. While the information in ``experiment.txt`` is fine for everyone to see, ``subject_1.dat`` and ``subject_2.dat`` contain personal and potentially identifying data that can not be shared.
Nevertheless, you want collaborators to know that these files exist.
By publishing only the file contents of ``experiment.txt`` with

.. code-block:: bash

  $ datalad push --to github experiment.txt

only meta data about file availability of ``subject_1.dat`` and ``subject_2.dat`` exists, but as these files' annexed data is not published, a :command:`datalad get`
will fail.
Note, though, that :command:`push` will publish the complete dataset history (unless you specify a commit range with the ``--since`` option -- see the `manual <http://docs.datalad.org/en/latest/generated/man/datalad-push.html>`_ for more information).



