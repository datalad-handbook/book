.. _procedures:

Running Procedures
------------------

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
that can be shipped within DataLad or its extensions,
lie on a system, or come within datasets, and process
datasets in a particular way.

One of such procedures is the ``text2git`` configuration.
Let's demystify what this exactly is: The procedure is
nothing more than a simple script that writes the relevant
configuration (``annex_largefiles = '(not(mimetype=text/*))'``)
to the ``.gitattributes`` file of a dataset and saves this
modification with the commit message
"Instruct annex to add text files to Git". This particular
procedure lives in a script called ``cfg_text2git`` in the
sourcecode of DataLad. The amount of code
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

Despite its simplicity, it is very handy to have preconfigured
procedures that can be run in a single command line call. In the
case of ``text2git``, all text files in a dataset will be stored
in Git -- this is a useful configuration that is applicable to a
wide range of datasets. The ``text2git`` shortcut
spares naive users the necessity to learn about the ``.gitattributes``
file when setting up a dataset.

Thus, this configuration helper can minimize technical complexities
in a dataset -- users can concentrate on the actual task while
the dataset is configured automatically. Especially in the case
of trainees and new users, ``run-procedures`` can help to ease
working with the dataset, as the use case `link supervision <TODOsupervision>`_
showcases.

The ``text2git`` configuration applies a configuration for how
Git-annex treats different file types. Other procedures do not
only modify ``.gitattributes``, but can also populate a dataset
with particular content, or automate routine tasks such as
synchronizing dataset content with certain siblings.
To find out which procedures are available, one can use the
:command:`datalad run-procedure --discover` command (:manpage:`datalad-run-procedure`
manual). The command will search the dataset, the source code of
DataLad or installed DataLad extensions, and the system for
available procedures:

.. runrecord:: _examples/DL-101-127-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad run-procedure --discover

The output shows that there are three procedures available:
``cfg_metadatatypes``, ``cfg_text2git``, and ``cfg_yoda``.
It also lists where they are stored -- in this case,
they are all part of the source code of DataLad.
To find out more about a given procedure, you can ask for help:

.. todo::

   Once there is help for these procedures (https://github.com/datalad/datalad/issues/2649),
   include it here:

   .. runrecord:: _examples/DL-101-127-102
      :workdir: dl-101/DataLad-101
      :language: console

      $ datalad run-procedure --help-proc cfg_text2git

   It might be helpful to have (or reference) a table with all available
   procedures and a short explanation.

:command:`datalad run-procedure` not only *discovers*
but also *executes* procedures. If given the name of
a procedure, this command will apply the procedure to
the current dataset, or the dataset that is specified
with the ``-d/--dataset`` flag::

   datalad run-procedure cfg_text2git

However, procedures -- at least the procedures with
a ``cfg_`` prefix that DataLad provides --
can also be applied right at the creation of a dataset with the
``-c/--cfg-proc <name>`` option in a :command:`datalad create`
command, as in ``datalad create -c text2git DataLad-101``.
Note that to keep it extra simple and short, the
``cfg_`` prefix of the procedures is omitted in these calls.

As a general note, it is useful to apply procedures
as early as possible. Procedures such
as ``cfg_yoda`` (explained in detail in section :ref:`yoda`),
assume clean, freshly created datasets when they run,
and given that many procedures create files or change ``.gitattributes``,
existing files or configurations in a dataset can lead to unexpected
problems or failures.


.. findoutmore:: Write your own procedures

   Procedures can come with source code or datasets, but anyone can
   write their own extension as well, if they wish. This allows to
   automate routine configurations or tasks in a dataset.
   Some general rules for creating a custom procedure are outlined
   below:

   - A procedure can be any executable. Executables must have the
     appropriate permissions and, in the case of a script,
     must contain an appropriate shebang (TODO: turn into term once
     PR#134 is merged).

       - If a procedure is not executable, but its filename ends with
         ‘.py’, it is automatically executed by the ‘python’ interpreter
         (whichever version is available in the present environment).
         Likewise, procedure implementations ending on ‘.sh’ are executed via ‘bash’.

   - Procedures can implement any argument handling, but must be capable
     of taking at least one positional argument (the absolute path to the
     dataset they shall operate on).

   - By default, DataLad will search for user procedures (i.e. procedures on the
     *global* level) in ``~/.config/datalad/procedures``, and for dataset procedures
     (i.e. the *local* level) in ``.datalad/procedures`` relative to a dataset root.

   Therefore, in order to create a custom procedure, a simple script
   in the appropriate location is fine. Placing a script ``myprocedure``
   into ``.datalad/procedures`` will allow running
   ``datalad run-procedure myprocedure`` in your dataset, and because
   it is part of the dataset it will also allow distributing the procedure.

   .. todo::

      maybe write a toy-example procedure here


Summing up, DataLads :command:`run-procedure` command is a handy tool
with useful existing procedures but much flexibility for own
DIY procedure scripts. With the information of the last three sections
you should be able to write and understand necessary configurations,
but you can also rely on existing, preconfigured templates in the
form of procedures, and even write and distribute your own.




