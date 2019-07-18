Run, Datalad! Summary
----------------------

In the last five sections, we demonstrated how to create a proper ``datalad run``
command, and discovered the concept of *locked* content.

* ``datalad run`` records and saves the changes a command makes in a dataset. That means
  that modifications to existing contents or new content is associated with a specific command
  and saved to the datasets history.

* A ``datalad run`` command generates a ``run-record`` in the commit. This :term:`run-record` can be used
  by datalad to re-execute a command with ``datalad rerun CHECKSUM``, where CHECKSUM is the
  commit hash of the ``datalad run`` command that should be re-executed.

* If a ``datalad run`` or ``datalad rerun`` does not modify any content, it will not write a
  record to history.

* With any ``datalad run``, specify a commit message, and whenever appropriate, specify its inputs
  to the executed command (using the ``-i``/``--input`` flag) and/or its output (using the ``-o``/
  ``--output`` flag). The full command structure is:

``datalad run -m "commit message here" --input "path/to/input/" --output "path/to/output" "command"``

* Anything specified as ``input`` will be retrieved if necessary with a ``datalad get`` prior to command
  execution. Anything specified as ``output`` will be ``unlocked`` prior to modifications.

* Getting and unlocking content is not only convenient for yourself, but enormously helpful
  for anyone you share your dataset with.

* To execute a ``datalad run`` or ``datalad rerun``, ``datalad status`` either needs to be clean,
  or the command needs to be extended with the ``--explicit`` option.



Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have procedurally experienced how to use ``datalad run`` and ``datalad rerun``. Both
of these commands make it easier for you and others to associate changes in a dataset with
a script or command, and are helpful as the exact command for a given task is stored by
DataLad, and does not need to be remembered.

Furthermore, by experiencing many common error messages in the context of ``datalad run``
commands, you have gotten some clues on where to look for problems, should you encounter
those errors in your own work.

Lastly, we've started to unveil some principles of :term:`Git-annex` that are relevant to
understanding how certain commands work and why certain commands may fail. We have seen that
Git-annex locks large files' content to prevent accidental modifications, and how the ``--output``
flag in ``datalad run`` can save as an intermediate ``datalad unlock`` to unlock this content.
The next section will elaborate on this a bit more.