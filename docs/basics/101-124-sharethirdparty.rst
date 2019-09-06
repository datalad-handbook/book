.. _sharethirdparty:

Sharing datasets: Third party infrastructure
--------------------------------------------

Section :ref:`sharelocal1` already outlined a common
set up for sharing datasets: Between users on a common, shared
computational infrastructure such as an SSH server.
However, not always do two or more parties share the same
server, or have access to the same systems. In these cases,
datasets need to be shared via a resource that can be
accessed by anyone who needs the data. Such a resource can
be third party services cloud storage such as
`Dropbox <https://dropbox.com>`_,
`Google <https://google.com>`_,
`Àmazon <https://aws.amazon.com/s3/?nc1=h_ls>`_,
`Box.com <https://www.box.com/en-gb/home>`_,
`Figshare <https://figshare.com/>`_,
`owncloud <https://owncloud.org/>`_,
`sciebo <https://sciebo.de/>`_,
or many more. This tutorial showcases the basics of how
data can be shared.


Note that the exact procedures are different from service
to service -- this is inconvenient, but inevitable given the
differences between the various third party infrastructures.
The general workflow however is the same:

#. Implement the appropriate Git-annex *special-remote* (different
   from service to service).
#. Push annexed file content to the third-party service to use it as a storage provider
#. Share the dataset (repository) via Github/Gitlab/...
#. If your repository is cloned by others, they can ``pull`` files
   and obtain them from the third-party service

Let's walk through all necessary steps to publish ``DataLad-101``
to Dropbox. The special-remote used to do this is
`rclone <https://github.com/DanielDent/git-annex-remote-rclone>`_.
This special remote is used for the majority of commercial
providers (Google, Amazon, ...), and quite easy to work with.
For a complete overview of which third-party services are
available and which special-remote they need, please see this
`list <http://git-annex.branchable.com/special_remotes/>`_.

- The first step is to `install <https://rclone.org/install/>`_
  rclone.

- Afterwards, run ``rclone config`` to configure ``rclone`` to
  work with Dropbox. Running this command will prompt interactively
  from the terminal to configure a remote (here it will have the
  name "dropbox-remote"):

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

- This will open a browser and ask you to authorize ``rclone`` to
  manage your Dropbox, or any other third-party service you have selected
  in the interactive prompt. Accepting will bring you to the final configuration
  prompts:

.. code-block:: bash

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
  repository to your machine.

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

   git annex initremote dropbox-remote type=external externaltype=rclone target=dropbox-remote prefix=git-annex chunk=50MiB encryption=shared mac=HMACSHA512 rclone_layout=lower

   initremote dropbox-remote (encryption setup) (encryption key stored in git repository) ok
   (recording state in git...)

Afterwards, the remote ``dropbox-remote`` is a :ref:`sibling` of the dataset,
and you can use the command :command:`datalad publish` to transfer data to it:

.. todo::

   Currently I'm just trying things out, later I need to redo this
   within the narrative

.. code-block:: bash

   datalad publish --to dropbox-remote --transfer-data all
   [INFO   ] Publishing <Dataset path=/tmp/DataLad-101> data to dropbox-remote
   publish(ok): books/TLCL.pdf (file)
   publish(ok): books/byte-of-python.pdf (file)
   publish(ok): books/progit.pdf (file)
   publish(ok): recordings/interval_logo_small.jpg (file)
   publish(ok): recordings/salt_logo_small.jpg (file)
   action summary:
     publish (ok: 5)

What has happened up to this point is that we have utilized Dropbox
as a third-party storage service for the annexed contents in the dataset.
However, it is not the location we would refer any collaborator to.
Indeed, the representation of the files in the special-remote is not
human-readable, it is a tree of annex objects.
Only through this design it becomes possible to chunk files into
smaller units, optionally encrypt content on its way from a local
machine to a storage service, and avoid leakage of information via
file names. Therefore these places are not something a real person
would take a look at, instead they are only meant to to be managed
and accessed via DataLad/Git-annex.

To actually share your dataset with someone outside, you need to
publish it to Github, Gitlab, ...

.. todo::

   try this

.. findoutmore:: Special remotes

    **Special-remotes**

    A special-remote is an extension to Git's concept of remotes,
    and can tie Git-annex to many cloud services.
    In this type of remote, Git-annex can store and retrieve file
    content, but they cannot be used by other Git commands, nor do
    they store the Git history. Don't envision a special-remote as a place
    or location. A special-remote is just a protocol that defines the
    underlying transport of your files.  Instead, the special-remote is a
    protocol to transfer the Git-annex object tree (? I need to find out
    what they are...)

Built-in data export
^^^^^^^^^^^^^^^^^^^^

DataLad also has some support for "exporting" data to other services.
For example the :command:`export-to-figshare`. The main difference is
that this moves data out of version control and decentralized tracking,
and essentially "throws it over the wall". Alternatively, git annex provides
"export/input" functionality that can be used to read and write from/to
a particular "human-facing" representation (which is not a git repo),
for example the content of a particular version of a particular branch.

.. todo::

   above is literally taken from mih, need to turn it into subsection.
   Probably can find a useful example in narrative.