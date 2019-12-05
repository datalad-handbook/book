.. _sibling:

Networking
----------

To get a hang on the basics of sharing a dataset,
you shared your ``DataLad-101`` dataset with your
room mate on a common, local file system. Your lucky
room mate now has your notes and can thus try to catch
up to still pass the course.
Moreover, though, he can also integrate all other notes
or changes you make to your dataset, and stay up to date.
This is because a DataLad dataset makes updating shared
data a matter of a single :command:`datalad update --merge` command.

But why does this need to be a one-way line? "I want to
provide helpful information for you as well!", says your
room mate. "How could you get any insightful notes that
I make in my dataset, or maybe the results of our upcoming
mid-term project? Its a bit unfair that I can get your work,
but you can not get mine."

Consider, for example, that your room mate might have googled about DataLad
a bit. On the `datalad homepage <https://www.datalad.org/>`_
he might have found very useful additional information, such
as the ascii-cast on `dataset nesting <https://www.datalad.org/for/git-users>`_.
Because he found this very helpful in understanding dataset
nesting concepts, he decided to download the ``shell`` script
that was `used to generate this example <https://raw.githubusercontent.com/datalad/datalad.org/7e8e39b1f08d0a54ab521586f27ee918b4441d69/content/asciicast/seamless_nested_repos.sh>`_
from GitHub, and saves it in the ``code/`` directory.

He does it using the datalad command :command:`datalad download-url`
that you experienced in section :ref:`createDS` already: This command will
download a file just as ``wget``, but it can also take a commit message
and will save the download right to the history of the dataset that you specify!

Navigate into your dataset copy in ``mock_user/DataLad-101``,
and run the following command

.. runrecord:: _examples/DL-101-121-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: Let's make changes in the copy of the original ds
   :cast: 04_collaboration

   # navigate into the installed copy
   $ cd ../mock_user/DataLad-101

   # download the shell script and save it in your code/ directory
   $ datalad download-url \
     -d . \
     -m "Include nesting demo from datalad website" \
     -O code/nested_repos.sh \
     https://raw.githubusercontent.com/datalad/datalad.org/7e8e39b1f08d0a54ab521586f27ee918b4441d69/content/asciicast/seamless_nested_repos.sh

Run a quick datalad status:

.. runrecord:: _examples/DL-101-121-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: the download url command takes care of saving contents for you
   :cast: 04_collaboration

   $ datalad status

Nice, the :command:`datalad download-url` command saved this download
right into the history, and :command:`datalad status` does not report
unsaved modifications! We'll show an excerpt of the last commit
here:

.. runrecord:: _examples/DL-101-121-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :lines: 1-30
   :notes: the ds copy has a change the original ds does not have:
   :cast: 04_collaboration

   $ git log -n 1 -p

Suddenly, your room mate has a file change that you do not have.
His dataset evolved.

So how do we link back from the copy of the dataset to its
origin, such that your room mate's changes can be included in
your dataset? How do we let the original dataset "know" about
this copy your room mate has?
Do we need to install the installed dataset of our room mate
as a copy again?

No, luckily, it's simpler and less convoluted. What we have to
do is to *register* a datalad :term:`sibling`: A reference to our room mate's
dataset in our own, original dataset.

.. gitusernote::

   Git repositories can configure clones of a dataset as *remotes* in
   order to fetch, pull, or push from and to them. A :command:`datalad sibling`
   is the equivalent of a git clone that is configured as a remote.

Let's see how this is done.

.. index:: ! datalad command; siblings

First of all, navigate back into the original dataset.
In the original dataset, "add" a "sibling" by using
the :command:`datalad siblings` command (:manpage:`datalad-siblings` manual).
The command takes the base command,
:command:`datalad siblings`, an action, in this case ``add``, a path to the
root of the dataset ``-d .``, a name for the sibling, ``-s/--name roommate``,
and a URL or path to the sibling, ``--url ../mock_user/DataLad-101``.
This registers your room mate's ``DataLad-101`` as a "sibling" (we will call it
"roommate") to your own ``DataLad-101`` dataset.


