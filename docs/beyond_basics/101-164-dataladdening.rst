.. _dataladdening:

Transitioning existing projects into DataLad
--------------------------------------------

Using DataLad offers exciting and useful features that warrant transitioning existing projects into DataLad datasets -- and in most cases, transforming your project into one or many DataLad datasets is easy.
This sections outlines the basic steps to do so, and offers examples as well as advice and caveats.

Important: Your safety net
^^^^^^^^^^^^^^^^^^^^^^^^^^

Chances are high that you are reading this section of the handbook after you stumbled across DataLad and were amazed by its features, and you're now looking for a quick way to get going.
If you haven't read much of the handbook, but are now planning to DataLad-ify the gigantic project you have been working on for the past months or years, this first paragraph is warning, advice, and a call for safety nets to prevent unexpected misery that can arise from transitioning to a new tool.
Because while DataLad *can* do amazing things, you shouldn't blindly trust it to do everything *you* think it can or should do, but gain some knowledge and familiarity about it.

If you're a DataLad novice, we highly recommend that you read through the :ref:`basics-intro` part of the handbook.
This part of the book provides you with a solid understanding of DataLad's functionality and a playground to experience working with DataLad.
If you're really pressed for time because your dog is sick, your toddler keeps eating your papers and your boss is behind you with a whip, the findoutmore below summarizes the most important sections from the Basics for you to read:

.. findoutmore:: The Basics for the impatient

   To get a general idea about DataLad, please read sections :ref:`philo` and :ref:`executive_summary` from the introduction (reading time: 15 min).

   To gain a good understanding of some important parts of DataLad, please read chapter :ref:`chapter_datasets`, :ref:`chapter_run`, and :ref:`chapter_gitannex` (reading time: 60 minutes).

   To become confident in using DataLad, sections :ref:`help`, :ref:`filesystem` can be very useful. Depending on your aim, :ref:`chapter_collaboration` (for collaborative workflows), :ref:`chapter_thirdparty` (for data sharing), or :ref:`chapter_yoda` (for data analysis) may contain the relevant background for you.

Prior to transforming your project, **we recommend to create a copy of it**.
We don't believe there is much that can go wrong from the software-side of things, but data is precious, so if its your first time using DataLad, better be safe than sorry.

Step 1: Planning
^^^^^^^^^^^^^^^^

The first step to DataLad-ify your project is to turn in into one or several nested datasets.
Whether you turn a project into a single dataset or several is dependent on the current size of your project and how much you expect it to grow overtime, but also on its contents.
Here are few things to keep in mind:

- Try to make your project modular and :ref:`yoda-compliant <yoda>`.
  If it consists of several separable components, for example input data and code, consider if each component should become a stand-alone dataset.
- How many files does your dataset consist of?
  If it exceeds 100.000, you should strongly consider splitting it into subdatasets
- If you split a project into several datasets, it depends on your project organization where sensible subdataset boundaries lie.
  One straightforward organization may be a top-level superdataset and subject-specific subdatasets, mimicking the structure chosen in the use case :ref:`usecase_HCP_dataset`

Step 2: Dataset creation
^^^^^^^^^^^^^^^^^^^^^^^^

- datalad create -f
- datalad save -r
- mention datalad -C
- toy example with a hierarchy of datasets


