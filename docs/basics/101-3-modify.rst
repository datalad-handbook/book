.. _modify:

Starting from scratch: Modifying content
----------------------------------------

So far, we've only added new content to the dataset. And we haven't done
much to that content up this point, to be honest. Lets see what happens if
we add content, and then modify it.

For this, in the root of ``DataLad-101``, create a simple text file
called ``notes.txt``. This will contain all of the notes that you take
throughout the course.

Pick an editor of your choice and write a short summary of how to create
a DataLad dataset from scratch. Below is one way to do it, using the
``cat`` command that comes with any Unix system, and a simple redirection
with ``>``.

.. runrecord:: _examples/DL-101-40
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && cat << EOT > notes.txt
      One can create a new dataset with 'datalad create [--description] PATH'.
      The dataset is created empty
      EOT

   $ cat << EOT > notes.txt
   One can create a new dataset with 'datalad create [--description] PATH'.
   The dataset is created empty
   EOT

Run ``datalad status`` to confirm that there is new, untracked content:

.. runrecord:: _examples/DL-101-42
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && datalad status

   $ datalad status

Save this file in its current state:

.. runrecord:: _examples/DL-101-43
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && datalad save -m "Add notes on datalad create" notes.txt

   $ datalad save -m "Add notes on datalad create" notes.txt

Modify this file by adding another note. After all, you already know how use
``datalad save``, so write a short summary on that as well.

Again, the example below uses Unix commands (``cat`` and redirecting)
to accomplish this, but you can take any editor of your choice.

.. runrecord:: _examples/DL-101-44
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT > notes.txt
   'datalad save [-m] PATH' saves the file (modifications) to history.
   Note to self: Always use informative, concise commit messages.
   EOT

Lets check the datasets current state:

.. runrecord:: _examples/DL-101-45
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad status

and save the file:

.. runrecord:: _examples/DL-101-46
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad save -m "add note on datalad save"

Let's take another look into our history to see the development of this file.
We're using ``git log -p`` to see the difference to the previous state of a
file within each commit. (Note: the output below is an excerpt, if you enter
the git log, your history will be longer. You can get out of git log by pressing
``q``.)

.. runrecord:: _examples/DL-101-47
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1-28
   :emphasize-lines: 6, 14, 20, 28

   $ git log -p

We can see that the history can not only show us the commit message attached to
a commit, but also the precise change that occured in the textfile in the commit.
Additions are marked with a ``+``, and deletions would be shown with a leading ``-``.
Thats quite neat.