.. runrecord:: _examples/DL-101-121-104
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :notes: To allow updates from copy to original we have to configure the copy as a sibling of the original
   :cast: 04_collaboration

   $ cd ../../DataLad-101
   # add a sibling
   $ datalad siblings add -d . --name roommate --url ../mock_user/DataLad-101

There are a few confusing parts about this command: For one, do not be surprised
about the ``--url`` argument -- it's called "URL" but it can be a path as well.
Also, do not forget to give a name to your dataset's sibling. Without the ``-s``/
``--name`` argument the command will fail. The reason behind this is that the default
name of a sibling if no name is given will be the host name of the specified URL,
but as you provide a path and not a URL, there is no host name to take as a default.

.. todo::

   remove this once https://github.com/datalad/datalad/issues/3553 is fixed

As you can see in the command output, the addition of a sibling succeeded:
``roommate(+)[../mock_user/DataLad-101]`` means that your room mate's dataset
is now known to your own dataset as "roommate"


.. runrecord:: _examples/DL-101-121-105
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: we can check which siblings the dataset has
   :cast: 04_collaboration

   $ datalad siblings

This command will list all known siblings of the dataset. You can see it
in the resulting list with the name "roommate" you have given to it.

.. findoutmore:: What if I mistyped the name or want to remove the sibling?

   You can remove a sibling using :command:`datalad siblings remove -s roommate`

The fact that the ``DataLad-101`` dataset now has a sibling means that we
can also :command:`datalad update` this repository. Awesome!

Your room mate previously ran a :command:`datalad update --merge` in the section
:ref:`update`. This got him
changes *he knew you made* into a dataset that *he so far did not change*.
This meant that nothing unexpected would happen with the
:command:`datalad update --merge`.

But consider the current case: Your room mate made changes to his
dataset, but you do not necessarily know which. You also made
changes to your dataset in the meantime, and added a note on
:command:`datalad update`.
How would you know that his changes and
your changes are not in conflict with each other?

This scenario is where a plain :command:`datalad update` becomes useful.
If you run a plain :command:`datalad update`, DataLad will query the sibling
for changes, and store those changes in a safe place in your own
dataset, *but it will not yet integrate them into your dataset*.
This gives you a chance to see whether you actually want to have the
changes your room mate made.

Let's see how it's done. First, run a plain :command:`datalad update` without
the ``--merge`` option.

.. runrecord:: _examples/DL-101-121-106
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: now we can update. Problem: how do we know whether we want the changes? --> plain datalad update
   :cast: 04_collaboration

   $ datalad update -s roommate

Note that we supplied the siblings name with the ``-s``/``--name`` option.
This is good practice, and allows you to be precise in where you want to get
updates from. It would have worked without the specification (just as a bare
:command:`datalad update --merge` worked for your room mate), because there is only
one other known location, though.

This plain :command:`datalad update` informs you that it "fetched" updates from
the dataset. The changes however, are not yet visible -- the script that
he added is not yet in your ``code/`` directory:

.. runrecord:: _examples/DL-101-121-107
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: no file changes there yet, but where are they?
   :cast: 04_collaboration

   $ ls code/

So where is the file? It is in a different *branch* of your dataset.

If you do not use :term:`Git`, the concept of a :term:`branch` can be a big
source of confusion. There will be sections later in this book that will
elaborate a bit more what branches are, and how to work with them, but
for now envision a branch just like a bunch of drawers on your desk.
The paperwork that you have in front of you right on your desk is your
dataset as you currently see it.
These drawers instead hold documents that you are in principle working on,
just not now -- maybe different versions of paperwork you currently have in
front of you, or maybe other files than the ones currently in front of you
on your desk.

