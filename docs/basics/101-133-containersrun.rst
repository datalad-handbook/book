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
`datalad containers <http://docs.datalad.org/projects/container/en/latest/>`_
extension [#f1]_.

This section will give a quick overview on what containers are and
demonstrate how ``datalad-containers`` helps to capture full provenance of an
analysis by linking containers to datasets and analyses.

Containers
^^^^^^^^^^

.. index:: ! software container, ! container

To put it simple, computational containers are cut-down virtual machines that
allow you to package all software libraries and their dependencies (all in the
precise version your analysis requires) into a bundle you can share with
others. On your own and other's machines, the container constitutes a secluded
software environment that

- contains the exact software environment that you specified, ready to run
  analyses in
- does not effect any software outside of the container

Unlike virtual machines, software containers do not have their own operating
system. Instead, they use basic services of the underlying operating system
of the computer they run on (in a read-only fashion). This makes them
lightweight and portable. By sharing software environments with containers,
others (and also yourself) have easy access to the correct software
without the need to modify the software environment of the machine the
container runs on. Thus, containers are ideal to encapsulate the software
environment and share it together with the analysis code and data to ensure
computational reproducibility of your analyses, or to create a suitable
software environment on a computer that you do not have permissions to deploy
software on.

There are a number of different tools to create and use containers, with
`Docker <https://www.docker.com/>`_ being one of the most well-known of them.
While being a powerful tool, it is only rarely used on high performance computing
(HPC) infrastructure [#f2]_. An alternative is `Singularity <https://sylabs
.io/docs/>`_.
Both of these tools share core terminology:

**Recipe**
   A text file template that lists all required components of the computational environment.
   It is made by a human user.

**Image**
   This is *built* from the recipe file. It is a static filesystem inside a file,
   populated with the software specified in the recipe, and some initial configuration.

**Container**
  A running instance of an Image that you can actually use for your computations.
  If you want to create and run your own software container, you start by writing
  a recipe file and build an Image from it. Alternatively, you can can also *pull*
  an Image built from a publicly shared recipe from the *Hub* of the tool you are using.

**Hub**
  A storage resource to share and consume images. There is
  `Singularity-Hub <https://singularity-hub.org/>`_ and
  `Docker-Hub <https://hub.docker.com/>`_. Both are optional, additional services
  not required to use software containers, but a convenient way to share recipes
  and have imaged built from them by a service (instead of building them
  manually and locally).

Note that as of now, the ``datalad-containers`` extension supports
Singularity and Docker images.
Singularity furthermore is compatible with Docker -- you can use
Docker Images as a basis for Singularity Images, or run Docker Images with
Singularity (even without having Docker installed).

.. note::

   In order to use Singularity containers (and thus ``datalad containers``), you have to
   `install <https://singularity.lbl.gov/docs-installation>`_ the software singularity.

Using ``datalad containers``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: ! datalad command; containers-add
.. index:: ! datalad command; containers-run

One core feature of the ``datalad containers`` extension is that it registers
computational containers to a dataset. This is done with the
:command:`datalad containers-add` command.
Once a container is registered, arbitrary commands can be executed inside of
it, i.e., in the precise software environment the container encapsulates. All it
needs for this it to swap the :command:`datalad run` command introduced in
section :ref:`run` with the :command:`datalad containers-run` command.

Let's see this in action for the ``midterm_analysis`` dataset by rerunning
the analysis you did for the midterm project within a Singularity container.
We start by registering a container to the dataset.
For this, we will pull an Image from Singularity hub. This Image was made
for the handbook, and it contains the relevant Python setup for
the analysis. Its recipe lives in the handbook's
`resources repository <https://github.com/datalad-handbook/resources>`_, and the
Image is built from the recipe via Singularity hub.
If you're curious how to create a Singularity Image, the hidden
section below has some pointers:

.. findoutmore:: How to make a Singularity Image

   Singularity containers are build from Image files, often
   called "recipes", that hold a "definition" of the software container and its
   contents and components. The
   `singularity documentation <https://sylabs.io/guides/3.4/user-guide/build_a_container.html>`_
   has its own tutorial on how to build such Images from scratch.
   An alternative to writing the Image file by hand is to use
   `Neurodocker <https://github.com/kaczmarj/neurodocker#singularity>`_. This
   command-line program can help you generate custom Singularity recipes (and
   also ``Dockerfiles``, from which Docker Images are build). A wonderful tutorial
   on how to use Neurodocker is
   `this introduction <https://miykael.github.io/nipype_tutorial/notebooks/introduction_neurodocker.html>`_
   by Michael Notter.

   Once a recipe exists, the command

   .. code-block:: bash

      sudo singularity build <NAME> <RECIPE>

   will build a container (called ``<NAME>``) from the recipe. Note that this
   command requires ``root`` privileges ("``sudo``"). You can build the container
   on any machine, though, not necessarily the one that is later supposed to
   actually run the analysis, e.g., your own laptop versus a compute cluster.
   Alternatively, `Singularity Hub <https://singularity-hub.org/>`_ integrates
   with Github and builds containers from Images pushed to repositories on Github.
   `The docs <https://singularityhub.github.io/singularityhub-docs/>`_
   give you a set of instructions on how to do this.

The :command:`datalad containers-add` command takes an arbitrary
name to give to the container, and a path or url to a container Image:

.. runrecord:: _examples/DL-101-133-101
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Computational reproducibility: add a software container

   # we are in the midterm_project subdataset
   $ datalad containers-add midterm-software --url shub://adswa/resources:1

.. findoutmore:: How do I add an Image from Dockerhub, or a local container?

   Should the Image you want to use lie on Dockerhub, specify the ``--url``
   option prefixed with ``docker://`` instead of ``shub://`` like this::

      datalad containers-add midterm-software --url docker://adswa/resources:1

   If you want to add a container that exists locally, specify the path to it
   like this::

      datalad containers-add midterm-software --url path/to/container

This command downloaded the container from Singularity Hub, added it to
the ``midterm_project`` dataset, and recorded basic information on the
container under its name "midterm-software" in the dataset's configuration at
``.datalad/config``.

.. findoutmore:: What has been added to .datalad/config?

   .. runrecord:: _examples/DL-101-133-102
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project

      $ cat .datalad/config

   This recorded the Image's origin on Singularity-Hub, the location of the
   Image in the dataset under ``.datalad/environments/<NAME>/image``, and it
   specifies the way in which the container should be used: The line

   .. code-block:: bash

       cmdexec = singularity exec {img} {cmd}

   can be read as: "If this container is used, take the ``cmd`` (what you wrap in a
   :command:`datalad containers-run` command) and plug it into a
   :command:`singularity exec` command. The mode of calling Singularity,
   namely ``exec``, means that the command will be executed inside of the container.

   Note that the Image is saved under ``.datalad/environments`` and the
   configuration is done in ``.datalad/config`` -- as these files are version
   controlled and shared with together with a dataset, your software
   container and the information where it can be re-obtained from are linked
   to your dataset.

   This is how the ``containers-add`` command is recorded in your history:

   .. runrecord:: _examples/DL-101-133-103
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project
      :cast: 10_yoda
      :notes: The software container got added to your datasets history

      $ git log -n 1 -p

Now that we have a complete computational environment linked to the ``midterm_project``
dataset, we can execute commands in this environment. Let us for example try to repeat
the :command:`datalad run` command from the section :ref:`yoda_project` as a
:command:`datalad containers-run` command.

The previous ``run`` command looked like this::

   $ datalad run -m "analyze iris data with classification analysis" \
     --input "input/iris.csv" \
     --output "prediction_report.csv" \
     --output "pairwise_relationships.png" \
     "python3 code/script.py"

How would it look like as a ``containers-run`` command?

.. runrecord:: _examples/DL-101-133-104
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: The analysis can be rerun in a software container

   $ datalad containers-run -m "rerun analysis in container" \
     --container-name midterm-software \
     --input "input/iris.csv" \
     --output "prediction_report.csv" \
     --output "pairwise_relationships.png" \
     "python3 code/script.py"

Almost exactly like a :command:`datalad run` command! The only additional parameter
is ``container-name``. At this point, though, the ``--container-name``
flag is even *optional* because there is only a single container registered to the dataset.
But if your dataset contains more than one container you will *need* to specify
the name of the container you want to use in your command.
The complete command's structure looks like this::

   $ datalad containers-run --name <containername> [-m ...] [--input ...] [--output ...] <COMMAND>

.. index:: ! datalad command; containers-remove
.. index:: ! datalad command; containers-list

.. findoutmore:: How can I list available containers or remove them?

   The command :command:`datalad containers-list` will list all containers in
   the current dataset:

   .. runrecord:: _examples/DL-101-133-110
      :language: console
      :workdir: dl-101/DataLad-101/midterm_project


      $ datalad containers-list

   The command :command:`datalad containers-remove` will remove a container
   from the dataset, if there exists a container with name given to the
   command. Note that this will remove not only the Image from the dataset,
   but also the configuration for it in ``.datalad/config``.


Here is how the history entry looks like:

.. runrecord:: _examples/DL-101-133-111
   :language: console
   :workdir: dl-101/DataLad-101/midterm_project
   :cast: 10_yoda
   :notes: Here is how that looks like in the history:

   $ git log -p -n 1

If you would :command:`rerun` this commit, it would be re-executed in the
software container registered to the dataset. If you would share the dataset
with a friend and they would :command:`rerun` this commit, the Image would first
be obtained from its registered url, and thus your
friend can obtain the correct execution environment automatically.

Note that because this new :command:`containers-run` command modified the
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


Software containers, the ``datalad-containers`` extension, and DataLad thus work well together
to make your analysis completely reproducible -- by not only linking code, data,
and outputs, but also the software environment of an analysis. And this does not
only benefit your future self, but also whomever you share your dataset with, as
the information about the container is shared together with the dataset. How cool
is that?

If you are interested in more, you can read about another example of :command:`datalad containers-run`
in the usecase :ref:`usecase_reproduce_neuroimg`.



.. only:: adminmode

    Add a tag at the section end.

      .. runrecord:: _examples/DL-101-133-114
         :language: console
         :workdir: dl-101/DataLad-101

         $ git branch sct_computational_reproducibility

.. rubric:: Footnotes

.. [#f1] To read more about DataLad's extensions, see section :ref:`extensions_intro`.
.. [#f2] The main reason why Docker is not deployed on HPC systems is because
         it grants users "`superuser privileges <https://en.wikipedia.org/wiki/Superuser>`_".
         On multi-user systems such as HPC, users should not have those
         privileges, as it would enable them to temper with other's or shared
         data and resources, posing a severe security threat.
