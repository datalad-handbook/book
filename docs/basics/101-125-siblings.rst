Collaboration [1]
-----------------

To get a hang on the basics of sharing a dataset,
you shared your ``DataLad-101`` dataset with your
room mate on a common, local file system. Your lucky
room mate now has your notes and can thus try to catch
up to still pass the course.
Moreover, though, he can also integrate all other notes
or changes you make to your dataset, and stay up to date.
This is because a DataLad dataset makes updating shared
data a matter of a single ``datalad update --merge`` command.

But why does this need to be a one-way line? "I want to
provide helpful information for you as well!", says your
room mate. "How could you get any insightful notes that
I make in my dataset, or maybe the results of our upcoming
mid-term project? Its a bit unfair that I can get your work,
but you can't get mine."

For example, your room mate might have googled about DataLad
a bit. On the `datalad homepage <https://www.datalad.org/>`_
he might have found very useful additional information, such
as the ascii-cast on `dataset nesting <https://www.datalad.org/for/git-users>`_.
Because he found this very helpful in understanding dataset
nesting concepts, he decided to download the ``shell`` script
that was used to generate this example from Github, and saves
it in the ``code/`` directory.
He also does it using the datalad command ``datalad download-url``
for it, that can take a commit message and will save the download
right to the history!

Navigate into your dataset copy in ``mock_user/DataLad-101``,
and run the following command

.. runrecord:: _examples/DL-101-125-101
   :language: console
   :workdir: dl-101/DataLad-101

   # navigate into the installed copy
   $ cd ../mock_user/DataLad-101

   # download the shell script and save it in your code/ directory
   $ datalad download-url \
     -m "Include nesting demo from datalad website" \
     -O code/nested_repos.sh \
     https://raw.githubusercontent.com/datalad/datalad.org/7e8e39b1f08d0a54ab521586f27ee918b4441d69/content/asciicast/seamless_nested_repos.sh

Run a quick datalad status:

.. runrecord:: _examples/DL-101-125-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad status

Nice, the ``datalad download-url`` command saved this download
right into the history! We'll show an excerpt of the last commit
here:

.. runrecord:: _examples/DL-101-125-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :lines: 1-30

   $ git log -1 -p

Suddenly, your room mate has a file change that you do not have.
His dataset evolved.

So how do we link back from the copy of the dataset to its
origin, such that your room mates changes can be included in
your dataset? How to we let the original dataset "know" about
this copy your room mate has?
Do we need to install the installed dataset of our room mate
as a copy again?

No, luckily, it's simpler and less convoluted. What we have to
do is to *register* a datalad ``sibling``: A reference to our room mates
dataset in our own, original dataset.

.. gitusernote::

   Git repositories can configure clones of a dataset as *remotes* in
   order to fetch, pull, or push from and to them. A ``datalad sibling``
   is the equivalent of a git clone that is configured as a remote.

Let's see how this is done.

First of all, navigate back into the original dataset.
In the original dataset, "add" a "sibling" by using
the ``datalad siblings`` command. The command takes the base command,
``datalad siblings``, an action, in this case ``add``, a path to the
root of the dataset ``-d .``, a name for the sibling, ``-s/--name roommate``,
and a URL or path to the sibling, ``--url ../mock_user/DataLad-101``.
This registers your roommates ``DataLad-101`` as a "sibling" (we will call it
"roommate") to your own ``DataLad-101`` dataset.


.. runrecord:: _examples/DL-101-125-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ cd ../../DataLad-101
   # add a sibling
   $ datalad siblings add -d . --name roommate --url ../mock_user/DataLad-101

There are a few confusing parts about this command: For one, don't be surprised
about the ``--url`` argument -- it's called "URL" but it can be a path as well.
Also, don't forget to give a name to your datasets sibling. Without the ``-s``/
``--name`` argument the command will fail. The reason behind this is that the default
name of a sibling if no name is given will be the hostname of the specified URL,
but as you provide a path and not a URL, there is no hostname to take as a default.

As you can see in the command output, the addition of a sibling succeeded:
``roommate(+)[../mock_user/DataLad-101]`` means that your room mates dataset
is now known to your own dataset as "roommate"


.. runrecord:: _examples/DL-101-125-105
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad siblings

This command will list all known siblings of the dataset. You can see it
in the resulting list with the name "roommate" you have given to it.

The fact that the ``DataLad-101`` dataset now has a sibling means that we
can also ``datalad update`` this repository. Awesome!

Your room mate previously ran a ``datalad update --merge``. This got him
changes he knew you made into a dataset that he so far did not change.
This meant that nothing unexpected would happen with the ``datalad update --merge``.

