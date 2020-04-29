.. _hirni_summary:

Summary
-------

``datalad-hirni`` is a neuroimaging specific extension for DataLad that aims to
make the process of converting raw neuroimaging data into BIDS compliant datasets
easier and reproducible.

- A DICOM to BIDS dataset conversion workflow can be started whenever it fits -
  be it right with the start of the MR acquisitions, or only years after the last
  DICOMs left the scanner. In the former case, continuous command line calls to
  import and edit specs are simple and easily included into the rest of the study
  acquisition routine. In the latter case, the complete process could be written
  up in a bash script

- Technically, ``hirni`` and its general approach are not limited to neuroimaging.
  If you are willing to invest time and thought, ``hirni``\s routines can
  accomplish conversions to other standards or structures.

Now what can I do with it?
^^^^^^^^^^^^^^^^^^^^^^^^^^

Reproducibly BIDSify all the neuroimaging studies!

.. todo::

   Find the marie kondo "BIDS sparks joy" meme from twitter again and add it