.. _sharethirdparty:

Sharing datasets: Third party infrastructure
--------------------------------------------

The sections :ref:`sharelocal1` and :ref:`yoda_project` already
outlined two common setups for sharing datasets:

The first was between users on a common, shared computational infrastructure
such as an :term:`SSH server`. In this case, sharing was easy via a simple
:command:`datalad install` command with a path to where the dataset lies.

In the second case, we shared the ``midterm_project`` dataset via :term:`GitHub`.
In this endeavour you noticed that the files stored in :term:`git-annex`
(among others, the results of your analysis,
``pairwise_comparisons.png`` and ``prediction_report.csv``) were not shared
via GitHub. There was meta data about their file availability, but a
:command:`datalad get` command on these files failed, because annexed content
in datasets can not be hosted on services like :term:`GitHub` and
:term:`GitLab`.
In the case of the ``midterm_project``, this was not a problem: The
computation that you ran were captured with :command:`datalad run`, and
instead of needing to obtain your results, others can just recompute them.

However, not always do two or more parties share the same
server, or have access to the same systems. Or you don't have something
that can be recomputed quickly, but need to actually share data contents
with someone else.

In these cases, the two approaches above do not suffice. What you
would need to do to share a dataset (e.g., via GitHub) and make a
:command:`datalad get` on annexed contents work, is an external
resource that holds your annexed data contents and that can be
accessed by the person you want to share your data with.
Such a resource can be third party services cloud storage such as
`Dropbox <https://dropbox.com>`_,
`Google <https://google.com>`_,
`Amazon <https://aws.amazon.com/s3/?nc1=h_ls>`_,
`Box.com <https://www.box.com/en-gb/home>`_,
`Figshare <https://figshare.com/>`_,
`owncloud <https://owncloud.org/>`_,
`sciebo <https://sciebo.de/>`_,
or many more. Services as the ones listed above need to be
configured as a large file storage, and afterwards, shared datasets
(e.g., via :term:`GitHub` or :term:`GitLab`) know where to obtain annexed
file contents from, such that :command:`datalad get` works.
This tutorial showcases how this can be done, and shows the basics of how
datasets can be shared via a third party infrastructure.

From the perspective of you as someone who wants to share data, you will
need to

- (potentially) install/setup the relevant *special-remote*
- find a place that the large file content can be stored in and set
  up a publication dependency on this location.
- publish your dataset

This gives you all the freedom to decide where your data lives, and
who can have access to it. Once this set up is complete, publishing and
accessing a published dataset and its data is as easy as if it would
lie on your own machine.

From the perspective of someone you share your dataset with, they will need
to

- (potentially) install the relevant *special-remote*
- do a normal :command:`datalad install` and :command:`datalad get` commands
  as necessary.

Thus, from their perspective, with the exception of installing/setting up
the relevant *special-remote*, obtaining your dataset and its
data is as easy as with any public DataLad dataset.

Thus, while you have to invest some setup effort in the beginning, once this
is done, the workflows of yours and others are the same that you are already
very familiar with.

Setting up 3rd party services to host your data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this paragraph you will see how a third party services can be configured
to host your data. Note that the *exact* procedures are different from service
to service -- this is inconvenient, but inevitable given the
differences between the various third party infrastructures.
The general workflow, however, is the same:

#. Implement the appropriate Git-annex *special-remote* (different
   from service to service).
#. Push annexed file content to the third-party service to use it as a storage provider
#. Share the dataset (repository) via GitHub/GitLab/...

If the above steps are implemented, other can :command:`install` or
:command:`clone` your shared dataset, and :command:`get` or :command:`pull` large
file content from the remote, third party storage without needing to
know *where* the data actually comes from.

.. findoutmore:: What is a special remote

   A special-remote is an extension to Git’s concept of remotes, and can
   enable git-annex to transfer data to and from places that are not Git
   repositories (e.g., cloud services or external machines such as an HPC
   system). Don’t envision a special-remote as a physical place or location
   – a special-remote is just a protocol that defines the underlying transport
   of your files to and from a specific location.

