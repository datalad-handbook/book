# Changelog

All notable changes to this project between releases will be documented in this
file.

## v0.13 (XX. XX. 2020) -- Towards a tetralogy!

Handbook release matching the release of DataLad v0.13.0
With contributions from Dorian Pustina, Sarah Oliveira, Tristan Glatard,
Hamzah Hamid Baagil, Giulia Ippoliti, Yaroslav Halchenko, Alex Waite,
and Michael Hanke -- thank you!

### Refactoring or deletions

- RF: Replace `datalad publish` with `datalad push` ([#412][])
- RF: The Basics part was split into a Basics and Advanced part ([#450][]). The
  chapters "[Advanced Options](http://handbook.datalad.org/en/latest/beyond_basics/basics-advancedoptions.html)"
  and "[Go big or go home](http://handbook.datalad.org/en/latest/beyond_basics/basics-scaling.html)"
  have been moved/added there.
- Installation instructions for Windows subsystem for linux have been removed ([#397][])

### Additions

#### Introduction

- Installation instructions for rpm-based Linux distributions were added ([#435][])
- A "user-type" overview now serves as a guide through the handbook ([#403][])

#### Basics

- A [stand-alone section](http://handbook.datalad.org/en/latest/basics/101-141-push.html)
  on `datalad push` summarizes all previous publishing-related information ([#417][])
- A section for collecting gists (nifty code snippets for various tasks) is added to the
  chapter on [help](http://handbook.datalad.org/en/latest/basics/basics-help.html)([#445][])
- `datalad drop` is introduced in the first chapter ([#463][])
- [Gin's](https://gin.g-node.org/) new feature of anonymous read-only access to datasets is
  now mentioned in the chapter on using
  [third party infrastructure](http://handbook.datalad.org/en/latest/basics/101-139-gin.html)([#456][])
- The [section on getting help](http://handbook.datalad.org/en/latest/basics/101-135-help.html)
  started to collect and explain common warnings and error messages ([#418][])

#### Advanced

- A new [chapter on scaling up with DataLad](http://handbook.datalad.org/en/latest/beyond_basics/basics-scaling.html) was added ([#414][])
- A [section on configuring custom data access](http://handbook.datalad.org/en/latest/beyond_basics/101-146-providers.html) was added to the chapter
  ["Advanced Options"](http://handbook.datalad.org/en/latest/beyond_basics/basics-advancedoptions.html)([#440][])
- The [extension overview](http://handbook.datalad.org/en/latest/extension_pkgs.html)
  has been updated to a complete overview ([#477][])
#### Usecases

- A new Usecase
  [Scaling Up: Managing 80TB and 15 Million files from the HCP release](http://handbook.datalad.org/en/latest/usecases/datastorage_for_institutions.html)
  was added ([#225][])
- Giulia Ippoliti contributed the Usecase
  [Using Globus as a data store for the Canadian Open Neuroscience Portal](http://handbook.datalad.org/en/latest/usecases/using_globus_as_datastore.html)
  (opened in [#421][], merged as [#479][])

#### Miscellaneous additions

- Introduction of a system to improve intersphinx linkage between the handbook
  and the technical docs & docstrings of DataLad ([#377][])
- Various improvements to the PDF version of the handbook ([#367][])
- Major toctree restructuring: Chapter-wise toctrees ([#367][]), robustified URLs ([#457][])
- Addition of short, README-ready explanations of DataLad datasets for published projects ([#370][])
- Redirections are now possible, using a ``?<label>`` element after ``handbook.datalad.org/r.html`` ([#518][])
- (Almost) complete correspondence between HTML and PDF part, chapter, and section labeling ([#500][])

## v0.12 (Jan. 11 2020) -- A good weekend read

Beta stage release matching the release of datalad v0.12.0.

### Refactoring or deletions

- RF: Replace `datalad install` with `datalad clone` ([#326][])

### Additions

#### Introduction
- High-level, one page description "What you really need to know" about DataLad
  ([#295][])

#### Basics

- The DataLad Cheatsheet ([#157][])

- Chapter "One step further" with content on advanced dataset nesting ([#226][])
  and computational reproducibility with the `datalad-containers` extension ([#242][])

- Chapter "Further options" with content on DataLad's result hooks ([#304][]),
  an overview on DataLad's extensions ([#242][]), and how to keep clean datasets despite
  untracked contents ([#84][])

- Chapter "Third party infrastructure" on how to use various hosting services to
  share DataLad datasets, with concrete demonstrations/step-by-step instructions
  of sharing via Dropbox and GIN ([#111][])

- Section "Frequently Asked Questions" ([#239][])

- Section "Back and forth in time" on interacting with dataset history with
  Git tools/commands ([#106][])

- Section "YODA-compliant data analysis project" with an example data science
  project (including Python API) ([#226][])

- Include `datalad download-url` in first chapter to emphasize provenance capture
  abilities of DataLad ([#294][])

#### Usecases

- Use case "An automatically reproducible analysis of public neuroimaging data" ([#205][])

- Use case "Building a scalable data storage for scientific computing" ([#223][])

#### Miscellaneous additions

- Adjust contents to [autorunrecord update][autorunrecord] to record a flexible
  set of code snippets in "casts" for live demonstrations. Add cast associations
  for existing contents with speakernotes ([#219][])

- Additional book segment "Code lists from chapters" with code lists used for
  workshops ([#273][]

- Illustrations from [undraw.co][undraw] (starting in [#329][])

- Tagged "showroom" repositories with branches reflecting dataset states at different
  book sections ([#341][])



## v0.1 (Oct. 10 2019) -- A lazy afternoon read

Alpha stage release with handbook content covering most of the core commands.

### Additions

#### Basics

- Chapter "DataLad datasets" on local version control (create, save, status,
  install)

- Chapter "DataLad, Run!" on reproducible execution with `datalad run` and
  `datalad rerun`

- Chapter "Under the hood: git-annex" on the dataset annex and the `text2git`
  procedure

- Chapter "Collaboration" on sharing datasets (on the same computational infrastructure),
  siblings, and updating.

- Chapter "Tuning datasets to your needs" on various configurations

- Chapter "Help yourself" on common file system operations and on help.

- Chapter "Make the most out of datasets" about the YODA principles

#### Usecases

- Use case "A typical collaborative data management workflow"

- Use case "Basic provenance tracking"

- Use case "Basic provenance tracking"

- Use case "Student supervision in a research project"


[autorunrecord]: https://github.com/mih/autorunrecord/pull/2
[undraw]: https://undraw.co/


[#84]: https://github.com/datalad-handbook/book/pull/84
[#106]: https://github.com/datalad-handbook/book/pull/106
[#111]: https://github.com/datalad-handbook/book/pull/111
[#157]: https://github.com/datalad-handbook/book/pull/157
[#205]: https://github.com/datalad-handbook/book/pull/205
[#219]: https://github.com/datalad-handbook/book/pull/219
[#223]: https://github.com/datalad-handbook/book/pull/223
[#225]: https://github.com/datalad-handbook/book/pull/225
[#226]: https://github.com/datalad-handbook/book/pull/226
[#239]: https://github.com/datalad-handbook/book/pull/239
[#242]: https://github.com/datalad-handbook/book/pull/242
[#273]: https://github.com/datalad-handbook/book/pull/273
[#294]: https://github.com/datalad-handbook/book/pull/294
[#295]: https://github.com/datalad-handbook/book/pull/295
[#304]: https://github.com/datalad-handbook/book/pull/304
[#326]: https://github.com/datalad-handbook/book/pull/326
[#329]: https://github.com/datalad-handbook/book/pull/329
[#341]: https://github.com/datalad-handbook/book/pull/341
[#367]: https://github.com/datalad-handbook/book/pull/367
[#370]: https://github.com/datalad-handbook/book/pull/370
[#377]: https://github.com/datalad-handbook/book/pull/377
[#397]: https://github.com/datalad-handbook/book/pull/397
[#403]: https://github.com/datalad-handbook/book/pull/403
[#412]: https://github.com/datalad-handbook/book/pull/412
[#414]: https://github.com/datalad-handbook/book/pull/414
[#417]: https://github.com/datalad-handbook/book/pull/417
[#418]: https://github.com/datalad-handbook/book/pull/418
[#421]: https://github.com/datalad-handbook/book/pull/421
[#435]: https://github.com/datalad-handbook/book/pull/435
[#440]: https://github.com/datalad-handbook/book/pull/440
[#445]: https://github.com/datalad-handbook/book/pull/445
[#456]: https://github.com/datalad-handbook/book/pull/456
[#457]: https://github.com/datalad-handbook/book/pull/457
[#463]: https://github.com/datalad-handbook/book/pull/463
[#450]: https://github.com/datalad-handbook/book/pull/450
[#477]: https://github.com/datalad-handbook/book/pull/477
[#479]: https://github.com/datalad-handbook/book/pull/479
[#500]: https://github.com/datalad-handbook/book/pull/500
[#518]: https://github.com/datalad-handbook/book/pull/518
