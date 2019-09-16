.. _cheat:

The DataLad Cheat-Sheet
-----------------------

DataLad is a data management and publication multitool based
on Git and Git-annex with a command line interface and a Python
API. With DataLad, you can version control arbitrarily large data,
share or consume data, and record changes made to data.

**Basic command structure**:

``datalad [-c <config-option>] COMMAND [--flag <optional flag specification>] [PATH]``

General flags for the command line interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following general flags can be supplied to most commands

- ``-d/--dataset``: A path that points to the root of the dataset an operation is performed on.
- ``-D/--description``: A description of the location (e.g. "my backup server").
- ``-f/--force``: Force execution of a command (Dangerzone!).
- ``-h/--help``: Call any command with this flag to get help.
- ``-m/--message``: A description about a change made to the dataset.
- ``-r/--recursive``: Perform an operation recursively in potential subdatasets.
- ``-R/--recursion limit <n>``: Limit recursive operations to *n* levels of subdatasets.

Commands
^^^^^^^^

If general flags can be applied to the commands below, this is indicated
by a lower-case letter in front of the command name.

Dataset operations
""""""""""""""""""

   +--------------+---------------+----------------------------------------------------------+
   | Command      |General flags  |    Description                                           |
   +==============+===============+==========================================================+
   |              |  [h/f/d/D]    | create a new dataset from scratch.                       |
   |  **create**  |               | If executed within a dataset and                         |
   |              |               | the ``-d/--dataset`` flag, it is                         |
   |              |               | created as a subdataset.                                 |
   +--------------+---------------+----------------------------------------------------------+
   |    ``datalad create [-c <config-procedure>] PATH``                                      |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/D/r/R]  | install an existing dataset from a path/url/open data    |
   |  **install** |               | collection. When using ``-g/--get-data``, all dataset    |
   |              |               | content is obtained with a ``get`` operation. Providing  |
   |              |               | ``-d`` installs a dataset as a subdataset.               |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad install -s/--source URL/PATH [-g/--get-data] [PATH]``                          |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/D/r/R]  | Get any dataset content (files/directories/subdatasets)  |
   |  **get**     |               | Will get *directory* content recursively by default, but |
   |              |               | not *subdataset* content. Specify the label of a data    |
   |              |               | source (e.g. sibling) with ``-s/--source``.              |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad get [-s/--source <label>] PATH``                                               |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R/m]  | Save the current state of a dataset. Use ``-u/--updated``|
   |   **save**   |               | to leave untracked files untouched, and ``--to-git`` to  |
   |              |               | save modifications to Git instead of Git-annex.          |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad save [-u/--updated] [PATH]``                                                   |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R]    | Update a dataset from a sibling. Updates are by default  |
   |  **update**  |               | on branch ``remotes/origin/master``. Changes can be      |
   |              |               | merged with ``--merge``. Without ``-s/--sibling``, all   |
   |              |               | siblings are updated.                                    |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad update [-s <sibling-name>] [--merge]``                                         |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R]    | Drop file content from dataset (remove data, retain      |
   |  **drop**    |               | symlink). Availability of at least one remote copy needs |
   |              |               | to be verified - disable with ``--nocheck``              |
   |              |               | Drops all contents if no PATH is given.                  |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad drop [--nocheck] [PATH]``                                                      |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R]    | Uninstall subdatasets. Availability of at least one      |
   |**uninstall** |               | remote copy needs to be verified - disable with          |
   |              |               | ``--nocheck``. PATH can not be the current directory.    |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad uninstall [--nocheck] PATH``                                                   |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R/m]  | Remove datasets + contents completely, and unregister    |
   |  **remove**  |               | from potential top-level datasets. Availability of at    |
   |              |               | least one remote copy needs to be verified - disable with|
   |              |               | ``--nocheck``. PATH can not be the current directory.    |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad drop [--nocheck] [PATH]``                                                      |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/r/R]    | Unlock file(s) of a dataset to enable editing their      |
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
   | Command      |General flags  |    Description                                           |
   +==============+===============+==========================================================+
   |              |  [h/d/m]      | Run an arbitrary shell command and record its impact on  |
   |  **run**     |               | a dataset. Only makes a record if the command modifies   |
   |              |               | the dataset. ``-i/--input`` is retrieved with ``get`` and|
   |              |               | ``-o/--output`` is unlocked, is necessary. Requires clean|
   |              |               | dataset status or ``--explicit`` flag.                   |
   +--------------+---------------+----------------------------------------------------------+
   | ``datalad run [--input <"input path">][--output <"output path">][--explicit] command``  |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/m]      | Re-execute a previous ``run`` command identified by its  |
   |  **rerun**   |               | hash, and save resulting modifications.                  |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad rerun [-s/--since <hash>][-o/--onto <hash>] HASH``                             |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d]        | Run prepared procedures (DataLad scripts) on a dataset.  |
   |**run-**      |               | To find available procedures, use ``--discover`` as the  |
   |**procedure** |               | only argument, else specify the name of the procedure.   |
   |              |               |                                                          |
   +--------------+---------------+----------------------------------------------------------+
   |    ``datalad run-procedure NAME [--discover]``                                          |
   +--------------+---------------+----------------------------------------------------------+

Miscellaneous commands
""""""""""""""""""""""

   +--------------+---------------+----------------------------------------------------------+
   | Command      |General flags  |    Description                                           |
   +==============+===============+==========================================================+
   |              |  [h/d/m]      | Download content from a URL. Specify a path to save the  |
   |**download-** |               | download with ``-O/--path``. If the target exists,       |
   |**url**       |               | ``-o/--overwrite`` will enable overwriting it.           |
   +--------------+---------------+----------------------------------------------------------+
   |``datalad download-url <url> [-o <path>][--overwrite]``                                  |
   +--------------+---------------+----------------------------------------------------------+
   |              |  [h/d/]       | Generate a report about the DataLad installation and     |
   |**wtf**       |               | configuration. Sharing this report with untrusted parties|
   |              |               | (e.g. on the web) should be done with care, as it may    |
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

TODO: table of DataLad core's extensions

- procedures

TODO: cross reference to the chapters
