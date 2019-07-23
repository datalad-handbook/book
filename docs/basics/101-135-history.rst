Back and forth in time: Working with history
--------------------------------------------

One powerful feature of a version control system is the ability to revert
data to a previous state and thus view earlier content or correct mistakes.

Everyone of us already inadvertently deleted or overwrote files. In some cases,
it might have been possible to restore the lost content. But surely each of us
is especially cautious with some command in the flavors of ``rm`` (remove files),
``save`` (save files -- maybe you accidentally deleted content), or similar
because of a hasty operation that caused data fatalities in the past.

With DataLad, no mistakes are forever. As long as the content was version
controlled, it is possible to look at previous states of the data, or revert
changes -- even years after they happened.

To get a glimpse into how to work with the history of a dataset, today's lecture
consists entirely of this topic.
But because working with the history of a dataset is entirely
:term:`Git`\-based, we have an external Git-expert as a guest lecturer.

"Good morning! What a wonderful day to learn some Git commands!" he greets
everyone. "I don't have enough time to go through all the details in only
one lecture. But I'll give you the basics. And always remember: Just google
what you need. You will find thousands of helpful post or blogs right away.
Even the experts will google which Git command to use, and how to use it, *constantly*.",
he reassures with a wink.

"I have seen everyone is already working relatively confidently with the
``git log`` or ``tig`` -- great! This is the basics of working with the
history, actually looking at it. Whatever tool you are using for it,
you need a way to see what has been done in a dataset."

In order to effectively work with the history, the most important
information associated with a commit is its checksum. This checksum is how
DataLad identifies dataset modifications in the history, and with this
checksum you can communicate with DataLad or :term:`Git` about these
modifications. The ``datalad rerun`` command introduced in section (todo:link)
for example takes such a checksum as an argument, and reruns the ``datalad run``
or ``datalad rerun`` command associated with this checksum.
Here is an excerpt from the ``DataLad-101`` history to show a few abbreviated
checksums of the 15 most recent commits:

.. runrecord:: _examples/DL-101-135-101
   :workdir: dl-101/DataLad-101
   :language: console

   $ git log -15 --oneline

Using these checksums for miscellaneous history management operations is also
a very fail-save method. An alternative way for example is to
"count" ancestors of the most recent commit using the notation
``HEAD~2``, ``HEAD^2`` or ``HEAD@{2}``, but using the commit checksum
saves you from accidentally miscounting. Just note that whenever you see
a post or blog using the above notation, some commit in the history is
referenced.

"I'll let you people direct this lecture", the guest lecturer proposes.
"You tell me what you would be interested in doing, and I'll show you how it's
done. For the rest of the lecture, call me Google!"

Let's start really simple, but also really magical: How does one *see*
data as it was at a previous state in history?

"To see a previous state of the data(set), you have to *checkout*
the commit you are interested in."
Let us for example view the contents of ``notes.txt`` back when we
had just started to learn how to use DataLad. Identify the commit
in which we added a note on ``datalad save`` in your own history
(it will not have the same checksum as the example below).

 How do you change or add the commit message
of the last commit?"
