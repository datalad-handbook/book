.. _providers:

Configuring new data providers
------------------------------

DataLad can download files via the ``http``, ``https``, ``ftp``, and ``s3``
protocol. If data retrieval requires authentication, DataLad's provides an interface to
query, request, and store the most common type of credentials. An example of this
is shown in the usecase :ref:`usecase_HCP_dataset`: :command:`datalad get` will
ask for AWS S3 credential to retrieve data that is stored in S3 buckets from
the command line once, and -- given valid credentials -- download the files
and all future files from this bucket right away. There
are a number of natively supported types of authentication (a list is given in
the hidden section below) and out-of-the box access to a broad range
of providers such as `S3 <https://aws.amazon.com/s3/?nc1=h_ls>`_ or
`LORIS <https://loris.ca/>`_.
If you attempt to retrieve data from supported providers that require authentication,
you will be prompted for your credentials from the command line at the time of
the first download, and subsequent downloads handle authentication in the background.

If a provider requires authentication but it is not known to DataLad yet, the
download will fail. However, the provider can be configured by
the user to enable interactions with it.
With a provider configuration in place, commands such as :command:`datalad download-url`
or :command:`datalad add-urls` can work with urls of custom providers, and
:command:`datalad get` is enabled to retrieve file contents from these sources.
The configuration can either be done in the terminal upon a prompt from the
command line when a download fails due to a missing provider configuration,
or by placing provider-specific configuration files into ``.datalad/providers``.

In order to configure a provider configuration, one needs to input a
provider name, a regular expression that can match a url one would want to download
from, an authentication type, and a credential type. The example below sheds some
light one this.

.. findoutmore:: Which authentication and credential types are possible?

   The following credential types are supported:

   - ``'user_password'``
   - ``'aws-s3'``
   - ``'nda-s3'``
   - ``'token'``
   - ``'loris-token'``

   The following authentication types are supported:

   - ``'html_form'``
   - ``'http_auth'``
   - ``'http_basic_auth'``
   - ``'http_digest_auth'``
   - ``'bearer_token'``
   - ``'aws-s3'``
   - ``'nda-s3'``
   - ``'loris-token'``

   Some pointers to read up more on these authetication types are here:
   `http basic access <https://en.wikipedia.org/wiki/Basic_access_authentication>`_,
   `http and html form-based authentication <https://en.wikipedia.org/wiki/HTTP%2BHTML_form-based_authentication>`_,
   `digest access authentication <https://en.wikipedia.org/wiki/Digest_access_authentication>`_,
   `http bearer token authentication <https://tools.ietf.org/html/rfc6750>`_.

Example: DataLad access to an XNAT server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`XNAT <https://www.xnat.org/about/>`_ is an open source imaging informatics platform
and it allows for data download after authentication.
In order to allow file retrieval from a custom deployed
`XNAT server <https://www.xnat.org/about/>`_ with DataLad, a file following a
similar structure as the example below (with adjusted urls and ports)
can be placed into ``.datalad/providers/xnat.cfg``:

.. code-block:: bash

   [provider:xnat]
   url_re = https://nmrxnat.ime.kfa-juelich.de:8443/xnat/.*
   credential = nmrxnat.ime.kfa-juelich.de:8443/xnat
   authentication_type = http_basic_auth

   [credential:nmrxnat.ime.kfa-juelich.de:8443/xnat]
   type = user_password

In the dataset that this file was placed into, downloading commands such as
:command:`datalad download-url` that point to
``https://nmrxnat.ime.kfa-juelich.de:8443/xnat`` will work and ask (once) for
the user's user name and password.