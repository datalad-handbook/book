.. _containersrun:

Computational reproducibility with software containers
------------------------------------------------------

Just after submitting your midterm data analysis project, you get together
with your friends. "I'm curious: So what kind of analyses did y'all carry out?"
you ask. The variety of methods and datasets the others used is huge, and
one analysis interests you in particular. Later that day, you decide to
install this particular analysis dataset to learn more about the methods used
in there. However, when you :command:`re-run` your friends analysis script,
it throws an error. Hastily, you call her -- maybe she can quickly fix her
script and resubmit the project with only minor delays. "I don't know what
you mean", you hear in return, "on my machine, everything works fine!"

On its own, DataLad datasets can contain almost everything that is relevant to
ensure reproducibility: Data, code, human-readable analysis descriptions
(e.g., ``README.md`` files), provenance on the origin of all files
obtained from elsewhere, and machine-readable records that link generated
outputs to the commands, scripts, and data they were created from.

This however may not be sufficient to ensure that an analysis *reproduces*
(i.e., produces the same or highly similar results), let alone *works* on a
computer different than the one it was initially composed on. This is because
the analysis does not only depend on data and code, but also the
*software environment* that it is conducted in.

A lack of information about the operating system of the computer, the precise
versions of installed software, or their configurations may
make it impossible to replicate your analysis on a different machine, or even
on your own machine once a new software update is installed. Therefore, it is
important to communicate all details about the computational environment for
an analysis as thoroughly as possible. Luckily, DataLad provides an extension
that can link computational environments to datasets, the
`datalad containers <http://docs.datalad.org/projects/container/en/latest/>`_
extension.

This section will give a quick overview on what containers are and
demonstrate how ``datalad-containers`` helps to capture full provenance of an
analysis by linking containers to datasets and analyses.

.. todo::

   - link to neuroimaging use case
   - maybe mention the 10 year code challenge by ReScience


Containers
^^^^^^^^^^

To put it simple, computational containers are cut-down virtual machines that
allow you to package all software libraries and their dependencies (all in the
precise version your analysis requires) into a bundle you can share with
others. On your own and others machines, the container constitutes a secluded
software environment that

- contains the exact software environment that you specified, ready to run
  analysis in
- does not effect any software outside of the container

Unlike virtual machines, software containers do not have their own operating
system. Instead, they use basic services of the underlying operating system
of the computer they run on (in a read-only fashion). This makes them
lightweight and portable. By sharing software environments with containers,
others (and also yourself) have easy access to the correct software
without the need to modify the software environment of the machine the
container runs on. Thus, containers are ideal to encapsulate the software
environment and share it together with the analysis code and data to ensure
computational reproducibility of your analyses.

