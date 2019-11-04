.. _usecase_external_collaboration:

Collaborations on sensitive data
--------------------------------

This usecase is based on a common problem: An external collaborator would
like to perform an analysis on a dataset that contains personal information
of participants and thus can't be shared outside of the lab. With DataLad,
the collaboration can succeed:

#. A mock dataset with the same structure (organization, file names) but
   without (access to) the actual problematic data is shared or made
   publicly available instead of the original dataset.
#. This mock dataset can assist others to develop their code, without
   disclosing personal information.
#. External collaborators create a new dataset for their analysis code, with
   the mock dataset as a subdataset.
#. The collaborator submits their dataset back to the lab that has all of the
   data. After code review, the code is executed on the actual data, its
   results are captured in the submitted dataset, and only results are pushed
   back to the external collaborators.

The Challenge
^^^^^^^^^^^^^

The ABC-Lab collected data from patients for one of their studies. After
publication, a Post-doc from the XYZ-Lab reaches out and proposes and
interesting analysis of the same data on a new research question. Everyone
involved is excited about this collaboration: The
XYZ-Lab is happy that such a valuable dataset exists and is eager to give
credit and co-authorship to collaborators in the ABC-Lab. The ABC-Lab is
happy that someone else is interested in using their data and appreciates the
possibility of another publication with lab-members as co-authors.

However, the legal department in ABC's institutes steps in: The data can not
be shared with anyone outside as this would be a privacy violation. The data
contains potentially identifying or personal information of the patients it
was collected from.

With such legal problems, the promising collaboration ceases before it even
started, the data remains disclosed but also unused, and an interesting
research question remains unanswered.

The DataLad Approach
^^^^^^^^^^^^^^^^^^^^

Scientists take their participant's privacy very seriously, and everyone is well
aware that certain data can not leave the institute's computational premises.
Nevertheless, valuable data should not remain accessible to only selected few.
To enable data analysis by others without disclosing private information
researchers can make use of DataLad.

In order to *develop* analysis scripts that can analyze the data, the actual
sensitive data is not needed. A mock dataset that has the same structural
layout and the same file names as the original dataset is sufficient
information to create a working script. Therefore, the ABC-lab shares a mock
dataset with its collaborators that does not contain sensitive information.
This can be achieved by not making the annexed data available and thus
providing only file availability information without content, or by adding
empty or simulated data instead of the actual files.

Collaborators can install this dataset as a subdataset in their own analysis
datasets, and develop their code against the layout. This ensures that the
script is adjusted to the actual file names and works "out-of-the-box".

Afterwards, this dataset is given back to the ABC-lab. They can review the
provided code and exchange the mock dataset with the original, sensitive data.
With this, they can run the code provided by the collaborator such that
sensitive data stays within their institute. All results computed from this
are aggregated into their collaborator's dataset. Upon completion, only the
results, not the sensitive input data, are pushed back.

Step-by-Step
^^^^^^^^^^^^