.. _dataladdening:

Transitioning existing projects into DataLad
--------------------------------------------

Using DataLad offers exciting and useful features that warrant transitioning existing projects into DataLad datasets -- and in most cases, transforming your project into one or many DataLad datasets is easy.
This sections outlines the basic steps to do so, and offers examples as well as advice and caveats.

Important: Your safety net
^^^^^^^^^^^^^^^^^^^^^^^^^^

Chances are high that you are reading this section of the handbook after you stumbled across DataLad and were intrigued by its features, and you're now looking for a quick way to get going.
If you haven't read much of the handbook, but are now planning to DataLad-ify the gigantic project you have been working on for the past months or years, this first paragraph is warning, advice, and a call for safety nets to prevent unexpected misery that can arise from transitioning to a new tool.
Because while DataLad *can* do amazing things, you shouldn't blindly trust it to do everything *you* think it can or should do, but gain some familiarity with it.

If you're a DataLad novice, we highly recommend that you read through the :ref:`basics-intro` part of the handbook.
This part of the book provides you with a solid understanding of DataLad's functionality and a playground to experience working with DataLad.
If you're really pressed for time because your dog is sick, your toddler keeps eating your papers and your boss is behind you with a whip, the findoutmore below summarizes the most important sections from the Basics for you to read:

.. findoutmore:: The Basics for the impatient

   To get a general idea about DataLad, please read sections :ref:`philo` and :ref:`executive_summary` from the introduction (reading time: 15 min).

   To gain a good understanding of some important parts of DataLad, please read chapter :ref:`chapter_datasets`, :ref:`chapter_run`, and :ref:`chapter_gitannex` (reading time: 60 minutes).

   To become confident in using DataLad, sections :ref:`help`, :ref:`filesystem` can be very useful. Depending on your aim, :ref:`chapter_collaboration` (for collaborative workflows), :ref:`chapter_thirdparty` (for data sharing), or :ref:`chapter_yoda` (for data analysis) may contain the relevant background for you.

Prior to transforming your project, regardless of how advanced of a user you are, **we recommend to create a copy of it**.
We don't believe there is much that can go wrong from the software-side of things, but data is precious and backups a necessity, so better be safe than sorry.

Step 1: Planning
^^^^^^^^^^^^^^^^

The first step to DataLad-ify your project is to turn it into one or several nested datasets.
Whether you turn a project into a single dataset or several is dependent on the current size of your project and how much you expect it to grow overtime, but also on its contents.
You can find guidance on this in paragraph below.

The next step is to save dataset contents.
You should take your time and invest thought into this, as this determines the looks and feels of your dataset, in particular the decision on which contents should be saved into :term:`Git` or :term:`git-annex`.
The section :ref:`symlink` should give you some necessary background information, and the chapter :ref:`chapter_config` the relevant skills to configure your dataset appropriately.
You should consider the size, file type and modification frequency of files in your decisions as well as potential plans to share a dataset with a particular third party infrastructure.

Step 2: Dataset creation
^^^^^^^^^^^^^^^^^^^^^^^^

Transforming a directory into a dataset is done with :command:`datalad create --force`.
The ``-f``/``--force`` option enforces dataset creation in non-empty directories.
Consider :ref:`applying procedures <procedures>` with ``-c <procedure-name>`` do apply configurations that suit your use case.

.. findoutmore:: What if my directory is already a Git repository?

   If you want to transform a Git repository to a DataLad dataset, a :command:`datalad create -f` is the way to go, too, and completely safe.
   Your Git history will stay intact and will not be tempered with.

If you want to transform a series of nested directories into nested datasets, continue with :command:`datalad create -f` commands in all further subdirectories.

.. findoutmore:: One or many datasets?

   In deciding how many datasets you need, try to follow the benchmarks in chapter :ref:`chapter_gobig` and the yoda principles in section :ref:`yoda`.
   Two simple questions can help you make a decision:

   #. Do you have independently reusable components in your directory, for example data from several studies, or data and code/results? If yes, make each individual component a dataset.
   #. How large is each individual component? If it exceeds 100k files, split it up into smaller datasets. The decision on where to place subdataset boundaries can be guided by the existing directory structure or by common access patterns, for example based on data type (raw, processed, ...) or subject association. One straightforward organization may be a top-level superdataset and subject-specific subdatasets, mimicking the structure chosen in the use case :ref:`usecase_HCP_dataset`.

