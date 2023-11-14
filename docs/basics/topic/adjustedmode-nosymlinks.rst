Windows has insufficient support for :term:`symlink`\s and revoking write :term:`permissions` on files.
Therefore, :term:`git-annex` classifies it as a :term:`crippled file system` and has to stray from its default behavior: it enters :term:`adjusted mode`.
While git-annex on Unix-based file operating systems stores data in the annex and creates a symlink in the data's original place, on Windows it moves data into the :term:`annex` and creates a *copy* of the data in its original place. This behavior is not specific to Windows, but is done for any impaired file system, such as a dataset on a USB-stick plugged into a Mac.

**Why is that?**
Data *needs* to be in the annex for version control and transport logistics -- the annex is able to store all previous versions of the data, and manage the transport to other storage locations if you want to publish your dataset.
But as the :ref:`Findoutmore in this section <fom-objecttree>` shows, the :term:`annex` is a non-human readable tree structure, and data thus also needs to exist in its original location.
Thus, it exists in both places: it has moved into the annex, and copied back into its original location.
Once you edit an annexed file, the most recent version of the file is available in its original location, and past versions are stored and readily available in the annex.
If you reset your dataset to a previous state, as is shown in the section :ref:`history`, the respective version of your data is taken from the annex and copied to replace the newer version, and vice versa.

**But doesn't a copy mean data duplication?**
Yes, absolutely!
And that is a big downside to DataLad and :term:`git-annex` on Windows.
If you have a dataset with annexed file contents (be that a dataset you created and populated yourself, or one that you cloned and got file contents with ``datalad get`` from), it will take up more space than on a Unix-based system.
How much more?
Every file that exists in your file hierarchy exists twice.
A fresh dataset with one version of each file is thus twice as big as it would be on a Linux computer.
Any past version of data does not exist in duplication.

**Step-by-step demonstration**:
Let's take a concrete example to explain the last point in more detail.
How much space, do you think, is taken up in your dataset by the resized ``salt_logo_small.jpg`` image?
As a reminder: It exists in two versions, a 400 by 400 pixel version (about 250Kb in size), and a 450 by 450 pixel version (about 310Kb in size).
The 400 by 400 pixel version is the most recent one.
The answer is: about 810Kb (~0.8 MB).
The most recent 400x400px version exists twice (in the annex and as a copy), and the 450x450px copy exists once in the annex.
If you would reset your dataset to the state when we created the 450x450px version, this file would instead exist twice.

.. index::
  pair: unused; git-annex command
  pair: dropunused; git-annex command

**Can I at least get unused or irrelevant data out of the dataset?**
Yes, either with convenience commands (e.g., ``git annex unused`` followed by ``git annex dropunused``), or by explicitly using ``drop`` on files (or their past versions) that you don't want to keep anymore.
Alternatively, you can transfer data you don't need but want to preserve to a different storage location.
Later parts of the book will demonstrate each of these alternatives.
