.. _containersrun:

Computational reproducibility with software containers
------------------------------------------------------

Just after submitting your midterm data analysis project, you get together
with your friends. "I'm curious: So what kind of analyses did y'all carry out?"
you ask. The variety of methods and datasets the others used is huge, and
one analysis interests you in particular. Later that day, you decide to
install this particular analysis dataset to learn more about the methods used
in there. However, when you :dlcmd:`rerun` your friends analysis script,
it throws an error. Hastily, you call her -- maybe she can quickly fix her
script and resubmit the project with only minor delays. "I don't know what
you mean", you hear in return.
"On my machine, everything works fine!"


On its own, DataLad datasets can contain almost anything that is relevant to
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
`datalad containers <https://docs.datalad.org/projects/container>`_
extension.

This section will give a quick overview on what containers are and
demonstrate how ``datalad-container`` helps to capture full provenance of an
analysis by linking containers to datasets and analyses.

.. index::
   pair: recipe; software container concept
   pair: image; software container concept
   pair: container; software container concept

Containers
^^^^^^^^^^

To put it simple, computational containers are cut-down virtual machines that
allow you to package all software libraries and their dependencies (all in the
precise version your analysis requires) into a bundle you can share with
others. On your own and other's machines, the container constitutes a secluded
software environment that

- contains the exact software environment that you specified, ready to run
  analyses
- does not effect any software outside of the container

Unlike virtual machines, software containers do not run a full operating
system on virtualized hardware. Instead, they use basic services of the host operating system
(in a read-only fashion). This makes them
lightweight and still portable. By sharing software environments with containers,
others (and also yourself) have easy access to the correct software
without the need to modify the software environment of the machine the
container runs on. Thus, containers are ideal to encapsulate the software
environment and share it together with the analysis code and data to ensure
computational reproducibility of your analyses, or to create a suitable
software environment on a computer that you do not have permissions to deploy
software on.

