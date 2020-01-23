.. _sharethirdparty:

Beyond shared infrastructure
----------------------------

From the sections :ref:`sharelocal1` and :ref:`yoda_project` you already
know about two common setups for sharing datasets:

Users on a common, shared computational infrastructure such as an :term:`SSH server`
can share datasets via simple installations with paths.

Without access to the same computer, it is possible to :command:`publish` datasets
to :term:`GitHub` or :term:`GitLab`. You have already done this when you shared
your ``midterm_project`` dataset via :term:`GitHub`. However, this section
demonstrated that the files stored in :term:`git-annex` (such as the results of
your analysis, ``pairwise_comparisons.png`` and ``prediction_report.csv``) are not
published to GitHub: There was meta data about their file availability, but a
:command:`datalad get` command on these files failed, because storing (large)
annexed content is currently not supported by :term:`GitHub` [#f1]_.
In the case of the ``midterm_project``, this was not a problem: The
computations that you ran were captured with :command:`datalad run`, and
others can just recompute your results instead of :command:`datalad get`\ting them.

However, not always do two or more parties share the same server, have access to
the same systems, or share something that can be recomputed quickly, but need to
actually share datasets with data, including the annexed contents.

Leveraging third party infrastructure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's say you'd like to share your complete ``DataLad-101`` dataset with
a friend overseas. After all you know about DataLad, you'd like to let more people
know about its capabilities. You and your friend, however, do not have access
to the same computational infrastructure, and there are also many annexed files, e.g.,
the PDFs in your dataset, that you'd like your friend to have but that can't be
simply computed or automatically obtained from web sources.

In these cases, the two previous approaches to share data do not suffice.
What you would like to do is to provide your friend with a GitHub URL to
install a dataset from *and* successfully run :command:`datalad get`, just as with
the many publicly available DataLad datasets such as the ``longnow`` podcasts.

To share all dataset contents with your friend, you need to configure an external
resource that stores your annexed data contents and that can be accessed by the
person you want to share your data with. Such a resource can be a private
web server, but also a third party services cloud storage such as
`Dropbox <https://dropbox.com>`_,
`Google <https://google.com>`_,
`Amazon S3 buckets <https://aws.amazon.com/s3/?nc1=h_ls>`_,
`Box.com <https://www.box.com/en-gb/home>`_,
`Figshare <https://figshare.com/>`_,
`owncloud <https://owncloud.org/>`_,
`sciebo <https://sciebo.de/>`_,
or many more. The key to achieve this lies within :term:`git-annex`.

In order to use third party services for file storage, you need to configure the
service of your choice and *publish* the annexed contents to it. Afterwards,
the published dataset (e.g., via :term:`GitHub` or :term:`GitLab`) stores the
information about where to obtain annexed file contents from such that
:command:`datalad get` works.

This tutorial showcases how this can be done, and shows the basics of how
datasets can be shared via a third party infrastructure. A much easier
alternative using another third party infrastructure is introduced in the next
section, :ref:`gin`, using the free G-Node infrastructure. If you prefer this as an
easier start, feel free to skip ahead.

From your perspective (as someone who wants to share data), you will
need to

- (potentially) install/setup the relevant *special-remote*,
- find a place that large file content can be stored in & set up a
  *publication dependency* on this location,
- publish your dataset

This gives you the freedom to decide where your data lives and
who can have access to it. Once this set up is complete, updating and
accessing a published dataset and its data is almost as easy as if it would
lie on your own machine.

From the perspective of your friend (as someone who wants to obtain a dataset),
they will need to

- (potentially) install the relevant *special-remote* and
- perform the standard :command:`datalad clone` and :command:`datalad get` commands
  as necessary.

Thus, from a collaborator's perspective, with the exception of potentially
installing/setting up the relevant *special-remote*, obtaining your dataset and its
data is as easy as with any public DataLad dataset.
While you have to invest some setup effort in the beginning, once this
is done, the workflows of yours and others are the same that you are already
very familiar with.

Setting up 3rd party services to host your data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this paragraph you will see how a third party service can be configured
to host your data. Note that the *exact* procedures are different from service
to service -- this is inconvenient, but inevitable given the
differences between the various third party infrastructures.
The general workflow, however, is the same:

#. Implement the appropriate Git-annex *special-remote* (different
   from service to service).
