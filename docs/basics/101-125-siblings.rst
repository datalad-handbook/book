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

Navigate into your dataset copy in ``mock_user/DataLad-101``,
and run the following command

.. runrecord:: _examples/DL-101-125-101
   :language: console
   :workdir: dl-101/DataLad-101

   # navigate into the installed copy
   $ cd ../mock_user/DataLad-101

   # download the shell script and save it in your code/ directory
   $ wget -nv https://raw.githubusercontent.com/datalad/datalad.org/7e8e39b1f08d0a54ab521586f27ee918b4441d69/content/asciicast/seamless_nested_repos.sh -O code/nested_repos.sh

Run a quick datalad status:

.. runrecord:: _examples/DL-101-125-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad status

Save this file:

.. runrecord:: _examples/DL-101-125-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101

   $ datalad save -m "add shell script from ascii cast on nesting" code/nested_repos.sh

Suddenly, your room mate has a file change that you do not have.
His dataset evolved.

So how do we link back from the copy of the dataset to its
origin, such that your room mates changes can be included in
your dataset? How to we let the original dataset "know" about
this copy your room mate has?
Do we need to install the installed dataset of our room mate
as a copy again?

No, luckily, it's simpler and less convoluted. What we have to
do is to create a datalad ``sibling``: A reference to our room mates
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

   cd ../../DataLad-101
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
can also ``datalad update`` this repository:

.. runrecord:: _examples/DL-101-125-106
   :language: console
   :workdir: dl-101/DataLad-101

   $ datalad update --merge -s roommate

Note that we supplied the siblings name with the ``-s``/``--name`` option.
This is good practice, and allows you to be precise in where you want to get
updates from. It would have worked without the specification (just as a bare
``datalad update --merge`` worked for your room mate), because there is only
one known other location, though.

.. container:: toggle

   .. container:: header

      **Addition: What if I mistyped the name or want to remove the sibling?**

   You can remove a sibling using ``datalad siblings remove -s roommate``

The exciting question is now whether your room mates change is now
also part of your own dataset. Let's list the contents of the ``code/``
directory and also peek into the history:

.. runrecord:: _examples/DL-101-125-107
   :language: console
   :workdir: dl-101/DataLad-101

   $ ls code/

.. runrecord:: _examples/DL-101-125-108
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

.. runrecord:: _examples/DL-101-125-109
   :language: console
   :workdir: dl-101/DataLad-101

   $ cat << EOT >> notes.txt
   To update from a dataset with a shared history, you
   need to add this dataset as a sibling to your dataset.
   "Adding a sibling" means providing DataLad with infos about
   the location of a dataset, and a name for it. Afterwards,
   a "datalad update --merge -s name" will integrate the changes
   made to the sibling into the dataset.

   EOT
   $ datalad save -m "Add note on adding siblings" notes.txt