As an example, Let's walk through all necessary steps to publish ``DataLad-101``
to **Dropbox**. The special-remote used to do this is
`rclone <https://github.com/DanielDent/git-annex-remote-rclone>`__.
It is a command line program to sync files and directories to and
from a large number of commercial providers (Google, Amazon, owncloud,
...), and quite easy to work with. By enabling it as a special remote,
:term:`Git-annex` gets the ability to do the same, and can thus take
care of publishing large file content to such sources conveniently under
the hood.

``rclone`` is a useful special-remote for this example, because
you can not only use it for Dropbox, but also for many other
third-party hosting services. If you follow along and install it, you are
ready to go to use it also with Google drive or Amazon S3, for example.
For a complete overview of which third-party services are
available and which special-remote they need, please see this
`list <http://git-annex.branchable.com/special_remotes/>`_.

- The first step is to `install <https://rclone.org/install/>`_
  ``rclone`` on your system. The installation instructions are straightforward
  and the installation quick if you are on a Unix-based system (macOS or any
  Linux distribution).

- Afterwards, run ``rclone config`` to configure ``rclone`` to
  work with Dropbox. Running this command will prompt interactively
  from the terminal to configure a remote (here it will have the
  name "dropbox-remote"). All parts of the dialog that require user input
  are highlighted in the code block below.

.. code-block::
   :emphasize-lines: 7-8, 22, 26, 30, 36

   $ rclone config
    2019/09/06 13:43:58 NOTICE: Config file "/home/adina/.config/rclone/rclone.conf" not found - using defaults
    No remotes found - make a new one
    n) New remote
    s) Set configuration password
    q) Quit config
    n/s/q> n
    name> dropbox-remote
    Type of storage to configure.
    Enter a string value. Press Enter for the default ("").
    Choose a number from below, or type in your own value
     1 / 1Fichier
       \ "fichier"
     2 / Alias for an existing remote
       \ "alias"
    [...]
     8 / Dropbox
       \ "dropbox"
    [...]
    31 / premiumize.me
       \ "premiumizeme"
    Storage> dropbox
    ** See help for dropbox backend at: https://rclone.org/dropbox/ **

    Dropbox App Client Id
    Leave blank normally.
    Enter a string value. Press Enter for the default ("").
    client_id>
    Dropbox App Client Secret
    Leave blank normally.
    Enter a string value. Press Enter for the default ("").
    client_secret>
    Edit advanced config? (y/n)
    y) Yes
    n) No
    y/n> n
    If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth
    Log in and authorize rclone for access
    Waiting for code...

- At this point, this will open a browser and ask you to authorize ``rclone`` to
  manage your Dropbox, or any other third-party service you have selected
  in the interactive prompt. Accepting will bring you back into the terminal
  to the final configuration prompts:

.. code-block:: bash
   :emphasize-lines: 12, 26

   Got code
   --------------------
   [dropbox-remote]
   type = dropbox
   token = {"access_token":"meVHyc[...]",
            "token_type":"bearer",
            "expiry":"0001-01-01T00:00:00Z"}
   --------------------
   y) Yes this is OK
   e) Edit this remote
   d) Delete this remote
   y/e/d> y
   Current remotes:

   Name                 Type
   ====                 ====
   dropbox-remote       dropbox

   e) Edit existing remote
   n) New remote
   d) Delete remote
   r) Rename remote
   c) Copy remote
   s) Set configuration password
   q) Quit config
   e/n/d/r/c/s/q> q

- ``git clone`` the
  `git-annex-remote-rclone <https://github.com/DanielDent/git-annex-remote-rclone>`_
  repository to your machine (not inside ``DataLad-101``)::

     $ git clone https://github.com/DanielDent/git-annex-remote-rclone.git

  This is a wrapper around `rclone <https://rclone.or>`__ that makes any
  destination supported by rclone usable with Git-annex.

