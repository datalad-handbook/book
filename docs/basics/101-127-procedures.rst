.. _procedures:

Configurations to go
--------------------

The past two sections should have given you a comprehensive
overview on the different configuration options the tools
Git, Git-annex, and DataLad provide. They not only
showed you a way to configure everything you may need to
configure, but also gave explanations about what the
configuration options actually mean.

But figuring out which configurations are useful and how
to apply them are also not the easiest tasks. Therefore,
some clever people decided to assist with
these tasks, and created pre-configured *procedures*
that process datasets in a particular way.
These procedures can be shipped within DataLad or its extensions,
lie on a system, or can be shared together with datasets.

One of such procedures is the ``text2git`` configuration.
In order to learn about procedures in general, let's demystify
what the ``text2git`` procedure exactly is: It is
nothing more than a simple script that

- writes the relevant configuration (``annex_largefiles = '(not(mimetype=text/*))'``,
  i.e., "Do not put anything that is a text file in the annex")
  to the ``.gitattributes`` file of a dataset, and
- saves this modification with the commit message
  "Instruct annex to add text files to Git".

This particular procedure lives in a script called
``cfg_text2git`` in the sourcecode of DataLad. The amount of code
in this script is not large, and the relevant lines of code
are highlighted:

.. code-block:: bash
   :emphasize-lines: 11, 17-18

    import sys
    import os.path as op
    from datalad.distribution.dataset import require_dataset

    ds = require_dataset(
        sys.argv[1],
        check_installed=True,
        purpose='configuration')

    # the relevant configuration:
    annex_largefiles = '(not(mimetype=text/*))'
    # check existing configurations:
    attrs = ds.repo.get_gitattributes('*')
    # if not already an existing configuration, configure Git-annex with the above rule
    if not attrs.get('*', {}).get(
            'annex.largefiles', None) == annex_largefiles:
        ds.repo.set_gitattributes([
            ('*', {'annex.largefiles': annex_largefiles})])

    # this saves and commits the changed .gitattributes file
    git_attributes_file = op.join(ds.path, '.gitattributes')
    ds.save(
        git_attributes_file,
        message="Instruct annex to add text files to Git",
    )

Just like ``cfg_text2git``, all DataLad procedures are
executables (such as a script, or compiled code).
In principle, they can be written in any language, and perform
any task inside of a dataset.
The ``text2git`` configuration for example applies a configuration for how
Git-annex treats different file types. Other procedures do not
only modify ``.gitattributes``, but can also populate a dataset
with particular content, or automate routine tasks such as
synchronizing dataset content with certain siblings.
What makes them a particularly versatile and flexible tool is
that anyone can write their own procedures. If a workflow is
a standard in a team and needs to be applied often, turning it into
a script can save time and effort. By pointing DataLad
to the location the procedures reside in they can be applied, and by
including them in a dataset they can even be shared.
And even if the script is simple, it is very handy to have preconfigured
procedures that can be run in a single command line call. In the
case of ``text2git``, all text files in a dataset will be stored
in Git -- this is a useful configuration that is applicable to a
wide range of datasets. It is a shortcut that
spares naive users the necessity to learn about the ``.gitattributes``
file when setting up a dataset.


.. index:: ! datalad command; run-procedure


To find out available procedures, the command
:command:`datalad run-procedure --discover` (:manpage:`datalad-run-procedure`
manual) is helpful.
This command will make DataLad search the default location for
procedures in a dataset, the source code of DataLad or
installed DataLad extensions, and the default locations for
procedures on the system for available procedures:

.. runrecord:: _examples/DL-101-127-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad run-procedure --discover

