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
it is good that some clever people decided to assist with
these tasks, and created pre-configured *run-procedures*
that can be shipped within DataLad, lie on a system, or
come within datasets.

One of such procedures is the ``text2git`` configuration.
Let's demystify what this exactly is. The procedure is
nothing more than a simple script that writes the relevant
configuration (``annex_largefiles = '(not(mimetype=text/*))'``)
to the ``.gitattributes`` file of a dataset and saves this
modification with the commit message
"Instruct annex to add text files to Git". This is all the
code there is in this script:

.. code-block:: bash
   :emphasize-lines: 6

    ds = require_dataset(
        sys.argv[1],
        check_installed=True,
        purpose='configuration')

    annex_largefiles = '(not(mimetype=text/*))'
    attrs = ds.repo.get_gitattributes('*')
    if not attrs.get('*', {}).get(
            'annex.largefiles', None) == annex_largefiles:
        ds.repo.set_gitattributes([
            ('*', {'annex.largefiles': annex_largefiles})])

    git_attributes_file = op.join(ds.path, '.gitattributes')
    ds.save(
        git_attributes_file,
        message="Instruct annex to add text files to Git",
    )

Despite its simplicity, it is very handy to have preconfigured
procedures that can be run in a single command line call. Other
procedures can also populate a dataset with particular content, or
automate routine tasks such as synchronizing dataset content with
certain siblings.

But before we use them, we need to find out which procedures are
available. This can be done with the :command:`datalad run-procedure --discover`
command (:manpage:`run-procedure` manual). This command will search
the dataset, the installation of datalad or datalad extensions,
and the system for available procedures:

.. runrecord:: _examples/DL-101-127-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ datalad run-procedure --discover

This says that there are three procedures available: ``cfg_metadatatypes``,
``cfg_text2git``, and ``cfg_yoda``. It also lists where they are stored --
in this case, they are all part of the source code of datalad.
To find out more about a given procedure, you can ask for help:

.. todo::

   Once there is help for these procedures (https://github.com/datalad/datalad/issues/2649),
   include it here:

   .. runrecord:: _examples/DL-101-127-102
      :workdir: dl-101/DataLad-101
      :language: console

      $ datalad run-procedure --help-proc cfg_text2git

:command:`datalad run-procedure` not only discovers but also executes procedures.
If given the name of a procedure, this command will apply the procedure to
the current dataset, or the dataset that is specified with the ``-d/--dataset``
flag::

   datalad run-procedure cfg_text2git

However, procedures can also be applied right at the creation of
a dataset with the ``-c <name>`` option in a :command:`datalad create`
command, as done in ``datalad create -c text2git DataLad-101``.

.. todo::

   resolve the mystery of inconsistent ``cfg`` prefixes in different
   commands calling the same procedures.