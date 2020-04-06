.. _providers:

Configure custom data access
----------------------------

DataLad can download files via the ``http``, ``https``, ``ftp``, and ``s3``
protocol from various data storage solutions via its downloading commands
(:command:`datalad download-url`, :command:`datalad addurls`,
:command:`datalad get`).
*Authentication* during such retrieval is the process by which is verified that
someone is who they claim they are, for example via a username and password
combination. If data retrieval from a storage solution requires authentication,
DataLad provides an interface to query, request, and store the most common
type of credentials that are necessary to authenticate, for a range of
authentication types.
There are a number of natively supported types of authentication and out-of-the
box access to a broad range of access providers, from common solutions such as
`S3 <https://aws.amazon.com/s3/?nc1=h_ls>`_ to special purpose solutions, such as
`LORIS <https://loris.ca/>`_. For any supported access type that requires
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
``.datalad/providers``.
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
the user's user name and password, and subsequently store these credentials