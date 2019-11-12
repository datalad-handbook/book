.. _sharelocal2:

Where's Waldo?
--------------

So far, your room mate and you have created a copy of the ``DataLad-101``
dataset on the same file system but a different place by installing
it from a path.

You have observed that the ``-r``/``--recursive``
option needs to be given to :command:`datalad install`
in order to install subdatasets right away. Only then
is the subdatasets file content availability metadata to explore
the file hierarchy available within the subdataset right
from the start. Alternatively, a subsequent :command:`datalad install`
in the subdataset or with a path to the subdataset takes care
of the missing installation.

And you have mesmerized your room mate by showing him how :term:`Git-annex`
retrieved large file contents from the original dataset.

Let's now see the :command:`git annex whereis` command in more detail,
and find out how Git-annex knows *where* file content can be obtained from.
Within the original ``DataLad-101`` dataset, you retrieved some of the ``.mp3``
files via :command:`datalad get`, but not others. How will this influence the
output of :command:`git annex whereis`, you wonder?

Together with your room mate, you decide to find out. You navigate
back into the installed copy, and run :command:`git annex whereis` on a
file that you once retrieved file content for, and on a file
that you did not yet retrieve file content for.
Here is the output for the retrieved file:

.. runrecord:: _examples/DL-101-117-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: More on how git-annex whereis behaves
   :cast: 04_collaboration

   # navigate back into the installed copy of DataLad-101
   $ cd ../mock_user/DataLad-101
   # navigate into the subdirectory
   $ cd recordings/longnow
   # file content exists in original DataLad-101 for this file
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

And here is the output for a file that you did not yet retrieve
content for in your original ``DataLad-101`` dataset.

.. runrecord:: _examples/DL-101-117-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow
   :cast: 04_collaboration

   # but not for this:
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2005_01_15__James_Carse__Religious_War_In_Light_of_the_Infinite_Game.mp3

As you can see, the file content previously downloaded with a
:command:`datalad get` has a third source, your original dataset on your computer.
The file we did not yet retrieve in the original dataset
only has only two sources.

Let's see how this affects a :command:`datalad get`:

.. runrecord:: _examples/DL-101-117-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow
   :notes: Get a file thats present in original and one that is not
   :cast: 04_collaboration

   # get the first file
   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3


.. runrecord:: _examples/DL-101-117-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow
   :cast: 04_collaboration

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
of this type of content source
once we cover the ``importfeed`` and ``add-url`` functions [#f1]_.

Let's for now add a note on the :command:`git annex whereis` command. Again, do
this in the original ``DataLad-101`` directory, and do not forget to save it.

.. runrecord:: _examples/DL-101-117-105
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow
   :notes: a note in original dataset
   :cast: 04_collaboration

   # navigate back:
   $ cd ../../../../DataLad-101

   # write the note
   $ cat << EOT >> notes.txt
   The command "git annex whereis PATH" lists the repositories that have
   the file content of an annexed file. When using "datalad get" to retrieve
   file content, those repositories will be queried.

   EOT

.. runrecord:: _examples/DL-101-117-106
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 04_collaboration

   $ datalad status

.. runrecord:: _examples/DL-101-117-107
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 04_collaboration

   $ datalad save -m "add note on git annex whereis"


.. rubric:: Footnotes

.. [#f1] Maybe you wonder what the location ``mih@medusa`` is. It is a copy of the
         data on an account belonging to user ``mih`` on the host name ``medusa``.
         Because we do not have the host names' address, nor log-in credentials for
         this user, we can not retrieve content from this location. However, somebody
         else (for example the user ``mih``) could.
