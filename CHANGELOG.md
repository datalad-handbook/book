# Changelog

All notable changes to this project between releases will be documented in this
file.

## v0.12 (Jan. 11 2019) -- A good weekend read

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