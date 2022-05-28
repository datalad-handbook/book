.. _extensions_create:

Create your own extension 
-------------------------

If your use case is not covered by DataLad's built-in functionality or by the
variety of `available DataLad extensions <https://pypi.org/search/?q=datalad>`_,
DataLad provides a mechanism for extending particular functionality or for providing
entire command suites via the `DataLad extension template <https://github.com/datalad/datalad-extension-template>`_.

Since DataLad extensions are proper Python packages, there can be a significant
amount of boilerplate code involved in the creation of a new extension. The
extension template removes this overhead from the developer by providing a
standard setup for Python packaging, test suite registration, and documentation.
It also contains a demo command suite that is automatically exposed via DataLad's
standard command line and Python API.

In this section, we provide an overview of the main content of the extension template,
as well the steps to follow when creating your own extension from the template.


The DataLad extension template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Apart from some standard git-, GitHub, versioning-, and Python packaging-specific
files, the extension template has the following core content:

- ``setup.cfg``: which contains the main metadata for the extension and 
  provides the means to specify package requirements and entry points for
  command and test suites.
- ``datalad_helloworld/``: which contains a basic implementation of an
  extension command suite (in the template: ``hello_cmd``) and demonstrates
  how extension command classes should inherit from DataLad classes in order
  for them to be exposed via the DataLad command line and Python API.
- ``docs/``: which contains a basic implementation of `Sphinx <https://www.sphinx-doc.org/en/master/index.html#>`_
  for document generation.
- ``.appveyor.yml``: which contains the setup for continuous integration
  with `Appveyor <https://www.appveyor.com/>`_.
- ``.codeclimate.yml``: which contains the setup for automated code review
  for test coverage, maintainability and more with `Code Climate <https://codeclimate.com/>`_
- ``requirements-devel.txt``: which lists the requirements for a pip-based
  development environment installation


Using the extension template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To develop your own extension, you can follow these steps to adjust the template
according to your own specifications:

1. **Create your extension repository** `from the DataLad extension template <https://github.com/datalad/datalad-extension-template/generate>`_
2. **Add your extension name**, which can be done by looking through the
   source code and replacing ``datalad_helloworld`` with ``datalad_<newname>``
   (hint: ``git grep datalad_helloworld`` should find all spots).
3. **Replace the example command implementation with your own**:
      - First replace the ``HelloWorld`` class with your own class implementation.
      - Then adjust the ``command_suite`` in ``datalad_helloworld/__init__.py`` by replacing the reference to ``HelloWorld`` with a reference to your newly implemented class.
4. **Allow automatic testing of extension installation** by replacing
   ``hello_cmd`` in ``datalad_helloworld/tests/test_register.py`` with
   the name of the new command.
5. **Update your documentation** in ``docs/source/index.rst`` by following 
   the guidelines on documentation building, testing, and publishing provided in
   ``docs/README.md``.
6. **Replace the main README** content of your repository with a description of your
   extension, including standard information such as an overview, installation
   instructions, documentation, and contributing guidelines.
7. **Update** ``setup.cfg`` with appropriate metadata on the new extension,
   including the Python version (``python_equires``), package requirements
   (``install_requires``) and entry points for command or testing suites
   (``datalad.extensions``)
8. **Publish your extension**, e.g. on GitHub.
9.  **Activate/link external services**, such as Appveyor for continuous
    integration, or `Read The Docs <https://readthedocs.org/>`_ for documentation.
10.  If you've written an extension that provides important functionality for you or your community, consider **registering your extension** at `github.com/datalad/datalad-extensions <https://github.com/datalad/datalad-extensions>`_ in order to test your extension's functionality against future DataLad releases and ensure interoperability across software versions. Ideally, `open an issue <https://github.com/datalad/datalad-extensions/issues/new>`_ to get in touch with the DataLad developers about this.  