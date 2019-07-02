

############
Introduction
############


Everyone uses data. But once it exists, it does not suffice for most data
to simply reside unchanged in a single location for eternity.

Most **data needs to be shared** - may it be a digital collection of family
photos, a genomic database between researchers around the world, or inventory
lists of one company division to another. Some data is public and should be
accessible to everyone.  Other data should circulate only among a select few.
There are various ways to distribute data, from emailing files to sending
physical storage media, from pointers to data locations on shared file systems
to using cloud computing or file hosting services. But what if there was an
easy, **generic way of sharing and obtaining data**?


Most **data changes and evolves**. A scientist extends a data collection or
performs computations on it. When applying for a new job, you update your
personal CV.  The documents required for an audit need to comply to a new
version of a common naming standard and the data files are thus renamed.  It may
be easy to change data, but it can be difficult to revert a change, get
information on previous states of this data, or even simply find out how a piece
of data came into existence. This latter aspect, the :term:`provenance` of data
- information on its lineage and *how* it came to be in its current state, - is
often key to understanding or establishing trust in data.  In collaborative
fields that work with small-sized data such as Wikipedia pages or software
development, :term:`version control` are established and indispensable. These
tools allow users to keep track of changes, view previous states, or restore
older versions.  How about a **version control system for data**?


If data is shared as a copy *of one state* of its history, **keeping all shared
copies of this data up-to-date** once the original data changes or evolves is at
best tedious, but likely impossible. What about ways to easily **update data and
its shared copies**?


The world is full of data. The public and private sector make use of it to
understand, improve, and innovate the complex world we live in.  Currently, this
process is far from optimal.  In order for society to get the most out of public
data collections, public **data need to be** `FAIR <go-fair.org>`_: Findable,
Accessible, Interoperable, and Reusable. Apart from easy ways to share or update
shared copies of data, extensive **metadata** is required to identify data, link
data collections together, and make them findable and searchable in a
standardized way. Can we also easily **attach metadata to our data and its
evolution**?


**DataLad** is a general purpose tool for managing everything involved in the
digital workflow of using data - regardless of the data's type, content, size,
location, generation, or development.  It provides functionality to share,
search, obtain, and version control data in a distributed fashion, and it aids
managing the evolution of digital objects in a way that fulfills the FAIR
principles.

This handbook is a living resource about why and - more importantly - *how* to
use DataLad. It aims to provide novices and advanced users of all backgrounds
with both the basics of DataLad and start-to-end use cases of specific
applications.

.. todo::
   * Add info on how to read this book.
   * Extend/adjust the aims of this book.
   * Add info on what prerequisites are useful, but also on what prerequisites
     are not required (git, you don't need to be a programmer, ...).
   * Add info on how to contribute
   * Add info on the structure of the book, possibly related to Lauras idea of
     "build your own DataLad adventure".

