.. _usecase_encrypted_annex:

Encrypted data storage and transport
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: ! Usecase; Encrypted data storage and transport

Some data are not meant for everybody's eyes - you can share a picture from a midflight-plane-window-view without a problem on your social media account, but you `shouldn't post a photo of your plane ticket next to it <https://mango.pdf.zone/finding-former-australian-prime-minister-tony-abbotts-passport-number-on-instagram>`_.
But there are also data so sensitive that not only should you not share them anywhere, you also need to make sure that they are inaccessible even when someone sneaks into your storage system or intercepts a file transfer - things such as passwords, private messages, or medical data.
One technical solution for this problem is `encryption <https://en.wikipedia.org/wiki/Encryption>`_.
During encryption, the sensitive data are obfuscated in a structured but secret manner, and only authorized agents have the knowledge how to decrypt the data back into a usable state.

Because encryption is relevant or at least attractive to many applications involving data in :term:`DataLad dataset`\s, this use case demonstrates how to
utilize `git-annex's encryption <https://git-annex.branchable.com/encryption/>`_ to keep data safely encrypted when it is not being used.
This example workflow mimics a sensitive data deposition use case, where data need to be securely deposited on one machine, and downloaded to another machine for processing and storage.
To make this work, in our workflow we will combine several independent pieces:

#. Using git-annex encryption
#. Using RIA stores
#. Working in temporary (ephemeral) clones that combine information from
   several remotes.

Note that these components were selected to fit a particular setup, but neither RIA stores nor temporary clones are required components for encryption.

The challenge
=============

Bob does data collection through a web form. Incoming form entries
are saved as individual files by the web server. Bob periodically
imports the data to his local machine, and uses them to produce an
updated summary. For security reasons, he does not want the data to lie
around unencrypted.

.. figure:: ../artwork/src/encryption_sketch.svg

The DataLad approach
====================

Bob sets up his remote machine (web server) so that incoming data are
saved in a DataLad dataset. On that machine, he also creates a RIA
sibling for the dataset (accessible from the outside through SSH, and
only to a few authorized users), and enables encryption for annexed
contents. He chooses a scheme in which the server only has the
encryption key. Each new data file will be saved in the dataset,
pushed to that RIA store, and dropped from the dataset, leaving only
the encrypted copy on the remote server. On his local machine, he also
sets up RIA stores, enables encryption, and scripts his analysis to
check out the datasets locally, fetch updates from the remote machine,
and push data back to local stores. In this way, data are not
available anywhere in decrypted form, except when it is being
processed.

Step by step
============

Before we start: GnuPG
----------------------

DataLad relies on :term:`git-annex` to manage large file content, and git-annex relies in part on `GnuPG <https://gnupg.org/>`__ to manage encryption via *public-key cryptography*.
`Public key cryptography <https://en.wikipedia.org/wiki/Public-key_cryptography>`_ relies on key pairs for encryption and decryption.
To proceed with the next steps, you will need at least one pair of GPG
keys, one *private* (used for decryption) and one *public* (used for
encryption). The relevant keys need to be known to the GPG program on
the machine you are using.

We won't go into detail about GPG, but the most useful commands are:

- ``gpg --full-generate-key`` to generate a key pair,
- ``gpg --list-keys`` and ``gpg --list-secret-keys`` to display known public and private keys,
- ``gpg --export -a [keyID] > my_public_key.asc`` to export a public key, and
- ``gpg --import my_public_key.asc`` to import the previously exported key on another machine.

Setup overview
--------------

In this workflow, we describe encrypted data storage and transport between two locations.
We will call them *remote server* and *local machine*.
In this example, the *remote server* is where the data originates (is created or deposited), and the *local server* is where the data is downloaded to, processed, and saved for future access.

Choices made in the following examples (encryption modes, sibling types, data flow) were dictated by the particular setup of the use case leading to this chapter.
Specifically, our data was entered through a web form; the script responsible for serving the website wrote incoming data into JSON files and saved them into a DataLad dataset.
Although the remote server used for data deposition provided authenticated access only, it was hosted outside of what we considered our trusted infrastructure.
Because of that, for further processing we fetched the encrypted data onto our local machine, which was the only place where we could store decryption keys and access credentials.
Ultimately, the examples should provide a good overview of encrypted data workflows with DataLad, easily adapted to different setups.

