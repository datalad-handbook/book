.. _share_hostingservice:

Publishing datasets to Git repository hosting
---------------------------------------------

Because DataLad datasets are :term:`Git` repositories, it is possible to
:command:`push` datasets to any Git repository hosting service, such as
:term:`GitHub`, :term:`GitLab`, :term:`Gin`, :term:`Bitbucket`, `Gogs <https://gogs.io/>`_, or `Gitea <https://gitea.io/en-us/>`_.
These published datasets are ordinary :term:`sibling`\s of your dataset, and among other advantages, they can constitute a back-up, an entry-point to retrieve your dataset for others or yourself, the backbone for collaboration on datasets, or the means to enhance visibility, findability and citeability of your work [#f1]_.
This section contains a brief overview on how to publish your dataset to different services.

Git repository hosting and annexed data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As outlined in a number of sections before, Git repository hosting sites typically do not support dataset annexes - some, like :term:`gin` however, do.
Depending on whether or not an annex is supported, you can push either only your Git history to the sibling, or the complete dataset including annexed file contents.
You can find out whether a sibling on a remote hosting services carries an annex or not by running the :command:`datalad siblings` command.
A ``+``, ``-``, or ``?`` sign in parenthesis indicates whether the sibling carries an annex, does not carry an annex, or whether this information isn't yet known.
In the example below you can see that a public GitHub repository `<https://github/psychoinformatics/studyforrest-data-phase2>`_ does not carry an annex on ``github``, but that the annexed data are served from an additional sibling ``mddatasrc`` (a :term:`special remote`).
Even though the dataset sibling on GitHub does not serve the data, it constitutes a simple, findable access point to retrieve the dataset, and can be used to provide updates and fixes via :term:`pull request`\s, issues, etc.

.. code-block:: bash

    # a clone of github/psychoinformatics/studyforrest-data-phase2 has the following siblings:
    $ datalad siblings
    .: here(+) [git]
    .: mddatasrc(+) [http://psydata.ovgu.de/studyforrest/phase2/.git (git)]
    .: origin(-) [git@github.com:psychoinformatics-de/studyforrest-data-phase2.git (git)]


There are multiple ways to create a dataset sibling on a repository hosting site to push your dataset to.

How to add a sibling on a Git repository hosting site: The manual way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#. Create a new repository via the webinterface of the hosting service of your choice.
   It does not need to have the same name as your local dataset, but it helps to associate local dataset and remote siblings.

.. find-out-more:: The webinterface for Gin

	.. figure:: ../artwork/src/GIN_newrepo.png

	   Webinterface of :term:`gin` during the creation of a new repository.

.. find-out-more:: The webinterface of GitHub

	.. figure:: ../artwork/src/newrepo-github.png

		Webinterface of :term:`github` during the creation of a new repository.

#. Afterwards, copy the :term:`SSH` or :term:`HTTPS` URL of the repository. Usually, repository hosting services will provide you with a convenient way to copy it to your clipboard. An SSH URL takes the form ``git@<hosting-service>:/<user>/<repo-name>.git`` and an HTTPS URL takes the form ``https://<hosting-service>/<user>/<repo-name>.git``. The type of URL you choose determines whether and how you will be able to ``push`` to your repository. Note that many services will require you to use the SSH URL to your repository in order to do :command:`push` operations, so make sure to take the :term:`SSH` and not the :term:`HTTPS` URL if this is the case.

#. If you pick the :term:`SSH` URL, make sure to have an :term:`SSH key` set up. This usually requires generating an SSH key pair if you do not have one yet, and uploading the public key to the repository hosting service.

.. _sshkey:

.. find-out-more:: What is an SSH key and how can I create one?
   :name: fom-sshkey

   An SSH key is an access credential in the :term:`SSH` protocol that can be used
   to login from one system to remote servers and services, such as from your private
   computer to an :term:`SSH server`. For repository hosting services such as :term:`GIN`,
   :term:`GitHub`, or :term:`GitLab`, it can be used to connect and authenticate
   without supplying your username or password for each action.

   This `tutorial by GitHub <https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_
   is a detailed step-by-step instruction to generate and use SSH keys for authentication,
   and it also shows you how to add your public SSH key to your GitHub account
   so that you can install or clone datasets or Git repositories via ``SSH`` (in addition
   to the ``http`` protocol), and the same procedure applies to GitLab and Gin.

   Don't be intimidated if you have never done this before -- it is fast and easy:
   First, you need to create a private and a public key (an SSH key pair).
   All this takes is a single command in the terminal. The resulting files are
   text files that look like someone spilled alphabet soup in them, but constitute
   a secure password procedure.
   You keep the private key on your own machine (the system you are connecting from,
   and that **only you have access to**),
   and copy the public key to the system or service you are connecting to.
   On the remote system or service, you make the public key an *authorized key* to
   allow authentication via the SSH key pair instead of your password. This
   either takes a single command in the terminal, or a few clicks in a web interface
   to achieve.
   You should protect your SSH keys on your machine with a passphrase to prevent
   others -- e.g., in case of theft -- to log in to servers or services with
   SSH authentication [#f2]_, and configure an ``ssh agent``
   to handle this passphrase for you with a single command. How to do all of this
   is detailed in the above tutorial.


#. Use the URL to add the repository as a sibling. There are two commands that allow you to do that; both require you give the sibling a name of your choice (common name choices are ``upstream``, or a short-cut for your user name or the hosting platform, but its completely up to you to decide):

   #. ``git remote add <name> <url>``
   #. ``datalad siblings-add --dataset . --name <name> --url <url>``

#. Push your dataset to the new sibling: ``datalad push --to <name>``


How to add a sibling on a Git repository hosting site: The automated way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad provides ``create-sibling-*`` commands to automatically create datasets on certain hosting sites.
DataLad versions ``0.16.0`` and higher contain more of these commands, and provide a more streamlined parametrization.
Please read the paragraph that matches your version of DataLad below, and be mindful of a change in command arguments between DataLad versions ``0.15.x`` and ``0.16.x``.

Using DataLad version < 0.16.0
""""""""""""""""""""""""""""""

If you are using DataLad version below ``0.16.0``, you can automatically create new repositories from the command line for :term:`GitHub` and :term:`GitLab` using the commands :command:`datalad create-sibling-github` and :command:`datalad create-sibling-gitlab`.
Due to the different representation of repositories on the two sites, the two commands are parametrized differently, and it is worth to consult each command's :term:`manpage` or ``--help``, but below are basic usage examples for the two commands:

**GitLab:**
Using :command:`datalad create-sibling-gitlab` is easiest with a ``python-gitlab`` configuration.
Please consult the ``python-gitlab`` `documentation <https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#configuration>`_ for details, but a basic configuration in the file ``~/.python-gitlab.cfg`` can look like this:

.. code-block::

	[global]
	default = gitlab
	ssl_verify = true
	timeout = 5

	[gitlab]
	url = https://gitlab.myinstance.com
	private_token = <super-secret-token>
	api_version = 4

This configures the default GitLab instance (here, we have called it ``gitlab``) with a specific base URL and the user's personal access token for authentication.
Note that you will need to generate and retrieve your own personal access token under the profile settings of the gitlab instance of your choice (see the :ref:`paragraph on authentication tokens below for more information <token>`).
With this configuration, the ``--site`` parameter can identify the GitLab instance by its name ``gitlab``.
If you have an :term:`SSH key` configured, it is useful to specify ``--access`` as ``ssh`` -- this saves you the need to authenticate with every ``push``:

.. code-block:: bash

   $ datalad create-sibling-gitlab \
     -d . \              	# current dataset
     --site gitlab \      	# to the configured GitLab instance
     --project DataLad-101 \	# repository name
     --layout flat \
     --access ssh 		# optional, but useful
	create_sibling_gitlab(ok): . (dataset)
	configure-sibling(ok): . (sibling)
	action summary:
	  configure-sibling (ok: 1)
	  create_sibling_gitlab (ok: 1)
   $ datalad siblings
     here(+) [git]
	 jugit(-) [git@gitlab.myinstance.com:<user>/<repo>.git (git)]
   $ datalad push --to gitlab
	publish(ok): . (dataset)
	action summary:
	  publish (ok: 1)


**GitHub:**
The command :command:`datalad create-sibling-github` requires a personal access token from GitHub (see the :ref:`paragraph on authentication tokens below for more information <token>`).
When you are using it for the first time, you should be queried interactively for it.
Subsequently, your token should be stored internally.
If you have an :term:`SSH key` configured, it is useful to specify ``--access-protocol`` as ``ssh`` -- this saves you the need to authenticate with every ``push``.

.. code-block:: bash

    $ datalad create-sibling-github \
      -d . \ 				# current dataset
      DataLad-101 \     		# repository name
      --access-protocol ssh 		# optional, but useful
    You need to authenticate with 'github' credentials. https://github.com/settings/tokens provides information on how to gain access
    token: <my-super-secret-token>
    create_sibling_github(ok): . (dataset) [Dataset sibling 'github', project at https://github.com/adswa/DataLad-101.git]
    configure-sibling(ok): . (sibling)
    action summary:
      configure-sibling (ok: 1)
      create_sibling_github (ok: 1)
    $ datalad push --to github
    publish(ok): . (dataset)
    action summary:
      publish (ok: 1)


Using DataLad version 0.16.0 and higher
"""""""""""""""""""""""""""""""""""""""

Starting with DataLad version ``0.16.0`` or higher, you can automatically create new repositories from the command line for :term:`GitHub`, :term:`GitLab`, :term:`gin`, `Gogs <https://gogs.io/>`__, or `Gitea <https://gitea.io/en-us/>`__.
This is implemented with a new set of commands called :command:`create-sibling-github`, :command:`create-sibling-gitlab`, :command:`create-sibling-gin`, :command:`create-sibling-gogs`, and :command:`create-sibling-gitea`.

.. gitusernote:: Get DataLad features ahead of time by installing from a commit

   If you want to get this feature ahead of the ``0.16.0`` release, you can install the most recent version of the :term:`master` :term:`branch` or a specific :term:`commit` hash from GitHub, for example with

   .. code-block::

      $ pip install git+git://github.com/datalad/datalad.git@master

   When getting features ahead of time, your feedback is especially valuable. If you find that something
   does not work, or if you have an idea for improvements, please `get in touch <https://github.com/datalad/datalad/issues/new>`_.

Each command is slightly tuned towards the peculiarities of each particular platform, but the most important common parameters are streamlined across commands as follows:

- ``[REPONAME]`` (required): The name of the repository on the hosting site. It will be created under a user's namespace, unless this argument includes an organization name prefix. For example, ``datalad create-sibling-github my-awesome-repo`` will create a new repository under ``github.com/<user>/my-awesome-repo``, while ``datalad create-sibling-github <orgname>/my-awesome-repo`` will create a new repository of this name under the GitHub organization ``<orgname>`` (given appropriate permissions).
- ``-s/--name <name>`` (required): A name under which the sibling is identified. By default, it will be based on or similar to the hosting site. For example, the sibling created with ``datalad create-sibling-github`` will  be called ``github`` by default.
- ``--credential <name>`` (optional): Credentials used for authentication are stored internally by DataLad under specific names. These names allow you to have multiple credentials, and flexibly decide which one to use. When ``--credential <name>`` is the name of an existing credential, DataLad tries to authenticate with the specified credential; when it does not yet exist DataLad will prompt interactively for a credential, such as an access token, and store it under the given ``<name>`` for future authentications. By default, DataLad will name a credential according to the hosting service URL it used for, for example ``datalad-api.github.com`` as the default for credentials used to authenticate against GitHub.
- ``--access-protocol {https|ssh|https-ssh}`` (default ``https``): Whether to use :term:`SSH` or :term:`HTTPS` URLs, or a hybrid version in which HTTPS is used to *pull* and SSH is used to *push*. Using :term:`SSH` URLs requires an :term:`SSH key` setup, but is a very convenient authentication method, especially when pushing updates -- which would need manual input on user name and token with every ``push`` over HTTPS.
- ``--dry-run`` (optional): With this flag set, the command will not actually create the target repository, but only perform tests for name collisions and report repository name(s).
- ``--private`` (optional): A switch that, if set, makes sure that the created repository is private.

Other streamlined arguments, such as ``--recursive`` or ``--publish-depends`` allow you to perform more complex configurations, for example publication of dataset hierarchies or connections to :term:`special remote`\s. Upcoming walk-throughs will demonstrate them.

Self-hosted repository services, e.g., Gogs or Gitea instances, have an additional required argument, the ``--api`` flag.
It needs to point to the URL of the instance, for example ``datalad create-sibling-gogs my_repo_on_gogs  --api "https://try.gogs.io"``


.. _token:

Authentication by token
^^^^^^^^^^^^^^^^^^^^^^^

To create or update repositories on remote hosting services you will need to set up appropriate authentication and permissions.
In most cases, this will be in the form of an authorization token with a specific permission scope.

What is a token?
""""""""""""""""

Personal access tokens are an alternative to authenticating via your password, and take the form of a long character string, associated with a human-readable name or description.
If you are prompted for ``username`` and ``password`` in the command line, you would enter your token in place of the ``password`` [#f3]_.
Note that you do not have to type your token at every authentication -- your token will be stored on your system the first time you have used it and automatically reused whenever relevant.

.. find-out-more:: How does the authentication storage work?

   Passwords, user names, tokens, or any other login information is stored in
   your system's (encrypted) `keyring <https://en.wikipedia.org/wiki/GNOME_Keyring>`_.
   It is a built-in credential store, used in all major operating systems, and
   can store credentials securely.

You can have multiple tokens, and each of them can get a different scope of permissions, but it is important to treat your tokens like passwords and keep them secret.

Which permissions do they need?
"""""""""""""""""""""""""""""""

The most convenient way to generate tokens is typically via the webinterface of the hosting service of your choice.
Often, you can specifically select which set of permissions a specific token has in a drop-down menu similar (but likely not identical) to this screenshot from GitHub:

.. figure:: ../artwork/src/github-token.png

   Webinterface to generate an authentication token on GitHub. One typically has to set a name and
   permission set, and potentially an expiration date.

For creating and updating repositories with DataLad commands it is usually sufficient to grant only repository-related permissions.
However, broader permission sets may also make sense.
Should you employ GitHub workflows, for example, a token without "workflow" scope could not push changes to workflow files, resulting in errors like this one::

    [remote rejected] (refusing to allow a Personal Access Token to create or update workflow `.github/workflows/benchmarks.yml` without `workflow` scope)]




.. rubric:: Footnotes


.. [#f1] Many repository hosting services have useful features to make your work citeable.
         For example, :term:`gin` is able to assign a :term:`DOI` to your dataset, and GitHub allows ``CITATION.cff`` files.

.. [#f2] Your private SSH key is incredibly valuable, and it is important to keep
         it secret!
         Anyone who gets your private key has access to anything that the public key
         is protecting. If the private key does not have a passphrase, simply copying
         this file grants a person access!

.. [#f3]  GitHub `deprecated user-password authentication <https://developer.github.com/changes/2020-02-14-deprecating-password-auth/>`_ and only supports authentication via personal access token from November 13th 2020 onwards. Supplying a password instead of a token will fail to authenticate.