There are a number of different tools to create and use containers, with
`Docker <https://www.docker.com>`_ being one of the most well-known of them.
While being a powerful tool, it is only rarely used on high performance computing
(HPC) infrastructure [#f2]_. An alternative is `Singularity <https://sylabs
.io/docs>`_.
Both of these tools share core terminology:

:term:`container recipe`
   A text file that lists all required components of the computational environment.
   It is made by a human user.

:term:`container image`
   This is *built* from the recipe file. It is a static file system inside a file,
   populated with the software specified in the recipe, and some initial configuration.

:term:`container`
  A running instance of an image that you can actually use for your computations.
  If you want to create and run your own software container, you start by writing
  a recipe file and build an image from it. Alternatively, you can can also *pull*
  an image built from a publicly shared recipe from the *Hub* of the tool you are using.

hub
  A storage resource to share and consume images. Examples are
  :term:`Singularity-Hub`, :term:`Docker-Hub`, and `Amazon ECR <https://aws.amazon.com/ecr>`_ which hosts Docker images.

Note that as of now, the ``datalad-container`` extension supports
Singularity and Docker images.
Singularity furthermore is compatible with Docker -- you can use
Docker images as a basis for Singularity images, or run Docker images with
Singularity (even without having Docker installed).
See the :windows-wit:`on Docker <ww-docker>` for installation options.

.. importantnote:: Additional requirement: Singularity

   To use Singularity containers you have to
   `install <https://docs.sylabs.io/guides/3.4/user-guide/installation.html>`_ the software singularity.

.. index::
   pair: installation; Docker
   pair: install Docker; on Windows
.. find-out-more:: Docker installation Windows
   :name: ww-docker

   The software singularity is not available for Windows.
   Windows users therefore need to install :term:`Docker`.
   The currently recommended way to do so is by installing `Docker Desktop <https://docs.docker.com/desktop/install/windows-install/>`_, and use its "WSL2" backend (a choice one can set during the installation).
   In the case of an "outdated WSL kernel version" issue, run ``wsl --update`` in a regular Windows Command Prompt (CMD).
   After the installation, run Docker Desktop, and wait several minutes for it to start the Docker engine in the background.
   To verify that everything works as it should, run ``docker ps`` in a Windows Command Prompt (CMD).
   If it reports an error that asks "Is the docker daemon running?" give it a few more minutes to let Docker Desktop start it.
   If it can't find the docker command, something went wrong during installation.

.. index::
   pair: containers-add; DataLad command
   pair: containers-run; DataLad command

Using ``datalad containers``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One core feature of the ``datalad containers`` extension is that it registers
computational containers with a dataset. This is done with the
:dlcmd:`containers-add` command.
Once a container is registered, arbitrary commands can be executed inside of
it, i.e., in the precise software environment the container encapsulates. All it
needs for this it to swap the :dlcmd:`run` command introduced in
section :ref:`run` with the :dlcmd:`containers-run` command.

Let's see this in action for the ``midterm_analysis`` dataset by rerunning
the analysis you did for the midterm project within a Singularity container.
We start by registering a container to the dataset.
For this, we will pull an image from Singularity hub. This image was made
for the online-handbook, and it contains the relevant Python setup for
the analysis. Its recipe lives in the online-handbook's
`resources repository <https://github.com/datalad-handbook/resources>`_.
If you are curious how to create a Singularity image, the :find-out-more:`on this topic <fom-container-creation>` has some pointers:

.. index::
   pair: build container image; with Singularity
.. windows-wit:: How to make a Singularity image
   :name: fom-container-creation

   Singularity containers are build from image files, often
   called "recipes", that hold a "definition" of the software container and its
   contents and components. The
   `singularity documentation <https://docs.sylabs.io/guides/3.4/user-guide/build_a_container.html>`_
   has its own tutorial on how to build such images from scratch.
   An alternative to writing the image file by hand is to use
   `Neurodocker <https://github.com/ReproNim/neurodocker>`_. This
   command-line program can help you generate custom Singularity recipes (and
   also ``Dockerfiles``, from which Docker images are built). A wonderful tutorial
   on how to use Neurodocker is
   `this introduction <https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html>`_
   by Michael Notter.

   Once a recipe exists, the command

   .. code-block:: console

      $ sudo singularity build <NAME> <RECIPE>

   will build a container (called ``<NAME>``) from the recipe. Note that this
   command requires ``root`` privileges ("``sudo``"). You can build the container
   on any machine, though, not necessarily the one that is later supposed to
   actually run the analysis, e.g., your own laptop versus a compute cluster.

.. index::
   pair: add container image to dataset; with DataLad

The :dlcmd:`containers-add` command takes an arbitrary
name to give to the container, and a path or URL to a container image:

.. runrecord:: _examples/DL-101-133-101
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Computational reproducibility: add a software container

   $ # we are in the midterm_project subdataset
   $ datalad containers-add midterm-software --url shub://adswa/resources:2

.. index::
   pair: hub; Docker
.. find-out-more:: How do I add an image from Docker-Hub, Amazon ECR, or a local container?

   Should the image you want to use sit on Dockerhub, specify the ``--url``
   option prefixed with ``docker://`` or ``dhub://`` instead of ``shub://``:

   .. code-block:: console

      $ datalad containers-add midterm-software --url docker://adswa/resources:2

   If your image lives on Amazon ECR, use a ``dhub://`` prefix followed by the AWS ECR URL as in

   .. code-block:: console

      $ datalad containers-add --url dhub://12345678.dkr.ecr.us-west-2.amazonaws.com/maze-code/data-import:latest data-import

   If you want to add a container that exists locally, specify the path to it
   like this:

   .. code-block:: console

      $ datalad containers-add midterm-software --url path/to/container

This command downloaded the container from Singularity Hub, added it to
the ``midterm_project`` dataset, and recorded basic information on the
container under its name "midterm-software" in the dataset's configuration at
``.datalad/config``. You can find out more about them in an upcoming dedicated section on these additional configurations.

Such configurations can, among other things, be important to ensure correct container invocation on specific systems or across systems.
One example is *bind-mounting* directories into containers, i.e., making a specific directory and its contents available inside a container.
Different containerization software (versions) or configurations of those determine *default bind-mounts* on a given system.
Thus, depending on the system and the location of the dataset on this system, a shared dataset may be automatically bind-mounted or not.
To ensure that the dataset is correctly bind-mounted on all systems, let's add a call-format specification with a bind-mount to the current working directory.

.. index::
   single: configuration.item; datalad.containers.<name>.cmdexec
.. runrecord:: _examples/DL-101-133-104
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda

   $ git config -f .datalad/config datalad.containers.midterm-software.cmdexec 'singularity exec -B {{pwd}} {img} {cmd}'
   $ datalad save -m "Modify the container call format to bind-mount the working directory"

.. index::
   pair: run command with provenance capture; with DataLad
   pair: run command; with DataLad containers-run

Now that we have a complete computational environment linked to the ``midterm_project``
dataset, we can execute commands in this environment. Let us, for example, try to repeat
the :dlcmd:`run` command from the section :ref:`yoda_project` as a
:dlcmd:`containers-run` command.

The previous ``run`` command looked like this:

.. code-block:: console

   $ datalad run -m "analyze iris data with classification analysis" \
     --input "input/iris.csv" \
     --output "pairwise_relationships.png" \
     --output "prediction_report.csv" \
     "python3 code/script.py {inputs} {outputs}"

How would it look like as a ``containers-run`` command?

.. runrecord:: _examples/DL-101-133-105
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: The analysis can be rerun in a software container

   $ datalad containers-run -m "rerun analysis in container" \
     --container-name midterm-software \
     --input "input/iris.csv" \
     --output "pairwise_relationships.png" \
     --output "prediction_report.csv" \
     "python3 code/script.py {inputs} {outputs}"

Almost exactly like a :dlcmd:`run` command! The only additional parameter
is ``container-name``. At this point, though, the ``--container-name``
flag is even *optional* because there is only a single container registered to the dataset.
But if your dataset contains more than one container you will *need* to specify
the name of the container you want to use in your command.
The complete command's structure looks like this:

.. code-block:: console

   $ datalad containers-run --name <containername> [-m ...] [--input ...] [--output ...] <COMMAND>

.. index::
   pair: containers-remove; DataLad command
   pair: containers-list; DataLad command
   pair: list known containers; with DataLad
.. find-out-more:: How can I list available containers or remove them?

   The command :dlcmd:`containers-list` will list all containers in
   the current dataset:

   .. runrecord:: _examples/DL-101-133-110
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project


      $ datalad containers-list

   The command :dlcmd:`containers-remove` will remove a container
   from the dataset, if there exists a container with name given to the
   command. Note that this will remove not only the image from the dataset,
   but also the configuration for it in ``.datalad/config``.


Here is how the history entry looks like:

.. runrecord:: _examples/DL-101-133-111
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Here is how that looks like in the history:

   $ git log -p -n 1

If you would :dlcmd:`rerun` this commit, it would be re-executed in the
software container registered to the dataset. If you would share the dataset
with a friend and they would :dlcmd:`rerun` this commit, the image would first
be obtained from its registered url, and thus your
friend can obtain the correct execution environment automatically.

Note that because this new :dlcmd:`containers-run` command modified the
``midterm_project`` subdirectory, we need to also save
the most recent state of the subdataset to the superdataset ``DataLad-101``.

.. runrecord:: _examples/DL-101-133-112
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Save the change in the superdataset

   $ cd ../
   $ datalad status

.. runrecord:: _examples/DL-101-133-113
   :language: console
   :workdir: dl-101/DataLad-101
   :cast: 10_yoda
   :notes: Save the change in the superdataset

   $ datalad save -d . -m "add container and execute analysis within container" midterm_project


Software containers, the ``datalad-container`` extension, and DataLad thus work well together
to make your analysis completely reproducible -- by not only linking code, data,
and outputs, but also the software environment of an analysis. And this does not
only benefit your future self, but also whomever you share your dataset with, as
the information about the container is shared together with the dataset. How cool
is that?


.. index::
   pair: DataLad concept; container image registration

What changes in .datalad/config when one adds a container?

.. include:: topic/container-imgcfg.rst

.. only:: adminmode

    Add a tag at the section end.

      .. runrecord:: _examples/DL-101-133-114
         :language: console
         :workdir: dl-101/DataLad-101

         $ git branch sct_computational_reproducibility

.. rubric:: Footnotes

.. [#f2] The main reason why Docker is not deployed on HPC systems is because
         it grants users "`superuser privileges <https://en.wikipedia.org/wiki/Superuser>`_".
         On multi-user systems such as HPC, users should not have those
         privileges, as it would enable them to tamper with other's or shared
         data and resources, posing a severe security threat.
