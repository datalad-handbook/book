Please use an editor of your choice to create a file ``list_titles.sh`` inside of the ``code`` directory.
These should be the contents:

.. code-block:: bash

   for i in recordings/longnow/Long_Now__Seminars*/*.mp3; do
      # get the filename
      base=$(basename "$i");
      # strip the extension
      base=${base%.mp3};
      # date as yyyy-mm-dd
      printf "${base%%__*}\t" | tr '_' '-';
      # name and title without underscores
      printf "${base#*__}\n" | tr '_' ' ';
   done

Note that this is not identical to the script in the text -- it lacks a few ``\`` characters, which is a meaningful difference.
