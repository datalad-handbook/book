.. _sharelocal2:

Where's Waldo?
--------------

So far, you and your room mate have created a copy of the ``DataLad-101``
dataset on the same file system but a different place by installing
it from a path.

You have observed that the ``-r``/``--recursive``
option needs to be given to :dlcmd:`get [-n/--no-data]`
in order to install further potential subdatasets in one go. Only then
is the subdatasets file content availability metadata present to explore
the file hierarchy available within the subdataset.
Alternatively, a :dlcmd:`get -n <subds>` takes care of installing
exactly the specified registered subdataset.

And you have mesmerized your room mate by showing him how :term:`git-annex`
retrieved large file contents from the original dataset.
Your room mate is excited by this magical command.
You however begin to wonder: how does DataLad know where to look for that original content?

This information comes from git-annex.
Before getting another PDF, let's query git-annex where its content is stored:

.. index::
   pair: whereis; git-annex command
   pair: show file content availability; with git-annex
.. runrecord:: _examples/DL-101-117-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: git-annex whereis to find out where content is stored
   :cast: 04_collaboration

   $ # navigate back into the clone of DataLad-101
   $ cd ../mock_user/DataLad-101
   $ git annex whereis books/TLCL.pdf

Oh, another :term:`shasum` - or, more specifically, a :term:`annex UUID`.
This time however not in a symlink...
"That's hard to read -- what is it?" your room mate asks.
You can recognize a path to the dataset on your computer, prefixed with the user and hostname of your computer.
"This", you exclaim, excited about your own realization, "is my dataset's location I'm sharing it from!"

.. index::
   pair: set description for dataset location; with DataLad
.. find-out-more:: What is this location, and what if I provided a description?

   Back in the very first section of the Basics, :ref:`createDS`, a :ref:`Find-out-more mentioned the '--description' option <createdescription>`   of :dlcmd:`create`.
   With this option, you can provide a description about the dataset *location*.

   The :gitannexcmd:`whereis` command, finally, is where such a description
   can become handy: If you had created the dataset with

   .. code-block:: console

      $ datalad create --description "course on DataLad-101 on my private laptop" -c text2git DataLad-101

   the command would show ``course on DataLad-101 on my private laptop`` after
   the :term:`shasum` -- and thus a more human-readable description of *where*
   file content is stored.
   This becomes especially useful when the number of repository copies
   increases. If you have only one other dataset it may be easy to
   remember what and where it is. But once you have one back-up
   of your dataset on a USB stick, one dataset shared with
   Dropbox, and a third one on your institutions
   :term:`GitLab` instance you will be grateful for the descriptions
   you provided these locations with.

   The current report of the location of the dataset is in the format
   ``user@host:path``.

   If the physical location of a dataset is not relevant, ambiguous, or volatile,
   or if it has an :term:`annex` that could move within the foreseeable lifetime of a
   dataset, a custom description with the relevant information on the dataset is
   superior. If this is not the case, decide for yourself whether you want to use
   the ``--description`` option for future datasets or not depending on what you
   find more readable -- a self-made location description, or an automatic
   ``user@host:path`` information.


The message further informs you that there is only "``(1 copy)``" of this file content.
This makes sense: There is only your own, original ``DataLad-101`` dataset in which this book is saved.

To retrieve file content of an annexed file such as one of these PDFs, git-annex will try to obtain it from the locations it knows to contain this content.
It uses the checksums to identify these locations.
Every copy of a dataset will get a unique ID with such a checksum.
Note however that just because git-annex knows a certain location where content was once it does not guarantee that retrieval will work.
If one location is a USB stick that is in your bag pack instead of your USB port, a second location is a hard drive that you deleted all of its previous contents (including dataset content) from,
and another location is a web server, but you are not connected to the internet, git-annex will not succeed in retrieving contents from these locations.
As long as there is at least one location that contains the file and is accessible, though, git-annex will get the content.
Therefore, for the books in your dataset, retrieving contents works because you and your room mate share the same file system.
If you'd share the dataset with anyone without access to your file system, ``datalad get`` would not work, because it cannot access your files.

But there is one book that does not suffer from this restriction:
The ``bash_guide.pdf``.
This book was not manually downloaded and saved to the dataset with ``wget`` (thus keeping DataLad in the dark about where it came from), but it was obtained with the :dlcmd:`download-url` command.
This registered the books original source in the dataset, and here is why that is useful:

.. runrecord:: _examples/DL-101-117-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ git annex whereis books/bash_guide.pdf

Unlike the ``TLCL.pdf`` book, this book has two sources, and one of them is ``web``.
The second to last line specifies the precise URL you downloaded the file from.
Thus, for this book, your room mate is always able to obtain it (as long as the URL remains valid), even if you would delete your ``DataLad-101`` dataset.

We can also see a report of the source that git-annex uses to retrieve the content from if we look at the very end of the ``get`` summary.

.. runrecord:: _examples/DL-101-117-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad get books/TLCL.pdf
   $ datalad get books/bash_guide.pdf

Both of these files were retrieved "``from origin...``".
``Origin`` is Git terminology for "from where the dataset was copied from" -- ``origin`` therefore is the original ``DataLad-101`` dataset from which file content can be retrieved from very fast.

If your roommate did not have access to the same file system or you deleted your ``DataLad-101`` dataset, this output would look differently.
The ``datalad get`` command would fail on the ``TLCL.pdf`` book without a known second source, and ``bash_guide.pdf`` would be retrieved "``from web...``" - the registered second source, its original download URL.
Let's see a retrieval from ``web`` in action for another file.
The ``.mp3`` files in the ``longnow`` seminar series have registered web URLs [#f1]_.

.. runrecord:: _examples/DL-101-117-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: More on how git-annex whereis behaves
   :cast: 04_collaboration

   $ # navigate into the subdirectory
   $ cd recordings/longnow
   $ git annex whereis Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3
   $ datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3

As you can see at the end of the ``get`` result, the files has been retrieved ``from web...``.
Quite useful, this provenance, right?
Let's add a note on the :gitannexcmd:`whereis` command.
Again, do this in the original ``DataLad-101`` directory, and do not forget to save it.

.. runrecord:: _examples/DL-101-117-105
   :language: console
   :workdir: dl-101/mock_user/DataLad-101/recordings/longnow
   :notes: a note in original dataset
   :cast: 04_collaboration

   $ # navigate back:
   $ cd ../../../../DataLad-101

   $ # write the note
   $ cat << EOT >> notes.txt
   The command "git annex whereis PATH" lists the repositories that have
   the file content of an annexed file. When using "datalad get" to
   retrieve file content, those repositories will be queried.

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


.. only:: adminmode

   Add a tag at the section end.

     .. runrecord:: _examples/DL-101-117-108
        :language: console
        :workdir: dl-101/DataLad-101

        $ git branch sct_where_is_waldo


.. rubric:: Footnotes

.. [#f1] Maybe you wonder what the location ``mih@medusa`` is. It is a copy of the
         data on an account belonging to user ``mih`` on the host name ``medusa``.
         Because we do not have the host names' address, nor log-in credentials for
         this user, we cannot retrieve content from this location. However, somebody
         else (for example, the user ``mih``) could.
