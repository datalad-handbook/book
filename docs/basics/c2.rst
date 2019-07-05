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
``echo`` command that comes with any Unix system, and a simple redirection
with ``>``.

.. runrecord:: _examples/DL-101-m-1
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && echo "One can create a new dataset with 'datalad create [--description] PATH'. The dataset is created empty" > notes.txt

   $ echo "One can create a new dataset with 'datalad create [--description] PATH'. The dataset is created empty" > notes.txt

Run ``datalad status`` to confirm that there is new, untracked content:

.. runrecord:: _examples/DL-101-m-2
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && datalad status

   $ datalad status

Save this file in its current state:

.. runrecord:: _examples/DL-101-m-3
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && datalad save -m "Add notes on datalad create" notes.txt

   $ datalad save -m "Add notes on datalad create" notes.txt

Modify this file by adding another note. After all, you already know how use
``datalad save``, so write a short summary on that as well.

Again, the example below uses Unix commands (``echo`` and redirecting, but *appending*
with ``>>``) to accomplish this, but you can take an editor of your choice.
