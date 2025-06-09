.. index::
   pair: create; DataLad command
   pair: create dataset; with DataLad
.. _challengeDS:

Challenge: DataLad Datasets
***************************

.. importantnote:: You can always get help

   In order to learn about available DataLad commands, use ``datalad --help``. In order to learn more about a specific command, use ``datalad <subcommand> --help``.


Challenge 1
"""""""""""

Create a dataset called ``my-dataset`` on your computer.
Inside of the dataset, run the command ``gitk`` and explore it.

Can you find:

- the dataset identifier?
- the version label?
- the dataset creator?
- the dataset creation date?

Afterwards, run the command ``gitk --all``. What is the difference from before?

.. find-out-more:: Show me how to do it

	To create a new dataset, run:

	.. runrecord:: _examples/cha-102-101-datasets-1
	   :language: console
	   :workdir: challenges/102-101-dataset

	   $ datalad create my-dataset

Finally, remove the dataset.

.. find-out-more:: How do I do that?

	To remove it, run :dlcmd:`drop`. Importantly, this command needs to run *outside* of the dataset.

	.. runrecord:: _examples/cha-102-101-datasets-2
	   :language: console
	   :workdir: challenges/102-101-dataset

	   $ datalad drop --what all -d my-dataset --reckless availability


Challenge 2
"""""""""""

Text files are digital files containing plain text.
Take a minute to think:
- Why is it often useful to keep textfiles out of git-annex?
On the other hand, what could be a reason to annex text files?

.. find-out-more:: Tell me!

   **Why is it useful to keep textfiles out of git-annex**?

   - To make editing easier (no need to unlock)
   - To have a nicer Git history (commits can show differences between file revisions)
   - To distribute the file automatically with every clone (unlike with annexed files, file content of files kept in Git is readily available in shared dataset clones)

   **What could be a reason to annex text files?**

   - To keep file contents private/secret (annexing files allows access control)
   - An unusually large text file (at least dozens of MB)

Create a DataLad dataset called ``text2gitdataset`` and configure it to never annex text files (there are several ways to do this!).

.. find-out-more:: Ok, show me the ways!

   **1. Right at dataset creation**

   .. runrecord:: _examples/cha-102-101-datasets-3
      :language: console
      :workdir: challenges/102-101-dataset

      $ datalad create -c text2git text2gitdataset

   **2. After dataset creation** with a :dlcmd:`run-procedure`

   .. runrecord:: _examples/cha-102-101-datasets-4
      :language: console
      :workdir: challenges/102-101-dataset

      $ datalad create text2gitdataset-2
      $ cd text2gitdataset-2
      $ datalad run-procedure cfg_text2git

   **3. By editing .gitattributes by hand**

   .. runrecord:: _examples/cha-102-101-datasets-5
      :language: console
      :workdir: challenges/102-101-dataset

      $ datalad create text2gitdataset-3
      $ cd text2gitdataset-3
      $ echo "* annex.largefiles=(mimeencoding=binary)and(largerthan=0))" >> .gitattributes
      $ datalad save -m "configure Dataset to keep text files in Git"

In the end, remove the datasets.

.. find-out-more:: Can you show me again?

   Clean-up:

   .. runrecord:: _examples/cha-102-101-datasets-6
      :language: console
      :workdir: challenges/102-101-dataset

      $ datalad drop -d text2gitdataset --what all --reckless availability
      $ datalad drop -d text2gitdataset-2 --what all --reckless availability
      $ datalad drop -d text2gitdataset-3 --what all --reckless availability

Challenge 3
"""""""""""

Version controlling a file means to record its changes over time, associate those changes with an author, date, and identifier, creating a lineage of file content, and being able to revert changes or restore previous file versions.
DataLad datasets can version control their contents, regardless of size.

Create a new dataset ``my-dataset`` that is configured to store text files in Git (see previous challenge) and add a ``README.md`` file with some content into it.
Make sure to save it with a helpful commit message, and inspect your datasets revision history.

.. find-out-more:: Let's go!

   Create the dataset and ``cd`` into it:

   .. runrecord:: _examples/cha-102-101-datasets-7
      :language: console
      :workdir: challenges/102-101-dataset

      $ datalad create -c text2git my-dataset
      $ cd my-dataset

   Create a text file and save it (you can also create a text file with an editor of your choice, e.g., :term:`vim`.)

   .. runrecord:: _examples/cha-102-101-datasets-8
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ echo "# Example Dataset" > README.md
      $ datalad status

   .. runrecord:: _examples/cha-102-101-datasets-9
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ datalad save -m "add a README to the dataset"

   Check the dataset's history:

   .. runrecord:: _examples/cha-102-101-datasets-10
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ git log

Run ``gitk`` again. Can you find the dataset modification date?

Finally, edit the README and save it again.

.. find-out-more:: Let's go!

   .. runrecord:: _examples/cha-102-101-datasets-11
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ echo "This is my example dataset" >> README.md
      $ datalad save -m "Add redundant explanation"

Challenge 4
"""""""""""

