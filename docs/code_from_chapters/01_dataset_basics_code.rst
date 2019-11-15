Code from chapter: 01_dataset_basics
------------------------------------

Code snippet 1::

   datalad create --description "course on DataLad-101 on my private Laptop" -c text2git DataLad-101


Code snippet 2::

   cd DataLad-101
   ls    # ls does not show any output, because the dataset is empty.


Code snippet 3::

   git log


Code snippet 4::

   ls -a # show also hidden files


Code snippet 5::

   mkdir books


Code snippet 6::

   tree


Code snippet 7::

   cd books && wget -nv https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download -O TLCL.pdf && wget -nv https://www.gitbook.com/download/pdf/book/swaroopch/byte-of-python -O byte-of-python.pdf && cd ../


Code snippet 8::

   tree


Code snippet 9::

   datalad status


Code snippet 10::

   datalad save -m "add books on Python and Unix to read later"


Code snippet 11::

   git log -p -n 1


Code snippet 12::

   cd books && wget -nv https://github.com/progit/progit2/releases/download/2.1.154/progit.pdf && cd ../


Code snippet 13::

   datalad status


Code snippet 14::

   datalad save -m "add reference book about git" books/progit.pdf


Code snippet 15::

   # lets make the output a bit more concise with the --oneline option
   git log --oneline


Code snippet 16::

   cat << EOT > notes.txt
   One can create a new dataset with 'datalad create [--description] PATH'.
   The dataset is created empty

   EOT


Code snippet 17::

   datalad status


Code snippet 18::

   datalad save -m "Add notes on datalad create"


Code snippet 19::

   cat << EOT >> notes.txt
   The command "datalad save [-m] PATH" saves the file
   (modifications) to history. Note to self:
   Always use informative, concise commit messages.

   EOT


Code snippet 20::

   datalad status


Code snippet 21::

   datalad save -m "add note on datalad save"


Code snippet 22::

   git log -p -n 2


Code snippet 23::

   # we are in the root of DataLad-101
   mkdir recordings


Code snippet 24::

   datalad install -d . -s https://github.com/datalad-datasets/longnow-podcasts.git recordings/longnow


Code snippet 25::

   tree -d   # we limit the output to directories


Code snippet 26::

   cd recordings/longnow/Long_Now__Seminars_About_Long_term_Thinking
   ls


Code snippet 27::

   cd ../      # in longnow/
   du -sh      # Unix command to show size of contents


Code snippet 28::

   datalad status --annex


Code snippet 29::

   datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3


Code snippet 30::

   datalad status --annex all


Code snippet 31::

   datalad get Long_Now__Seminars_About_Long_term_Thinking/2003_11_15__Brian_Eno__The_Long_Now.mp3 \
   Long_Now__Seminars_About_Long_term_Thinking/2003_12_13__Peter_Schwartz__The_Art_Of_The_Really_Long_View.mp3 \
   Long_Now__Seminars_About_Long_term_Thinking/2004_01_10__George_Dyson__There_s_Plenty_of_Room_at_the_Top__Long_term_Thinking_About_Large_scale_Computing.mp3


Code snippet 32::

   git log --reverse


Code snippet 33::

   # in the root of DataLad-101:
   cd ../../
   cat << EOT >> notes.txt
   The command 'datalad install [--source] PATH'
   installs a dataset from e.g., a URL or a path.
   If you install a dataset into an existing
   dataset (as a subdataset), remember to specify the
   root of the superdataset with the '-d' option.

   EOT
   datalad save -m "Add note on datalad install"


Code snippet 34::

   git log -p


Code snippet 35::

   cd recordings/longnow
   git log --oneline


Code snippet 36::

   cd ../../


