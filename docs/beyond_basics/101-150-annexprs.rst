.. _annexprs:

Pull requests with annexed file contents
----------------------------------------

:term:`Git` has revolutionized collaborative processes on text files.
The concept is simple: In order to integrate new changes into a main development line, the changes are :term:`merge`\d in from a different branch.
Individual contributors were able to clone repositories, make changes in new branches, and email these changes as patches or requests to pull from their branches to maintainers.
Hosting platforms like :term:`GitHub` or :term:`GitLab` made this even simpler by introducing :term:`pull request`\s (GitHub) or :term:`merge request`\s (GitLab) that contributors can initiate when they push new branches to their :term:`fork`\s.


.. figure:: ../artwork/src/branching/collab_4.svg
   :scale: 150%

   A typical collaborative setup. A repository (upstream) is the central development place, living on a hosting site such as GitHub. Individual contributors :term:`fork` this repository. Rather than addings commits to the blue main development line, they make changes on new branches - here denoted with different colors. By requesting that the central repository "pulls in" or "merges" from their branch, e.g., the ``fix-paths`` branch, the main line in the central repository grows collaboratively.

This process is not as straight-forward when both forks and annexed file contents are involved, for example if a collaborator adds a commit in their fork that added a new annexed file.
In this scenario, a regular Git branch learns about the file identity (its hash and name), but not about its availability information, for example from which :term:`special remote` the file content can be obtained from - this information is on the :term:`git-annex` branch [#1]_.
And as this crucial availability information is tracked on the :term:`git-annex branch`, a "single branch PR" is not able to propagate all relevant information.
After merging only the Git branch, without the availability information on the annex-branch, collaborators know that the file exists, but have no way of ``get``\ting or even querying it: the git-annex branch on the main development repository would not know about the file.
And annexed content is not copied between a fork and the main repository when a pull request is merged.

At the same time, the :term:`git-annex branch` is not a branch that one can create a pull request with - in fact, it shouldn't even really be checked out manually.
It is automatically managed by git-annex, and the necessary synchronization to update availability information across dataset siblings usually requires a ``git annex sync``.

Especially with the availability of annex-aware hosting like :term:`Gin` or :term:`forgejo-aneksajo`, it becomes more and more relevant to know about the issues with annex PRs.
But what are the solutions?
At the moment, there are mostly work-arounds.
The easiest is skipping the :term:`fork`, whenever permission management allows that, and instead working within the main development dataset: PRs from a branch within the dataset instead of from a fork are not an issue.
Sometimes, though, this isn't possible, for example because an organization doesn't want to make every possible contributor from the outside a member with the necessary write access.
The templateflow project came up with an :term:`Open Science Framework` based approach for external contributors: `www.templateflow.org/contributing/submission <https://www.templateflow.org/contributing/submission>`_.


.. rubric:: Footnotes

.. [#1] If this does not sound familiar to you, please re-read chapter :ref:`chapter_gitannex`.