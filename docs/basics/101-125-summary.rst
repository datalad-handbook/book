.. _summary_config:

Summary
-------

This has been a substantial amount of information regarding various configuration
types, methods, and files. After this lecture, you have greatly broadened
your horizon about configurations of datasets:

- Configurations exist at different scopes and for different tools. Each
  of such configuration scopes exists in an individual file, on a *system-wide*,
  *global* (user-specific) or *local* (repository specific) level. In addition
  to Git's *local* scope in ``.git/config``, DataLad introduces its own configurations within
  ``.datalad/config`` that apply to a specific dataset, but are committed and
  therefore distributed. More specialized scopes take precedence over more global scopes.

- Almost all configurations can be set with the :gitcmd:`config`.
  Its structure looks like this::

   git config --local/--global/--system --add/remove-all/--list section.[subsection.]variable "value"

- The ``.git/config`` configuration file is not version controlled, other
  configuration files (``.gitmodules``, ``.gitattributes``, ``.datalad/config``)
  however are, and can be shared together with the dataset. Non-shared configurations
  will take precedence over shared configurations in a dataset clone.

- Other tools than Git can be configured with the :gitcmd:`config` command
  as well. If configurations needs to be written to a file other than a
  ``.git(/)config`` file, supply a path to this file with the ``-f/--file`` flag
  in a :gitcmd:`config` command.

- The ``.gitattributes`` file is the only configuration file the :gitcmd:`config`
  can not write to, because it has a different layout. However, run-procedures or
  the user can write simple rules into it that determine which files are annexed
  and which are stored in Git.

- DataLad's ``run-procedure``\s offer an easy and fast alternative to DIY
  configurations, structuring, or processing of the dataset, and offer means to share or ship configurations together with a dataset.
  They can be applied already at creation of a dataset with ``datalad create -c <procedure>``,
  or executed later with a :dlcmd:`run-procedure` command.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Configurations are not a closed book for you anymore. What will probably be
especially helpful is your new knowledge about ``.gitattributes`` and
DataLad's ``run-procedure`` command that allow you to configure the behavior
of git-annex in your dataset.
