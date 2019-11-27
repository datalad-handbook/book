.. _nesting2:

More on Dataset nesting
^^^^^^^^^^^^^^^^^^^^^^^

You may have noticed how working in the subdataset felt as if you would be
working in an independent dataset -- there was no information or influence at
all from the top-level ``DataLad-101`` superdataset, and you build up a
completely stand-alone history:

.. runrecord:: _examples/DL-101-132-101
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   $ git log --oneline

In principle, this is no news to you. From section :ref:`nesting` and the
YODA principles you already know that nesting allows for a modular re-use of
any other DataLad dataset, and that this re-use is possible and simple
precisely because all of the information is kept within a (sub)dataset.

What is new now, however, is that you applied changes to the dataset. While
you already explored the looks and feels of the ``longnow`` subdataset in
previous sections, you now *modified* the contents of the ``midterm_project``
subdataset.
How does this influence the superdataset, and how does this look like in the
superdataset's history? You know from section :ref:`nesting` that the
superdataset only stores the *state* of the subdataset. Upon creation of the
dataset, the very first, initial state of the subdataset was thus recorded in
the superdataset. But now, after you finished your project, your subdataset
evolved. Let's query the superdataset what it thinks about this.

.. runrecord:: _examples/DL-101-132-102
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   # move into the superdataset
   $ cd ../
   $ datalad status

From the superdataset's perspective, the subdataset appears as being
"modified". Note that these modifications of the subdataset are not
automatically recorded to the superdataset! This makes sense -- after all it
should be up to you to decide whether you want record something or not --,
but it is worth repeating: If you modify a subdataset, you will need to save
this *in the superdataset* in order to have a clean superdataset status.

Let's save the modification of the subdataset into the history of the
superdataset:

.. runrecord:: _examples/DL-101-132-103
   :language: console
   :workdir: dl-101/DataLad-101/

   $ datalad save -m "finished my midterm project"

Let's check which subproject commit is now recorded in the superdataset:

.. runrecord:: _examples/DL-101-132-104
   :language: console
   :workdir: dl-101/DataLad-101/

   $ git log -p -n 1

As you can see in the log entry, the subproject commit changed from the
first commit hash in the subdataset history to the most recent one. With this
change, therefore, your superdataset tracks the most recent version of
the ``midterm_project`` dataset, and your dataset's status is clean again.
