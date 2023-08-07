.. _run6:

Summary
-------

In the last four sections, we demonstrated how to create a proper :dlcmd:`run`
command, and discovered the concept of *locked* content.

* :dlcmd:`run` records and saves the changes a command makes in a dataset. That means
  that modifications to existing content or new content are associated with a specific command
  and saved to the dataset's history. Essentially, :dlcmd:`run` helps you to keep
  track of what you do in your dataset by capturing all :term:`provenance`.

* A :dlcmd:`run` command generates a ``run record`` in the commit. This :term:`run record` can be used
  by datalad to re-execute a command with :dlcmd:`rerun SHASUM`, where SHASUM is the
  commit hash of the :dlcmd:`run` command that should be re-executed.

* If a :dlcmd:`run` or :dlcmd:`rerun` does not modify any content, it will not write a
  record to history.

* With any :dlcmd:`run`, specify a commit message, and whenever appropriate, specify its inputs
  to the executed command (using the ``-i``/``--input`` flag) and/or its output (using the ``-o``/
  ``--output`` flag). The full command structure is::

     $ datalad run -m "commit message here" --input "path/to/input/" --output "path/to/output" "command"

* Anything specified as ``input`` will be retrieved if necessary with a :dlcmd:`get` prior to command
  execution. Anything specified as ``output`` will be ``unlocked`` prior to modifications.

* It is good practice to specify ``input`` and ``output`` to ensure that a :dlcmd:`rerun` works, and to capture the relevant elements of a computation in a machine-readable record.
  If you want to spare yourself preparation time in case everything is already retrieved and unlocked, you can use ``--assume-ready {input|output|both}`` to skip a check on whether inputs are already present or outputs already unlocked.

.. figure:: ../artwork/src/run.svg
   :alt: Schematic illustration of datalad run.
   :width: 80%

   Overview of ``datalad run``.

* Getting and unlocking content is not only convenient for yourself, but enormously helpful
  for anyone you share your dataset with, but this will be demonstrated in an upcoming section
  in detail.

* To execute a :dlcmd:`run` or :dlcmd:`rerun`, a :dlcmd:`status`
  either needs to report that the dataset has no uncommitted changes (the dataset state
  should be "clean"), or the command needs to be extended with the ``--explicit`` option.


Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have procedurally experienced how to use :dlcmd:`run` and :dlcmd:`rerun`. Both
of these commands make it easier for you and others to associate changes in a dataset with
a script or command, and are helpful as the exact command for a given task is stored by
DataLad, and does not need to be remembered.

Furthermore, by experiencing many common error messages in the context of :dlcmd:`run`
commands, you have gotten some clues on where to look for problems, should you encounter
those errors in your own work.

Lastly, we've started to unveil some principles of :term:`git-annex` that are relevant to
understanding how certain commands work and why certain commands may fail. We have seen that
git-annex locks large files' content to prevent accidental modifications, and how the ``--output``
flag in :dlcmd:`run` can save us an intermediate :dlcmd:`unlock` to unlock this content.
The next section will elaborate on this a bit more.




Further reading
^^^^^^^^^^^^^^^

The chapter on :dlcmd:`run` provided an almost complete feature overview of the command.
If you want, you can extend this knowledge with computational environments and :dlcmd:`containers-run` in chapter :ref:`containersrun`.
In addition, you can read up on other forms of computing usecases - for example, how to use :dlcmd:`run` in interactive computing environments such as `Jupyter Notebooks <https://knowledge-base.psychoinformatics.de/kbi/0003>`_.
