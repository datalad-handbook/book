Heredocs rely on Unix-type redirection and multi-line commands -- which is not supported on most native Windows terminals or the Anaconda prompt on Windows.
If you are using an Anaconda prompt or a Windows terminal other than Git Bash, instead of executing heredocs, please open up an editor and paste and save the text into it.

The relevant text in the snippet below would be:

.. code-block:: text

  One can create a new dataset with 'datalad create [--description] PATH'.
  The dataset is created empty

If you are using Git Bash, however, here docs will work just fine.   
