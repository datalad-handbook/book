Please use an editor of your choice to replace the contents of ``list_titles.sh`` inside of the ``code`` directory with the following:

.. code-block:: bash

   for i in recordings/longnow/Long_Now*/*.mp3; do
      # get the filename
      base=$(basename "$i");
      # strip the extension
      base=${base%.mp3};
      # date as yyyy-mm-dd
      printf "${base%%__*}\t" | tr '_' '-';
      # name and title without underscores
      printf "${base#*__}\n" | tr '_' ' ';
   done
