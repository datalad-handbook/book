.. _shell:

Using Common Shell Commands on DataLad Repositories
---------------------------------------------------

There are a number of gotchas when using common shell commands to manipulate DataLad Repositories.
This stems mostly due to the reliance of git-annex on symlinks, as well as due to permissions management under the ``.git`` directory.
Thus, the usage of common shell tools, including `GNU coreutils <https://www.gnu.org/software/coreutils/>`_, can often yield unintuitive results.
This is a list referencing such cases, providing instructions on how to mitigate them, as well as indicating alternative processes using datalad-specific commands, where such are feasible substitutes.

Removal via ``rm``
~~~~~~~~~~~~~~~~~~

Problem
^^^^^^^

Removing datalad repositories with ``rm`` will fail due to missing write permissions under ``.git/annex/objects/..``:

.. code-block::
   [deco]/tmp ❱ datalad clone https://github.com/datalad/testrepo--basic--r1
   [INFO   ] Remote origin not usable by git-annex; setting annex-ignore
   [INFO   ] https://github.com/datalad/testrepo--basic--r1/config download failed: Not Found
   install(ok): /tmp/testrepo--basic--r1 (dataset)
   [deco]/tmp ❱ cd testrepo--basic--r1/
   [deco]/tmp/testrepo--basic--r1 ❱ datalad get .
   get(ok): test-annex.dat (file) [from web...]
   [deco]/tmp/testrepo--basic--r1 ❱ cd ..
   [deco]/tmp ❱ rm -rf testrepo--basic--r1/
   rm: cannot remove 'testrepo--basic--r1/.git/annex/objects/zk/71/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat': Permission denied

Solution
^^^^^^^^

This can be mitigated by manually changing permissions:

.. code-block::
   [deco]/tmp ❱ chmod -R 775 testrepo--basic--r1/
   [deco]/tmp ❱ rm -rf testrepo--basic--r1/

Alternative
^^^^^^^^^^^

DataLad provides its own command to substitute for ``rm`` functionality:

.. code-block::
   [deco]/tmp ❱ datalad remove -d testrepo--basic--r1/
   drop(ok): . (key)
   uninstall(ok): . (dataset)
   action summary:
     drop (ok: 1)
     uninstall (ok: 1)

