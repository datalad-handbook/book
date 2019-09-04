.. _supervision:

Student supervision in a research project
-----------------------------------------

This use case will demonstrate a workflow that uses DataLad tools and principles
to assist in technical aspects of supervising research projects with computational
components.
It demonstrates how a DataLad dataset comes with advantages that ease technical
complexities for trainees and allows high-quality supervision from afar with minimal
effort and time commitment from busy supervisors. It furthermore serves to log
undertaken steps, establishes trust in an analysis, and eases collaboration.

Successful workflows rely on more knowledgeable "trainers" (i.e. supervisors, or a more
experienced collaborator) for a quick initial dataset setup with optimal configuration, and
an introduction to the YODA principles and basic DataLad commands.
Subsequently, supervision and collaboration is made easy by the distributed nature of a dataset.
Afterwards, reuse of a students work is made possible by the modular nature of the dataset.
Students can concentrate on questions relevant for the field and research topic,
and computational complexities are minimized.

The Challenge
^^^^^^^^^^^^^

Megan is a graduate student and does a 4-month internship in the lab of a professor
at a partnering research institution. As she already has experience in data analysis,
her supervisor wants her to work on a relevant project, and the time of her supervisor
is limited, she is given a research question to work on autonomously. The question is
related to a different project in the lab for which the data is already collected. Thus,
everyone involved is certain that Megan will be fine performing the analyses she has
experience with, and her supervisor confidently proposes the research project as a
conference talk Megan should give at the end of her stay. Megan is excited about the
responsibility and her project, and can not wait to start.

At her first day, her supervisor takes an hour to show her the office,
the coffee machine, and the toilets, and they chat about the high-level aspects
of the projects: Which is the relevant literature that she should read to get an idea
of the theoretical background of the question, which researcher collected the data,
how long should the talk be that she is to give on the results.
Megan has many more procedural questions, but the hour is over fast, and as it turns out,
Megan's supervisor will leave the country for a three month visit
to a lab in Japan soon, and is very busy preparing this stay and coordinating projects.
However, everyone is confident that Megan will be just fine. The IT office issues an
account on the compute cluster for Megan, and the Post-doc that
collected the data points her to the directories in which the data live.

When she wants to start, Megan realizes that she has no experience with the
Linux-based operating system running on the compute cluster. She knows very well how
to write Python scripts to perform very complex analyses, but needs to invest almost
two weeks to google how to log into an SSH server and perform standard UNIX commands
because no-one is around to give her a quick introduction.
When she starts her computations, she accidentally overwrites a data file in the
data collection, and emails the Post-doc for help. This Post-doc luckily has a back-up
of the data and is able to restore the original data sate, but grimly CCs her supervisor
in Japan in his response email to her. Not being told where to store analysis results in,
Megan saves the results in a non-backed up ``scratch`` directory. With ambiguous,
hard-to-make-sense-of emails her supervisor sends from Japan at 3am, Megan tries to
comply to the instructions she extracts from the emails. But without an interactive
discussion component, she is very unsure about what she is supposed to do, and saves
multiple different analysis scripts and results of them inside of the scratch folder.

When her supervisor returns and meets for a project update, he scolds her for the
bad organization, and the not-backed up storage choice. As the conference is only
one week away, Megan is told to write down her results and email her slides for
feedback, but is left discouraged when she learns that she interpreted
one piece of information she found in the very beginning in her supervisors email
differently from what was meant by it, deeming all of her results irrelevant.
Not trusting Megan's analyses anymore, her supervisor cancels the talk she was about
to give and has the Post doc take over. Megan feels incompetent and regards the stay
as a waste of time, her supervisor is unhappy about the miscommunication and lack of
results, and the Post doc taking over is unable to comprehend what was done so far
and needs to start over new, even though all analysis scripts were correct and very
relevant for the future of the project.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