#. Push annexed file content to the third-party service to use it as a storage provider
#. Share the dataset (repository) via GitHub/GitLab/... for others to install from

If the above steps are implemented, others can :command:`install` or
:command:`clone` your shared dataset, and :command:`get` or :command:`pull` large
file content from the remote, third party storage.

.. findoutmore:: What is a special remote

   A special-remote is an extension to Git’s concept of remotes, and can
   enable :term:`git-annex` to transfer data to and from places that are not Git
   repositories (e.g., cloud services or external machines such as an HPC
   system). Don’t envision a special-remote as a physical place or location
   – a special-remote is just a protocol that defines the underlying transport
   of your files to and from a specific location.

As an example, let's walk through all necessary steps to publish ``DataLad-101``
to **Dropbox**. If you instead are interested in learning how to set up a public
`Amazon S3 bucket <https://aws.amazon.com/s3/?nc1=h_ls>`_, there is a single-page, step-by-step
walk-through `in the documentation of git-annex <https://git-annex.branchable.com/tips/public_Amazon_S3_remote/>`_
that shows how you can create an S3 special remote and share data with anyone who
gets a clone of your dataset, without them needing Amazon AWS credentials. Likewise,
the documentation provides step-by-step walk-throughs for many other services,
such as `Google Cloud Storage <https://git-annex.branchable.com/tips/using_Google_Cloud_Storage/>`_,
`Box.com <https://git-annex.branchable.com/tips/using_box.com_as_a_special_remote/>`__,
`Amazon Glacier <https://git-annex.branchable.com/tips/using_Amazon_Glacier/>`_,
`OwnCloud <https://git-annex.branchable.com/tips/owncloudannex/>`__, and many more.
Here is the complete list: `git-annex.branchable.com/special_remotes/ <https://git-annex.branchable.com/special_remotes/>`_.

For Dropbox, the relevant special-remote to configures is
`rclone <https://github.com/DanielDent/git-annex-remote-rclone>`__.
It is a command line program to sync files and directories to and
from a large number of commercial providers [#f2]_ (Amazon Cloud Drive, Microsoft
One Drive, ...). By enabling it as a special remote, :term:`git-annex` gets the
ability to do the same, and can thus take care of publishing large file content
to such sources conveniently under the hood.


- The first step is to `install <https://rclone.org/install/>`_
  ``rclone`` on your computer. The installation instructions are straightforward
  and the installation is quick if you are on a Unix-based system (macOS or any
  Linux distribution).

- Afterwards, run ``rclone config`` from the command line to configure ``rclone`` to
  work with Dropbox. Running this command will a guide you with an interactive
  prompt through a ~2 minute configuration of the remote (here we will name the
  remote "dropbox-for-friends" -- the name will be used to refer to it later during the
  configuration of the dataset we want to publish). The interactive dialog is
  outlined below, and all parts that require user input are highlighted.

.. code-block::
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

.. code-block:: bash
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

- Once this is done, ``git clone`` the
  `git-annex-remote-rclone <https://github.com/DanielDent/git-annex-remote-rclone>`_
  repository to your machine (do not clone it into ``DataLad-101`` but somewhere
  else on your computer)::

     $ git clone https://github.com/DanielDent/git-annex-remote-rclone.git

  This is a wrapper around `rclone <https://rclone.or>`__ that makes any
  destination supported by rclone usable with :term:`git-annex`. If you are on
  a recent version of Debian or Ubuntu, you alternatively can get it more
  conveniently via your package manager with ``sudo apt-get install git-annex-remote-rclone``.

