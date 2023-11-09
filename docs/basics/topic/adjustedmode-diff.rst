While this example works on Unix file systems, it will not provide the same output on Windows.
This is due to different file handling on Windows.
When executing this command, you will see *all* files being modified between the most recent and the second-most recent commit.
On a technical level, this is correct given the underlying file handling on Windows, and chapter :ref:`chapter_gitannex` will shed light on why that is.

For now, to get the same output as shown in the code snippet below, use the following command where ``main`` (or ``master``) is the name of your default branch:

.. code-block:: console

  $ datalad diff --from main --to HEAD~1

The ``--from`` argument specifies a different starting point for the comparison - the ``main`` or :term:`master` :term:`branch`, which would be the starting point on most Unix-based systems.
