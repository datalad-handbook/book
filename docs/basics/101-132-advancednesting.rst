.. _nesting2:

More on Dataset nesting
^^^^^^^^^^^^^^^^^^^^^^^

Working on the YODA-compliant data analysis project gave you the opportunity
to thoroughly experience dataset nesting for the first time. The ``longnow``
dataset was only installed and explored -- but the ``midterm_project``
subdataset is a subdataset that you modified and worked in.

Note a few things:

- Being inside of the dataset feels normal, and no info about anything
  outside of the dataset
- Build up a standalone history in the subdataset


BUT how does this look like in the superdataset? You know from section
:ref:`nesting` that the superdataset only stores the *state* of the
subdataset. Upon creation of the dataset, the very first, initial state of
the subdataset was thus recorded in the superdataset. But now, after you
finished your project, your subdataset evolved. Let's query the superdataset
what it thinks about this.


todo: the Git -C option to perform command across dataset boundaries without
cd'ing