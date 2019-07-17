Sharing datasets: Common File systems [2]
-----------------------------------------

In the last section we created a copy of the ``DataLad-101``
dataset on the same file system but a different place by installing
it from a path.

We have observed that in order to install subdatasets right away to
obtain their file content availability meta data to explore
the file hierarchy within the subdatasets the ``-r``/``recursive``
option needs to be given to ``datalad install``

Let's now however see the ``git annex whereis`` command in more detail.
Within the original ``DataLad-101`` dataset, we retrieved some of the ``.mp3``
files via ``datalad get``, but now others. How will this influence the
output of ``git annex whereis``?

.. runrecord:: _examples/DL-101-121-108
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   # navigate into the subdirectory
   $ cd recordings/longnow
   # file content exists in original DataLad-101 for this file
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

.. runrecord:: _examples/DL-101-121-109
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow

   # but not for this:
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2005_01_15__James_Carse__Religious_War_In_Light_of_the_Infinite_Game.mp3

.. todo::

   at some point explain that and why it does not work like this from outside the subdataset

The file thats content is present in the original DataLad-101 has one more copy available
than the file that is not present.

.. todo::

   elaborate on what web and mih@medusa are.

.. todo::

   TODO: back in old directory, updates notes with

   cat << EOT >> notes.txt
   The command git annex whereis PATH lists the repositories that have
   file content.
   EOT


TODO update dataset after note