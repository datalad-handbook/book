.. _ukbatjsc:

Processing the UKBiobank FAIRly
-------------------------------



- probably split into data transfer aspects (download, staging, storage),
  (pre)processing (CAT, fMRIprep), layout/structure, potentially a section with
  caveats or gotchas that we discovered.

Preprocessing with fMRIprep
^^^^^^^^^^^^^^^^^^^^^^^^^^^

`fMRIprep <https://fmriprep.readthedocs.io/en/stable/index.html>`_ is a
containarized preprocessing pipeline for fMRI data based on
`nipype <https://nipype.readthedocs.io/en/latest/>`_ and using tools from
`FSL <https://fsl.fmrib.ox.ac.uk/fsl/fslwiki>`_, `ANTS <http://picsl.upenn.edu/software/ants/>`_,
`FreeSurfer <https://surfer.nmr.mgh.harvard.edu/>`_, and
`AFNI <https://afni.nimh.nih.gov/>`_,
It performs basic processing steps (coregistration, normalization, unwarping,
noise component extraction, segmentation, skullstripping, etc.) and provides
outputs that can be used for a variety of group level analyses, including
task-based or resting-state fMRI, graph theory measures, surface or
volume-based statistics, and others.
For preprocessing the UKBiobank data, fMRIprep version ???? was run in a
`Singularity <https://sylabs.io/>`_ container via :command:`datalad containers-run`.

Testing and simulations
^^^^^^^^^^^^^^^^^^^^^^^

The size of the dataset led to the uncomfortable situation of "mistakes are
bloody painful". Any re-downloading, re-structuring, or re-preprocessing that
would need to be done to fix mistakes would not take hours or days, but
consume weeks. If software components turned out to be buggy, or if
proposed solutions happened to not scale as expected, the complete project
was under threat. What made this worse was that the project was unprecedented,
and that many software components have never been tested to work at this scale.
Therefore, the project involved many simulations and thorough data testing that
are described in more detail in the hidden section below.

.. findoutmore:: Testing and simulations

   **Subdataset scaling**:
   The first considerations concerned the number of subdatasets. Previous efforts
   such as preparing the Human Connectome Project Data as a DataLad dataset
   (see :ref:`usecase_HCP_dataset`) demonstrated that subdataset nesting is robust and
   scalable. Nevertheless: Wrapping up the HCP dataset involved a superdataset
   with 4500 subdatasets - wrapping up the UKBiobank dataset would involve
   a superdataset with 100.000 subdatasets.

   In order to find out whether 40k (the amount of subdatasets to start with)
   and 100k (the final amount) subdatasets are possible at all, simulations
   were consulted.

   .. findoutmore:: Simulating large dataset hierarchies

      In principle, simulations like this are simple. Here is an example:

      .. code-block:: bash

         #!/bin/bash
         set -x

         # build a dummy subdataset to be referenced 40k times:
         datalad create dummy_sub
         echo "whatever" > dummy_sub/some_file
         datalad save -d dummy_sub

         sub_id=$(datalad -f "{infos[dataset][id]}"  wtf -d dummy_sub)
         sub_commit=$(git -C dummy_sub show --no-patch --format=%H)


         # the actual super dataset and use some config procedure to get
         # an initial history
         datalad create -c yoda dummy_super_100k

         cd dummy_super_100k

         for ((i=1;i<=100000;i++)); do
             git config -f .gitmodules "submodule.sub$i.path" "sub$i";
             git config -f .gitmodules "submodule.sub$i.url" ../dummy_sub;
             git config -f .gitmodules "submodule.sub$i.datalad-id" "$sub_id";
             git update-index --add --replace --cacheinfo 160000 "$sub_commit" "sub$i";
         done;

         git add .gitmodules
         git commit -m "Add submodules"

      This creates a subdataset with 100k subdatasets in ``dummy_super_100k``,
      but with a twist:

      - One test dataset (``dummy_sub``) with some test content (``some_file``),
        and one super dataset (``dummy_super_100k``) is created.
      - Instead of cloning the subdataset 100k times into the superdataset (which would
        lead to a directory with 100k subdirectories), only *Git's index* is updated
        with the `git update-index <https://git-scm.com/docs/git-update-index>`_
        command. Thus, it appears afterwards as if 100k subdirectories have
        been deleted.
      - Subdataset information is written "manually" (instead via cloning as
        subdatasets) by simply adding the relevant information into the
        ``.gitmodules`` file and saving it.

      This is a time efficient hack that allows to simulate dataset nesting
      scalability, without actually clogging the filesystem with tens of thousands
      of files.

   The next line of though concerned RIA stores. Just like a dataset with 100k subdatasets
   had never before been attempted, neither had a RIA store with 100k archived
   datasets ever been constructed or used.

   .. findoutmore:: TODO: how we checked the RIA store

      TODO