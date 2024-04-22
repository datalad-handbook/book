.. runrecord:: /basics/_examples/DL-101-133-102
  :language: console
  :workdir: dl-101/DataLad-101/midterm_project

  $ cat .datalad/config

This recorded the image's origin on Singularity-Hub, the location of the
image in the dataset under ``.datalad/environments/<NAME>/image``, and it
specifies the way in which the container should be used: The line

.. code-block:: ini

   cmdexec = singularity exec {img} {cmd}

can be read as: "If this container is used, take the ``cmd`` (what you wrap in a
:dlcmd:`containers-run` command) and plug it into a
:shcmd:`singularity exec` command. The mode of calling Singularity,
namely ``exec``, means that the command will be executed inside of the container.

You can configure this call format by modifying it in the config file, or calling :dlcmd:`containers-add` with the option ``--call-fmt <alternative format>``.
This can be useful to, for example, automatically bind-mount the current working directory in the container.
In the alternative call format, the placeholders ``{img}``, ``{cmd}``, and ``{img_dspath}`` (a relative path to the dataset containing the image) are available.
In all other cases with variables that use curly brackets, you need to escape them with another curly bracket.
Here is an example call format that bind-mounts the current working directory (and thus the dataset) automatically:

.. code-block:: console

  $ datalad containers-add --call-fmt 'singularity exec -B {{pwd}} --cleanenv {img} {cmd}'

Note that the image is saved under ``.datalad/environments`` and the
configuration is done in ``.datalad/config`` -- as these files are version
controlled and shared with together with a dataset, your software
container and the information where it can be reobtained from are linked
to your dataset.

This is how the ``containers-add`` command is recorded in your history:

.. runrecord:: /basics/_examples/DL-101-133-103
  :language: console
  :workdir: dl-101/DataLad-101/midterm_project
  :cast: 10_yoda
  :notes: The software container got added to your datasets history

  $ git log -n 1 -p
