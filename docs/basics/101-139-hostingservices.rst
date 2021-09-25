.. _share_hostingservice:

Publishing datasets to Git repository hosting
---------------------------------------------

Because DataLad datasets are :term:`Git` repositories, it is possible to
:command:`push` datasets to any Git repository hosting service, such as
:term:`GitHub`, :term:`GitLab`, :term:`Gin`, :term:`Bitbucket`, `Gogs <https://gogs.io/>`_,
or `Gitea <https://gitea.io/en-us/>`_.


How to add a sibling on a Git repository hosting site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are multiple ways to create a dataset sibling on a repository hosting site to push your dataset to.


The manual way
""""""""""""""

#. Create a new repository via the webinterface of the hosting service of your choice.
   It does not need to have the same name as your local dataset, but it helps to associate local dataset and remote siblings.

.. figure:: ../artwork/src/GIN_newrepo.png

   Webinterface of :term:`gin` during the creation of a new repository.

#. Afterwards, copy the :term:`SSH` URL of the repository. Usually, repository hosting services will provide you with a convenient way to copy it to your clipboard. An SSH URL takes the following form: ``git@<hosting-service>:/<user>/<repo-name>.git``. Note that almost all services will require you to use the SSH URL to your repository in order to do :command:`push` operations, so make sure to take the :term:`SSH` and not the :term:`HTTPS` URL.

#. Make sure to have an :term:`SSH key` set up. This usually requires generating an SSH key pair if you do not have one yet, and uploading the public key to the repository hosting service.

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


#. Use the SSH URL to add the repository as a sibling. There are two commands that allow you to do that; both require you give the sibling a name of your choice:

   #. ``git remote add <name> <ssh-url>``
   #. ``datalad siblings-add --dataset . --name <name> --url <ssh-url>``

#. Push your dataset to the new sibling.
