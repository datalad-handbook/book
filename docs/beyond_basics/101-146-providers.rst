.. _providers:

Configure custom data access
----------------------------

DataLad can download files via the ``http``, ``https``, ``ftp``, and ``s3``
protocol from various data storage solutions via its downloading commands
(:command:`datalad download-url`, :command:`datalad addurls`,
:command:`datalad get`).
If data retrieval from a storage solution requires *authentication*,
for example via a username and password combination, DataLad provides an
interface to query, request, and store the most common type of credentials that
are necessary to authenticate, for a range of authentication types.
There are a number of natively supported types of authentication and out-of-the
box access to a broad range of access providers, from common solutions such as
`S3 <https://aws.amazon.com/s3/?nc1=h_ls>`_ to special purpose solutions, such as
`LORIS <https://loris.ca/>`_. However, beyond natively supported services,
custom data access can be configured as long as the required authentication
and credential type are supported.
In addition, starting with DataLad version ``0.16``, authentication can be
"outsourced" to Git's `credential helper <https://git-scm.com/docs/gitcredentials>`_ and vice versa.
This makes DataLad even more flexible for retrieving data, and can allow tools like Git to use DataLad's credentials as well.

Basic process
^^^^^^^^^^^^^

For any supported access type that requires
authentication, the procedure is always the same:
Upon first access via any downloading command, users will be prompted for their
credentials from the command line. Subsequent downloads handle authentication
in the background as long as the credentials stay valid. An example of this
credential management is shown in the usecase :ref:`usecase_HCP_dataset`:
Data is stored in S3 buckets that require authentication with AWS credentials.
The first :command:`datalad get` to retrieve any of the data will prompt for
the credentials from the terminal. If the given credentials are valid, the
requested data will be downloaded, and all subsequent retrievals via
:command:`get` will authenticate automatically, without user input, as long as
the entered credentials stay valid.

.. find-out-more:: How does the authentication work?

   Passwords, user names, tokens, or any other login information is stored in
   your system's (encrypted) `keyring <https://en.wikipedia.org/wiki/GNOME_Keyring>`_.
   It is a built-in credential store, used in all major operating systems, and
   can store credentials securely.
   DataLad uses the `Python keyring <https://keyring.readthedocs.io/en/latest/>`_
   package to access the keyring. In addition to a standard interface to the
   keyring, this library also has useful special purpose backends that come in
   handy in corner cases such as HPC/cluster computing, where no interactive
   sessions are available.

If a particular storage solution requires authentication but it is not known
to DataLad yet, the download will fail. Here is how this looks like if data is
retrieved from a server that requires HTTP authentication, but DataLad -- or the
dataset -- lacks a configuration for data access about this server::

   $ datalad download-url  \
     https://example.com/myuser/protected/path/to/file
     [INFO   ] Downloading 'https://example.com/myuser/protected/path/to/file' into 'local/path/'
     Authenticated access to https://example.com/myuser/protected/path/to/file has failed.
     Would you like to setup a new provider configuration to access url? (choices: [yes], no): yes

However, data access can be configured by
the user if the required authentication and credential type are supported by
DataLad (a list is given in the hidden section below).
With a data access configuration in place, commands such as
:command:`datalad download-url` or :command:`datalad addurls` can work with urls
the point to the location of the data to be retrieved, and
:command:`datalad get` is enabled to retrieve file contents from these sources.

The configuration can either be done in the terminal upon a prompt from the
command line when a download fails due to a missing provider configuration as
shown above, or by placing a configuration file for the required data access into
``.datalad/providers/<provider-name>.cfg``.
The following information is needed:

- An arbitrary name that the data access is identified with,
- a regular expression that can match a url one would want to download from,
- an authentication type, and
- a credential type.

The example below sheds some light one this.

.. find-out-more:: Which authentication and credential types are possible?

   When configuring custom data access, credential and authentication type
   are required information. Below, we list the most common choices for these fields.

   Among the most common credential types, ``'user_password'``, ``'aws-s3'``, and
   ``'token'`` authentication is supported. For a full list, including some
   less common authentication types, please see the technical documentation
   of DataLad.

   For authentication, the most common supported solutions are ``'html_form'``,
   ``'http_auth'`` (   `http and html form-based authentication <https://www.javaxt.com/wiki/Tutorials/Javascript/Form_Based_HTTP_Authentication>`_),
   ``'http_basic_auth'`` (`http basic access <https://en.wikipedia.org/wiki/Basic_access_authentication>`_),
   ``'http_digest_auth'`` (   `digest access authentication <https://en.wikipedia.org/wiki/Digest_access_authentication>`_),
   ``'bearer_token'`` (`http bearer token authentication <https://tools.ietf.org/html/rfc6750>`_)
   and ``'aws-s3'``. A full list can be found in the technical docs.