- Copy the path to this repository into your ``$PATH`` variable. If the
  clone is in ``/home/user-bob/repos``, the command would look like this [#f3]_::

   $ export PATH="/home/user-bob/repos/git-annex-remote-rclone:$PATH"

- Finally, in the dataset you want to share, run the :command:`git annex initremote` command.
  Give the remote a name (it is ``dropbox-for-friends`` here), and specify the name of
  the remote you configured with ``rclone`` with the ``target`` parameters:

.. code-block:: bash

   $ git annex initremote dropbox-for-friends type=external externaltype=rclone chunk=50MiB encryption=none target=dropbox-for-friends

   initremote dropbox-for-friends ok
   (recording state in git...)

What has happened up to this point is that we have configured Dropbox
as a third-party storage service for the annexed contents in the dataset.
On a conceptual, dataset level, your Dropbox folder is now a :term:`sibling`:

.. code-block:: bash

   $ datalad siblings
    .: here(+) [git]
    .: dropbox-for-friends(+) [rclone]
    .: roommate(+) [../mock_user/DataLad-101 (git)]

On Dropbox, a new folder, ``git-annex`` will be created for your annexed files.
However, this is not the location you would refer your friend or a collaborator to.
The representation of the files in the special-remote is not human-readable --
it is a tree of annex objects, and thus looks like a bunch of very weirdly named
folders and files to anyone.
Through this design it becomes possible to chunk files into smaller units (see
`the git-annex documentation <https://git-annex.branchable.com/chunking/>`_ for more on this),
optionally encrypt content on its way from a local machine to a storage service
(see `the git-annex documentation <https://git-annex.branchable.com/encryption/>`__ for more on this),
and avoid leakage of information via file names. Therefore, the Dropbox remote is
not a places a real person would take a look at, instead they are only meant to
be managed and accessed via DataLad/git-annex.

To actually share your dataset with someone, you need to *publish* it to Github,
Gitlab, or a similar hosting service.

You could, for example, create a sibling of the ``DataLad-101`` dataset
on GitHub with the command :command:`datalad-sibling-github`.
This will create a new GitHub repository called "DataLad-101" under your account,
and configure this repository as a :term:`sibling` of your dataset
called ``github`` (exactly like you have done in :ref:`yoda_project`
with the ``midterm_project`` subdataset).
However, in order to be able to link the contents stored in Dropbox, you also need to
configure a *publication dependency* to the ``dropbox-for-friends`` sibling -- this is
done with the ``publish-depends <sibling>`` option.

.. code-block:: bash

   $ datalad create-sibling-github -d . DataLad-101 --publish-depends dropbox-for-friends
     [INFO   ] Configure additional publication dependency on "dropbox-for-friends"
     .: github(-) [https://github.com/<user-name>/DataLad-101.git (git)]
     'https://github.com/<user-name>/DataLad-101.git' configured as sibling 'github' for <Dataset path=/home/me/dl-101/DataLad-101>

:command:`datalad siblings` will again list all available siblings:

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

With this setup, we can publish the dataset to GitHub. Note how the publication
dependency is served first:

.. code-block:: bash
   :emphasize-lines: 2

   $ datalad publish --to github --transfer-data all
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

The option ``--transfer-data`` determines how publishing annexed contents should
be handled. With the option ``all``, *all* annexed contents are published to the
third-party data storage.
``--transfer-data none``, however, only publishes information stored in Git --
that is: The symlink, as information about file availability, but no file
content. Anyone who attempts to :command:`datalad get` a file from a dataset clone
if its contents were not published will fail.

.. findoutmore:: What if I don't want to share a dataset with everyone, or only some files of it?

   There are a number of ways to restrict access to your dataset or individual
   files of your dataset. One is via choice of (third party) hosting service
   for annexed file contents.
   If you chose a service only selected people have access to, and publish annexed
   contents exclusively there, then only those selected people can perform a
   successful :command:`datalad get`. On shared file systems you may achieve
   this via :term:`permissions` for certain groups or users, and for third party
   infrastructure you may achieve this by invitations/permissions/... options
   of the respective service.

   If it is individual files that you don't want to share, you can selectively
   publish the contents of all files you want others to have, and withhold the data
   of the files you don't want to share. This can be done by providing paths
   to the data that should be published, and the ``--transfer-data auto`` option.

   Let's say you have a dataset with three files:

   - ``experiment.txt``
   - ``subject_1.dat``
   - ``subject_2.data``

   Consider that all of these files are annexed. While the information in
   ``experiment.txt`` is fine for everyone to see, ``subject_1.dat`` and
   ``subject_2.dat`` contain personal and potentially identifying data that
   can not be shared. Nevertheless, you want collaborators to know that these
   files exist. The use case

   .. todo::

      Write use case "external researcher without data access"

   details such a scenario and demonstrates how external collaborators (with whom data
   can not be shared) can develop scripts against the directory structure and
   file names of a dataset, submit those scripts to the data owners, and thus still perform an
   analysis despite not having access to the data.

   By publishing only the file contents of ``experiment.txt`` with

   .. code-block:: bash

      $ datalad publish --to github --transfer-data auto experiment.txt

   only meta data about file availability of ``subject_1.dat`` and ``subject_2.dat``
   exists, but as these files' annexed data is not published, a :command:`datalad get`
   will fail. Note, though, that :command:`publish` will publish the complete
   dataset history (unless you specify a commit range with the ``--since`` option
   -- see the `manual <http://docs.datalad.org/en/latest/generated/man/datalad-publish.html>`_
   for more information).


From the perspective of whom you share your dataset with...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your friend would now want to get your dataset including the annexed
contents, and you made sure that they can access the Dropbox folder with
the annexed files (e.g., by sharing an access link), here is what they would
have to do:

If the repository is on GitHub, a :command:`datalad clone` with the URL
will install the dataset::

   $ datalad clone https://github.com/<user-name>/DataLad-101.git
   [INFO   ] Cloning https://github.com/<user-name>/DataLad-101.git [1 other candidates] into '/Users/awagner/Documents/DataLad-101'
   [INFO   ]   Remote origin not usable by git-annex; setting annex-ignore
   [INFO   ] access to 1 dataset sibling dropbox-for-friends not auto-enabled, enable with:
   |         datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-for-friends
   install(ok): /Users/awagner/Documents/DataLad-101 (dataset)

Pay attention to one crucial information in this output::

   [INFO   ] access to 1 dataset sibling dropbox-for-friends not auto-enabled, enable with:
   |         datalad siblings -d "/Users/<user-name>/Documents/DataLad-101" enable -s dropbox-for-friends

This means that someone who wants to access the data from dropbox needs to
enable the special remote.
For this,  this person first needs to install and configure ``rclone``
as well: Since ``rclone`` is the protocol with which
annexed data can be transferred from and to Dropbox, anyone who needs annexed
data from Dropbox needs this special remote. Therefore, the first steps are
the same as before:

- `Install <https://rclone.org/install/>`__ ``rclone`` (as described above).
- Run ``rclone config`` to configure ``rclone`` to work with Dropbox (as described
  above). It is important to name the remote "dropbox-for-friends" (i.e., give it the
  same name as the one configured in the dataset).
- ``git clone`` the
  `git-annex-remote-rclone <https://github.com/DanielDent/git-annex-remote-rclone>`_
  repository and copy the path into your ``$PATH`` variable (as described above).

After this is done, you can execute what DataLad's output message suggests
to "enable" this special remote (inside of the installed ``DataLad-101``)::

   $ datalad siblings -d "/Users/awagner/Documents/DataLad-101" enable -s dropbox-for-friends
   .: dropbox-for-friends(?) [git]

And once this is done, you can get any annexed file contents, for example the
books, or the cropped logos from chapter :ref:`chapter_run`::

   $ datalad get books/TLCL.pdf
   get(ok): /home/some/other/user/DataLad-101/books/TLCL.pdf (file) [from dropbox-for-friends]

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
special features a DataLad dataset provides will be available, such as its
history or configurations.

.. rubric:: Footnotes

.. [#f1] :term:`GitLab`, on the other hand, provides a git-annex configuration. It
         is disabled by default, and to enable it you would need to have administrative
         access to the server and client side of your GitLab instance. Find out more
         `here <https://docs.gitlab.com/ee/administration/git_annex.html>`_.

.. [#f2] ``rclone`` is a useful special-remote for this example, because
         you can not only use it for Dropbox, but also for many other
         third-party hosting services.
         For a complete overview of which third-party services are
         available and which special-remote they need, please see this
         `list <http://git-annex.branchable.com/special_remotes/>`_.

.. [#f3] Note that ``export`` will extend your ``$PATH`` *for your current shell*.
         This means you will have to repeat this command if you open a new shell.
         Alternatively, you can insert this line into your shells configuration file
         (e.g., ``~/.bashrc``) to make this path available to all future shells of
         your user account.
