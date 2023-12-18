As section :ref:`config` explains, each
sibling is registered in ``.git/config`` in a "submodule" section.
Let's look at how our sibling "roommate" is registered there:

.. runrecord:: /basics/_examples/DL-101-136-160
  :language: console
  :workdir: dl-101/DataLad-101
  :emphasize-lines: 18-19

  $ cat .git/config

As you can see, its "url" is specified as a relative path. Say your
room mate's directory is a dataset you would want to move. Let's see
what happens if we move the dataset such that the path does not point
to the dataset anymore:

.. runrecord:: /basics/_examples/DL-101-136-161
  :language: console
  :workdir: dl-101/DataLad-101

  $ # add an intermediate directory
  $ cd ../mock_user
  $ mkdir onemoredir
  $ # move your room mates dataset into this new directory
  $ mv DataLad-101 onemoredir

This means that relative to your ``DataLad-101``, your room mates
dataset is not at ``../mock_user/DataLad-101`` anymore, but in
``../mock_user/onemoredir/DataLad-101``. The path specified in
the configuration file is thus wrong now.

.. runrecord:: /basics/_examples/DL-101-136-162
  :language: console
  :exitcode: 1
  :workdir: dl-101/mock_user

  $ # navigate back into your dataset
  $ cd ../DataLad-101
  $ # attempt a datalad update
  $ datalad update

Here we go:

.. code-block:: text

  'fatal: '../mock_user/DataLad-101' does not appear to be a git repository
   fatal: Could not read from remote repository.

Git seems pretty insistent (given the amount of error messages) that
it cannot seem to find a Git repository at the location the ``.git/config``
file specified. Luckily, we can provide this information. Edit the file with
an editor of your choice and fix the path from
``url = ../mock_user/DataLad-101`` to
``url = ../mock_user/onemoredir/DataLad-101``.

Below, we are using the stream editor `sed <https://en.wikipedia.org/wiki/Sed>`_
for this operation.

.. runrecord:: /basics/_examples/DL-101-136-163
  :language: console
  :workdir: dl-101/DataLad-101

  $ sed -i 's/..\/mock_user\/DataLad-101/..\/mock_user\/onemoredir\/DataLad-101/' .git/config

This is how the file looks now:

.. runrecord:: /basics/_examples/DL-101-136-164
  :language: console
  :workdir: dl-101/DataLad-101
  :emphasize-lines: 19

  $ cat .git/config

Let's try to update now:

.. runrecord:: /basics/_examples/DL-101-136-165
  :workdir: dl-101/DataLad-101
  :language: console

  $ datalad update

Nice! We fixed it!
Therefore, if a dataset you move or rename is known to other
datasets from its path, or identifies siblings with paths,
make sure to adjust them in the ``.git/config`` file.

To clean up, we'll redo the move of the dataset and the
modification in ``.git/config``.

.. runrecord:: /basics/_examples/DL-101-136-166
  :language: console
  :workdir: dl-101/DataLad-101

  $ cd ../mock_user && mv onemoredir/DataLad-101 .
  $ rm -r onemoredir
  $ cd ../DataLad-101 && sed -i 's/..\/mock_user\/onemoredir\/DataLad-101/..\/mock_user\/DataLad-101/' .git/config