When Megan arrives in the lab, her supervisor and the Post doc that collected the
data take an hour to meet and talk about the upcoming project. To ease the technical
complexities for a new student like Megan on an unfamiliar computational infrastructure,
they talk about the yoda principles and basic DataLad commands, and
set up a project dataset for Megan to work in. Inside of this dataset, the original
data is installed as a subdataset, code is tracked with Git, and the appropriate software
is provided with a containerized image tracked in the dataset.
Megan can adopt the version control workflows and data
analysis principles very fast and is thankful for the brief but sufficient introduction.
When her supervisor leaves for Japan, they stay in touch via email, but her
supervisor also checks the development of the project and occasionally skims through Megan's code
updates from afar every other week. When he notices that one of his instructions was ambiguous and Megan's
approach to it misguided, he can intervene right away. Megan feels comfortable and confident
that she is doing something useful and learns a lot about data management in the safe space
of a version controlled dataset. Her supervisor in Japan can see how well
coded and ingenious Megan's analysis methods are, and has trust in her results. Megan
proudly presents the results of her analysis at the conference, and receives a gleaming
letter of recommendation about how autonomous she worked on this project from her supervisor.
She leaves with many good experiences and lots of new knowledge, her supervisor is happy
about the progress done on the project, and the dataset is a standalone "lab-notebook"
that anyone can later use as a detailed log to make sense of what was done. As an ongoing
collaboration, Megan, the Post-doc, and her supervisor use the analysis project as a subdataset
in a new dataset that they write a paper about the analysis in.

Step-by-Step
^^^^^^^^^^^^

Megan's supervisor is excited that she comes to visit the lab and trusts her to be a diligent,
organized, and capable researcher. But he also doesn't have much time for a lengthy introduction
to technical aspects unrelated to the project, interactive teaching, or in-person supervision.
Megan in turn is a competent student and eager to learn new things, but she
doesn't have experience with DataLad, version control, or the computational cluster.

As a first step, therefore, her supervisor and the Post-doc prepare a preconfigured
dataset in a dedicated directory everyone involved in the project has access to:

.. code-block:: bash

   $ datalad create -c yoda project-megan

All data that this lab generates or uses is a standalone DataLad dataset that lives
in a dedicated ``data\`` directory on a server. To give Megan access to the data without
endangering or potentially modifying the pristine data kept in there, complying to the
yoda principles, they install the data she is supposed to analyze as a subdataset:

.. code-block:: bash

   $ cd project-megan
   $ datalad install -d . \
     --source /home/data/ABC-project \
     data/ABC-project

    [INFO   ] Cloning /home/data/ABC-project [1 other candidates] into '/home/projects/project-megan/data/ABC-project'
    [INFO   ] Remote origin not usable by git-annex; setting annex-ignore
    install(ok): data/ABC-project (dataset)
    action summary:
      add (ok: 2)
      install (ok: 1)
      save (ok: 1)

The yoda principle and the data installation created a comprehensive directory
structure and configured the ``code\`` directory to be tracked in Git, to allow
for easy, version-controlled modifications without the necessity to learn about
locked content in the annex.

.. code-block:: bash

   $ tree
   .
   ├── CHANGELOG.md
   ├── code
   │   └── README.md
   ├── data
   │   └── ABC-project [13 entries exceeds filelimit, not opening dir]
   └── README.md

