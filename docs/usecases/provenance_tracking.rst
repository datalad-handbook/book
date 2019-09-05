.. _prov:

Basic provenance tracking
-------------------------

This use case demonstrates how the provenance of downloaded and generated files
can be captured with DataLad by

#. downloading a data file from an arbitrary URL from the web
#. perform changes to this data file and
#. capture provenance for all of this

.. note::

   This section uses advanced Git commands and concepts on the side
   that are not covered in the book. If you want to learn more about
   the Git commands shown here, the `ProGit book <https://git-scm.com/book/en/v2>`_
   is an excellent resource.

The Challenge
^^^^^^^^^^^^^

Rob needs to turn in an art project at the end of the high school year.
He wants to make it as easy as possible and decides to just make a
photomontage of some pictures from the internet. When he submits the project,
he doesn't remember where he got the input data from, nor the exact steps to
create his project, even though he tried to take notes.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Rob starts his art project as a DataLad dataset. When downloading the
images he wants to use for his project, he tracks where they come from.
And when he changes or creates output, he tracks how, when and why and
this was done using standard DataLad commands.
This will make it easy for him to find out or remember what he has
done in his project, and how it has been done, a long time after he
finished the project, without any note taking.

Step-by-Step
^^^^^^^^^^^^

Rob starts by creating a dataset, because everything in a dataset can
be version controlled and tracked:

.. code-block:: bash

   $ datalad create artproject

     [INFO   ] Creating a new annex repo at /home/rob/artproject
     create(ok): /home/rob/artproject (dataset)
   $ cd artproject

For his art project, Rob decides to download a mosaic image composed of flowers
from Wikimedia. As a first step, he extracts some of the flowers into individual
files to reuse them later.
He uses the :command:`datalad download-url` command to get the resource straight
from the web, but also capture all provenance automatically, and save the
resource in his dataset together with a useful commit message:

.. code-block:: bash

    $ mkdir sources
    $ datalad download-url -m "Added flower mosaic from wikimedia" \
      https://upload.wikimedia.org/wikipedia/commons/a/a5/Flower_poster_2.jpg \
      --path sources/flowers.jpg

      [INFO   ] Downloading 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Flower_poster_2.jpg' into 'sources/flowers.jpg'
      download_url(ok): sources/flowers.jpg (file)
      add(ok): sources/flowers.jpg (file)
      save(ok): . (dataset)
      action summary:
        add (ok: 1)
        download_url (ok: 1)
        save (ok: 1)


