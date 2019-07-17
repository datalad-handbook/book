Sharing datasets: Common File systems [2]
-----------------------------------------

In the last section we created a copy of the ``DataLad-101``
dataset on the same file system but a different place by installing
it from a path.

We have observed that in order to install subdatasets right away to
obtain their file content availability meta data to explore
the file hierarchy within the subdatasets the ``-r``/``recursive``
option needs to be given to ``datalad install``.

And we have demonstrated how :term:`Git-annex` retrieved large file
contents from the original dataset.

Let's now see the ``git annex whereis`` command in more detail.
Within the original ``DataLad-101`` dataset, we retrieved some of the ``.mp3``
files via ``datalad get``, but not others. How will this influence the
output of ``git annex whereis``?

.. runrecord:: _examples/DL-101-121-101
   :language: console
   :workdir: dl-101/DataLad-101

   # navigate back into the installed copy of DataLad-101
   $ cd ../mock_user/DataLad-101
   # navigate into the subdirectory
   $ cd recordings/longnow
   # file content exists in original DataLad-101 for this file
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

.. runrecord:: _examples/DL-101-121-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # but not for this:
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2005_01_15__James_Carse__Religious_War_In_Light_of_the_Infinite_Game.mp3

As you can see, the file we downloaded with ``datalad get`` has a third source,
our own computer. The file we did not yet retrieve in the original dataset
only has two sources.

Let's see how this affects a ``datalad get``:

.. runrecord:: _examples/DL-101-121-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # get the first file
   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3


.. runrecord:: _examples/DL-101-121-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # get the second file
   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2005_01_15__James_Carse__Religious_War_In_Light_of_the_Infinite_Game.mp3


The most important thing to note is: It worked in both cases, regardless of whether the original
``DataLad-101`` dataset contained the file content or not.

We can see that Git-annex used two different sources to retrieve the content from,
though, if we look at the very end of the ``get`` summary.
The first file was retrieved "``from origin...``". ``Origin`` is Git terminology
for "from where the dataset was copied from" -- ``origin`` therefore is the
original ``DataLad-101`` dataset.

The second file was retrieved "``from web...``", and thus from a different source.
This source is called ``web`` because it actually is a URL through which this particular
podcast-episode is made available in the first place. You might also have noticed that the
download from web took longer than the retrieval from the directory on the same
file system. But we will get into the details
of this once we cover the ``importfeed`` and ``add-url`` functions.

Let's for now add a note on the ``git annex whereis`` command. Again, do
this in the original ``DataLad-101`` directory, and don't forget to save it.

.. runrecord:: _examples/DL-101-121-105
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # navigate back:
   $ cd ../../../../DataLad-101

   # write the note
   $ cat << EOT >> notes.txt
   The command "git annex whereis PATH" lists the repositories that have
   the file content of an annexed file. When using ``datalad get`` to retrieve
   file content, those repositories will be queried.
   EOT
   $ datalad status
   $ datalad save -m "add note on git annex whereis" notes.txt


.. todo::

   Do we at some point need to explain that and why it does not work like this from
   outside the subdataset?

   Do we need to explain what mih@medusa is?
