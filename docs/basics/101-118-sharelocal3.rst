.. _sharelocal3:

Retrace and reenact
-------------------

"Thanks a lot for sharing your dataset with me! This
is super helpful. I'm sure I'll catch up in no time!",
your room mate says confidently. "How far did you get
with the DataLad commands yet?" he asks at last.

"Mhh, I think the last big one was :command:`datalad run`.
Actually, let me quickly show you what this command
does. There is something that I've been wanting to try
anyway." you say.

The dataset you shared contained a number of :command:`datalad run`
commands. For example, you created the simple ``podcasts.tsv``
file that listed all titles and speaker names of the longnow
podcasts.

Given that you learned to created "proper" :command:`datalad run` commands,
complete with ``--input`` and ``--output`` specification,
anyone should be able to :command:`datalad rerun` these commits
easily. This is what you want to try now.

You begin to think about which :command:`datalad run` commit would be
the most useful one to take a look at. The creation of
``podcasts.tsv`` was a bit lame -- at this point in time, you
didn't yet know about ``--input`` and ``--output`` arguments,
and the resulting output is present anyway because text files
like this ``.tsv`` file are stored in Git.
However, one of the attempts to resize a picture could be
useful. The input, the podcast logos, is not yet retrieved,
nor is the resulting, resized image. "Let's go for this!",
you say, and drag your confused room mate to the computer
screen.

First of all, find the commit shasum of the command you
want to run by taking a look into the history of the dataset
(in the shared dataset):

.. runrecord:: _examples/DL-101-118-101
   :language: console
   :workdir: dl-101/DataLad-101
   :notes: More cool things on shared datasets: rerunning run commands
   :cast: 04_collaboration

   # navigate into the shared copy
   $ cd ../mock_user/DataLad-101

.. runrecord:: _examples/DL-101-118-102
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :emphasize-lines: 4
   :notes: find the shasum
   :cast: 04_collaboration

   # lets view the history
   $ git log --oneline

Ah, there it is, the second most recent commit.
Just as already done in section :ref:`run2`,
take this shasum and plug it into a :command:`datalad rerun`
command:

.. runrecord:: _examples/DL-101-118-103
   :language: console
   :workdir: dl-101/mock_user/DataLad-101
   :realcommand: echo "$ datalad rerun $(git rev-parse HEAD~1)" && datalad rerun $(git rev-parse HEAD~1)
   :notes: plug the shasum into a rerun command
   :cast: 04_collaboration

"This was so easy!" you exclaim. DataLad retrieved the missing
file content from the subdataset and it tried to unlock the output
prior to the command execution. Note that because you did not retrieve
the output, ``recordings/salt_logo_small.jpg``, yet, the missing content
could not be unlocked. DataLad warns you about this, but proceeds
successfully.

Your room mate now not only knows how exactly the resized file
came into existence, but he can also reproduce your exact steps to
create it. "This is as reproducible as it can be!" you think in awe.
