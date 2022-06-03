.. _summaryshare:

Summary
-------

Without access to the same computational infrastructure, you can share your
DataLad datasets with friends and collaborators by leveraging third party
services. DataLad integrates well with a variety of free or commercial services,
and with many available service options this gives you freedom in deciding where
you store your data and thus who can get access.

- An easy, free, and fast option is `GIN <https://gin.g-node.org>`_, a
  web-based repository store for scientific data management. If you are registered
  and have SSH authentication set up, you can create a new, empty repository,
  add it as a sibling to your dataset, and publish all dataset contents -- including
  annexed data, as GIN supports repositories with an annex.

- Other repository hosting services such as GitHub and GitLab [#f1]_ do not support
  an annex. If a dataset is shared via one of those platforms, annexed data needs
  to be published to an external data store. The published dataset stores
  information about where to obtain annexed file contents from such that a
  :command:`datalad get` works.

- The external data store can be any of a variety of third party hosting providers.
  To enable data transfer to and from this service, you (may) need to configure an
  appropriate :term:`special remote`, and configure a publication dependency. The
  section :ref:`sharethirdparty` walked you through how this can be done with
  `Dropbox <https://dropbox.com>`_.

- The ``--data`` and ``--force`` options of :command:`datalad push` allows to override
  automatic decision making on to-be-published contents. If it isn't specified,
  DataLad will attempt to figure out itself which and how dataset contents
  shall be published. With a path to files, directories, or subdatasets you
  can also publish only selected contents' data.


.. figure:: ../artwork/src/going_up.svg
   :width: 40%


Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Finally you can share datasets and their annexed contents with others without the
need for a shared computational infrastructure. It remains your choice where to
publish your dataset to -- considerations of data access, safety, or potential
costs will likely influence your choice of service.


.. rubric:: Footnotes

.. [#f1] Older versions of :term:`GitLab` provide a git-annex configuration, but it is disabled
         by default, and to enable it you would need to have administrative
         access to the server and client side of your GitLab instance.