- Copy the path to this repository into your ``$PATH`` variable. If the
  clone is in ``/home/user-bob/repos``, the command would look like this::

   $ export PATH="/home/user-bob/repos/git-annex-remote-rclone:$PATH"

- Chose a repository *layout* for the remote. There are many to chose from
  (``lower``, ``directory``, ``nodir``, ``mixed`` and ``frankencase``;
  see `here <https://github.com/DanielDent/git-annex-remote-rclone>`_)
  and ``git-annex-remote-rclone`` suggests ``lower``, when in doubt.

- Finally, in the dataset, run the :command:`git annex initremote` command.
  Give the remote a name (it is ``dropbox-remote`` here), specify the name of
  the remote your configured with ``rclone`` with the ``target`` parameters,
  and supply your choice of layout with the ``rclone_layout`` keyword:

.. code-block:: bash

   $ git annex initremote dropbox-remote type=external externaltype=rclone encryption=none target=dropbox-remote

   initremote dropbox-remote ok
   (recording state in git...)

What has happened up to this point is that we have configured Dropbox
as a third-party storage service for the annexed contents in the dataset.
On a conceptual, dataset level, your Dropbox folder is now a :term:`sibling`:

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: dropbox-remote(+) [rclone]
    .: roommate(+) [../mock_user/DataLad-101 (git)]

On Dropbox, a new folder, ``git-annex`` was created.
However, this is not the location we would refer any collaborator to.
Indeed, the representation of the files in the special-remote is not
human-readable, it is a tree of annex objects.
Only through this design it becomes possible to chunk files into
smaller units, optionally encrypt content on its way from a local
machine to a storage service, and avoid leakage of information via
file names. Therefore these places are not something a real person
would take a look at, instead they are only meant to to be managed
and accessed via DataLad/Git-annex.

To actually share your dataset with someone outside, you need to
publish it to Github, Gitlab, or a similar place.

You could, for example, create a sibling of the ``DataLad-101`` dataset
on GitHub with :command:`datalad-sibling-github`.
This will create a new GitHub repository called "DataLad-101" under your account,
and configure this repository as a :term:`sibling` of your dataset
called ``github`` (exactly the same as what you have done in :ref:`yoda_project`
with the ``midterm_project`` subdataset).
However, in order to be able to link contents stored in Dropbox, you need to
configure a publication dependency to the ``dropbox-remote`` sibling.

