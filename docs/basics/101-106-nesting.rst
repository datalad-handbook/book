.. _nesting:

Dataset nesting
---------------

.. index:: ! nesting

Without noticing, the previous section demonstrated another core principle
and feature of DataLad datasets: *Nesting*.

Within DataLad datasets one can *nest* other DataLad
datasets arbitrarily deep. We for example just installed one dataset, the
``longnow`` podcasts, *into* another dataset, the ``DataLad-101`` dataset.
This was done by supplying the ``--dataset``/``-d`` flag in the command call.

At first glance, nesting does not seem particularly spectacular --
after all, any directory on a file system can have other directories inside of it.

The possibility for nested Datasets, however, is one of many advantages
DataLad datasets have:

One aspect of nested datasets is that any DataLad dataset
(*subdataset* or *superdataset*) keeps their stand-alone
history. The top-level DataLad dataset (the *superdataset*) only stores
*which version* of the subdataset is currently used through an identifier.

Let's dive into that.
Remember how we had to navigate into ``recordings/longnow`` to see the history,
and how this history was completely independent of the ``DataLad-101``
superdataset history? This was the subdataset's own history.

Apart from stand-alone histories of super- or subdatasets, this highlights another
very important advantage that nesting provides: Note that the ``longnow`` dataset
is a completely independent, standalone dataset that was once created and
published. Nesting allows for a modular re-use of any other DataLad dataset,
and this re-use is possible and simple precisely because all of the information
is kept within a (sub)dataset.

But now let's also check out how the *superdataset's* (``DataLad-101``) history
looks like after the addition of a subdataset. To do this, make sure you are
*outside* of the subdataset ``longnow``. Note that the first commit is our recent
addition to ``notes.txt``, so we'll look at the second most recent commit in
this excerpt.

.. runrecord:: _examples/DL-101-106-101
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1, 22-62
   :emphasize-lines: 25
   :realcommand: git log -p
   :cast: 01_dataset_basics
   :notes: The superdataset only stores the version of the subdataset.  Let's take a look into how the superdataset's history looks like

   $ git log -p -n 3

We have highlighted the important part of this rather long commit summary.
Note that you can not see any ``.mp3``\s being added to the dataset,
as was previously the case when we :command:`datalad save`\d PDFs that we
downloaded into ``books/``. Instead,
DataLad stores what it calls a *subproject commit* of the subdataset.
The cryptic character sequence in this line is the :term:`shasum` we have briefly
mentioned before, and it is the identifier that
DataLad internally used to identify the files and the changes to the files in the subdataset. Exactly, this
:term:`shasum` is what identifies the state of the subdataset.


Navigate back into ``longnow`` and try to find the highlighted shasum in the
subdataset's history:

.. runrecord:: _examples/DL-101-106-102
   :language: console
   :workdir: dl-101/DataLad-101
   :lines: 1-9
   :emphasize-lines: 3
   :cast: 01_dataset_basics
   :notes: We can find this shasum in the subdatasets history: it's the most recent change

   $ cd recordings/longnow
   $ git log --oneline

We can see that it is the most recent commit shasum of the subdataset
(albeit we can see only the first seven characters here -- a :command:`git log`
would show you the full shasum). Thus, your dataset does not only know the origin
of its subdataset, but also which version of the subdataset to use,
i.e., it has the identifier of the stage/version in the subdataset's evolution to be used.
This is what is meant by "the top-level DataLad dataset (the *superdataset*) only stores
*which version* of the subdataset is currently used through an identifier".



Importantly, once we learn how to make use of the history of a dataset,
we can set subdatasets to previous states, or *update* them.

.. find-out-more:: Do I have to navigate into the subdataset to see it's history?

   Previously, we used :command:`cd` to navigate into the subdataset, and
   subsequently opened the Git log. This is necessary, because a :command:`git log`
   in the superdataset would only return the superdatasets history.
   While moving around with ``cd`` is straightforward, you also found it
   slightly annoying from time to time to use the ``cd`` command so often and also
   to remember in which directory you currently are in. There is one
   trick, though: ``git -C`` (note that it is a capital C) lets you perform any
   Git command in a provided path. Providing this option together with a path to
   a Git command let's you run the command as if Git was started in this path
   instead of the current working directory.
   Thus, from the root of ``DataLad-101``, this command would have given you the
   subdataset's history as well::

      $ git -C recordings/longnow log --oneline

In the upcoming sections, we'll experience the perks of dataset nesting
frequently, and everything that might seem vague at this point will become
clearer. To conclude this demonstration,
the figure below illustrates the current state of our dataset, ``DataLad-101``, with its nested subdataset.

.. figure:: ../artwork/src/virtual_dstree_dl101.svg
   :width: 70%

   Virtual directory tree of a nested DataLad dataset

Thus, without being consciously aware of it, by taking advantage of dataset
nesting, we took a dataset ``longnow`` and installed it as a
subdataset within the superdataset  ``DataLad-101``.

If you have executed the above code snippets, make sure to go back into the
root of the dataset again:

.. runrecord:: _examples/DL-101-106-103
   :language: console
   :workdir: dl-101/DataLad-101/recordings/longnow
   :cast: 01_dataset_basics

   $ cd ../../
