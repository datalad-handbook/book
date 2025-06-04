.. _challengeSubDS:

Challenge: DataLad Subdatasets
******************************

Datasets can have subdatasets.
Let's build a nested dataset from scratch.

Challenge 1
"""""""""""

Start by creating a dataset called ``penguin-report``, and inside of it, create a subdataset called ``inputs``::

   penguin-report
   └── inputs


.. find-out-more:: Show me how to do it

   Create a new dataset as the superdataset:

   .. runrecord:: _examples/cha-102-102-subdatasets-1
      :language: console
      :workdir: challenges/102-102-subdataset

      $ datalad create penguin-report
      $ cd penguin-report

   Next, a subdataset ``inputs`` is created and registered inside of the superdataset using ``-d``:

   .. runrecord:: _examples/cha-102-102-subdatasets-2
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report

      $ datalad create -d . inputs

Challenge 2
"""""""""""

Let's populate the subdataset with contents.
Download the following set of CSV files into the ``inputs`` dataset and save them:

- adelie.csv: https://pasta.lternet.edu/package/data/eml/knb-lter-pal/219/5/002f3893385f710df69eeebe893144ff
- gentoo.csv: https://pasta.lternet.edu/package/data/eml/knb-lter-pal/220/7/e03b43c924f226486f2f0ab6709d2381
- chinstrap.csv: https://pasta.lternet.edu/package/data/eml/knb-lter-pal/221/8/fe853aa8f7a59aa84cdd3197619ef462

Afterwards, record the new subdataset state in the superdataset.

.. find-out-more:: Downloading first:

   There are several ways to accomplish this. The solution below uses :dlcmd:`download` inside of the subdataset.

   .. runrecord:: _examples/cha-102-102-subdatasets-3
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report

      $ cd inputs
      $ datalad download-url -d . -m "Add Adelie data" -O adelie.csv https://pasta.lternet.edu/package/data/eml/knb-lter-pal/219/5/002f3893385f710df69eeebe893144ff
      $ datalad download-url -d . -m "Add Gentoo data" -O gentoo.csv https://pasta.lternet.edu/package/data/eml/knb-lter-pal/220/7/e03b43c924f226486f2f0ab6709d2381
      $ datalad download-url -d . -m "Add Chinstrap data" -O chinstrap.csv https://pasta.lternet.edu/package/data/eml/knb-lter-pal/221/8/fe853aa8f7a59aa84cdd3197619ef462


.. find-out-more:: Saving the updated subdataset state

   ``datalad status`` in the superdataset will show that the subdataset changed:

   .. runrecord:: _examples/cha-102-102-subdatasets-4
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report/inputs

      $ cd ..
      $ datalad status

   To save this most recent state use :dlcmd:`save` with ``-d``:

   .. runrecord:: _examples/cha-102-102-subdatasets-5
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report/inputs

      # navigate into penguin-report superdataset
      $ cd ..
      $ datalad save -d . -m "Save updated subdataset version"

Challenge 3
"""""""""""

Where can you find out about the subdataset version?

.. find-out-more:: Tell me!

   The information is stored in commits about the subdataset - but only in the superdataset. Take a look at the so called "subproject commit":

   .. runrecord:: _examples/cha-102-102-subdatasets-6
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report

      $ git show inputs

