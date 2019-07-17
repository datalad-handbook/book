Updating datasets: The basics
-----------------------------

So far sharing the dataset with DataLad was remarkably
unexciting. To be honest, you're not yet certain whether
sharing data with DataLad really improves your life up
until this point. After all, you could have just copied
your directory into your ``mock_user`` directory and
this would have resulted in about the same output, right?

What we will be looking into now is how shared DataLad
datasets can be updated.

Remember that you added some notes on ``datalad install``
and ``git annex whereis`` into the original ``DataLad-101``?

This is a change that is not reflected in your "shared"
installation in ``../mock_user/DataLad-101``:

.. runrecord:: _examples/DL-101-122-101
   :language: console
   :workdir: dl-101/DataLad-101

   # we navigate into the installed copy:
   $ cd ../mock_user/DataLad-101
   $ cat notes.txt

However, this installed copy knows its ``origin``, i.e.
the place it was installed from. Using this information,
it can query the original dataset whether any changes
happened since the last time it checked.

This is done with the ``datalad update --merge`` command.

.. runrecord:: _examples/DL-101-122-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad update --merge

Importantly, run this command either within the specific
(sub)dataset you are interested in, or provide a path to
the root of the dataset you are interested in with the
``-d``/``--dataset`` flag. If you would run the command
within the ``longnow`` subdataset, you would query this
subdatasets' ``origin`` for updates, not the original
``DataLad-101`` dataset.

Let's check the contents in ``notes.txt`` to see whether
the previously missing changes are now present:



.. gitusernote::

   ``datalad update`` is the DataLad equivalent of a ``git fetch``,
   ``datalad update --merge`` is the DataLad equivalent of a
   ``git pull``.
   Upon a simple ``datalad update``, the remote information
   is available on a branch seperate from the master branch
   -- in most cases this will be ``remotes/origin/master``.
   You can ``git checkout`` this branch or run ``git diff`` to
   explore the changes and identify potential merge conflicts.