Imagine that a :command:`datalad update` created a small drawer, placed all of
the changed or added files from the sibling inside, and put it on your
desk. You can now take a look into that drawer to see whether you want
to have the changes right in front of you.

The drawer is a branch, and it is usually called ``remotes/origin/master``.
To look inside of it you can :command:`git checkout BRANCHNAME`, or you can
do a ``diff`` between the branch (your drawer) and the dataset as it
is currently in front of you (your desk). We will do the latter, and leave
the former for a different lecture:

.. runrecord:: _examples/DL-101-121-108
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: on a different branch: remotes/roommate/master. Do a git remote -v here
   :cast: 04_collaboration

   $ datalad diff --to remotes/roommate/master

This shows us that there is an additional file, and it also shows us
that there is a difference in ``notes.txt``! Let's ask
:command:`git diff` to show us what the differences in detail:

.. runrecord:: _examples/DL-101-121-109
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: also git diff
   :cast: 04_collaboration

   $ git diff remotes/roommate/master

Let's digress into what is shown here.
We are comparing the current state of your dataset against
the current state of your room mate's dataset. Everything marked with
a ``-`` is a change that your room mate has, but not you: This is the
script that he downloaded!

Everything that is marked with a ``+`` is a change that you have,
but not your room mate: It is the additional note on :command:`datalad update`
you made in your own dataset in the previous section.

Cool! So now that you know what the changes are that your room mate
made, you can safely :command:`datalad update --merge` them to integrate
them into your dataset. In technical terms you will
"*merge the branch remotes/roommate/master into master*".
But the details of this will be stated in a standalone section later.

Note that the fact that your room mate does not have the note
on :command:`datalad update` does not influence your note. It will not
get deleted by the merge. You do not set your dataset to the state
of your room mate's dataset, but you incorporate all changes he made
-- which is only the addition of the script.

.. runrecord:: _examples/DL-101-121-110
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: no we can safely merge
   :cast: 04_collaboration

   $ datalad update --merge -s roommate

The exciting question is now whether your room mate's change is now
also part of your own dataset. Let's list the contents of the ``code/``
directory and also peek into the history:

.. runrecord:: _examples/DL-101-121-111
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: check for the updated files... they are there!
   :cast: 04_collaboration

   $ ls code/

.. runrecord:: _examples/DL-101-121-112
   :language: console
   :lines: 1-6
   :emphasize-lines: 2, 4
   :workdir: dl-101/DataLad-101
   :notes: and here is the summary in the log
   :cast: 04_collaboration

   $ git log --oneline

Wohoo! Here it is: The script now also exists in your own dataset.
You can see the commit that your room mate made when he saved the script,
and you can also see a commit that records how you ``merged`` your
room mate's dataset changes into your own dataset. The commit message of this
latter commit for now might contain many words yet unknown to you if you
do not use Git, but a later section will get into the details of what
the meaning of ":term:`merge`", ":term:`branch`", "refs"
or ":term:`master`" is.

For now, you're happy to have the changes your room mate made available.
This is how it should be! You helped him, and he helps you. Awesome!
There actually is a wonderful word for it: *Collaboration*.
Thus, without noticing, you have successfully collaborated for the first
time using DataLad datasets.

Create a note about this, and save it.

.. runrecord:: _examples/DL-101-121-113
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: write a note
   :cast: 04_collaboration

   $ cat << EOT >> notes.txt
   To update from a dataset with a shared history, you
   need to add this dataset as a sibling to your dataset.
   "Adding a sibling" means providing DataLad with info about
   the location of a dataset, and a name for it. Afterwards,
   a "datalad update --merge -s name" will integrate the changes
   made to the sibling into the dataset.
   A safe step in between is to do a "datalad update -s name"
   and checkout the changes with "git/datalad diff"
   to remotes/origin/master

   EOT
   $ datalad save -m "Add note on adding siblings"