.. code-block:: bash

   $ datalad create-sibling-github -d . DataLad-101 --publish-depends dropbox-remote
     [INFO   ] Configure additional publication dependency on "dropbox-remote"
     .: github(-) [https://github.com/adswa/DataLad-101.git (git)]
     'https://github.com/adswa/DataLad-101.git' configured as sibling 'github' for <Dataset path=/home/me/dl-101/DataLad-101>

:command:`datalad siblings` will again list all available siblings:

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: dropbox-remote(+) [rclone]
    .: roommate(+) [../mock_user/DataLad-101 (git)]
    .: github(-) [https://github.com/adswa/DataLad-101.git (git)]

Note that each sibling has either a ``+`` or ``-`` attached to its name. This
indicates the presence (``+``) or absence (``-``) of a remote data annex at this
remote. You can see that your ``github`` sibling indeed does not have a remote
data annex.

Therefore, instead of "only" publishing to this GitHub repository (as done in section
:ref:`yoda_project`), in order to also publish annex contents, we made
publishing to GitHub dependent on the ``dropbox-remote`` sibling
(that has a remote data annex), so that annexed contents are published
there first.

With this setup, we can publish the dataset to GitHub.

.. code-block:: bash

   $ datalad publish --to github --transfer-data all
   [INFO   ] Transferring data to configured publication dependency: 'dropbox-remote'
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> data to dropbox-remote
   publish(ok): books/TLCL.pdf (file)
   publish(ok): books/byte-of-python.pdf (file)
   publish(ok): books/progit.pdf (file)
   publish(ok): recordings/interval_logo_small.jpg (file)
   publish(ok): recordings/salt_logo_small.jpg (file)
   [INFO   ] Publishing to configured dependency: 'dropbox-remote-2'
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> data to dropbox-remote
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> to github
   Username for 'https://github.com': adswa
   Password for 'https://adswa@github.com':
   publish(ok): . (dataset) [pushed to github: ['[new branch]', '[new branch]']]
   action summary:
     publish (ok: 6)


Afterwards, your dataset can be found on GitHub, and ``cloned`` or ``installed``.

From the perspective of whom you share your dataset with...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say another person would want to get your dataset including the annexed
contents.

If the repository is on GitHub, a :command:`datalad install` with the url
will install the dataset::

   $ datalad install https://github.com/adswa/DataLad-101.git
   [INFO   ] Cloning https://github.com/adswa/DataLad-101.git [1 other candidates] into '/Users/awagner/Documents/DataLad-101'
   [INFO   ]   Remote origin not usable by git-annex; setting annex-ignore
   [INFO   ] access to 1 dataset sibling dropbox-remote not auto-enabled, enable with:
   |         datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-remote
   install(ok): /Users/awagner/Documents/DataLad-101 (dataset)

Pay attention to one crucial information in this output::

   [INFO   ] access to 1 dataset sibling dropbox-remote not auto-enabled, enable with:
   |         datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-remote

This means that someone who wants to access the data from dropbox needs to
enable the special remote.
For this,  this person first needs to install and configure ``rclone`` first
as well: Since ``rclone`` is the protocol with which
annexed data can be transferred from and to Dropbox, anyone who needs annexed
data from Dropbox needs this special remote. Therefore, the first steps are
the same as before:

- `Install <https://rclone.org/install/>`__ ``rclone`` on your system.
- Run ``rclone config`` to configure ``rclone`` to work with Dropbox. It is
  important to name the remote "dropbox-remote" (i.e., give it the same name
  as the one configured in the dataset)
- ``git clone`` the
  `git-annex-remote-rclone <https://github.com/DanielDent/git-annex-remote-rclone>`_
  repository to your machine
- Copy the path to this repository into your ``$PATH`` variable. If the
  clone is in ``/home/user-bob/repos``, the command would look like this::

  $ export PATH="/home/user-bob/repos/git-annex-remote-rclone:$PATH"

After this is done, you can execute that DataLad's output message suggests
(inside of the installed ``DataLad-101``)::

   $ datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-remote
   .: dropbox-remote(?) [git]

And once this is done, you can get any annexed file contents, for example the
books, or the cropped logos from chapter "DataLad, Run!"::

   $ datalad get books/TLCL.pdf
   get(ok): /home/some/other/user/DataLad-101/books/TLCL.pdf (file) [from dropbox-remote]

Built-in data export
^^^^^^^^^^^^^^^^^^^^

Apart from flexibly configurable special remotes that allow publishing
annexed content to a variety of third party infrastructure, DataLad also has
some build-in support for "exporting" data to other services.

One example is the command :command:`export-to-figshare`. Running
this command allows you to publish the dataset to
`Figshare <https://figshare.com/>`_. The main difference is
that this moves data out of version control and decentralized tracking,
and essentially "throws it over the wall". This means, while your data (also
the annexed data) will be available for download on Figshare, none of the
special features a DataLad dataset provides will be available, such a its
history or configurations.

.. rubric:: Footnotes

[#f1] Note that ``export`` will extend your ``$PATH`` *for your current shell*.
      This means you will have to repeat this command if you open a new shell.
      Alternatively, you can insert this line into your shells configuration file
      (e.g., ``~/.bashrc``) to make this path available to all future shells of
      your user account.