You can automate this with :term:`bash` loops, if you want.

.. findoutmore:: Example bash loops

   Consider a directory structure that follows a naming standard such as `BIDS <https://bids.neuroimaging.io/>`_::

      # create a mock-directory structure:
      $ mkdir -p study/sub-0{1,2,3,4,5}/{anat,func}
      $ tree study
      study
        ├── sub-01
        │   ├── anat
        │   └── func
        ├── sub-02
        │   ├── anat
        │   └── func
        ├── sub-03
        │   ├── anat
        │   └── func
        ├── sub-04
        │   ├── anat
        │   └── func
        └── sub-05
            ├── anat
            └── func

   Consider further that you have transformed the toplevel ``study`` directory into a dataset and now want to transform all ``sub-*`` directories into further subdatasets, registered in ``study``.
   Here is a line that would do this for the example above::

      $ for dir in study/sub-0{1,2,3,4,5}; do datalad -C $dir create --force; done

Step 3: Saving dataset contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any existing content in your newly created dataset(s) still needs to be saved into its dataset at this point (unless it was already under version control with Git).
This can be done with the :command:`datalad save` command -- either "in one go" using a plain ``datalad save`` (saves all untracked files and modifications to a dataset -- by default into the dataset annex), or step-by-step by attaching paths to the ``save`` command.
Make sure to run :command:`datalad status` frequently.

.. findoutmore:: Save things to Git or to git-annex?

   By default, all dataset contents are saved into :term:`git-annex`.
   Depending on your data and use case, this may or may not be useful for all files.
   Here are a few things to keep in mind:

   - large files, in particular binary files should almost always go into :term:`git-annex`. If you have pure data dataset made up of large files, put it into the dataset annex.
   - small files, especially if they are text files and undergo frequent modifications (e.g., code, manuscripts, notes) are best put under version control by :term:`Git`.
   - If you plan to publish a dataset to a repository hosting site without annex support such as :term:`GitHub` or :term:`GitLab`, and do not intend to set up third party storage for annexed contents, be aware that only contents placed in Git will be available to others after cloning your repository. At the same time, be mindful of file size limits the services impose. The largest file size GitHub allows is 100MB -- a dataset with files exceeding 100MB in size in Git will be rejected by GitHub. :term:`Gin` is an alternative hosting service with annex support.

   You can find guidance on how to create configurations for your dataset (which need to be in place and save prior to saving contents!) in the chapter :ref:`chapter_config`, in particular section :ref:`config2`.

.. note::

   Be mindful during saving if you have a directory that should hold more, yet uncreated datasets down its hierarchy, as a plain ``datalad save`` will save *all* files and directories to the dataset!

If you are operating in a hierarchy of datasets, running a recursive save from the top-most dataset (``datalad save -d . -r``) will save you time: All contents are saved to their respective datasets, all subdatasets are registered to their respective superdatasets.


Step 4: Rerunning analyses reproducibly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are transforming a complete data analysis into a dataset, you may also want to rerun any computation with DataLad's ``run`` commands.
You can compose any :command:`datalad run` or :command:`datalad containers-run` [#f1]_ command to recreate and capture your previous analysis.
Make sure to specify your previous results as ``--output`` in order to unlock them [#f2]_.

Summary
^^^^^^^

Existing projects and analysis can be DataLad-ified with a few standard commands.
Be mindful about dataset sizes and whether you save contents into Git or git-annex, though, as these choices could potentially spoil your DataLad experience.
The sections :ref:`filesystem` and :ref:`cleanup` can help you to undo unwanted changes, but its better to do things right instead of having to fix them up.
If you can, read up on the DataLad Basics to understand what you are doing, and create a backup in case things go not as planned in your first attempts.

.. rubric:: Footnotes

.. [#f1] Prior to using a software container, install the :ref:`datalad-containers <extensions_intro>` extension and add the container with the :command:`datalad containers-add` command. You can find a concrete data analysis example with ``datalad-containers`` in the section :ref:`containersrun`.

.. [#f2] If you are unfamiliar with ``datalad run``, please work through chapter :ref:`chapter_run` first.