If he later wants to find out where he obtained this file from, a
:command:`git annex whereis` [#f1]_ command will tell him:

.. code-block:: bash

   $ git annex whereis sources/flowers.jpg
    whereis flowers.jpg (2 copies)
        00000000-0000-0000-0000-000000000001 -- web
        48ef1b37-f798-470b-9f59-ee9ea92ffa12 -- rob@mylaptop:/home/rob/artproject [here]

      web: https://upload.wikimedia.org/wikipedia/commons/a/a5/Flower_poster_2.jpg
    ok

To extract some image parts for the first step of his project, he uses
the ``extract`` tool from `ImageMagick <https://imagemagick.org/index.php>`_ to
extract the St. Bernard's Lily from the upper left corner, and the pimpernel
from the upper right corner. The commands will take the
Wikimedia poster as an input and produce output files from it. To capture
provenance on this action, Rob wraps it into :command:`datalad run` [#f2]_
commands.

.. code-block:: bash

   $ datalad run -m "extract st-bernard lily" \
    --input "sources/flowers.jpg" \
    --output "st-bernard.jpg" \
    "convert -extract 1522x1522+0+0 sources/flowers.jpg st-bernard.jpg"

    [INFO   ] Making sure inputs are available (this may take some time)
    [INFO   ] == Command start (output follows) =====
    [INFO   ] == Command exit (modification check follows) =====
    add(ok): st-bernard.jpg (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 1)
      get (notneeded: 1)
      save (ok: 1)

.. code-block:: bash

    $ datalad run -m "extract pimpernel" \
     --input "sources/flowers.jpg" \
     --output "pimpernel.jpg" \
     convert -extract 1522x1522+1470+1470 sources/flowers.jpg pimpernel.jpg

     [INFO   ] Making sure inputs are available (this may take some time)
     [INFO   ] == Command start (output follows) =====
     [INFO   ] == Command exit (modification check follows) =====
     add(ok): pimpernel.jpg (file)
     save(ok): /demo/demo (dataset)
     action summary:
       add (ok: 1)
       get (notneeded: 1)
       save (ok: 1)

He continues to process the images, capturing all provenance with DataLad.
Later, he can always find out which commands produced or changed which file.
This information is easily accessible within the history of his dataset,
both with Git and DataLad commands such as :command:`git log` or
:command:`datalad diff`.

.. code-block:: bash

    $ git log --oneline @~3..@
     73832b3 (HEAD -> master) [DATALAD RUNCMD] extract pimpernel
     cce0c79 [DATALAD RUNCMD] extract st-bernard lily
     8a21b21 Added flower mosaic from wikimedia

    $ datalad diff -f HEAD~3
        added: pimpernel.jpg (file)
        added: sources/flowers.jpg (file)
        added: st-bernard.jpg (file)

Based on this information, he can always reconstruct how an when
any data file came to be – across the entire life-time of a project.

He decides that one image manipulation for his art project will
be to displace pixels of an image by a random amount to blur the image:

.. code-block:: bash

    $ datalad run -m "blur image" \
      --input "st-bernard.jpg" \
      --output "st-bernard-displaced.jpg" \
      "convert -spread 10 st-bernard.jpg st-bernard-displaced.jpg"

      [INFO   ] Making sure inputs are available (this may take some time)
      [INFO   ] == Command start (output follows) =====
      [INFO   ] == Command exit (modification check follows) =====
         add(ok): st-bernard-displaced.jpg (file)
         save(ok): /demo/demo (dataset)
         action summary:
           add (ok: 1)
           get (notneeded: 1)
           save (ok: 1)

Because he is not completely satisfied with the first random pixel displacement,
he decides to retry the operation. Because everything was wrapped in :command:`datalad run`,
he can rerun the command. The command will produce a commit, because the displacement is
random and the output file changes slightly from its previous version.


.. code-block:: bash

   $ git log -1 --oneline HEAD
     643c175 (HEAD -> master) [DATALAD RUNCMD] blur image
   # rerun with the commit hash:
   $ datalad rerun 643c175

   [INFO   ] Making sure inputs are available (this may take some time)
   unlock(ok): st-bernard-displaced.jpg (file)
   [INFO   ] == Command start (output follows) =====
   [INFO   ] == Command exit (modification check follows) =====
   add(ok): st-bernard-displaced.jpg (file)
   save(ok): . (dataset)
   action summary:
     add (ok: 1)
     get (notneeded: 1)
     save (ok: 1)
     unlock (ok: 1)

This blur also does not yet fulfill Robs expectations, so he decides to
discard the change, using standard Git tools [#f3]_.

.. code-block:: bash

   $ git reset --hard HEAD~1
     HEAD is not at 643c175 [DATALAD RUNCMD] blur image

He knows that within a DataLad dataset, he can also rerun multiple commands
with ``--since``  and ``--onto`` to specify where to start rerunning from and
up to which point.
When both arguments are set to empty strings, it means
"rerun all commands with HEAD at the parent of the first commit a command".
In other words, he can "replay" all the history for his artproject in a single
command. Using the ``--branch`` option of :command:`datalad rerun`,
he does it on a new branch he names ``replay``:

.. code-block:: bash

   $ datalad rerun --since= --onto= --branch=replay

    [INFO   ] Making sure inputs are available (this may take some time)
    [INFO   ] == Command start (output follows) =====
    [INFO   ] == Command exit (modification check follows) =====
    add(ok): st-bernard.jpg (file)
    save(ok): . (dataset)
    [INFO   ] Making sure inputs are available (this may take some time)
    [INFO   ] == Command start (output follows) =====
    [INFO   ] == Command exit (modification check follows) =====
    add(ok): pimpernel.jpg (file)
    save(ok): . (dataset)
    [INFO   ] Making sure inputs are available (this may take some time)
    [INFO   ] == Command start (output follows) =====
    [INFO   ] == Command exit (modification check follows) =====
    add(ok): st-bernard-displaced.jpg (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 3)
      get (notneeded: 3)
      save (ok: 3)

Now he is on a new branch of his project, which contains "replayed" history.

.. code-block:: bash

   $ git log --oneline --graph master replay

    * d4f7e3f (HEAD -> verify) [DATALAD RUNCMD] blur image
    * d125c7a [DATALAD RUNCMD] extract pimpernel
    * 9391ccb [DATALAD RUNCMD] extract st-bernard lily
    | * d16bf05 (master) [DATALAD RUNCMD] blur image
    | * 643c175 [DATALAD RUNCMD] extract pimpernel
    | * 53cb5dc [DATALAD RUNCMD] extract st-bernard lily
    |/
    * 0e2a0e6 Added flower mosaic from wikimedia
    * 5881108 [DATALAD] new dataset

He can even compare the two branches:

.. code-block:: bash

   $ datalad diff -t master -f replay
     modified: st-bernard-displaced.jpg (file)

He can see that the blurring, which involved a random element,
produced different results. Because his dataset contains two branches,
he can compare the two branches using normal Git operations.
The next command, for example, marks which commits are "patch-equivalent"
between the branches.
Notice that all commits are marked as equivalent (=) except the ‘random spread’ ones.

.. code-block:: bash

   $ git log --oneline --left-right --cherry-mark master...replay

    > d4f7e3f (HEAD -> verify) [DATALAD RUNCMD] blur image
    = d125c7a [DATALAD RUNCMD] extract pimpernel
    = 9391ccb [DATALAD RUNCMD] extract st-bernard lily
    < d16bf05 (master) [DATALAD RUNCMD] blur image
    = 643c175 [DATALAD RUNCMD] extract pimpernel
    = 53cb5dc [DATALAD RUNCMD] extract st-bernard lily

Rob can continue processing images, and will turn in a sucessful art project.
Long after he finishes high school, he finds his dataset on his old computer
again and remembers this small project fondly.

.. rubric:: Footnotes


.. [#f1] If you want to learn more about :command:`git annex whereis`, re-read
         section :ref:`sharelocal2`.
.. [#f2] If you want to learn more about :command:`datalad run`, read on from
         section :ref:`run`.
.. [#f3] Find out more about working with the history of a dataset with Git in
         section <yettolink>