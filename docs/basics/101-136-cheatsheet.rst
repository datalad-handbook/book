.. _cheat:

The DataLad Cheat-Sheet
-----------------------

DataLad is a data management and publication multitool based
on Git and Git-annex with a command line interface and a Python
API. With DataLad, you can version control arbitrarily large data,
share or consume data, and record changes made to data.

**Basic command structure**:

``datalad [--DATALAD-OPTION <opt. flag spec.>] COMMAND [--COMMAND-OPTION <opt. flag spec.>] [PATH]``

General options for commands in the command line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following general options can be supplied to most commands

- ``-d/--dataset``: A path that points to the root of the dataset an operation is performed on.
  Supplying ``^`` points to the top-most superdataset.
- ``-D/--description``: A description of the location (e.g., "my backup server").
- ``-f/--force``: Force execution of a command (Dangerzone!).
- ``-m/--message``: A description about a change made to the dataset.
- ``-r/--recursive``: Perform an operation recursively in potential subdatasets.
- ``-R/--recursion limit <n>``: Limit recursive operations to *n* levels of subdatasets.

Supplying ``-h/--help`` after any command opens the command's help-page in a terminal.

General options for DataLad itself

General options for DataLad itself in the command line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``datalad`` invocation has its own options. They need to be specified
prior to the command specification.

- ``-c``: Set configuration variables to override configurations from files.
- ``-f/--output-format``: Specify the format (default, json, json_pp, tailored) for
  command rendering.
- ``-l/--log-level``: Set logging verbosity level (critical, error, warning, info,
  debug).

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

The column ``General options`` displays which of the general options can be applied to a
command. Additional options are mentioned in ``Description``, if applicable.

Dataset operations
""""""""""""""""""

   +--------------+---------------+----------------------------------------------------------+
   | Command      |General options|    Description                                           |
   +==============+===============+==========================================================+
   |              |    [f/d/D]    | create a new dataset from scratch.                       |
   |  **create**  |               | If executed within a dataset and                         |
   |              |               | the ``-d/--dataset`` flag, it is                         |
   |              |               | created as a subdataset.                                 |
   +--------------+---------------+----------------------------------------------------------+
   |*Command structure*:                                                                     |
   |    ``datalad create [-c <config-procedure>] PATH``                                      |
   |*Example invocation*:                                                                    |
   |    ``datalad create -c yoda my_first_ds``                                               |
   |                                                                                         |
   |    Create dataset "my_first_ds" with yoda setup at current location.                    |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/D/r/R]  | install an existing dataset from a path/url/open data    |
   |  **install** |               | collection (``///``). With ``-g/--get-data``, all dataset|
   |              |               | content is obtained with a ``get`` operation. Providing  |
   |              |               | ``-d`` installs a dataset as a subdataset.               |
   +--------------+---------------+----------------------------------------------------------+
   |*Command structure*:                                                                     |
   |    ``datalad install -s/--source URL/PATH [-g/--get-data] [PATH]``                      |
   |*Example invocation*:                                                                    |
   |    ``datalad install -s https://github.com/datalad/datalad.git repos/datalad``          |
   |                                                                                         |
   |    Install the Github repository of DataLad into ``repos/datalad``.                     |
   |                                                                                         |
   |    ``datalad install ///``                                                              |
   |                                                                                         |
   |    Install the DataLad superdataset into the current location.                          |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/D/r/R]  | Get any dataset content (files/directories/subdatasets)  |
   |  **get**     |               | Will get *directory* content recursively by default, but |
   |              |               | not *subdataset* content. Specify the label of a data    |
   |              |               | source (e.g., sibling) with ``-s/--source``.             |
   +--------------+---------------+----------------------------------------------------------+
   |*Command structure*:                                                                     |
   |    ``datalad get [-s/--source <label>] PATH``                                           |
   |*Example invocation*:                                                                    |
   |    ``datalad get file_xyz.pdf directory_1``                                             |
   |                                                                                         |
   |    Get the contents for ``file_xyz`` and for all files inside of ``directory_1``        |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R/m]  | Save the current state of a dataset. Use ``-u/--updated``|
   |   **save**   |               | to leave untracked files untouched, and ``--to-git`` to  |
   |              |               | save modifications to Git instead of Git-annex.          |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad save [-u/--updated] [PATH]``                                                   |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R]    | Update a dataset from a sibling. Updates are by default  |
   |  **update**  |               | on branch ``remotes/origin/master``. Changes can be      |
   |              |               | merged with ``--merge``. Without ``-s/--sibling``, all   |
   |              |               | siblings are updated.                                    |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad update [-s <sibling-name>] [--merge]``                                         |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R]    | Drop file content from dataset (remove data, retain      |
   |  **drop**    |               | symlink). Availability of at least one remote copy needs |
   |              |               | to be verified - disable with ``--nocheck``.             |
   |              |               | Drops all contents if no PATH is given.                  |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad drop [--nocheck] [PATH]``                                                      |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R]    | Uninstall subdatasets. Availability of at least one      |
   |**uninstall** |               | remote copy needs to be verified - disable with          |
   |              |               | ``--nocheck``. PATH can not be the current directory.    |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad uninstall [--nocheck] PATH``                                                   |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R/m]  | Remove datasets + contents completely, and unregister    |
   |  **remove**  |               | from potential top-level datasets. Availability of at    |
   |              |               | least one remote copy needs to be verified - disable with|
   |              |               | ``--nocheck``. PATH can not be the current directory.    |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad drop [--nocheck] [PATH]``                                                      |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/r/R]    | Unlock file(s) of a dataset to enable editing their      |
   |  **unlock**  |               | content. If PATH is not provided, all files are unlocked.|
   |              |               |                                                          |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad unlock [PATH]``                                                                |
   +--------------+---------------+----------------------------------------------------------+