Example: Data access to a server that requires basic HTTP authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a private `Apache web server <https://httpd.apache.org/>`_ with an
``.htaccess`` file that configures a range of allowed users to access a certain
protected directory on this server via
`basic HTTP authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_.
If opened in a browser, such a setup would prompt visitors of this directory on
the web server for their username and password, and only grant access if valid
credentials are entered. Unauthenticated requests cause ``401 Unauthorized Status``
responses.

By default, when DataLad attempts to retrieve files from this protected directory,
the authentication and credential type that are required are unknown to DataLad
and authentication fails. An attempt to download or get a file from this directory
with DataLad can only succeed if a "provider configuration", i.e., a configuration
how to access the data, for this specific web server with information on how to
authenticate exists.

"Provider configurations" are small text files that either exist on a per-dataset
level in ``.datalad/providers/<name>.cfg``, or on a user-level in
``~/.config/datalad/providers/<name>.cfg``. They can be created and saved
by hand, or configured "on the fly" from the command line upon unsuccessful
download attempts. A configuration file follows a similar structure as the example
below:

.. code-block:: bash

   [provider:my-webserver]
   url_re = https://example.com/~myuser/protected/.*
   credential = my-webserver
   authentication_type = http_basic_auth

   [credential:my-webserver]
   type = user_password

For a *local* [#f1]_, i.e., dataset-specific, configuration, place the file into
``.datalad/providers/my-webserver.cfg``. Subsequently, in the dataset that
this file was placed into, downloading commands that point to
``https://example.com/~myuser/protected/<path>`` will ask (once) for
the user's user name and password, and subsequently store these credentials.
In order to make it a *global* configuration,
i.e., enable downloads from the web server from within all datasets of the user,
place the file into the users home directory under
``~/.config/datalad/providers/my-webserver.cfg``.

If the file is generated "on the fly" from the terminal, it will prompt for
exactly the same information as specified in the example above and write the
required ``.cfg`` based on the given information. Note that this will configure
data access *globally*, i.e., it will place the file under
``~/.config/datalad/providers/<name>.cfg``. Here is how that would look like::

   $ datalad download-url  https://example.com/~myuser/protected/my_protected_file
    [INFO   ] Downloading 'https://example.com/~myuser/protected/my_protected_file' into '/tmp/ds/'
    Authenticated access to https://example.com/~myuser/protected/my_protected_file has failed.
    Would you like to setup a new provider configuration to access url? (choices: [yes], no): yes

    New provider name
    Unique name to identify 'provider' for https://example.com/~myuser/protected/my_protected_file [https://example.com]:
    my-webserver

    New provider regular expression
    A (Python) regular expression to specify for which URLs this provider
    should be used [https://example\.com/\~myuser/protected/my_protected_file]:
    https://example.com/~myuser/protected/.*

    Authentication type
    What authentication type to use (choices: aws-s3, bearer_token, html_form,
    http_auth, http_basic_auth, http_digest_auth, loris-token, nda-s3, none, xnat):
    http_basic_auth

    Credential
    What type of credential should be used? (choices: aws-s3, loris-token, nda-s3,
    token, [user_password]):
    user_password

    Save provider configuration file
    Following configuration will be written to /home/me/.config/datalad/providers/my-webserver.cfg:
    # Provider configuration file created to initially access
    # https://example.com/~myuser/protected/my_protected_file

    [provider:my-webserver]
    url_re = https://example.com/~myuser/protected/.*
    authentication_type = http_basic_auth
    # Note that you might need to specify additional fields specific to the
    # authenticator.  Fow now "look into the docs/source" of <class 'datalad.downloaders.http.HTTPBasicAuthAuthenticator'>
    # http_basic_auth_
    credential = my-webserver

    [credential:my-webserver]
    # If known, specify URL or email to how/where to request credentials
    # url = ???
    type = user_password
     (choices: [yes], no):
    yes

    You need to authenticate with 'my-webserver' credentials.
    user: <user name>

    password: <password>
    password (repeat): <password>
    [INFO   ] http session: Authenticating into session for https://example.com/~myuser/protected/my_protected_file
    https://example.com/~myuser/protected/my_protected_file:   0%| | 0.00/611k
    download_url(ok): /https://example.com/~myuser/protected/my_protected_file (file)
    add(ok): my_protected_file (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 1)
      download_url (ok: 1)
      save (ok: 1)

Subsequently, all downloads from ``https://example.com/~myuser/protected/*``
by the user will succeed. If something went wrong during this interactive
configuration, delete or edit the file at ``~/.config/datalad/providers/<name>.cfg``.

Example: Data access via Git's credential system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a private repository on :term:`GitHub`.
When cloning such datasets via the :term:`https` protocol, every connection needs a user name and a password in the form of a `Personal Access Token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_.

.. code-block:: bash

   $ git clone https://github.com/adswa/my-super-secret-work.git
     Cloning into 'my-super-secret-work'...
     Username for 'https://github.com': <user-name>
     Password for 'https://github.com': <GitHub Access Token>