Remote server: encrypted deposition
-----------------------------------

On the remote server, we start by creating a DataLad dataset to track the deposition of raw data.
Since encryption is enabled for git-annex :term:`special remote`\s (thus only applies to annexed files), we stay with the default dataset configuration, which annexes all files.

.. code:: bash

   $ datalad create incoming_data
   $ cd incoming data

Then, we create a local :term:`Remote Indexed Archive (RIA) store` as a :term:`sibling` for the dataset. We chose a local RIA because we don't want to move the data outside the server yet.

.. note::

   Using a RIA store is a choice for this use case, but *not* a requirement for data encryption. Encryption can be enabled in the same way for any kind of git-annex :term:`special remote`.
   In fact, the primary use-case for encryption in git-annex is sending file content to remotes hosted by an untrusted party.

The created sibling is called ``entrystore`` in the example below, but by default, a RIA sibling consists of two parts, with ``entrystore`` being only one of them.
The other, which by default uses the sibling name with a ``-storage`` suffix ("``entrystore-storage``"), is an automatically created :term:`special remote` to store annexed files in.

.. code:: bash

   $ datalad create-sibling-ria \
     --new-store-ok --name entrystore \
     --alias incoming-data \
     ria+file:///data/project/store

Now we tell git-annex to encrypt annexed content placed in the store.
We choose regular public key encryption with shared filename encryption (``sharedpubkey``).
In this method, access to *public* keys is required to store files in the remote, but a *private* key is required for retrieval.
So if we only store our public key on the machine, an intruder will have no means to decrypt the data even if they gain access to the server.

.. code:: bash

   $ git annex enableremote \
      entrystore-storage \
      encryption=sharedpubkey \
      keyid=9AB670707D8EA564119785922EF857223E033AF1
   enableremote entrystore-storage (encryption setup) (to gpg keys: 2EF857223E033AF1) ok
   (recording state in git...)

If we want to add another encryption key, the step above can be repeated
with ``keyid+=...``.

With this setup, whenever a new data file is uploaded into the dataset on the server, this file needs to be saved, pushed to encrypted storage, and finally, the unencrypted file needs to be dropped:

.. code:: bash

   $ datalad save -m "Adding new file" entry-file-name.dat
   $ datalad push --to entrystore entry-file-name.dat
   $ datalad drop entry-file-name.dat

An important technical detail about git-annex is that  ``sharedpubkey`` mode encrypts file *content* using GPG, but file *names* using `HMAC <https://en.wikipedia.org/wiki/HMAC>`_.
However, the "HMAC cipher" (the secret used to encrypt) is stored unencrypted in the git repository.
This makes it possible to add new files without access to the private GPG keys - but also means that
access to the git repository will reveal file names.
Since a RIA store combines a bare git repository with annex storage in the same location, this means that we should take care to not include sensitive information in file names.
You can see `git-annex's documentation <https://git-annex.branchable.com/encryption/>`__ and the section :ref:`privacy` for more details.

Local machine: Decryption
-------------------------

In order to retrieve the encrypted data securely from the remote server and perform processing on unencrypted data, we start once again by creating a DataLad dataset:

.. code:: bash

   $ datalad create derived_data
   $ cd derived_data

We then install the dataset from the RIA store on the remote server as a subdataset with input data using :command:`datalad clone` and an :term:`SSH` URL to the dataset in the RIA store.

.. code:: bash

   $ datalad clone -d . ria+ssh://... inputs

Next, we can retrieve all data:

.. code:: bash

   $ datalad get inputs

As long as we have the required private key, GPG will be used to quietly
decrypt all files during the ``get`` operation, so our dataset clone
will contain already decrypted data.

At this stage we may add our data processing code (likely putting it
under ``code`` directory, and using ``.gitattributes`` to decide whether
code files should be tracked by :term:`Git`), and use ``datalad run`` to produce
derived data.

Since we intend all our data to be encrypted at rest also on this
machine, we will create another set of RIA siblings and tell git-annex to use encryption.
Because here we have access to our private key, we will use the default, more flexible, scheme with ``hybrid`` encryption keys.