TODO:

- publish
- create-sibling


Metadata

- search
- metadata
- aggregate_metadata
- extract_metadata

Reproducible execution
""""""""""""""""""""""

   +--------------+---------------+----------------------------------------------------------+
   | Command      |General options|    Description                                           |
   +==============+===============+==========================================================+
   |              |    [d/m]      | Run an arbitrary shell command and record its impact on  |
   |  **run**     |               | a dataset. Only makes a record if the command modifies   |
   |              |               | the dataset. ``-i/--input`` is retrieved with ``get`` and|
   |              |               | ``-o/--output`` is unlocked, is necessary. Requires clean|
   |              |               | dataset status or ``--explicit`` flag.                   |
   +--------------+---------------+----------------------------------------------------------+
   | ``datalad run [--input <"input path">] [--output <"output path">] [--explicit] command``|
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/m]      | Re-execute a previous ``run`` command identified by its  |
   |  **rerun**   |               | hash, and save resulting modifications.                  |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad rerun [-s/--since <hash>] [-o/--onto <hash>] HASH``                            |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d]        | Run prepared procedures (DataLad scripts) on a dataset.  |
   |**run-**      |               | To find available procedures, use ``--discover`` as the  |
   |**procedure** |               | only argument, else specify the name of the procedure.   |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |    ``datalad run-procedure NAME [--discover]``                                          |
   +--------------+---------------+----------------------------------------------------------+

Miscellaneous commands
""""""""""""""""""""""

   +--------------+---------------+----------------------------------------------------------+
   | Command      |General options|    Description                                           |
   +==============+===============+==========================================================+
   |              |    [d/m]      | Download content from a URL. Specify a path to save the  |
   |**download-** |               | download with ``-O/--path``. If the target exists,       |
   |**url**       |               | ``-o/--overwrite`` will enable overwriting it.           |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad download-url <url> [-o <path>] [--overwrite]``                                 |
   +--------------+---------------+----------------------------------------------------------+
   |              |    [d/]       | Generate a report about the DataLad installation and     |
   |**wtf**       |               | configuration. Sharing this report with untrusted parties|
   |              |               | (e.g., on the web) should be done with care, as it may   |
   |              |               | include identifying information or access tokens.        |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad wtf [-s/--sensitive {some/all}]``                                              |
   +--------------+---------------+----------------------------------------------------------+

TODO:
- test
- ls
- clean
- add-archive-content

Plumbing
""""""""

plumbing
- annotate-paths
- clone
- create-test-dataset
- status
- diff
- siblings
- sshrun
- subdatasets

Concepts
^^^^^^^^

**Dataset nesting**

DataLad datasets can contain other DataLad datasets, enabling arbitrarily deep nesting
inside of a dataset. Each individual dataset is a modular component with a stand-alone
history. A superdataset only registers the version (via commit hash) of the subdataset.
A dataset knows its installed subdatasets, but has no way of knowing about its superdataset(s).
To apply commands not only to the dataset the action is performed in but also in subdatasets,
run commands *recursively*, i.e. with ``-r/--recursive``.

**Recursion**


- recursion

**DataLad procedures**

Datalad procedures are algorithms that alter datasets in certain ways. They are used to
automate routine tasks such as configurations, synchronizing datasets with siblings, or
populating datasets. :command:`datalad run-procedure --discover`` finds available
procedures, :command:`datalad run-procedure <Procedure-name>` applies a given procedure
to a dataset.

.. todo::

   table of DataLad core's extensions.
   - cfg_text2git
   - cfg_yoda
   - ...?

- procedures

.. todo::

   cross references to the chapters

.. todo::

   Path handling/treatment, esp. for relative paths and when pointing to a subdataset.


Configuration
^^^^^^^^^^^^^

Within a dataset the following files contain configurations for
DataLad, Git-annex, and Git: ``.git/config``, ``.datalad/config``, ``.gitmodules``,
``.gitattributes``. All but ``.git/config`` are version controlled and can be distributed
with a dataset. The :command:`git config` command can modify all but ``.gitattributes``.
``.gitattributes`` contains rules about which files to annex based on file path, type
and/or size.
Environment variables for configurations override options set in configuration files.