But consider the current case: Your room mate made changes to his
dataset, but you don't necessarily know which. Maybe you also made
changes to your dataset. How would you know that his changes and
your changes are not in conflict with each other?

This scenario is where a plain ``datalad update`` becomes useful.
If you run a plain ``datalad update``, DataLad will query the sibling
for changes, and store those changes in a safe place in your own
dataset, *but it will not yet integrate them into your dataset*.
This gives you a chance to see whether you actually want to have the
changes your room mate made.

Let's see how it's done. First, run a plain ``datalad update`` without
the ``--merge`` option.

.. runrecord:: _examples/DL-101-125-106
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad update -s roommate

Note that we supplied the siblings name with the ``-s``/``--name`` option.
This is good practice, and allows you to be precise in where you want to get
updates from. It would have worked without the specification (just as a bare
``datalad update --merge`` worked for your room mate), because there is only
one other known location, though.

.. container:: toggle

   .. container:: header

      **Addition: What if I mistyped the name or want to remove the sibling?**

   You can remove a sibling using ``datalad siblings remove -s roommate``


This plain ``datalad update`` informs you that it "fetched" updates from
the dataset. The changes however, are not yet visible:

.. runrecord:: _examples/DL-101-125-107
   :language: console
   :workdir: dl-101/DataLad-101

   $ ls code/

So where is the content? It is in a different *branch* of your dataset.
If you don't use :term:`Git`, the concept of a branch can be a big
source of confusion. There will be sections later in this book that will
elaborate a bit more what branches are, and how to work with them, but
for now envision a branch just like a bunch of drawers on your desk.
The paperwork that you have in front of you right on your desk is your
dataset as you currently see it.
These drawers instead hold documents that you are in principle working on,
just not now -- maybe different versions of paperwork you currently have in
front of you, or maybe other files than the ones currently in front of you
on your desk.

Imagine that a ``datalad update`` created a small drawer, placed all of
the changed or added files from the sibling inside, and put it on your
desk. You can now take a look into that drawer to see whether you want
to have the changes right in front of you.

The drawer is a branch, and it is usually called ``remotes/origin/master``.
To look inside of it you can ``git checkout BRANCHNAME``, or you can
do a ``diff`` between the branch (your drawer) and the dataset as it
is currently in front of you (your desk). We will do the latter, and leave
the former for a different lecture:

.. runrecord:: _examples/DL-101-125-108
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad diff --to remotes/roommate/master

This shows us that there is an additional file! Let's ask
git diff to show us what is inside:

.. runrecord:: _examples/DL-101-125-109
   :language: console
   :workdir: dl-101/DataLad-101

   $ git diff remotes/roommate/master

Cool! So now that you know what the changes are that your room mate
made, you can safely ``datalad update --merge`` them to integrate
them into your dataset. In technical terms you will
*merge the branch remotes/roommate/master into master*.
But the details of this will be stated in a standalone section later.

.. runrecord:: _examples/DL-101-125-110
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad update --merge -s roommate

The exciting question is now whether your room mates change is now
also part of your own dataset. Let's list the contents of the ``code/``
directory and also peek into the history:

.. runrecord:: _examples/DL-101-125-111
   :language: console
   :workdir: dl-101/DataLad-101

   $ ls code/

.. runrecord:: _examples/DL-101-125-112
   :language: console
   :lines: 1-6
   :emphasize-lines: 2-3
   :workdir: dl-101/DataLad-101

   $ git log --oneline

Wohoo! Here it is: The script now also exists in your own dataset.
You can see the commit that your room mate made when he saved the script,
and you can also see a commit that records how you ``merged`` your
roommates dataset changes into your own dataset. The commit message of this
latter commit for now might contain many words yet unknown to you if you
don't use Git, but a later section will get into the details of what
the meaning of "merge", "branch", "refs" or "master" is.

For now, you're happy to have the changes your room mate made available.
This is how it should be! You helped him, and he helps you. Awesome!
There actually is a wonderful word for it: *Collaboration*.
Thus, without noticing, you have successfully collaborated for the first
time using DataLad datasets.

Create a note about this, and save it.

.. runrecord:: _examples/DL-101-125-113
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT >> notes.txt
   To update from a dataset with a shared history, you
   need to add this dataset as a sibling to your dataset.
   "Adding a sibling" means providing DataLad with infos about
   the location of a dataset, and a name for it. Afterwards,
   a "datalad update --merge -s name" will integrate the changes
   made to the sibling into the dataset.
   A safe step in between is to do a "datalad update -s name"
   and checkout the changes with "git/datalad diff"
   to remotes/origin/master

   EOT
   $ datalad save -m "Add note on adding siblings" notes.txt