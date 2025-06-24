.. _challengeSubDS:

Challenge: DataLad Subdatasets
******************************

.. importantnote:: You can always get help

   In order to learn about available DataLad commands, use ``datalad --help``. In order to learn more about a specific command, use ``datalad <subcommand> --help``.


Challenge 1
"""""""""""

Datasets can have subdatasets.
Let's build a nested dataset from scratch.
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

.. find-out-more:: Downloading first:

   There are several ways to accomplish this. The solution below uses ``download`` command from ``datalad-next`` and :dlcmd:`run` inside of the subdataset.

   .. runrecord:: _examples/cha-102-102-subdatasets-3
      :language: console
      :workdir: challenges/102-102-subdataset/penguin-report

      $ cd inputs
      $ datalad run -m "Download penguin data" "datalad download 'https://pasta.lternet.edu/package/data/eml/knb-lter-pal/219/5/002f3893385f710df69eeebe893144ff adelie.tst' 'https://pasta.lternet.edu/package/data/eml/knb-lter-pal/220/7/e03b43c924f226486f2f0ab6709d2381 gentoo.tsv' 'https://pasta.lternet.edu/package/data/eml/knb-lter-pal/221/8/fe853aa8f7a59aa84cdd3197619ef462 chinstrap.csv'"


Afterwards, record the new subdataset state in the superdataset.

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

Challenge 4
"""""""""""

Clone the following dataset: https://github.com/psychoinformatics-de/studyforrest-data.
Try to list the available subdatasets.


.. find-out-more:: I'm excited!

   Start with cloning:

   .. runrecord:: _examples/cha-102-102-subdatasets-7
      :language: console
      :workdir: challenges/102-102-subdataset

      $ datalad clone https://github.com/psychoinformatics-de/studyforrest-data.git


   Find out about subdatasets afterwards:

   .. runrecord:: _examples/cha-102-102-subdatasets-8
      :language: console
      :workdir: challenges/102-102-subdataset

      $ cd studyforrest-data
      $ datalad subdatasets

Take a look at any of the subdatasets' directories. Why do they appear to be empty?
What do you need to do to retrieve availability information about a dataset, but not download its content? Try with the subdataset ``original/phase2``.

.. find-out-more:: Okidoki, I'm ready.

   .. runrecord:: _examples/cha-102-102-subdatasets-9
      :language: console
      :workdir: challenges/102-102-subdataset/studyforrest-data

      $ datalad get -n original/phase2

   .. windows-wit:: Beware of Windows path semantics

      On Windows, make sure to adjust the path to the subdataset::

         $ datalad get -r original\phase2

Where can you find out about the origin location of a dataset's subdatasets?

.. find-out-more:: Let's see!

   The information is stored in the superdatasets' ``.gitmodules`` file:

   .. runrecord:: _examples/cha-102-102-subdatasets-11
      :language: console
      :workdir: challenges/102-102-subdataset/studyforrest-data

      $ cat .gitmodules

Navigate into the newly installed subdataset ``original/phase2``.
Run :term:`gitk` and explore its files to find out what this dataset is all about.