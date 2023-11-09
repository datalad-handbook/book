Many versions of Windows do not ship with the tool ``wget``.
You can install it, but it may be easier to use the pre-installed ``curl`` command:

.. code-block:: console

  $ cd books
  $ curl -L https://sourceforge.net/projects/linuxcommand/files/TLCL/19.01/TLCL-19.01.pdf/download \
    -o TLCL.pdf
  $ curl -L https://github.com/swaroopch/byte-of-python/releases/download/vadb91fc6fce27c58e3f931f5861806d3ccd1054c/byte-of-python.pdf \
    -o byte-of-python.pdf
  $ cd ../
