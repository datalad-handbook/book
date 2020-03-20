Ephemeral clones
================

Ephemerality (from the Greek word `ephemeros`, meaning "lasting a day")
refers to the short life span of something: "Fame in the world of rock
and pop is largely ephemeral", for example.
Given how important it is to create lasting, complete records (as stressed by
:ref:`yoda`, for example), ephemerality does not appear to be a desirable
quality for a DataLad dataset on first sight. But there can be exceptions.
This section introduces the concept of an *ephemeral dataset clone*.

The origins of ephemeral clones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Most DataLad users will not have a use case for ephemeral clones as they serve
quite specialized demands.
To understand what an ephemeral clone is, consider the use case that led to
their development:

A research group in a neuroscientific institute has a particular analysis
set-up: Their input datasets contain gigantic files - each up to several dozen
GBs in size.
While it is not a problem to version control these files, executing
reproducible analyses on them is cumbersome: Retrieving the files prior to a
:command:`datalad run` is an IO bottleneck. It takes up a sizeable chunk of
additional storage and a long time to perform the copying of the data.
The results from their analyses are comparably small