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

.. runrecord::
   :language: console
   :exitcode:1
   :workdir: basics/shell

   $ datalad clone https://github.com/datalad/testrepo--basic--r1
   [INFO   ] Remote origin not usable by git-annex; setting annex-ignore
   [INFO   ] https://github.com/datalad/testrepo--basic--r1/config download failed: Not Found
   install(ok): /tmp/testrepo--basic--r1 (dataset)
   $ cd testrepo--basic--r1/
   $ datalad get .
   get(ok): test-annex.dat (file) [from web...]
   $ cd ..
   $ rm -rf testrepo--basic--r1/
   rm: cannot remove 'testrepo--basic--r1/.git/annex/objects/zk/71/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat': Permission denied

Solution
^^^^^^^^

This can be mitigated by manually changing permissions:

.. runrecord::
   :language: console
   :exitcode:0
   :workdir: basics/shell

   $ chmod -R 775 testrepo--basic--r1/
   $ rm -rf testrepo--basic--r1/

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


Pattern search via ``grep`` alternatives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Problem
^^^^^^^

While ``grep -R`` follows symlinks by default, the original GNU implementation is often too slow for power-users.
Faster alternative implementations commonly do not follow symlinks, by default, or at all.

.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ git grep -r 123 | cat
   test.dat:123
   [deco]/mnt/data/testrepo--basic--r1 ❱ ag 123
   test.dat
   1:123
   [deco]/mnt/data/testrepo--basic--r1 ❱ rg 123
   test.dat
   1:123
   [deco]/mnt/data/testrepo--basic--r1 ❱ ack 123
   test.dat
   1:123

Solution
^^^^^^^^

Thankfully, most of these implementations provide an optional flag which enables symlink support.
Thus users should be advised to always remember using these flags when dealing with DataLad repositories, or to set them globally via an alias.
Notably, however, ``git grep`` `does not support symlinks <https://git.vger.kernel.narkive.com/q1CpMpoI/grep-doesn-t-follow-symbolic-link>`_, meaning that this command cannot reliably be used with DataLad datasets.

.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ ag -f 123
   test.dat
   1:123

   test-annex.dat
   1:123
   [deco]/mnt/data/testrepo--basic--r1 ❱ rg -L 123
   test.dat
   1:123

   test-annex.dat
   1:123
   [deco]/mnt/data/testrepo--basic--r1 ❱ ack --follow 123
   test-annex.dat
   1:123

   test.dat
   1:123


Creating archives via ``tar``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Problem
^^^^^^^

When creating archives with ``tar`` symlinks are by default stored as symlinks.
This will break if individual files or subdirectories of a datalad repository are archived:

.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ tar cJf mytest.tar.xz test-annex.dat
   [deco]/mnt/data/testrepo--basic--r1 ❱ mv mytest.tar.xz /tmp/
   [deco]/mnt/data/testrepo--basic--r1 ❱ cd /tmp
   [deco]/tmp ❱ tar xvf mytest.tar.xz
   test-annex.dat
   [deco]/tmp ❱ ls -lah test-annex.dat
   lrwxrwxrwx 1 chymera chymera 186 May 31 16:01 test-annex.dat -> .git/annex/objects/zk/71/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat/SHA256E-s4--181210f8f9c779c26da1d9b2075bde0127302ee0e3fca38c9a83f5b1dd8e5d3b.dat


Solution
^^^^^^^^

This can be solved by explicitly instructing ``tar`` to follow symlinks via its ``-h, --dereference`` option, e.g.:


.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ tar -hcJf mytest.tar.xz test-annex.dat
   [deco]/mnt/data/testrepo--basic--r1 ❱ mv mytest.tar.xz /tmp/
   [deco]/mnt/data/testrepo--basic--r1 ❱ cd /tmp
   [deco]/tmp ❱ tar xvf mytest.tar.xz
   test-annex.dat
   [deco]/tmp ❱ ls -lah test-annex.dat
   -r--r--r-- 1 chymera chymera 4 May 31 16:01 test-annex.dat


Reporting file/directory size via `du`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Problem
^^^^^^^

The ``du`` command will also not follow symlinks by default:

.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ head -c 1M </dev/urandom >myfile
   [deco]/mnt/data/testrepo--basic--r1 ❱ du -s myfile
   1024	myfile
   [deco]/mnt/data/testrepo--basic--r1 ❱ datalad save myfile
   add(ok): myfile (file)
   save(ok): . (dataset)
   action summary:
     add (ok: 1)
     save (ok: 1)
   [deco]/mnt/data/testrepo--basic--r1 ❱ du -s myfile
   4	myfile


Solution
^^^^^^^^

This can again be compensated for by explicitly instructing the command to follow symlinks:

.. code-block::

   [deco]/mnt/data/testrepo--basic--r1 ❱ du -sL myfile
   1024	myfile
