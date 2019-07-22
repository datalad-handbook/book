Sharing datasets: Common File systems [3]
-----------------------------------------

"Thanks a lot for sharing your dataset with me! This
is super helpful. I'm sure I'll catch up in no time!",
your room mate says confidently. "How far did you get
with the DataLad commands yet?" he asks at last.

"Mhh, I think the last big one was ``datalad run``.
Actually, let me quickly show you what this command
does. There is something that I've been wanting to try
anyway." you say.

The dataset you shared contained a number of ``datalad run``
commands. For example, you created the simple ``Podcasts.tsv``
file that listed all titles and speaker names of the longnow
podcasts.

Given that you learned to created "proper" ``datalad run`` commands,
complete with ``--input`` and ``--output`` specification,
anyone should be able to ``datalad rerun`` these commits
easily. This is what you want to try now.

You begin to think about which ``datalad run`` commit would be
the most useful one to take a look at. The creation of
``Podcasts.tsv`` was a bit lame -- at this point in time, you
didn't yet know about ``--input`` and ``--output`` arguments,
and the resulting output is present anyway because text files
like this ``.tsv`` file are stored in Git.
However, one of the attempts to resize a picture could be
useful. The input, the podcast logos, is not yet retrieved,
nor is the resulting, resized image. "Let's go for this!",
you say, and drag your confused room mate to the computer
screen.

First of all, find the commit checksum of the command you
want to run by taking a look into the history of the dataset
(in the shared dataset)

.. runrecord:: _examples/DL-101-122-101
   :language: console
   :workdir: dl-101/DataLad-101

   # navigate into the shared copy
   $ cd ../mock_user/DataLad-101
   # let's view the history:
   $ git log --oneline


Ah, there it is. Just as already done in LINK RUN SECTION,
take this checksum and plug it into a ``datalad rerun``
command:

