
Basic DataLad Magic: Dataset nesting
------------------------------------

Without noticing, the previous section demonstrated another core principle
and feature of DataLad datasets: *Nesting*.

Within DataLad datasets one can *nest* other DataLad
datasets arbitralily deep. This does not seem particulary spectacular -
after all, any directory on a filesystem can have other directories inside it.
The possibility for nested Datasets, however, is one of many advantages
DataLad datasets have:

Any lower-level DataLad dataset (the *subdataset*) has a stand-alone
history. The top-level DataLad dataset (the *superdataset*) only stores
*which version* of the subdataset is currently used.

Remember how we had to navigate into ``books/ml-books`` to see the history,
and how this history was completely indeptendent of the ``DataLad-101``
superdataset history?
Let's check out how the superdatasets history looks like. Make sure you are
not inside of ``ml-books``.

.. runrecord:: _examples/DL-101-6-1
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && git log

   $ git log

By taking advantage of dataset nesting, one can take datasets such as
``ml-books`` and install it as a subdataset within a
superdataset like ``DataLad-101``.

Should the book dataset get extended or changed,
its subdataset can be updated to include the changes easily.

The figure below illustrates dataset nesting schematically:
