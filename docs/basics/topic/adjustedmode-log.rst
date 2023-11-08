The output of :gitcmd:`log` shown in the handbook and the output you will see in your own datasets when executing the same commands may not always match -- many times you might see commits about a "git-annex adjusted branch" in your history.
This is expected, and if you want to read up more about this, please progress on to chapter :ref:`chapter_gitannex` and afterwards take a look at `this part of git-annex documentation <https://git-annex.branchable.com/design/adjusted_branches>`_.

In order to get a similar experience in your dataset, please add the name of your default :term:`branch` (it will likely have the name ``main`` or ``master``) to every ``git log`` command.
This should display the same output that the handbook displays.
The reason behind this is that datasets are using a special :term:`branch` to be functional on Windows.
This branch's history differs from the history that would be in the default branch.
With this workaround, you will be able to display the dataset history from the same branch that the handbook and all other operating system display.
Thus, whenever the handbook code snippet contains a line that starts with ``git log``, copy it and append the term ``main`` or ``master``, whichever is appropriate.

If you are eager to help to improve the handbook, you could do us a favor by reporting any places with mismatches between Git logs on Windows and in the handbook.
`Get in touch <https://github.com/datalad-handbook/book/issues/new>`_!
