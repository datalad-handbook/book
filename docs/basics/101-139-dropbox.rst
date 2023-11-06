.. _dropbox:

Walk-through: Dropbox as a special remote
-----------------------------------------

Let's say you'd like to share your complete ``DataLad-101`` dataset with
a friend overseas. After all you know about DataLad, you'd like to let more people
know about its capabilities. You and your friend, however, do not have access
to the same computational infrastructure, and there are also many annexed files, e.g., the PDFs in your dataset, that you'd like your friend to have but that can't be simply computed or automatically obtained from web sources.
What you would like to do is to provide your friend with a URL to
install a dataset from *and* successfully run :dlcmd:`get`, just as with
the many publicly available DataLad datasets such as the ``longnow`` podcasts.


As an example, let's walk through all necessary steps to publish the ``DataLad-101`` dataset to GitHub, and its file contents to **Dropbox**.
To make this as convenient as possible, we will also set up a :term:`publication dependency` between the two.

To set up Dropbox as a third party storage provide you need to configure a special-remote called
git-annex-remote-rclone_.
It is a command line program to sync files and directories to and
from a large number of commercial providers [#f2]_.

- The first step is to `install <https://rclone.org/install>`_
  ``rclone`` on your computer. The installation instructions are straightforward
  and the installation is quick if you are on a Unix-based system (macOS or any
  Linux distribution).

- Afterwards, run ``rclone config`` from the command line to configure ``rclone`` to
  work with Dropbox. Running this command will a guide you with an interactive
  prompt through a ~2 minute configuration of the remote (here we will name the
  remote "dropbox-for-friends" -- the name will be used to refer to it later during the
  configuration of the dataset we want to publish). The interactive dialog is
  outlined below, and all parts that require user input are highlighted.

.. code-block:: text
   :emphasize-lines: 7-8, 22, 26, 30, 36

   $ rclone config
    2019/09/06 13:43:58 NOTICE: Config file "/home/me/.config/rclone/rclone.conf" not found - using defaults
    No remotes found - make a new one
    n) New remote
    s) Set configuration password
    q) Quit config
    n/s/q> n
    name> dropbox-for-friends
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

.. code-block:: text
   :emphasize-lines: 12, 26

   Got code
   --------------------
   [dropbox-for-friends]
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
   dropbox-for-friends  dropbox

   e) Edit existing remote
   n) New remote
   d) Delete remote
   r) Rename remote
   c) Copy remote
   s) Set configuration password
   q) Quit config
   e/n/d/r/c/s/q> q