Within a 20-minute walk-through, Megan learns the general concepts of version-
control, gets an overview of the yoda principles [#f1]_,
configures her Git identity with the help of her supervisor, and is
given an introduction to the most important DataLad commands relevant to her,
:command:`datalad save` [#f2]_, :command:`datalad containers-run` [#f3]_,
and :command:`datalad rerun` [#f4]_.
For reference, they also give her the `cheat sheet <TODO: link>`_ and the link
to the DataLad handbook as a resource if she has further questions.

To make the analysis reproducible, they spent the final minutes on adding the labs
default singularity image to the dataset. The lab has a singularity image with
all the relevant software on `Singularity-Hub <https://singularity-hub.org/>`_,
and it can easily be added to the dataset with the DataLad-containers extension [#f3]_:

.. code-block:: bash

   $ datalad containers-add somelabsoftware --url shub://somelab/somelab-container:Softwaresetup

This will download the container image, add it to the dataset, and record basic information on the
container under its name “somelabsoftware” in the dataset’s configuration at ``.datalad/config``.

With only a single command to run, Megan finds it easy to version control her
scripts and gets into the habit of
running :command:`datalad save` frequently. This way, she can fully concentrate
on writing up the analysis. In the beginning, her commit messages
may not be optimal, and the changes she commits into a single commit might have
better been split up into separate commits. But from the very beginning she is
able to version control her progress, and she gets more and more proficient as
the project develops.

Knowing the three yoda principles gives her clear and easy-to-follow guidelines
on how to work. Her scripts are producing results in dedicated ``output/`` directories
and are executed with :command:`datalad containers-run` to capture the provenance of how
which result came to be with which software. These guidelines are not complex, and yet
make her whole workflow much more comprehensible, organized, and transparent.

The preconfigured DataLad dataset thus minimized the visible technical complexity.
With just a few commands and standards, Megan can learn fast, and the commands and
standards have a large positive impact on her project. At the
same time, it did not take her supervisor much time to configure the dataset or give
her an introduction to the relevant commands, and yet it ensured her to be able to
productively work and contribute her expertise to the project.

Her supervisor can also check how the project develops if Megan asks for assistance or if
he is curious -- even from Japan and whenever he has some 15 minutes of spare-time.
When he notices that Megan must have misunderstood one of his emails in
the changes captured in the Git log, he can intervene and contact Megan by their
preferred method of communication, and/or push a fix or comment to the project,
as he has write-access. This enables him to stay up-to-date independent of emails
or meetings with Megan, and to help when necessary without much trouble. When they
email or skype, the focus is on the work being done, and not solely on verbal reports.

Megan finishes her analysis well ahead of time and can prepare her talk for the
conference. Together with her supervisor she decides which figures look good and
which results are important. All results that are deemed irrelevant can be dropped
to keep the dataset lean, but could be recomputed as their provenance was tracked.

After a successful talk, the data analysis project is installed into a new dataset,
created for collaborative paper-writing on the analysis, as an input:

.. code-block:: bash

   $ datalad create megans-paper
   $ cd megans-paper
   $ datalad install -d . \
     --source /home/projects/project-megan \
     analysis

   [INFO   ] Cloning /home/projects/project-megan [1 other candidates] into '/home/paper/megans-paper'
   [INFO   ]   Remote origin not usable by git-annex; setting annex-ignore
   install(ok): analysis (dataset)
   action summary:
     add (ok: 2)
     install (ok: 1)
     save (ok: 1)

Even though Megan returns to her home institution, they can write up the paper
on her analysis collaboratively, just as easy as collaboration worked in her
analysis project.

Thus, DataLad can help to effectively manage student supervision in computational
projects. It requires minimal effort, but comes with great benefit:

- Appropriate data management is made a key element of the project and handled from the start,
  not an afterthought that needs to be addressed at the end of its lifetime

- The dataset becomes the lab notebook, hence a valid and detailed log is always
  available and accessible to supervisor and supervisee

- supervisors can efficiently prepare for meetings in a way that does not rely
  exclusively on a students report. This shifts the focus from trust in a student
  to trust in a student's work.

- supervisors can provide feedback, not only high-level based on a presentation,
  but much more detailed, and also on process aspects if desired/necessary:
  supervisors can directly contribute in a way that is as auditable/accountable as
  the student's own contributions -- for both parties the strict separation and tracking
  of any external inputs of a project make it possible (when a project is completed)
  that a supervisor can efficiently test the integrity of the inputs, discard them
  (if unmodified), and only archive the outputs that are unique to the project --
  which then can become a modular component for re-use in a future project.


.. rubric:: Footnotes

.. [#f1] Find out more about the yoda principles in section :ref:`yoda`
.. [#f2] Find out more about datalad save in section :ref:`modify`
.. [#f3] Find out more about the ``datalad containers`` extension in section TODO:link once it exists
.. [#f4] Find out more about the ``datalad rerun`` command in :ref:`run2`