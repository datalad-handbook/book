.. _usecase_encrypted_annex:

Encrypted data storage and transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: ! Usecase; Encrypted data storage and transport

This use case demonstrates how to utilise `git-annex
encryption <https://git-annex.branchable.com/encryption/>`__ to keep
data encrypted when it is not being used. In this workflow, data need
to be securely deposited on one machine, and downloaded to another
machine for processing and storage. For this reason, in our workflow we
will combine several independent pieces:

#. Using git-annex encryption
#. Using RIA stores
#. Working in temporary (ephemeral) clones that combine information from
   several remotes.

The challenge
=============

Bob does data collection through a web form. Incoming form entries
are saved as individual files by the web server. Bob periodically
imports the data to his local machine, and uses them to produce an
updated summary. For security reasons, he does not want the data to lie
around unencrypted.

The DataLad approach
====================

Bob sets up his remote machine (web server) so that incoming data is
saved in a DataLad dataset. On that machine, he also creates a RIA
sibling for the dataset (accessible from the outside through ssh), and
enables encryption for annexed contents. He chooses a scheme in which
the server only has the encryption key. Each new data file will be saved
in the dataset, pushed to that RIA store, and dropped from the dataset,
leaving only the encrypted copy on the remote server. On his local
machine, he also sets up RIA stores, enables encryption, and scripts his
analysis to check out the datasets locally, fetch updates from the
remote machine, and push data back to local stores. In this way, data is
not available anywhere in decrypted form, except when it is being
processed.

Step by step
============

Before we start: GnuPG
----------------------

DataLad relies on git-annex to manage large file content, and git-annex
relies on `GnuPG <https://gnupg.org/>`__ to manage encryption. To
proceed with the next steps, you will need at least one pair of GPG
keys, one *private* (used for decryption) and one *public* (used for
encryption). The relevant keys need to be known to the GPG program on
the machine you are using.

We won't go into detail about GPG, but the most useful commands are:
``gpg --full-generate-key`` to generate a key pair, ``gpg --list-keys``
and ``gpg --list-secret-keys`` to display known public and private keys,
``gpg --export -a [keyID] > my_public_key.asc`` to export a public key
to export a public key, and ``gpg --import my_public_key.asc`` to import
the previously exported key on another machine.

Remote server: encrypted deposition
-----------------------------------

We start by creating a DataLad dataset to track deposition of raw data.
Since encryption is enabled for git annex special remotes, we are
satisfied by the default configuration, which annexes all files.

.. code:: bash

   $ datalad create incoming_data
   $ cd incoming data

Then, we create a RIA sibling. We chose a local RIA because we don't
want to move the data outside the server yet. But the logic would be the
same for all kinds of git-annex special remotes.

.. code:: bash

   $ datalad create-sibling-ria \
     --new-store-ok --name entrystore \
     --alias incoming-data \
     ria+file:///data/project/store

Now we tell git annex to encrypt annexed content placed in the store. We
choose regular public key encryption with shared filename encryption
(``sharedpubkey``). In this method, access to *public* keys is required
to store files in the remote, but *private* key is required for
retrieval. So if we only store our public key on the machine, its users
will have no means to decrypt the data.

.. code:: bash

   $ git annex enableremote \
      entrystore-storage \
      encryption=sharedpubkey \
      keyid=9AB670707D8EA564119785922EF857223E033AF1
   enableremote entrystore-storage (encryption setup) (to gpg keys: 2EF857223E033AF1) ok
   (recording state in git...)

If we want to add another encryption key, the step above can be repeated
with ``keyid+=...``.

With this setup, whenever a new data file is generated, the addition
process would involve:

::

   $ datalad save -m "Adding new file" entry-file-name.dat
   $ datalad push --to entrystore entry-file-name.dat
   $ datalad drop entry-file-name.dat

Note: with ``sharedpubkey`` mode, git-annex encrypts file content using
GPG, and file names using HMAC. However, the HMAC cipher is stored
unencrypted in the git repository. This makes it possible to add new
files without access to the private gpg keys - but also means that
access to the git repository will reveal file names.

Since a RIA store combines a bare git repository with annex storage in
the same location, this means that we should take care to not include
sensitive information in file names. See `git-annex's
documentation <https://git-annex.branchable.com/encryption/>`__ for more
details.

Local server
------------

Here, we start once again by creating a DataLad dataset:

.. code:: bash

   $ datalad create derived_data
   $ cd derived_data

We install a subdataset with input data by using datalad clone:

.. code:: bash

   $ datalad clone -d . ria+ssh://... inputs

Next, we can retrieve all data:

.. code:: bash

   $ datalad get inputs

As long as we have the required private key, gpg will be used to quietly
decrypt all files during the ``get`` operation, so our dataset clone
will contain already decrypted data.

At this stage we may add our data processing code (likely putting it
under ``code`` directory, and using ``.gitattributes`` to decide whether
code files should be tracked by git), and use ``datalad run`` to produce
derived data.

