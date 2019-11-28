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
"modified". Note how it is not individual files that show up as "modified", but
indeed the complete subdataset as a single entity.

What this shows you is that the modifications of the subdataset you performed are not
automatically recorded to the superdataset. This makes sense -- after all it
should be up to you to decide whether you want record something or not --,
but it is worth repeating: If you modify a subdataset, you will need to save
this *in the superdataset* in order to have a clean superdataset status.

Let's save the modification of the subdataset into the history of the
superdataset. For this, to avoid confusion, you can specify explicitly to
which dataset you want to save a modification. ``-d .`` specifies the current
dataset, i.e., ``DataLad-101``, as the dataset to save to:

.. runrecord:: _examples/DL-101-132-103
   :language: console
   :workdir: dl-101/DataLad-101/

   $ datalad save -d . -m "finished my midterm project!" midterm_project

.. findoutmore:: More on how save can operate on nested datasets

   In a superdataset with subdatasets, :command:`datalad save` by default
   tries to figure out on its own which dataset's history of all available
   datasets a :command:`save` should be written to. However, it can reduce
   confusion or allow specific operations to be very explicit in the command
   call and tell DataLad where to save what kind of modifications to.

   If you want to save the current state of the subdataset into the superdataset
   (as necessary here), start a ``save`` from the superdataset and have the
   ``-d/--dataset`` option point to its root::

      # in the root of the superds
      $ datalad save -d . -m "update subdataset"

   If you are in the superdataset, and you want to save an unsaved modification
   in a subdataset to the *subdatasets* history, let ``-d/--dataset`` point to
   the subdataset::

      # in the superds
      $ datalad save -d path/to/subds -m "modified XY"

   The recursive option allows you to save any content underneath the specified
   directory, and recurse into any potential subdatasets::

      $ datalad save . --recursive

Let's check which subproject commit is now recorded in the superdataset:

.. runrecord:: _examples/DL-101-132-104
   :language: console
   :workdir: dl-101/DataLad-101/

   $ git log -p -n 1

As you can see in the log entry, the subproject commit changed from the
first commit hash in the subdataset history to the most recent one. With this
change, therefore, your superdataset tracks the most recent version of
the ``midterm_project`` dataset, and your dataset's status is clean again.