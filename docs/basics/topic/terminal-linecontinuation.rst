In Unix shells, ``\`` can be used to split a command into several lines, for example to aid readability.
Standard Windows terminals (including the Anaconda prompt) do not support this.
They instead use the ``^`` character:

.. code-block:: console

 $ wget -q https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download ^
 -O TLCL.pdf

If you are not using the Git Bash, you will either need to copy multi-line commands into a single line, or use ``^`` (make sure that there is **no space** afterwards) instead of ``\``.
