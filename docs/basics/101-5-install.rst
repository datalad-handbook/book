Basic DataLad magic: Installing datasets
----------------------------------------

So far, we have created a ``DataLad-101`` course dataset. We saved some additional readings
into the dataset, and have carefully made and saved notes on the DataLad
commands we discovered.

But we've been told that with DataLad we could very easily get vast amounts of data to our
computer. Rumor has it that this would be only a single command in the terminal!
Therefore, everyone in todays lecture exitedly await todays topic: Installing datasets.

"With DataLad, users can *install* existing
DataLad datasets from paths, urls, or open-data collections." our lecturer begins.
"This makes accessing data fast and easy. A dataset that others could install can be
created by anyone, without a need for external software. Your own Datasets can be
installed by others, should you want that, for example. Therefore, not only accessing
data becomes fast and easy, but also *sharing*."

"Thats so cool!", you think. "Exam preparation will be a piece of cake if all of us
can share our mid-term and final projects easily!"

"But today, lets only focus on how to install a dataset", she continuous.

"Damn it! Can't we have longer lectures?", you think and set alarms to all of the
upcoming lecture dates in your calender.
There is so much exciting stuff to come, you can't miss a single one.

Installing an existing dataset is done with the ``datalad install`` command.
The command takes a location of an existing dataset (the *source*), and a path to where you want
the dataset to be installed. The source can be a URL or a path to a local directory,
or an SSH server. Additionally, it can also be a pointer to an open-data collection,
for example :term:`the DataLad superdataset ///` (more on this later, though).

Let's try this. To practice, we're using one of the many openly available datasets that
DataLad provides in a public registry that anyone can access. One of these datasets is a
collection of great (and free) machine learning books. The DataLad-101 course is not
a machine-learning course, but those are nevertheless a good addition to the large stash
of yet-to-read text books we piled up. Lets install this dataset into our exisiting
DataLad-101 dataset, inside the directory books.

Because we are installing a dataset within an existing dataset, we supply the ``-d``
(``--dataset``) flag. This specifies the dataset to perform the operation on. Because we are inside
of the ``DataLad-101`` dataset, the pointer to the dataset is a ``.`` (which is Unix
way for saying "current directory"). The dataset to be installed lives on Github, and
we can give its Github URL as a source (``-s``, ``--source``).

.. runrecord:: _examples/DL-101-5-1
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 &&  datalad install -d . -s https://github.com/datalad-datasets/machinelearning-books.git books/ml-books

   $  datalad install -d . -s https://github.com/datalad-datasets/machinelearning-books.git books/ml-books

This command copied the repository found at the URL https://github.com/datalad-datasets/machinelearning-books.git
into the existing ``DataLad-101`` dataset, into the directory ``books/ml-books``.

Note: if we had not specified the path ``books/ml-books``, the command would have installed the
dataset in the root of the directory and used the name of the remote repository
"``machinelearning-books``". Alternatively, you could have also installed the dataset from within
the books directory. Important: If you are installing *within* a dataset,
but execute the command not from the root of this dataset, your ``-d`` option needs to specify
the path to the root of the dataset, and the path needs to start from the directory root. For example:
``datalad install -d ../ -s https://github.com/datalad-datasets/machinelearning-books.git books/ml-books``
(with ``../`` being the Unix expression for ``parent directory``, i.e. "one-directory-up").

.. container:: toggle

   .. container:: header

       **Addition: What if I don't install into an existing dataset?**

   If you don't install inside an existing dataset, you only need to omit the ``dataset``
   option. You can try ``datalad install -s https://github.com/datalad-datasets/machinelearning-books.git``
   anywhere outside of your ``Datalad-101`` dataset to install the dataset into a new directory
   called ``machinelearning-books``.

.. gitusernote::

   The ``datalad install`` command uses ``git clone``.

Here is the repository structure:

.. runrecord:: _examples/DL-101-5-2
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101 && tree

   $ tree

We can see that books contains the three PDFs we downloaded and saved previously.
Additionally, there is another directory ``ml-books`` which contains 10 more books,
and a ``README.md`` file.
You might be confused by the small arrows and cryptic paths that follow every PDF -
we'll get to what that is in the next section.


Dataset content identity and availability information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You might have been surprised by how fast the datalad was installed. Shouldn't
a download of many books should take much more time? Here you can see another
import feature of DataLad datasets and the ``datalad install`` command:

Upon installation of a DataLad dataset, DataLad retrieves only small files
(for examples text file or markdown files) and (small) metadata
information about the dataset. It does not, however, download any large files
(yet). This exposes the datasets file hierarchy
for exploration, and speeds up the installation of a DataLad dataset
of many TB in size to a few seconds. Just now, after installation, the dataset is
small in size:

.. runrecord:: _examples/DL-101-5-3
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101/books/ml-books && du -sh

   $ cd books/ml-books
   $ du -sh      # Unix command to show size of contents

This is tiny. So lets see whats in this dataset.

.. runrecord:: _examples/DL-101-5-4
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101/books/ml-books && ls

   $ ls

If you are doing this in your own terminal, you might see the PDFs and the ``README.md``
file highlighted in different colors. On your computer, try to open first ``README.md``
and then one of the PDF files.

You will notice that the (small) README.md file exists. But you cannot open any of the
PDF files. This is not your fault: None of the PDFs exists on your computer yet.

This sounds strange, but it has many advantages. Apart from a fast installation,
it allows you to retrieve precisely the content you need, instead of all the contents
of a dataset. Thus, even if you install a dataset that is many TB in size,
it takes up only few MB of space after installation, and you can retrieve only those
components of the dataset you need.

The command to retrieve file content is ``datalad get``. You can specify (a) specific
file(s), or ``get`` all of the dataset by specifying ``datalad get .`` (with ``.``
denoting "current directory").
Let's try both ways:

First, we get one of the PDFs in the dataset - take any one of your choice (here, its the first).

.. runrecord:: _examples/DL-101-5-5
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101/books/ml-books && datalad get A.Shashua-Introduction_to_Machine_Learning.pdf

   $ datalad get A.Shashua-Introduction_to_Machine_Learning.pdf

Try to open it with a PDF viewer - it will now work.

Lets now get the rest of the missing data. Instead of specifying all of them, we can
use ``.`` to refer to all of the dataset.

.. runrecord:: _examples/DL-101-5-6
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101/books/ml-books && datalad get .

   $ datalad get .

Wasn't that easy?

Note that any data that is already retrieved (one book) is not downloaded again.
Datalad summarizes the outcome of the execution of ``get`` in the end and informs
that one file was ``notneeded`` and the retrieval of the other files was ``ok``.

You have now experienced how easy it is to share data with DataLad.
Moreover, beyond simply sharing the *data* in the dataset, when sharing or installing
a DataLad dataset, all copies also include the datasets *history*.

For example, we can find out who created with dataset in the first place
(the output shows an excerpt):

.. runrecord:: _examples/DL-101-5-7
   :language: console
   :workdir: dl-101
   :realcommand: cd DataLad-101/books/ml-books && git log
   :lines: 51-61
   :emphasize-lines: 2

   $ git log

But thats not all. Lets pretend Yaroslav finds another useful machine-learning book
he wants to share in this dataset. He can add it to the original dataset (that
we installed from Github), and because an installed
dataset knows the dataset it was installed from,
the locally installed dataset can simply be updated. But we will see examples
of this later in this handbook.

Now you can not only create datasets and work with them locally, you can also consume
existing datasets by installing them.