- Once this is done, install ``git-annex-remote-rclone``.
  It is a wrapper around rclone_ that makes any   destination supported by rclone usable with :term:`git-annex`.
  If you are on a recent version of Debian or Ubuntu (or have enabled the `NeuroDebian <https://neuro.debian.net>`_ repository), you can get it conveniently via your package manager, e.g., with ``sudo apt-get install git-annex-remote-rclone``.
  Alternatively, ``git clone`` the `git-annex-remote-rclone <https://github.com/git-annex-remote-rclone/git-annex-remote-rclone>`_ repository to your machine (do not clone it into ``DataLad-101`` but somewhere else on your computer), and copy the path to this repository into your ``$PATH`` variable. If you
  clone into ``/home/user-bob/repos``, the command would look like this [#f3]_:

  .. code-block:: bash

     $ git clone https://github.com/DanielDent/git-annex-remote-rclone.git
     $ export PATH="/home/user-bob/repos/git-annex-remote-rclone:$PATH"

- Finally, in the dataset you want to share, run the :gitannexcmd:`initremote` command.
  Give the remote a name (it is ``dropbox-for-friends`` here), and specify the name of  the remote you configured with ``rclone`` with the ``target`` parameters:

.. code-block:: bash

   $ git annex initremote dropbox-for-friends type=external externaltype=rclone chunk=50MiB encryption=none target=dropbox-for-friends prefix=my_awesome_dataset

   initremote dropbox-for-friends ok
   (recording state in git...)

What has happened up to this point is that we have configured Dropbox
as a third-party storage service for the annexed contents in the dataset.
On a conceptual, dataset level, your Dropbox folder is now a :term:`sibling` -- the sibling name is the first positional argument after ``initremote``, i.e., "dropbox-for-friends":

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: dropbox-for-friends(+) [rclone]
    .: roommate(+) [../mock_user/DataLad-101 (git)]

On Dropbox, a new folder will be created for your annexed files.
By default, this folder will be called ``git-annex``, but it can be configured using the ``--prefix=<whatitshouldbecalled>`` option, as done above.
However, this directory on Dropbox is not the location you would refer your friend or a collaborator to.
The representation of the files in the special-remote is not human-readable --
it is a tree of annex objects, and thus looks like a bunch of very weirdly named
folders and files to anyone.
Through this design it becomes possible to chunk files into smaller units (see
`the git-annex documentation <https://git-annex.branchable.com/chunking>`_ for more on this),
optionally encrypt content on its way from a local machine to a storage service
(see `the git-annex documentation <https://git-annex.branchable.com/encryption>`__ for more on this),
and avoid leakage of information via file names. Therefore, the Dropbox remote is
not a places a real person would take a look at, instead they are only meant to
be managed and accessed via DataLad/git-annex.

To actually share your dataset with someone, you need to *publish* it to Github,
Gitlab, or a similar hosting service.

.. index::
   pair: create-sibling-github; DataLad command

You could, for example, create a sibling of the ``DataLad-101`` dataset
on GitHub with the command :dlcmd:`create-sibling-github`.
This will create a new GitHub repository called "DataLad-101" under your account,
and configure this repository as a :term:`sibling` of your dataset
called ``github`` (exactly like you have done in :ref:`yoda_project`
with the ``midterm_project`` subdataset).
However, in order to be able to link the contents stored in Dropbox, you also need to
configure a *publication dependency* to the ``dropbox-for-friends`` sibling -- this is
done with the ``publish-depends <sibling>`` option.

.. code-block:: bash

   $ datalad create-sibling-github -d . DataLad-101 \
     --publish-depends dropbox-for-friends
     [INFO   ] Configure additional publication dependency on "dropbox-for-friends"
     .: github(-) [https://github.com/<user-name>/DataLad-101.git (git)]
     'https://github.com/<user-name>/DataLad-101.git' configured as sibling 'github' for <Dataset path=/home/me/dl-101/DataLad-101>

:dlcmd:`siblings` will again list all available siblings:

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: dropbox-for-friends(+) [rclone]
    .: roommate(+) [../mock_user/DataLad-101 (git)]
    .: github(-) [https://github.com/<user-name>/DataLad-101.git (git)]

Note that each sibling has either a ``+`` or ``-`` attached to its name. This
indicates the presence (``+``) or absence (``-``) of a remote data annex at this
remote. You can see that your ``github`` sibling indeed does not have a remote
data annex.
Therefore, instead of "only" publishing to this GitHub repository (as done in section
:ref:`yoda_project`), in order to also publish annex contents, we made
publishing to GitHub dependent on the ``dropbox-for-friends`` sibling
(that has a remote data annex), so that annexed contents are published
there first.

.. index::
   pair: publication dependency; DataLad concept
.. importantnote:: Publication dependencies are strictly local configuration

   Note that the publication dependency is only established for your own dataset,
   it is not shared with clones of the dataset. Internally, this configuration
   is a key value pair in the section of your remote in ``.git/config``:

   .. code-block:: bash

      [remote "github"]
         annex-ignore = true
         url = https://github.com/<user-name>/DataLad-101.git
         fetch = +refs/heads/*:refs/remotes/github/*
         datalad-publish-depends = dropbox-for-friends

With this setup, we can publish the dataset to GitHub. Note how the publication
dependency is served first:

.. code-block:: bash
   :emphasize-lines: 2

   $ datalad push --to github
   [INFO   ] Transferring data to configured publication dependency: 'dropbox-for-friends'
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> data to dropbox-for-friends
   publish(ok): books/TLCL.pdf (file)
   publish(ok): books/byte-of-python.pdf (file)
   publish(ok): books/progit.pdf (file)
   publish(ok): recordings/interval_logo_small.jpg (file)
   publish(ok): recordings/salt_logo_small.jpg (file)
   [INFO   ] Publishing to configured dependency: 'dropbox-for-friends'
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> data to dropbox-for-friends
   [INFO   ] Publishing <Dataset path=/home/me/dl-101/DataLad-101> to github
   Username for 'https://github.com': <user-name>
   Password for 'https://<user-name>@github.com':
   publish(ok): . (dataset) [pushed to github: ['[new branch]', '[new branch]']]
   action summary:
     publish (ok: 6)


Afterwards, your dataset can be found on GitHub, and ``cloned`` or ``installed``.


From the perspective of whom you share your dataset with...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your friend would now want to get your dataset including the annexed
contents, and you made sure that they can access the Dropbox folder with
the annexed files (e.g., by sharing an access link), here is what they would
have to do:

If the repository is on GitHub, a :dlcmd:`clone` with the URL
will install the dataset:

.. code-block:: bash

   $ datalad clone https://github.com/<user-name>/DataLad-101.git
   [INFO   ] Cloning https://github.com/<user-name>/DataLad-101.git [1 other candidates] into '/Users/awagner/Documents/DataLad-101'
   [INFO   ]   Remote origin not usable by git-annex; setting annex-ignore
   [INFO   ] access to 1 dataset sibling dropbox-for-friends not auto-enabled, enable with:
   |         datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-for-friends
   install(ok): /Users/awagner/Documents/DataLad-101 (dataset)

Pay attention to one crucial information in this output:

.. code-block:: bash

   [INFO   ] access to 1 dataset sibling dropbox-for-friends not auto-enabled, enable with:
   |         datalad siblings -d "/Users/<user-name>/Documents/DataLad-101" enable -s dropbox-for-friends

This means that someone who wants to access the data from dropbox needs to
enable the special remote.
For this,  this person first needs to install and configure ``rclone``
as well: Since ``rclone`` is the protocol with which
annexed data can be transferred from and to Dropbox, anyone who needs annexed
data from Dropbox needs *this* special remote. Therefore, the first steps are
the same as before:

- `Install <https://rclone.org/install>`__ ``rclone`` (as described above).
- Run ``rclone config`` to configure ``rclone`` to work with Dropbox (as described above). **It is important to name the remote identically** - in the example above, it would need to be "dropbox-for-friends".
  This means: You need to communicate the name of your special remote to your friend, and they have to give it the same name as the one configured in the dataset).
  (There are efforts towards extracting this information automatically from datasets, but for the time being, this is an important detail to keep in mind).
- install git-annex-remote-rclone_ (as described above).

After this is done, you can execute what DataLad's output message suggests
to "enable" this special remote (inside of the installed ``DataLad-101``):

.. code-block:: bash

   $ datalad siblings -d "/Users/awagner/Documents/DataLad-101" \
     enable -s dropbox-for-friends
   .: dropbox-for-friends(?) [git]

And once this is done, you can get any annexed file contents, for example, the
books, or the cropped logos from chapter :ref:`chapter_run`:

.. code-block:: bash

   $ datalad get books/TLCL.pdf
   get(ok): /home/some/other/user/DataLad-101/books/TLCL.pdf (file) [from dropbox-for-friends]

.. _rclone: https://rclone.org
.. _git-annex-remote-rclone: https://github.com/git-annex-remote-rclone/git-annex-remote-rclone

.. rubric:: Footnotes

.. [#f2] ``rclone`` is a useful special-remote for this example, because
         you can not only use it for Dropbox, but also for many other
         third-party hosting services.
         For a complete overview of which third-party services are
         available and which special-remote they need, please see this
         `list <https://git-annex.branchable.com/special_remotes>`_.

.. [#f3] Note that ``export`` will extend your ``$PATH`` *for your current shell*.
         This means you will have to repeat this command if you open a new shell.
         Alternatively, you can insert this line into your shells configuration file
         (e.g., ``~/.bashrc``) to make this path available to all future shells of
         your user account.
         If you are unsure what any of this means, take a look at :ref:`this additional information on environment variables <envvars>`
