**********************
Test for autorunrecord
**********************

.. runrecord:: _examples/firstdemo
   :language: console

   $ date > testfile

.. runrecord:: _examples/seconddemo
   :language: console
   :emphasize-lines: 2
   :realcommand: cat testfile

   $ funky-file-viewer

