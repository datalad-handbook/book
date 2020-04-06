.. _providers:

Configure custom data access
----------------------------

DataLad can download files via the ``http``, ``https``, ``ftp``, and ``s3``
protocol from various data storage solutions via its downloading commands
(:command:`datalad download-url`, :command:`datalad addurls`,
:command:`datalad get`).
If data retrieval from a storage solution requires *authentication*,
i.e., for example via a username and password combination, DataLad provides an
interface to query, request, and store the most common type of credentials that
are necessary to authenticate, for a range of authentication types.
There are a number of natively supported types of authentication and out-of-the
box access to a broad range of access providers, from common solutions such as
`S3 <https://aws.amazon.com/s3/?nc1=h_ls>`_ to special purpose solutions, such as
`LORIS <https://loris.ca/>`_. However, beyond natively supported services,
custom data access can be configured as long as the required authentication
and credential type are supported. This makes DataLad even more flexible for
retrieving data.

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


If a particular storage solution requires authentication but it is not known
to DataLad yet, the download will fail. Here is how this looks like if data is
retrieved from a server that requires HTTP authentication, but is not configured
for data access::

   $ datalad download-url  https://example.com/myuser/protected/path/to/file
     [INFO   ] Downloading 'https://example.com/myuser/protected/path/to/file' into 'local/path/file'
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
The following information is needed: An arbitrary name that the data access is
identified with, a regular expression that can match a url one would want to
download from, an authentication type, and a credential type. The example
below sheds some light one this.

.. findoutmore:: Which authentication and credential types are possible?

   When configuring custom data access, credential and authentication type
   are required information. Below, we list the most common choices for these fields.

   Among the most common credential types, ``'user_password'``, ``'aws-s3'``, and
   ``'token'`` authentication is supported. For a full list, including some
   less common authentication types, please see the technical documentation
   of DataLad.

   For authentication, the most common supported solutions are ``'html_form'``,
   ``'http_auth'`` (   `http and html form-based authentication <https://en.wikipedia.org/wiki/HTTP%2BHTML_form-based_authentication>`_),
   ``'http_basic_auth'`` (`http basic access <https://en.wikipedia.org/wiki/Basic_access_authentication>`_),
   ``'http_digest_auth'`` (   `digest access authentication <https://en.wikipedia.org/wiki/Digest_access_authentication>`_),
   ``'bearer_token'`` (`http bearer token authentication <https://tools.ietf.org/html/rfc6750>`_)
   and ``'aws-s3'``. A full list can be found in the technical docs.


Example: Data access to a server that requires basic HTTP authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a private `Apache webserver <https://httpd.apache.org/>`_ with an
``.htaccess`` file that configures a range of allowed users to access a certain
protected directory on this server via
`basic HTTP authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_.
If opened in a browser, such a setup would prompt visitors of this directory on
the webserver for their username and password, and only grant access if valid
credentials are entered. Unauthenticated requests cause ``401 Unauthorized Status``
responses.

By default, when DataLad attempts to retrieve files from this protected directory,
the authentication and credential type that are required are unknown to DataLad
and authentication fails. An attempt to download or get a file from this directory
with DataLad can only succeed if a "provider configuration", i.e., a configuration
how to access the data, for this specific webserver with information on how to
authenticate exists.

"Provider configurations" are small text files that exist on a per-dataset level
in ``.datalad/providers/<name>.cfg``. They can be created and saved to the dataset
by hand, or configured "on the fly" from the command line upon unsuccessful
download attempts. A configuration file follows a similar structure as the example
below:

.. code-block:: bash

   [provider:example.com]
   url_re = https://example.com/~myuser/protected/.*
   credential = example.com/~myuser
   authentication_type = http_basic_auth

   [credential:example.com/~myuser]
   type = user_password

In the dataset that this file was placed into, downloading commands
that point to ``https://example.com/~myuser/protected/<path>`` will ask (once) for
the user's user name and password, and subsequently store these credentials.

If the file is generated "on the fly" from the terminal, it will prompt for
exactly the same information as specified in the example above and write the
required ``.cfg`` based on the given information. Here is how that would look like::

   $ datalad download-url  https://example.com/~myuser/protected/my_protected_file
    [INFO   ] Downloading 'https://example.com/~myuser/protected/my_protected_file' into '/tmp/ds/'
    Authenticated access to https://example.com/~myuser/protected/my_protected_file has failed.
    Would you like to setup a new provider configuration to access url? (choices: [yes], no): yes

    New provider name
    Unique name to identify 'provider' for https://example.com/~myuser/protected/my_protected_file [https://example.com]: my-webserver

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
    https://example.com/~myuser/protected/my_protected_file:   0%| | 0.00/611k                                                                                                                                                                                                                                                 download_url(ok): /tmp/xnat2/0015911870_1.3.12.2.1107.5.2.32.35135.2011102112040130362336780.dcm (file)
    add(ok): my_protected_file (file)
    save(ok): . (dataset)
    action summary:
      add (ok: 1)
      download_url (ok: 1)
      save (ok: 1)

Subsequently, all downloads from ``https://example.com/~myuser/protected/*`` will
succeed.