The output shows that in this particular dataset, on the particular
system the book is written on, there are at least three procedures available:
``cfg_metadatatypes``, ``cfg_text2git``, and ``cfg_yoda``.
It also lists where they are stored -- in this case,
they are all part of the source code of DataLad [#f1]_.

- ``cfg_yoda`` configures a dataset according to the yoda
  principles -- the section :ref:`yoda` talks about this in detail.
- ``cfg_text2git`` configures text files to be stored in Git.
- ``cfg_metadatatypes`` lets users configure additional metadata
  types -- more about this in a later section on DataLads metadata
  handling.

Applying procedures
^^^^^^^^^^^^^^^^^^^

:command:`datalad run-procedure` not only *discovers*
but also *executes* procedures. If given the name of
a procedure, this command will apply the procedure to
the current dataset, or the dataset that is specified
with the ``-d/--dataset`` flag::

   datalad run-procedure [-d <PATH>] cfg_text2git

The typical workflow is to create a dataset and apply
a procedure afterwards.
However, some procedures shipped with DataLad or its extensions with a
``cfg_`` prefix can also be applied right at the creation of a dataset
with the ``-c/--cfg-proc <name>`` option in a :command:`datalad create`
command. This is a peculiarity of these procedures because, by convention,
all of these procedures are written to not require arguments.
The command structure looks like this::

   datalad create -c text2git DataLad-101

Note that the ``cfg_`` prefix of the procedures is omitted in these
calls to keep it extra simple and short. The
available procedures in this example (``cfg_yoda``, ``cfg_text2git``)
could thus be applied within a :command:`datalad create` as

- ``datalad create -c yoda <DSname>``
- ``datalad create -c text2git <DSname>``

.. findoutmore:: Applying procedures in subdatasets

   Procedures can be applied in datasets on any level in the dataset hierarchy, i.e.,
   also in subdatasets. Note, though, that a subdataset will show up as being
   ``modified`` in :command:`datalad status` *in the superdataset*
   after applying a procedure.
   This is expected, and it would also be the case with any other modification
   (saved or not) in the subdataset, as the version of the subdataset that is tracked
   in the superdataset simply changed. A :command:`datalad save` in the superdataset
   will make sure that the version of the subdataset gets updated in the superdataset.

As a general note, it can be useful to apply procedures
early in the life of a dataset. Procedures such
as ``cfg_yoda`` (explained in detail in section :ref:`yoda`),
create files, change ``.gitattributes``, or apply other configurations.
If many other (possibly complex) configurations are
already in place, or if files of the same name as the ones created by
a procedure are already in existence, this can lead to unexpected
problems or failures, especially for naive users. Applying ``cfg_text2git``
to a default dataset in which one has saved many text files already
(as per default added to the annex) will not place the existing, saved
files into Git -- only those text files created *after* the configuration
was applied.


.. findoutmore:: Write your own procedures

   Procedures can come with DataLad or its extensions, but anyone can
   write their own ones in addition, and deploy them on individual machines,
   or ship them within DataLad datasets. This allows to
   automate routine configurations or tasks in a dataset.
   Some general rules for creating a custom procedure are outlined
   below:

   - A procedure can be any executable. Executables must have the
     appropriate permissions and, in the case of a script,
     must contain an appropriate :term:`shebang`.

       - If a procedure is not executable, but its filename ends with
         ``.sh``, it is automatically executed via :term:`bash`.

   - Procedures can implement any argument handling, but must be capable
     of taking at least one positional argument (the absolute path to the
     dataset they shall operate on).

   - Custom procedures rely heavily on configurations in ``.datalad/config``
     (or the associated environment variables). Within ``.datalad/config``,
     each procedure should get an individual entry that contains at least
     a short "help" description on what the procedure does. Below is a minimal
     ``.datalad/config`` entry for a custom procedure:

     .. code-block:: bash

        [datalad "procedures.<NAME>"]
           help = "This is a string to describe what the procedure does"

   - By default, on GNU/Linux systems, DataLad will search for system-wide procedures
     (i.e., procedures on the *system* level) in ``/etc/xdg/datalad/procedures``,
     for user procedures (i.e., procedures on the *global* level) in ``~/.config/datalad/procedures``,
     and for dataset procedures (i.e., the *local* level [#f2]_) in ``.datalad/procedures``
     relative to a dataset root.
     Note that ``.datalad/procedures`` does not exist by default, and the ``procedures``
     directory needs to be created first.

       - Alternatively to the default locations, DataLad can be pointed to the
         location of a procedure with a configuration in ``.datalad/config``
         (or with the help of the associated :term:`environment variable`\s).
         The appropriate configuration keys for ``.datalad/config`` are either
         ``datalad.locations.system-procedures`` (for changing the *system* default),
         ``datalad.locations.user-procedures`` (for changing the *global* default),
         or ``datalad.locations.dataset-procedures`` (for changing the *local* default).
         An example ``.datalad/config`` entry for the local scope is shown below.

         .. code-block:: bash

            [datalad "locations"]
                dataset-procedures = relative/path/from/dataset-root

    - By default, DataLad will call a procedure with a standard template
      defined by a format string::

         interpreter {script} {ds} {arguments}

      where arguments can be any additional command line arguments a script
      (procedure) takes or requires. This default format string can be
      customized within ``.datalad/config`` in ``datalad.procedures.<NAME>.call-format``.
      An example ``.datalad/config`` entry with a changed call format string
      is shown below.

      .. code-block:: bash

         [datalad "procedures.<NAME>"]
            help = "This is a string to describe what the procedure does"
            call-format = "python {script} {ds} {somearg1} {somearg2}"

    - By convention, procedures should leave a dataset in a clean state.

   Therefore, in order to create a custom procedure, an executable script
   in the appropriate location is fine. Placing a script ``myprocedure``
   into ``.datalad/procedures`` will allow running
   ``datalad run-procedure myprocedure`` in your dataset, and because
   it is part of the dataset it will also allow distributing the procedure.
   Below is a toy-example for a custom procedure:

   .. runrecord:: _examples/DL-101-127-103
      :language: console
      :workdir: procs

      $ datalad create somedataset; cd somedataset

   .. runrecord:: _examples/DL-101-127-104
      :language: console
      :workdir: procs/somedataset

      $ mkdir .datalad/procedures
      $ cat << EOT > .datalad/procedures/example.py
      """A simple procedure to create a file 'example' and store
      it in Git, and a file 'example2' and annex it. The contents
      of 'example' must be defined with a positional argument."""

      import sys
      import os.path as op
      from datalad.distribution.dataset import require_dataset
      from datalad.utils import create_tree

      ds = require_dataset(
          sys.argv[1],
          check_installed=True,
          purpose='showcase an example procedure')

      # this is the content for file "example"
      content = """\
      This file was created by a custom procedure! Neat, huh?
      """

      # create a directory structure template. Write
      tmpl = {
          'somedir': {
              'example': content,
          },
          'example2': sys.argv[2] if sys.argv[2] else "got no input"
      }

      # actually create the structure in the dataset
      create_tree(ds.path, tmpl)

      # rule to store 'example' Git
      ds.repo.set_gitattributes([('example', {'annex.largefiles': 'nothing'})])

      # save the dataset modifications
      ds.save(message="Apply custom procedure")

      EOT

   .. runrecord:: _examples/DL-101-127-105
      :language: console
      :workdir: procs/somedataset

      $ datalad save -m "add custom procedure"

   At this point, the dataset contains the custom procedure ``example``.
   This is how it can be executed and what it does:

   .. runrecord:: _examples/DL-101-127-106
      :language: console
      :workdir: procs/somedataset

      $ datalad run-procedure example "this text will be in the file 'example2'"

   .. runrecord:: _examples/DL-101-127-107
      :language: console
      :workdir: procs/somedataset

      #the directory structure has been created
      $ tree

   .. runrecord:: _examples/DL-101-127-108
      :workdir: procs/somedataset
      :language: console

      #lets check out the contents in the files
      $ cat example2  && echo '' && cat somedir/example

   .. runrecord:: _examples/DL-101-127-109
      :workdir:  procs/somedataset
      :language: console

      $ git config -f .datalad/config datalad.procedures.example.help "A toy example"
      $ datalad save -m "add help description"

   To find out more about a given procedure, you can ask for help:

   .. runrecord:: _examples/DL-101-127-110
      :workdir: procs/somedataset
      :language: console

      $ datalad run-procedure --help-proc example

   .. todo::

      It might be helpful to have (or reference) a table with all available
      procedures and a short explanation. Maybe on the cheatsheet.

Summing up, DataLads :command:`run-procedure` command is a handy tool
with useful existing procedures but much flexibility for own
DIY procedure scripts. With the information of the last three sections
you should be able to write and understand necessary configurations,
but you can also rely on existing, preconfigured templates in the
form of procedures, and even write and distribute your own.

Therefore, envision procedures as
helper-tools that can minimize technical complexities
in a dataset -- users can concentrate on the actual task while
the dataset is set-up, structured, processed, or configured automatically
with the help of a procedure.
Especially in the case of trainees and new users, applying procedures
instead of doing relevant routines "by hand" can help to ease
working with the dataset, as the use case :ref:`usecase_student_supervision`
showcases.

Finally, make a note about running procedures inside of ``notes.txt``:

.. runrecord:: _examples/DL-101-127-111
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT >> notes.txt
   It can be useful to use pre-configured procedures that can apply
   configurations, create files or file hierarchies, or perform
   arbitrary tasks in datasets. They can be shipped with DataLad,
   its extensions, or datasets, and you can even write your own
   procedures and distribute them. The "datalad run-procedure"
   command is used to apply such a procedure to a dataset. Procedures
   shipped with DataLad or its extensions starting with a "cfg" prefix
   can also be applied at the creation of a dataset with
   "datalad create -c <PROC-NAME> <PATH>" (omitting the "cfg" prefix).

   EOT

.. runrecord:: _examples/DL-101-127-112
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad save -m "add note on DataLads procedures"

.. rubric:: Footnotes

.. [#f1] In theory, because procedures can exist on different levels, and
         because anyone can create (and thus name) their own procedures, there
         can be name conflicts. The order of precedence in such cases is:
         user-level, system-level, dataset, DataLad extension, DataLad, i.e.,
         local procedures take precedence over those coming from "outside" via
         datasets or datalad extensions.
         If procedures in a higher-level dataset and a subdataset have the same
         name, the procedure closer to the dataset ``run-procedure`` is
         operating on takes precedence.

.. [#f2] Note that we simplify the level of procedures that exist within a dataset
         by calling them *local*. Even though they apply to a dataset just as *local*
         Git configurations, unlike Git's *local* configurations in ``.git/config``,
         the procedures and procedure configurations in ``.datalad/config`` are committed
         and can be shared together with a dataset. The procedure level *local* therefore
         does not exactly corresponds to the *local* scope in the sense that Git uses it.