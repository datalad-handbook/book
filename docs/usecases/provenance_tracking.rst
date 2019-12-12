.. _usecase_provenance_tracking:

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
he does not remember where he got the input data from, nor the exact steps to
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

.. runrecord:: _examples/prov-101
   :workdir: usecases/provenance
   :language: console

   $ datalad create artproject && cd artproject

For his art project, Rob decides to download a mosaic image composed of flowers
from Wikimedia. As a first step, he extracts some of the flowers into individual
files to reuse them later.
He uses the :command:`datalad download-url` command to get the resource straight
from the web, but also capture all provenance automatically, and save the
resource in his dataset together with a useful commit message:

.. runrecord:: _examples/prov-102
   :workdir: usecases/provenance/artproject
   :language: console

   $ mkdir sources
   $ datalad download-url -m "Added flower mosaic from wikimedia" \
     https://upload.wikimedia.org/wikipedia/commons/a/a5/Flower_poster_2.jpg \
     --path sources/flowers.jpg

If he later wants to find out where he obtained this file from, a
:command:`git annex whereis` [#f1]_ command will tell him:

.. runrecord:: _examples/prov-103
   :workdir: usecases/provenance/artproject
   :language: console

   $ git annex whereis sources/flowers.jpg

To extract some image parts for the first step of his project, he uses
the ``extract`` tool from `ImageMagick <https://imagemagick.org/index.php>`_ to
extract the St. Bernard's Lily from the upper left corner, and the pimpernel
from the upper right corner. The commands will take the
Wikimedia poster as an input and produce output files from it. To capture
provenance on this action, Rob wraps it into :command:`datalad run` [#f2]_
commands.

.. runrecord:: _examples/prov-104
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad run -m "extract st-bernard lily" \
    --input "sources/flowers.jpg" \
    --output "st-bernard.jpg" \
    "convert -extract 1522x1522+0+0 sources/flowers.jpg st-bernard.jpg"

.. runrecord:: _examples/prov-105
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad run -m "extract pimpernel" \
     --input "sources/flowers.jpg" \
     --output "pimpernel.jpg" \
     "convert -extract 1522x1522+1470+1470 sources/flowers.jpg pimpernel.jpg"

He continues to process the images, capturing all provenance with DataLad.
Later, he can always find out which commands produced or changed which file.
This information is easily accessible within the history of his dataset,
both with Git and DataLad commands such as :command:`git log` or
:command:`datalad diff`.

.. runrecord:: _examples/prov-106
   :workdir: usecases/provenance/artproject
   :language: console

   $ git log --oneline HEAD~3..HEAD

.. runrecord:: _examples/prov-107
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad diff -f HEAD~3

Based on this information, he can always reconstruct how an when
any data file came to be – across the entire life-time of a project.

He decides that one image manipulation for his art project will
be to displace pixels of an image by a random amount to blur the image:

.. runrecord:: _examples/prov-108
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad run -m "blur image" \
      --input "st-bernard.jpg" \
      --output "st-bernard-displaced.jpg" \
      "convert -spread 10 st-bernard.jpg st-bernard-displaced.jpg"

Because he is not completely satisfied with the first random pixel displacement,
he decides to retry the operation. Because everything was wrapped in :command:`datalad run`,
he can rerun the command. Rerunning the command will produce a commit, because the displacement is
random and the output file changes slightly from its previous version.

.. runrecord:: _examples/prov-109
   :workdir: usecases/provenance/artproject
   :language: console

   $ git log -1 --oneline HEAD

.. runrecord:: _examples/prov-110
   :workdir: usecases/provenance/artproject
   :language: console
   :realcommand: echo "$ datalad rerun $(git rev-parse HEAD)" && datalad rerun $(git rev-parse HEAD)

This blur also does not yet fulfill Robs expectations, so he decides to
discard the change, using standard Git tools [#f3]_.

.. runrecord:: _examples/prov-111
   :workdir: usecases/provenance/artproject
   :language: console

   $ git reset --hard HEAD~1

He knows that within a DataLad dataset, he can also rerun *a range*
of commands with the ``--since``  flag, and even specify alternative
starting points for rerunning them with the ``--onto`` flag. Every
command from commits reachable from the specified checksum until
``--since`` (but not including ``--since``) will be re-executed.
For example, ``datalad rerun --since=HEAD~5`` will re-execute any
commands in the last five commits.
``--onto`` indicates where to start rerunning the commands from.
The default is ``HEAD``, but anything other than HEAD will be
checked out prior to execution, such that re-execution happens in
a detached HEAD state, or checked out out on the new branch specified
by the ``--branch`` flag.
If ``--since`` is an empty string, it is set to rerun every command from the
first commit that contains a recorded command. If ``--onto`` is an empty
string, re-execution is performed on top to the parent of the first
run commit in the revision list specified with ``--since``.
When both arguments are set to empty strings, it therefore means
"rerun all commands with HEAD at the parent of the first commit a command".
In other words, Rob can "replay" all the history for his artproject in a single
command. Using the ``--branch`` option of :command:`datalad rerun`,
he does it on a new branch he names ``replay``:

.. runrecord:: _examples/prov-112
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad rerun --since= --onto= --branch=replay

Now he is on a new branch of his project, which contains "replayed" history.

.. runrecord:: _examples/prov-113
   :workdir: usecases/provenance/artproject
   :language: console

   $ git log --oneline --graph master replay

He can even compare the two branches:

.. runrecord:: _examples/prov-114
   :workdir: usecases/provenance/artproject
   :language: console

   $ datalad diff -t master -f replay

He can see that the blurring, which involved a random element,
produced different results. Because his dataset contains two branches,
he can compare the two branches using normal Git operations.
The next command, for example, marks which commits are "patch-equivalent"
between the branches.
Notice that all commits are marked as equivalent (=) except the ‘random spread’ ones.

.. runrecord:: _examples/prov-115
   :workdir: usecases/provenance/artproject
   :language: console

   $ git log --oneline --left-right --cherry-mark master...replay

Rob can continue processing images, and will turn in a sucessful art project.
Long after he finishes high school, he finds his dataset on his old computer
again and remembers this small project fondly.

.. rubric:: Footnotes


.. [#f1] If you want to learn more about :command:`git annex whereis`, re-read
         section :ref:`sharelocal2`.
.. [#f2] If you want to learn more about :command:`datalad run`, read on from
         section :ref:`run`.
.. [#f3] Find out more about working with the history of a dataset with Git in
         section :ref:`filesystem`
