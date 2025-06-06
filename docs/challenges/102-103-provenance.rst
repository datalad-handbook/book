.. _challengeProv:

Challenge: Provenance Capture
*****************************


.. importantnote:: You can always get help

   In order to learn about available DataLad commands, use ``datalad --help``. In order to learn more about a specific command, use ``datalad <subcommand> --help``.


Challenge 1:
""""""""""""

Create a DataLad dataset called ``iyoda``, applying a specific post-creation routine called ``yoda`` (``-c yoda``).

.. find-out-more:: Okidoki!

   Creating the dataset

   .. runrecord:: _examples/cha-102-103-provenance-1
      :language: console
      :workdir: challenges/102-103-provenance

      $ datalad create -c yoda iyoda

Run the command ``gitk``:

- What did the "YODA" setup actually do?
- How do we know that data module should go into ``inputs/``?

Add the following dataset as a subdataset called ``inputs``: https://github.com/datalad-handbook/iris_data.
Inspect its history with ``gitk``. When was it made, what does it contain?

.. find-out-more:: Show me the solution

   .. runrecord:: _examples/cha-102-103-provenance-2
      :language: console
      :workdir: challenges/102-103-provenance/

      $ cd iyoda
      $ datalad clone -d . https://github.com/datalad-handbook/iris_data.git inputs

   Hint: In order to investigate the subdatasets history, enter it first.

Inside of ``iyoda``, create a script ``code/extract.py`` with the following content::

   from os.path import join as opj
   import csv
   with open(opj('inputs', 'iris.csv')) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
          if row['variety'] != 'Setosa':
              continue
          print(row['petal.length'])


.. runrecord:: _examples/cha-102-103-provenance-3
   :language: console
   :workdir: challenges/102-103-provenance/iyoda/

   $ cat << EOT > code/extract.py

   from os.path import join as opj
   import csv
   with open(opj('inputs', 'iris.csv')) as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
           if row['variety'] != 'Setosa':
               continue
           print(row['petal.length'])

   EOT

This Python script will print all rows matching the Setosa variety.
Be careful: With Python, consistent indentation with tabs OR spaces is necessary!

You can test your script with ``$ python code/extract.py``

.. windows-wit:: Beware of path semantics on Windows

   On Windows, test the script with::

      $ python code\extract.py

If there are no errors, save the script.

.. find-out-more:: Tell me how!

   .. runrecord:: _examples/cha-102-103-provenance-4
      :language: console
      :workdir: challenges/102-103-provenance/iyoda/

      $ datalad save -m "Save data extraction script"

Try to figure out why there was no output when running the script.

[ ... ]

*space for a dramatic pause*

[ ... ]

Retry running the script after getting content from the subdataset.

.. find-out-more:: Right, let's go!

   To retrieve contents from the subdataset run:

   .. runrecord:: _examples/cha-102-103-provenance-5
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad get inputs


   .. runrecord:: _examples/cha-102-103-provenance-6
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ python code/extract.py

Now that the script works as intended, run it and write its outputs into a file for further processing using the following code:

.. runrecord:: _examples/cha-102-103-provenance-7
   :language: console
   :workdir: challenges/102-103-provenance/iyoda/

   $ python code/extract.py > outputs.dat

.. windows-wit:: Beware of path semantics on Windows

   On Windows, test the script with::

      $ python code\extract.py > outputs.dat

Check the dataset state and save the modification. Inspect the change record:

- What information is captured?
- Imagine yourself in a year. What information would you be missing?


.. find-out-more:: Let's take a look

   .. runrecord:: _examples/cha-102-103-provenance-8
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad status

   and save:

   .. runrecord:: _examples/cha-102-103-provenance-9
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad save -m "Create the desired setosa variety petal length data file"

Run the script again, but through DataLad, and declare inputs and outputs.
This time, save the output file as ``plength.txt``.
Use ``gitk`` to inspect the change record.
What is different now?

.. find-out-more:: Let's take a look

   .. runrecord:: _examples/cha-102-103-provenance-10
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad run -i inputs/iris.csv -o plength.txt "python code/extract.py > {outputs}"

   But beware on Windows!

   .. windows-wit:: paths strike again!

      .. code-block::

         $ datalad run -i inputs\iris.csv -o plength.txt "python code\extract.py > {outputs}"

Finally, force DataLad to lose the file ``plength.txt``.
Re-execute the provenance record.
Afterwards, check what has changed.

.. find-out-more:: Final stretch now

   First, drop recklessy:

   .. runrecord:: _examples/cha-102-103-provenance-11
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad drop --reckless availability plength.txt

   Then, rerun:

   .. runrecord:: _examples/cha-102-103-provenance-12
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad rerun HEAD

   What changed?

   .. runrecord:: _examples/cha-102-103-provenance-13
      :language: console
      :workdir: challenges/102-103-provenance/iyoda

      $ datalad status