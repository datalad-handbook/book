.. _summary_sharelocal:

Summary
-------

Together with your room mate you have just discovered how
to share, update, and collaborate on a DataLad dataset on a shared file system.
Thus, you have glimpsed into the principles and advantages of
sharing a dataset with a simple example.

* To obtain a dataset, one can also use :dlcmd:`clone` with a path.
  Potential subdatasets will not be installed right away. As they are registered in
  the superdataset, you can do :dlcmd:`get -n/--no-data`,
  or specify the ``-r``/``--recursive`` (``datalad get -n -r <subds>``)
  with a decent ``-R/--recursion-limit`` choice to install them afterwards.

* The configuration of the original dataset determines which types
  of files will have their content available right after the installation of
  the dataset, and which types of files need to be retrieved via
  :dlcmd:`get`: Any file content stored in :term:`Git` will be available
  right away, while all file content that is ``annexed`` only has
  small metadata about its availability attached to it. The original
  ``DataLad-101`` dataset used the ``text2git`` configuration template
  to store text files such as ``notes.txt`` and ``code/list_titles.sh``
  in Git -- these files' content is therefore available right after
  installation.

* Annexed content can be retrieved via :dlcmd:`get` from the
  file content sources.

* :gitannexcmd:`whereis PATH` will list all locations known to contain file
  content for a particular file. This location is where :term:`git-annex`
  will attempt to retrieve file content from, and it is described with the
  ``--description`` provided during a :dlcmd:`create`. It is a very
  helpful command to find out where file content resides, and how many
  locations with copies exist.

* A shared copy of a dataset includes the datasets history. If well made,
  :dlcmd:`run` commands can then easily be ``rerun``.

* Because an installed dataset knows its origin -- the place it was
  originally installed from -- it can be kept up-to-date with the
  :dlcmd:`update` command. This command will query the origin of the
  dataset for updates, and a :dlcmd:`update --how merge` will integrate
  these changes into the dataset copy.

* Thus, using DataLad, data can be easily shared and kept up to date
  with only two commands: :dlcmd:`clone` and :dlcmd:`update`.

* By configuring a dataset as a :term:`sibling`, collaboration becomes easy.

* To avoid integrating conflicting modifications of a sibling dataset into your
  own dataset, a :dlcmd:`update -s SIBLINGNAME` will "``fetch``" modifications
  and store them on a different :term:`branch` of your dataset. The commands
  :dlcmd:`diff` and :gitcmd:`diff` can subsequently help to find
  out what changes have been made in the sibling.

Now what I can do with that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most importantly, you have experienced the first way of sharing
and updating a dataset.
The example here may strike you as too simplistic, but in later parts of
the book you will see examples in which datasets are shared on the same
file system in surprisingly useful ways.

Simultaneously, you have observed dataset properties you already knew
(for example how annexed files need to be retrieved via :dlcmd:`get`),
but you have also seen novel aspects of a dataset -- for example that
subdatasets are not automatically installed by default, how
:gitannexcmd:`whereis` can help you find out where file content might be stored,
how useful commands that capture provenance about the origin or creation of files
(such as :dlcmd:`run` or :dlcmd:`download-url`) are,
or how a shared dataset can be updated to reflect changes that were made
to the original dataset.

Also, you have successfully demonstrated a large number of DataLad dataset
principles to your room mate: How content stored in Git is present right
away and how annexed content first needs to be retrieved, how easy a
:dlcmd:`rerun` is if the original :dlcmd:`run` command was well
specified, how a datasets history is shared and not only its data.

Lastly, with the configuration of a sibling, you have experienced one
way to collaborate in a dataset, and with :dlcmd:`update --how merge`
and :dlcmd:`update`, you also glimpsed into more advances aspects
of Git, namely the concept of a branch.

Therefore, these last few sections have hopefully been a good review
of what you already knew, but also a big knowledge gain, and cause
joyful anticipation of collaboration in a real-world setting of one
of your own use cases.