There are a number of different tools to create and use containers, with
`Docker <https://www.docker.com/>`_ being one of the most well-known of them.
While being a powerful tool, it can not be used on high performance computing
(HPC) infrastructure [#f1]_. An alternative is `Singularity <https://sylabs
.io/docs/>`_.
Both of these tools share core terminology:

**Image**
   A template or "recipe" from which containers are build. It lists all
   required components of the computational environment, and is made by a
   human user. If you want to create your own container, you start by writing
   an Image file, but you can also *pull* a publicly shared image from the
   *Hub* of the tool you are using. Based on images, containers are *build*.

**Container**
  The instance that you can actually use for your computations, *build* from
  an image.

**Hub**
  A storage resource to share and consume images. There is
  `Singularity-Hub <https://singularity-hub.org/>`_ and
  `Docker-Hub <https://hub.docker.com/>`_.

Note that as of now, the ``datalad-containers`` extensions only supports
Singularity images, but support for Docker is being actively developed.
Singularity is however very compatible with Docker -- you can, for example, use
Docker images as a basis for Singularity images, or run Docker images with
Singularity (even without having Docker installed). Note further that in order
to use Singularity containers, you have to
`install <https://singularity.lbl.gov/docs-installation>`_ the software
singularity.

Using ``datalad containers``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One core feature of the ``datalad containers`` extension is that it registers
computational containers to a dataset. This is done with the
:command:`datalad containers-add` command. The command takes an arbitrary
name to give to the container, and a path or url to a container image.

Let's see this in action for the ``midterm_analysis`` dataset by rerunning
the analysis you did for the midterm project within a Singularity container.
For this we will pull a container from Singularity hub. This container has
been build for the handbook, and it contains the relevant Python setup for
the analysis. If you're curious how to create a Singularity image, the hidden
section below has some pointers:

.. findoutmore:: How to make a Singularity image

   A singularity containers are build from definition files, often
   called "recipes". The
   `singularity documentation <https://sylabs.io/guides/3.4/user-guide/build_a_container.html>`_
   has its own tutorial. One other way to build one is with
   `Neurodocker <https://github.com/kaczmarj/neurodocker#singularity>`_. This
   command-line program can help you generate custom Singularity recipes (and
   also Dockerfiles, from which Docker images are build). A wonderful tutorial
   on how to use Neurodocker is
   `this introduction <https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html>`_
   by Michael Notter.

   Once a recipe exists, the command

   .. code-block:: bash

      sudo singularity build <NAME> <RECIPE>

   will build a container (callen ``<NAME>``) from the recipe. Alternatively,
   ``Singularity Hub <https://singularity-hub.org/>`_ integrates with Github
   and builds containers from recipes pushed to repositories on Github.
   `The docs <https://singularityhub.github.io/singularityhub-docs/>`_ can
   give you an easy set of instructions for this.

.. runrecord:: _examples/DL-101-145-101
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project

   # we are in the midterm_project subdataset
   $ datalad containers-add python shub://adswa/resources:1


This command downloaded the container from Singularity Hub, added it to
the ``midterm_project`` dataset, and recorded basic information on the
container under its name "python" in the dataset's configuration at
``.datalad/config``.

.. findoutmore:: What has been added to .datalad/config?

   .. runrecord:: _examples/DL-101-145-102
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ cat .datalad/config

   This recorded the images origin on Singularity-Hub, the location of the
   image in the dataset, and

   .. todo::

      what exactly is ``cmdexec = singularity exec {img} {cmd}``?

   Note that the image is saved under ``.datalad/environments`` and the
   configuration is done in ``.datalad/config`` -- as these files are version
   controlled and shared with together with a dataset, your software
   container and the information where it can be re-obtained from are linked
   to your dataset.

   This is how the ``containers-add`` command is recorded in your history:

   .. runrecord:: _examples/DL-101-145-103
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ git log -n 1 -p

Once a container is registered, arbitrary commands can be executed inside of
it, i.e., in the precise software environment the container encapsulates. All it
needs for this it to swap the :command:`datalad run` command introduced in
section :ref:`run` with the :command:`datalad containers-run` command.

.. runrecord:: _examples/DL-101-145-104
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :realcommand: echo "datalad containers-run -m "rerun analysis in container" \--container-name python \ datalad rerun $(git rev-parse HEAD~2)" && datalad containers-run -m "rerun analysis in container" \--container-name python \ datalad rerun $(git rev-parse HEAD~2)

.. todo::

   re-do a previous (yet) to write run command for a data analysis in
   ``midterm_project``.


Note: The ``--container-name`` flag is optional at this point. Only if your dataset
contains more than one container, you will *need* to specify the name of the container
you want to use in your command. The complete command's structure looks like this::

   $ datalad containers-run --name <containername> [--input ...] [--output ...] <COMMAND>

.. findoutmore:: How can I list available containers or remove them?

   The command :command:`datalad containers-list` will list all containers in
   the current dataset:

   .. runrecord:: _examples/DL-101-145-110
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ datalad containers-list

   The command :command:`datalad containers-remove` will remove a container
   from the dataset, if there exists a container with name given to the
   command. Note that this will remove not only the image from the dataset,
   but also the configuration for it in ``.datalad/config``.

.. rubric:: Footnotes

.. [#f1] The main reason why Docker is not deployed on HPC systems is because
         it grants users "`superuser privileges <https://en.wikipedia.org/wiki/Superuser>`_".
         On multi-user systems such as HPC, users should not have those
         privileges, as it would enable them to temper with other's or shared
         data and resources, posing a severe security threat.