Because this can be tedious, Git has a credential system that can help to store and provide the necessary configurations automatically.
One of its pieces are so called `credential helper`, executables that ultimately store credentials for specific hosts, and will provide them automatically in place of an interactive query to the user.

This system is particularly flexible because Git allows users to create *custom* helpers that fit specific usecases.
Here is one example: A server contains a number of DataLad datasets, but a different and changing number of users of the shared computational infrastructure has access to each one.
In order to centralize and automate authentication, a system-wide Git configuration [#f1]_ is employed:

.. code-block:: bash

    $ git config --list
      credential.https://cool-dataset.ds.research-center.de.helper=/usr/local/bin/research-center_datastore_pw

This credential helper for host ``https://cool-dataset.ds.research-center.de`` points to an executable, ``/usr/local/bin/research-center_datastore_pw``, which determines, for example by querying a password database, whether the given user has access or not.
If they have, it returns the user name and password required for authentication to the Git process that tried to access the server.

Beginning with DataLad version ``0.16``, DataLad's own credential management can interface with Git's by its aforementioned mechanism of provider configurations.
A basic mock example can illustrate the necessary steps to set this up.

Here is a short list of preparations if you want to try this out for yourself:

#. Create a private repository on GitHub. This can be done via `GitHub's webinterface <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility#changing-a-repositorys-visibility>`_ or the ``--private`` flag of :command:`create-sibling-github` (requires DataLad version ``0.16`` or higher).
#. The repository should contain a file, like a simple ``README.md``, and can be a pure Git repository.
#. Ensure that all tokens in Git configurations files are commented out, because those would provide authentication as well. Running ``git config --list`` can give you an overview, but you can also check that ``git clone <repo>`` with a :term:`https` URL prompts for user name and password.

The challenge is to ``datalad download-url`` the file successfully.
This is difficult because the repository is private and requires authentication that DataLad is yet unaware about.
For fun, you can check that a download via ``wget`` from the command line also fails:

.. code-block:: bash

   # try to download a file from a private repo with this url scheme
   $ wget https://raw.githubusercontent.com/<username>/<reponame>/<branch-name>/<filename.txt>
   # should return a 404

To achieve a successful download, we will create a small, custom credential helper for Git, and tell DataLad about it with a provider configuration.
First, we will store the password on your system.
Create a `personal access token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_ on :term:`GitHub`, and, for simplicity, write it into a text file ``github`` in your home directory.
Please do note that it is highly discouraged to store passwords in plain files, and only done for demonstration here.

Next, we will write a credential helper that will retrieve this password.
Open your ``.gitconfig`` file in your home directory, and add the following contents to it, replacing the user name placeholder with your GitHub handle:

.. code-block:: bash

	[credential "https://raw.githubusercontent.com"]
		username = <your-user-name-here>
		helper = "!f() { echo \"password=$(cat ~/github)\"; }; f"

This configuration will be queried by Git when a URL matches ``https://raw.githubusercontent.com`` and runs the ``helper``, which here is a shell function that prints the string ``password=`` and the content of the file containing the token.
This function is rudimentary, but does the job for this illustration.

Finally, we will teach DataLad to use on this configuration to authenticate.
For this, create a new dataset, and, with your favourite editor, create a new provider configuration ``.datalad/providers/github.cfg`` in it.
Depending on your editor, you will need to create the directory ``providers`` under ``.datalad`` first.
This provider configuration should contain the following:

.. code-block:: bash

	[provider:github]
	  url_re = https://.*github.*\.com
	  authentication_type = http_basic_auth
	  credential = data_example_cred
	[credential:data_example_cred]
	  type = git

Importantly, the ``type`` key should specify ``git``, the ``provider:<name>`` name should match the name of the provider configuration filename, the ``url_re`` should be a regular expression that can match the credential URL in your ``.gitconfig`` file, and the ``credential`` value should be the same string as the ``[credential:<credential>]`` name.
With this setup, a ``datalad download-url`` succeeds, authenticating via the Git credential helper.

.. gitusernote:: Git authenticating via DataLad's credential system

   Not only can DataLad use Git's credential system, Git can also query credentials from DataLad.
   This requires DataLad version ``0.16`` or higher, and a Git configuration pointing to the credential helper ``git-credential-datalad`` for a given URL scheme:

   .. code-block:: bash

      [credential "https://*data.example.com"]
         helper = "datalad"

To find out more about DataLad's integration with Git's credential system, take a look into the more technical documentation at `docs.datalad.org/credentials.html <http://docs.datalad.org/credentials.html>`_ and `docs.datalad.org/design/credentials.html <http://docs.datalad.org/design/credentials.html>`_.

.. rubric:: Footnotes

.. [#f1] To re-read on configurations and their scope, check out chapter
         :ref:`chapter_config` again.