Note: In the ``hybrid`` mode, a private key is needed for *both* retrieval
and deposition of annexed contents, but it is easy to add new keys
without having to re-encrypt data.
File content and names are encrypted with a symmetric cipher, which is itself encrypted using GPG and stored encrypted in the git repository.
See `git-annex's documentation <https://git-annex.branchable.com/encryption/>`__ for more details.

.. code:: bash

   $ datalad create-sibling-ria \
       --new-store-ok --name localstore \
       --alias derived \
       ria+file:///data/project/store
   $ git annex enableremote \
       localstore-storage \
       encryption=hybrid \
       keyid=2EF857223E033AF1

We repeat the same for the input subdataset, so that we can maintain a local copy of the raw data.

.. code:: bash

   $ cd input
   $ datalad create-sibling-ria \
       --name localstore --alias raw \
       ria+file:///data/project/store
   $ git annex enableremote \
       localstore-storage \
       encryption=hybrid \
       keyid+=2EF857223E033AF1
   $ cd ..

Depending on what is more convenient for us, we could either decide to keep the current dataset clones and drop only the annexed file content after pushing, or treat the clones as temporary and remove them altogether.
Here, we will use the second option.
For this reason, we need to declare the current clones "dead" to git-annex before pushing, so that subsequent clones from the RIA store won't consider this location for obtaining files.
Since we gave the super- and subdataset's siblings the same name, "``localstore``", we can use ``push --recursive``.

.. code:: bash

   $ datalad foreach-dataset git annex dead here
   $ datalad push --recursive --to localstore

And in the end we can clean up by removing the temporary clone:

.. code:: bash

   $ cd ..
   $ datalad drop --recursive --what all --dataset derived_data

.. note::

   Although locations declared to be "dead" are not considered for obtaining files, they still leave a record in the git-annex branch.
   An even better solution would be to create the repository (and subsequent temporary clones) using git-annex's private mode, however, it is not yet fully supported by DataLad.
   See `git-annex's documentation <https://git-annex.branchable.com/tips/cloning_a_repository_privately/>`__
   for private mode and `this DataLad issue <https://github.com/datalad/datalad/issues/6456>`__
   tracking DataLad's support for the configuration.


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

Since we cloned the superdataset from local RIA store, also the subdataset has the `origin` (:term:`Git` :term:`remote`) pointing to that store.
It also has the ``local-storage`` and ``entrystore-storage`` :term:`sibling`\s; these are the
git-annex :term:`special remote`\s for the local and remote RIA stores, respectively.
But to learn about new files that were added in the remote server since we last cloned from there, we need the Git remote.

.. note::

   In the future, adding the git remote manually may become unnecessary.
   See `this issue <https://github.com/datalad/datalad-next/issues/170>`__ tracking related work in DataLad-next extension.

Let's add it then (note that when working with ``datalad
siblings`` or ``git remote`` commands, we cannot use the
``ria+ssh://...#~alias`` URL, and need to use the actual SSH URL and filesystem path).

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

.. find-out-more:: A note to users of Python API

   The results of the ``diff`` command include files that were not changed, so to look for changes we need to filter them by state;
   e.g. if we only expect additions, we can do this:

	.. code:: python

		 added_files = subds.diff(
		   fr='main',
		   to='entrystore/main',
		   result_filter=lambda x: x['state'] == 'added',
	   )

Now that we have the latest version of the subdataset, we can repeat the update procedure (note that this time we push to ``origin``)

.. code:: bash

   $ datalad save -m "Updated subdataset"
   $ datalad run ...
   $ datalad foreach-dataset git annex dead here
   $ datalad push --recursive --to origin
   $ cd ..
   $ datalad drop --recursive --what all --dataset derived_data

Note: in this case our input dataset has two RIA siblings, one local (``ria+file://``) and one remote (``ria+ssh``).
Due to this difference, they should be configured with different "cost" for updating data (inspect the output of ``git annex info entrystore-storage``).
The section :ref:`cloneprio` shows how this can be done.
So when DataLad gets files as part of ``datalad run``, the local storage will be prioritized, and only the recently added files will be downloaded from the remote storage.
Subsequent push will bring the local storage up to
date, and the process can be repeated.
