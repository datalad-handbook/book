.. _sharelocal4:

.. _update:

Stay up to date
---------------

All of what you have seen about sharing dataset was really
cool, and for the most part also surprisingly intuitive.
:dlcmd:`run` commands or file retrieval worked exactly as
you imagined it to work, and you begin to think that slowly but
steadily you are getting a feel about how DataLad really works.

But to be honest, so far, sharing the dataset with DataLad was
also remarkably unexciting given that you already knew most of
the dataset magic that your room mate currently is still
mesmerized about.
To be honest, you are not yet certain whether
sharing data with DataLad really improves your life up
until this point. After all, you could have just copied
your directory into your ``mock_user`` directory and
this would have resulted in about the same output, right?

What we will be looking into now is how shared DataLad
datasets can be updated.

Remember that you added some notes on :dlcmd:`clone`,
:dlcmd:`get`, and :gitannexcmd:`whereis` into the
original ``DataLad-101``?

This is a change that is not reflected in your "shared"
installation in ``../mock_user/DataLad-101``:

.. runrecord:: _examples/DL-101-119-101
   :workdir: dl-101/mock_user/DataLad-101
   :notes: On updating dataset. How do we get the updated notes from the original dataset?
   :cast: 04_collaboration

   $ # Inside the installed copy, view the last 15 lines of notes.txt
   $ tail notes.txt

But the original intention of sharing the dataset with
your room mate was to give him access to your notes.
How does he get the notes that you have added in the last
two sections, for example?

This installed copy of ``DataLad-101`` knows its ``origin``, i.e.,
the place it was installed from. Using this information,
it can query the original dataset whether any changes
happened since the last time it checked, and if so, retrieve and
integrate them.

.. index::
   pair: update; DataLad command
   pair: update dataset with remote change; with DataLad

This is done with the :dlcmd:`update --how merge`
command.

.. runrecord:: _examples/DL-101-119-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: retrieve and integrate changes from origin with datalad update --merge
   :cast: 04_collaboration

   $ datalad update --how merge

Importantly, run this command either within the specific
(sub)dataset you are interested in, or provide a path to
the root of the dataset you are interested in with the
``-d``/``--dataset`` flag. If you would run the command
within the ``longnow`` subdataset, you would query this
subdatasets' ``origin`` for updates, not the original
``DataLad-101`` dataset.

Let's check the contents in ``notes.txt`` to see whether
the previously missing changes are now present:

.. runrecord:: _examples/DL-101-119-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: let's check whether the updates are there
   :cast: 04_collaboration

   $ # view the last 15 lines of notes.txt
   $ tail notes.txt

Wohoo, the contents are here!

Therefore, sharing DataLad datasets by installing them
enables you to update the datasets content should the
original datasets' content change -- in only a single
command. How cool is that?!

Conclude this section by adding a note about updating a
dataset to your own ``DataLad-101`` dataset:

.. runrecord:: _examples/DL-101-119-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: note in original ds
   :cast: 04_collaboration

   $ # navigate back:
   $ cd ../../DataLad-101

   $ # write the note
   $ cat << EOT >> notes.txt
   To update a shared dataset, run the command "datalad update --how merge".
   This command will query its origin for changes, and integrate the
   changes into the dataset.

   EOT

.. runrecord:: _examples/DL-101-119-105
   :language: console
   :workdir: dl-101/DataLad-101
   :notes:
   :cast: 04_collaboration

   $ # save the changes
   $ datalad save -m "add note about datalad update"


PS: You might wonder what a plain :dlcmd:`update` command with no option does.
If you are a Git-user and know about branches and merging you can read the
``Note for Git-users``. However, a thorough explanation
and demonstration will be in the next section.

.. index::
   pair: update; DataLad concept
.. gitusernote:: Update internals

   :dlcmd:`update` is the DataLad equivalent of a :gitcmd:`fetch`,
   :dlcmd:`update --how merge` is the DataLad equivalent of a
   :gitcmd:`pull`.
   Upon a simple :dlcmd:`update`, the remote information
   is available on a branch separate from the main branch
   -- in most cases this will be ``remotes/origin/main``.
   You can :gitcmd:`checkout` this branch or run :gitcmd:`diff` to
   explore the changes and identify potential merge conflicts.


.. only:: adminmode

   Add a tag at the section end.

     .. runrecord:: _examples/DL-101-119-106
        :language: console
        :workdir: dl-101/DataLad-101

        $ git branch sct_stay_up_to_date
