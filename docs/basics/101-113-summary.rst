.. _run6:

Summary
-------

In the last four sections, we demonstrated how to create a proper :command:`datalad run`
command, and discovered the concept of *locked* content.

* :command:`datalad run` records and saves the changes a command makes in a dataset. That means
  that modifications to existing content or new content is associated with a specific command
  and saved to the dataset's history. Essentially, :command:`datalad run` helps you to keep
  track of what you do in your dataset.

* A :command:`datalad run` command generates a ``run record`` in the commit. This :term:`run record` can be used
  by datalad to re-execute a command with :command:`datalad rerun SHASUM`, where SHASUM is the
  commit hash of the :command:`datalad run` command that should be re-executed.

* If a :command:`datalad run` or :command:`datalad rerun` does not modify any content, it will not write a
  record to history.

* With any :command:`datalad run`, specify a commit message, and whenever appropriate, specify its inputs
  to the executed command (using the ``-i``/``--input`` flag) and/or its output (using the ``-o``/
  ``--output`` flag). The full command structure is:

:command:`datalad run -m "commit message here" --input "path/to/input/" --output "path/to/output" "command"`

* Anything specified as ``input`` will be retrieved if necessary with a :command:`datalad get` prior to command
  execution. Anything specified as ``output`` will be ``unlocked`` prior to modifications.

.. figure:: ../artwork/src/run.svg
   :alt: Schematic illustration of datalad run.
   :figwidth: 100%

   Overview of ``datalad run``.

* Getting and unlocking content is not only convenient for yourself, but enormously helpful
  for anyone you share your dataset with, but this will be demonstrated in an upcoming section
  in detail.

* To execute a :command:`datalad run` or :command:`datalad rerun`, a :command:`datalad status`
  either needs to report that the dataset has no uncommitted changes (the dataset state
  should be "clean"), or the command needs to be extended with the ``--explicit`` option.


Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have procedurally experienced how to use :command:`datalad run` and :command:`datalad rerun`. Both
of these commands make it easier for you and others to associate changes in a dataset with
a script or command, and are helpful as the exact command for a given task is stored by
DataLad, and does not need to be remembered.

Furthermore, by experiencing many common error messages in the context of :command:`datalad run`
commands, you have gotten some clues on where to look for problems, should you encounter
those errors in your own work.

Lastly, we've started to unveil some principles of :term:`Git-annex` that are relevant to
understanding how certain commands work and why certain commands may fail. We have seen that
Git-annex locks large files' content to prevent accidental modifications, and how the ``--output``
flag in :command:`datalad run` can save us an intermediate :command:`datalad unlock` to unlock this content.
The next section will elaborate on this a bit more.
