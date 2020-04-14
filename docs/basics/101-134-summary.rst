.. _summary_containers:

Summary
-------

The last two sections have first of all extended your knowledge on dataset nesting:

- When subdatasets are created or installed, they are registered to the superdataset
  in their current version state (as identified by their most recent commit's hash).
  For a freshly created subdatasets, the most recent commit is at the same time its
  first commit.

- Once the subdataset evolves, the superdataset recognizes this as a ``modification``
  of the subdatasets version state. If you want to record this, you need to
  :command:`save` it in the superdataset::

   $ datalad save -m "a short summary of changes in subds" <path to subds>

But more than nesting concepts, they have also extended your knowledge on
reproducible analyses with :command:`datalad run` and you have experienced
for yourself why and how software containers can go hand-in-hand with DataLad:

- A software container encapsulates a complete software environment, independent
  from the environment of the computer it runs on. This allows you to create or
  use secluded software and also share it together with your analysis to ensure
  computational reproducibility. The DataLad extension
  `datalad containers <http://docs.datalad.org/projects/container/en/latest/>`_
  can make this possible.

- The command :command:`datalad containers-add` registers an Image from a path or
  url to your dataset.

- If you use :command:`datalad containers-run` instead of :command:`datalad run`,
  you can reproducibly execute a command of your choice *within* the software
  environment.

- A :command:`datalad rerun` of a commit produced with :command:`datalad containers-run`
  will re-execute the command in the same software environment.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

For one, you will not be surprised if you ever see a subdataset being shown as
``modified`` by :command:`datalad status`: You now know that if a subdataset
evolves, it's most recent state needs to be explicitly saved to the superdatasets
history.

On a different matter, you are now able to capture and share analysis provenance that
includes the relevant software environment. This does not only make your analyses
projects automatically reproducible, but automatically *computationally* reproducible -
you can make sure that your analyses runs on any computer with Singularity,
regardless of the software environment on this computer. Even if you are unsure how you can wrap up an
environment into a software container Image at this point, you could make use of
hundreds of publicly available Images on `Singularity-Hub <https://singularity-hub.org/>`_ and
`Docker-Hub <https://hub.docker.com/>`_.

With this, you have also gotten a first glimpse into an extension of DataLad: A
Python module you can install with Python package managers such as ``pip`` that
extends DataLad's functionality.