Download and save the following set of penguin images available at the URLs below into a dataset:

- ``chinstrap_01.jpg``: https://unsplash.com/photos/3Xd5j9-drDA/download?force=true
- ``chinstrap_02.jpg``: https://unsplash.com/photos/8PxCm4HsPX8/download?force=true

You can reuse the dataset from the previous challenge, or create a new one.
Can you do the download while recording provenance?

.. find-out-more:: Give me a hint about provenance

   Try using :dlcmd:`download-url` or `datalad-next's  "download" command <https://docs.datalad.org/projects/next/en/stable/generated/man/datalad-download.html>`_ combined with :dlcmd:`run`.

.. find-out-more:: Show me the entire solution

   You can download a file and save it manually:

   .. runrecord:: _examples/cha-102-101-datasets-12
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ wget -q -O chinstrap_01.jpg "https://unsplash.com/photos/3Xd5j9-drDA/download?force=true"
      $ datalad save -m "Add image manually downloaded from unsplash"

   Or download it recording its origin as provenance:

   .. runrecord:: _examples/cha-102-101-datasets-13
      :language: console
      :workdir: challenges/102-101-dataset/my-dataset

      $ datalad run -m "Add image from unsplash" " datalad download 'https://unsplash.com/photos/8PxCm4HsPX8/download?force=true chinstrap_02.jpg'"

Run ``gitk`` in the dataset.
Can you find the file identifier of any of the newly downloaded files?

Challenge 5
"""""""""""

Other than creating datasets on your own, DataLad allows to clone existing datasets, too.
Clone and explore the dataset from the following publication:

> *Wittkuhn, L., Schuck, N.W. Dynamics of fMRI patterns reflect sub-second activation sequences and reveal replay in human visual cortex. Nat Commun 12, 1795 (2021). https://doi.org/10.1038/s41467-021-21970-2*

You can find it at https://github.com/lnnrtwttkhn/highspeed-analysis.


.. find-out-more:: Show me how to clone it

   .. runrecord:: _examples/cha-102-101-datasets-14
      :language: console
      :workdir: challenges/102-101-dataset/

      $ datalad clone https://github.com/lnnrtwttkhn/highspeed-analysis.git

Explore the dataset:

- When was it created?
- When was it last updated?
- How many contributors does it have?
- How much annexed file content does it contain?
- How many subdatasets are there?

.. find-out-more:: Let's compare explorations

   When was it created?

   .. runrecord:: _examples/cha-102-101-datasets-15
      :language: console
      :workdir: challenges/102-101-dataset/

      $ cd highspeed-analysis
      # first commit
      $ git log $(git rev-list --max-parents=0 HEAD)

   When was it last updated?

   .. runrecord:: _examples/cha-102-101-datasets-16
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      # most recent commit
      $ git show

   How many contributors does it have?

   .. runrecord:: _examples/cha-102-101-datasets-17
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      # contributions by contributor
      $ git shortlog -s

   How much annexed file content does it contain?

   .. runrecord:: _examples/cha-102-101-datasets-18
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      $ datalad status --annex all

   How many subdatasets are there?

   .. runrecord:: _examples/cha-102-101-datasets-19
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      $ datalad subdatasets

Finally, get the annexed file content and drop it afterwards.

.. find-out-more:: Yeah, data!

   Get it...

   .. runrecord:: _examples/cha-102-101-datasets-20
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      $ datalad get .

   Drop it!

   .. runrecord:: _examples/cha-102-101-datasets-21
      :language: console
      :workdir: challenges/102-101-dataset/highspeed-analysis

      $ datalad drop .
