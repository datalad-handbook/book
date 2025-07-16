Code from chapter: 02_reproducible_execution
--------------------------------------------

Code snippet 40::

   cd DataLad-101 && mkdir code && tree -d


Code snippet 41::

   cat << EOT > code/list_titles.sh
   for i in recordings/longnow/Long_Now__Seminars*/*.mp3; do
      # get the filename
      base=\$(basename "\$i");
      # strip the extension
      base=\${base%.mp3};
      # date as yyyy-mm-dd
      printf "\${base%%__*}\t" | tr '_' '-';
      # name and title without underscores
      printf "\${base#*__}\n" | tr '_' ' ';
   done
   EOT


Code snippet 42::

   datalad status


Code snippet 43::

   datalad save -m "Add short script to write a list of podcast speakers and titles"


Code snippet 44::

   datalad run -m "create a list of podcast titles" "bash code/list_titles.sh > recordings/podcasts.tsv"


Code snippet 45::

   git log -p -n 1


Code snippet 46::

   datalad run -m "Try again to create a list of podcast titles" "bash code/list_titles.sh > recordings/podcasts.tsv"


Code snippet 47::

   git log --oneline


Code snippet 48::

   less recordings/podcasts.tsv


Code snippet 49::

   cat << EOT >| code/list_titles.sh
   for i in recordings/longnow/Long_Now*/*.mp3; do
      # get the filename
      base=\$(basename "\$i");
      # strip the extension
      base=\${base%.mp3};
      printf "\${base%%__*}\t" | tr '_' '-';
      # name and title without underscores
      printf "\${base#*__}\n" | tr '_' ' ';

   done
   EOT


Code snippet 50::

   datalad status


Code snippet 51::

   datalad save -m "BF: list both directories content" code/list_titles.sh


Code snippet 52::

   git log -n 2


Code snippet 53::

   echo "$ datalad rerun $(git rev-parse HEAD~1)" && datalad rerun $(git rev-parse HEAD~1)


Code snippet 54::

   git log -n 1


Code snippet 55::

   datalad diff --to HEAD~1


Code snippet 56::

   git diff HEAD~1


Code snippet 57::

   cat << EOT >> notes.txt
   There are two useful functions to display changes between two
   states of a dataset: "datalad diff -f/--from COMMIT -t/--to COMMIT"
   and "git diff COMMIT COMMIT", where COMMIT is a shasum of a commit
   in the history.

   EOT


Code snippet 58::

   datalad save -m "add note datalad and git diff"


Code snippet 59::

   git log -- recordings/podcasts.tsv


Code snippet 60::

   cat << EOT >> notes.txt
   The datalad run command can record the impact a script or command has on a Dataset.
   In its simplest form, datalad run only takes a commit message and the command that
   should be executed.

   Any datalad run command can be re-executed by using its commit shasum as an argument
   in datalad rerun CHECKSUM. DataLad will take information from the run record of the original
   commit, and re-execute it. If no changes happen with a rerun, the command will not be written
   to history. Note: you can also rerun a datalad rerun command!

   EOT


Code snippet 61::

   datalad save -m "add note on basic datalad run and datalad rerun"


Code snippet 62::

   ls recordings/longnow/.datalad/feed_metadata/*jpg


Code snippet 63::

   datalad run -m "Resize logo for slides" \
   "convert -resize 400x400 recordings/longnow/.datalad/feed_metadata/logo_salt.jpg recordings/salt_logo_small.jpg"


Code snippet 64::

   datalad run --input "recordings/longnow/.datalad/feed_metadata/logo_salt.jpg" "convert -resize 400x400 recordings/longnow/.datalad/feed_metadata/logo_salt.jpg recordings/salt_logo_small.jpg"


Code snippet 65::

   datalad run --input "recordings/longnow/.datalad/feed_metadata/logo_salt.jpg" "convert -resize 450x450 recordings/longnow/.datalad/feed_metadata/logo_salt.jpg recordings/salt_logo_small.jpg"


Code snippet 66::

   datalad unlock recordings/salt_logo_small.jpg


Code snippet 67::

   datalad status


Code snippet 68::

   convert -resize 450x450 recordings/longnow/.datalad/feed_metadata/logo_salt.jpg recordings/salt_logo_small.jpg


Code snippet 69::

   datalad save -m "resized picture by hand"


Code snippet 70::

   datalad run --input "recordings/longnow/.datalad/feed_metadata/logo_interval.jpg" --output "recordings/interval_logo_small.jpg" "convert -resize 450x450 recordings/longnow/.datalad/feed_metadata/logo_interval.jpg recordings/interval_logo_small.jpg"


Code snippet 71::

   cat << EOT >> notes.txt
   You should specify all files that a command takes as input with an -i/--input flag. These
   files will be retrieved prior to the command execution. Any content that is modified or
   produced by the command should be specified with an -o/--output flag. Upon a run or rerun
   of the command, the contents of these files will get unlocked so that they can be modified.

   EOT


Code snippet 72::

   datalad run -m "Resize logo for slides" \
   --input "recordings/longnow/.datalad/feed_metadata/logo_interval.jpg" \
   --output "recordings/interval_logo_small.jpg" \
   "convert -resize 400x400 recordings/longnow/.datalad/feed_metadata/logo_interval.jpg recordings/interval_logo_small.jpg"


Code snippet 73::

   datalad status


Code snippet 74::

   datalad save -m "add additional notes on run options"


Code snippet 75::

   datalad run -m "Resize logo for slides" \
   --input "recordings/longnow/.datalad/feed_metadata/logo_interval.jpg" \
   --output "recordings/interval_logo_small.jpg" \
   "convert -resize 400x400 recordings/longnow/.datalad/feed_metadata/logo_interval.jpg recordings/interval_logo_small.jpg"


Code snippet 76::

   cat << EOT >> notes.txt
   Important! If the dataset is not "clean" (a datalad status output is empty),
   datalad run will not work - you will have to save modifications present in your
   dataset.
   EOT


Code snippet 77::

   datalad run -m "Resize logo for slides" \
   --input "recordings/longnow/.datalad/feed_metadata/logo_salt.jpg" \
   --output "recordings/salt_logo_small.jpg" \
   --explicit \
   "convert -resize 400x400 recordings/longnow/.datalad/feed_metadata/logo_salt.jpg recordings/salt_logo_small.jpg"


Code snippet 78::

   datalad status


Code snippet 79::

   cat << EOT >> notes.txt
   A suboptimal alternative is the --explicit flag,
   used to record only those changes done
   to the files listed with --output flags.

   EOT


Code snippet 80::

   datalad save -m "add note on clean datasets"


Code snippet 81::

   git log -p -n 2