Since we intend all our data to be encrypted at rest also on this
machine, we will also create RIA siblings and tell git-annex to use
encryption. Because here we have access to our private key, we will use
the default, more flexible, scheme with hybrid encryption keys.

Note: In the ``hybrid`` mode, private key is needed for both retrieval
and deposition of annexed contents, but it is easy to add new keys
without having to reencrypt data. File content and names are encrypted
with a symmetric cypher, which is encrypted using gpg and stored
encrypted in the git repository. See `git-annex's
documentation <https://git-annex.branchable.com/encryption/>`__ for more
details.

.. code:: bash

   $ datalad create-sibling-ria --new-store-ok --name localstore --alias derived ria+file:///data/project/store
   $ git annex enableremote localstore-storage keyid+=2EF857223E033AF1

And we repeat the same for the input subdataset, so that we can maintain
a local copy of the raw data.

.. code:: bash

   $ cd input
   $ datalad create-sibling-ria \
     --name localstore --alias raw \
     ria+file:///data/project/store
   $ git annex enableremote \
     localstore-storage keyid+=2EF857223E033AF1
   $ cd ..

Depending on what is more convenient for us, we could either decide to
keep the current dataset clones and drop only the annexed file content
after pushing, or treat the clones as temporary and remove them
altogether. Here, we will use the second option. For this reason, we
need to declare the current clones "dead" to git annex before pushing,
so that subsequent clones from the RIA store won't consider this
location for obtaining files. Since we gave the super- and sub-dataset's
siblings the same name, "localstore", we can use ``push --recursive``.

.. code:: bash

   $ datalad foreach-dataset git annex dead here
   $ datalad push --recursive --to localstore

And in the end we can clean up by removing the temporary clone:

.. code:: bash

   $ cd ..
   $ datalad drop --recursive --what all --dataset derived_data

Performing updates with temporary (ephemeral) clones
----------------------------------------------------

The remaining part of the workflow focuses on working with temporary
clones and using them to transfer updates between different data stores.
The process is not affected by whether encryption was used or not (as it
happens quietly on ``get`` & ``push``).

Any time we want to include new data from ``entrystore`` in our local
copy / derived dataset, we would start by cloning the derived dataset
from the local RIA, and getting the input subdataset (without getting
contents yet):

.. code:: bash

   $ datalad clone \
      ria+file:///data/project/entrystore#~derived \
      derived_data
   $ cd derived_data
   $ datalad get --no-data inputs

Our next step would be to obtain files from the remote server that we
don't yet have locally. At this moment it is a good idea to stop and
consider what the input dataset "knows" about other locations:

.. code:: bash

   $ datalad siblings -d inputs
   .: here(+) [git]
   .: origin(-) [/data/project/store/8e4/65aa4-af88-4abd-aaa0-d248339780be (git)]
   .: localstore-storage(+) [ora]
   .: entrystore-storage(+) [ora]

Since we cloned the superdataset from local RIA store, also the
subdataset has the origin (git remote) pointing to that store. It also
has the local-storage and entrystore-storage siblings; these are the
git-annex special remotes for the local and remote RIA stores,
respectively. But to learn about new files that were added in the
remote server since we last cloned from there, we need the git
remote. Let's add it then (note that when working with ``datalad
siblings`` or ``git remote`` commands, we cannot use the
``ria+ssh://...#~alias`` url, and need to use the actual ssh url and
filesystem path).

.. code:: bash

   $ cd inputs
   $ git remote add entrystore \
      ssh://example.com:/data/project/store/alias/incoming-data

Now we can obtain updates from the entrystore sibling (pair). We may
choose to fetch only, to see what is new before merging:

.. code:: bash

   $ datalad update --sibling entrystore --how fetch
   $ datalad diff --from main --to entrystore/main

If there were no updates reported, we could decide to finish our work
right there. Since there are new files, we will integrate the changes
(since we didn't change the input dataset locally, there is no practical
difference in using ``ff-only`` versus ``merge``).

.. code:: bash

   $ datalad update --sibling entrystore --how merge

Note to users of python API: the results of the ``diff`` command include
files that were not changed, so to look for changes we need to filter
them by state; e.g. if we only expect additions, we can do this:

.. code:: python

     added_files = subds.diff(
       fr='main',
       to='entrystore/main',
       result_filter=lambda x: x['state'] == 'added',
   )

Now that we have the latest version of the subdataset, we can repeat the
update procedure (note that this time we push to ``origin``)

.. code:: bash

   $ datalad save -m "Updated subdataset"
   $ datalad run ...
   $ datalad foreach-dataset git annex dead here
   $ datalad push --recursive --to origin
   $ cd ..
   $ datalad drop --recursive --what all --dataset derived_data

Note: in this case our input dataset has two ria siblings, one local
(``ria+file://``) and one remote (``ria+ssh``). Due to this difference,
they should be configured with different "cost" for updating data
(inspect the output of ``git annex info entrystore-storage``). So when
DataLad gets files as part of ``datalad run``, the local storage will be
prioritised, and only the recently added files will be downloaded from
the remote storage. Subsequent push will bring the local storage up to
date, and the process can be repeated.
