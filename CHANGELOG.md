# Changelog

All notable changes to this project between releases will be documented in this
file.

## v0.16 (April 13 2022) -- Spring cleaning

Handbook release matching the release of DataLad v0.16.0.
This release contains a number of updates for respective changes in DataLad ``0.16``'s API, including the overhaul of existing commands, reimplementations of commands, and additional commands.

It includes contributions the new contributors @eort, @mslw, @tguiot, @jhpb7 and @eltociear, as well as contributions from established contributors @jsheunis, @mih, @adswa, @yarikoptic, and @Remi-Gau.


### Refactoring or deletions


### Additions

#### Introduction

- Installation instructions on Windows now recommend git-annex'es filter-process configuration for performance improvements ([#791][])

#### Basics

- The chapter on publishing datasets was overhauled and now includes a general overview of publishing routines and hosting service differences. ([#762][])
- Content on ``datalad run`` now mentions its superglob abilities ([#692][]) and how to glob across directories hierarchies with earlier datalad versions ([#785][])
- A few fixes and improvements to the section on publishing datasets to Gin  ([#793][])

#### Advanced

- The enki walkthrough links the FAIRly big paper and tutorial as an improved alternative ([#783][])
- A new chapter contains a section on contributing to DataLad and DataLad's design docs  ([#782][])
- A new section guides through the process of creating your own extensions  ([#812][])
- The section on configuring additional data providers now includes content on DataLad 0.16's credential integration with Git  ([#814][])

#### Usecases

- A new general section on how to create interoperable file names was added  ([#796][])

#### Miscellaneous additions

- The GitHub project of the handbook now uses templates for easier issue generation. ([#768][])
- A number of CSS improvements fix the rendering of bullet points ([#770][])
- The ML usecase was minified to speed up builds ([#790][])
- A new code list for the DGPA workshop was added  ([#820][])

## v0.15 (November 25 2021) -- LaTeX improvements

Handbook release matching the release of DataLad v0.15.0.
This release contains major improvements of the handbook's LaTeX backbone.

With thanks to the new contributors @oesteban, @AKSoo, and @jsheunis, and established contributors @eknahm, @kyleam, @RemiGau, @bpoldrack, @yarikoptic, @effigies @sappelhof, @lilikapa, @arokem

### Refactoring or deletions

- The deprecated --no-storage-sibling parameter was removed from the RIA store chapter ([#641][])

### Additions

#### Introduction

- The installation instructions were updated for Python ([#651][]) and Mac ([#675][]), and overall improved ([#682][])

#### Basics

- The help section was extended with a note on asyncio-related errors in Jupyter ([#646][]) and information on line-endings and and autocrfl true configurations for windows users ([#723][])
- The section on publishing with Gin was amended with content on using Gin as an autoenabled special remote ([#707][])
- The chapter on run now mentions its ``--assume-ready`` and ``--dry-run` parameter ([#699][])`, ([#724][])
- There now is a FAQ on how to fix GitHub displaying the git-annex branch as the default ([#722][])
- A new chapter on Publishing to S3 walks through publishing to a public S3 bucket ([#721][])

#### Miscellaneous additions

- A wide range of improvements in the LaTeX rendering of the handbook ([#647][]), ([#648][]), ([#650][]), ([#655][]), ([#656][]), ([#657][]), ([#658][]), ([#658][]), ([#660][]), ([#661][]), ([#662][]), ([#663][]), ([#665][]), ([#666][]), ([#679][]), ([#684][]), ([#685][]), ([#694][]), ([#759][])
- A number of textual changes to improve the PDF rendering of the handbook ([#48][]), ([#669][]), ([#670][]), ([#671][]), ([#678][]), ([#680][]), ([#691][]), ([#704][])
- New artwork ([#667][]), ([#672][]),
- A new code list for a Repronim Workshop in Yale ([#693][])
- Continuous integration was migrated to GitHub actions ([#703][])
- The Zenodo record now resolves to the latest version ([#717][])
- The code blocks now have copy-buttons ([#615][])
- A monthly linkchecker was implemented to better catch unresolving URLs ([#743][])

## v0.14 (January XX 2021) -- slightly less dreadfulness for Windows users

Handbook release matching the release of DataLad v0.14.0.
Like the software release, this handbook release improves the situation on/for Windows systems starkly from what we had before.
With contributions from Tristan Glatard, Ariel Rokem, Remi Gau, Surya Teja Togaru, Judith Bomba, Konrad Hinsen, Wu Jianxiao, Małgorzata Wierzba, Stefan Appelhoff, and Michael Joseph -- thank you!

### Refactoring or deletions

- Overhaul Windows installation instructions ([#588][])
- Adjustments for GitHub's user-password deprecation ([#626][]), ([#592][])

### Additions

#### Introduction

- git-annex installations with custom built git-annex with MagicMime support ([#603][])
- A quick-start guide for OpenNeuro ([#585][])

#### Basics

- Disambiguation on configurations ([#627][]) with thanks to John Lee for the issue at datalad
- A new section on how to debug and troubleshoot problems - with thanks to Tristan Glatard for the idea and contributions ([#538][])

#### Advanced

- A chapter on large-scale fair processing with parallel datalad-run calls ([#591][])
- A new section on configuring subdataset clone candidates and their priority ([#548][])
- A new chapter/section that compares the tool DVC to DataLad ([#569][])

#### Usecases

- Addition of a machine-learning application with DataLad ([#581][])
- Addition on Human Connectome Project (HCP) AWS credentials (thanks to Michael Joseph) ([#622][])
- Addition of a hands-on tutorial for reproducible papers ([#608][]), with thanks to Małgorzata Wierzba for feedback and contributions

#### Miscellaneous additions

- A variety of code lists and introductions ([#630][]), ([#613][])
- A few new permalinks: git-lfs ([#624][]), MPIB intro ([#614][])
- A new expandable section "Windows workaround" for Windows-specific notes and explanations([#532][])
- Large amount of Windows adjustments in the Basics ([#588][])
- FAQs on copying locked files out of datasets, and on caveats with the BIDS validator - with thanks to Remi Gau ([#570][]), ([#562][])
- The handbook's GitHub repository received a welcome bot (with thanks to The Turing Way project for CC-BY illustrations), and a "Discussions" Forum
- The handbook's frontpage links to the cheat sheet with a nice illustration ([#578][])

## v0.13 (June 23rd 2020) -- Towards a tetralogy!

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
[#532]: https://github.com/datalad-handbook/book/pull/532
[#548]: https://github.com/datalad-handbook/book/pull/548
[#562]: https://github.com/datalad-handbook/book/pull/562
[#569]: https://github.com/datalad-handbook/book/pull/569
[#570]: https://github.com/datalad-handbook/book/pull/570
[#578]: https://github.com/datalad-handbook/book/pull/578
[#581]: https://github.com/datalad-handbook/book/pull/581
[#585]: https://github.com/datalad-handbook/book/pull/585
[#588]: https://github.com/datalad-handbook/book/pull/588
[#591]: https://github.com/datalad-handbook/book/pull/591
[#592]: https://github.com/datalad-handbook/book/pull/592
[#603]: https://github.com/datalad-handbook/book/pull/603
[#608]: https://github.com/datalad-handbook/book/pull/608
[#613]: https://github.com/datalad-handbook/book/pull/613
[#614]: https://github.com/datalad-handbook/book/pull/614
[#615]: https://github.com/datalad-handbook/book/pull/615
[#622]: https://github.com/datalad-handbook/book/pull/622
[#624]: https://github.com/datalad-handbook/book/pull/624
[#626]: https://github.com/datalad-handbook/book/pull/626
[#627]: https://github.com/datalad-handbook/book/pull/627
[#630]: https://github.com/datalad-handbook/book/pull/630
[#641]: https://github.com/datalad-handbook/book/pull/641
[#646]: https://github.com/datalad-handbook/book/pull/646
[#647]: https://github.com/datalad-handbook/book/pull/647
[#648]: https://github.com/datalad-handbook/book/pull/648
[#650]: https://github.com/datalad-handbook/book/pull/650
[#651]: https://github.com/datalad-handbook/book/pull/651
[#655]: https://github.com/datalad-handbook/book/pull/655
[#656]: https://github.com/datalad-handbook/book/pull/656
[#657]: https://github.com/datalad-handbook/book/pull/657
[#658]: https://github.com/datalad-handbook/book/pull/658
[#659]: https://github.com/datalad-handbook/book/pull/659
[#660]: https://github.com/datalad-handbook/book/pull/660
[#661]: https://github.com/datalad-handbook/book/pull/661
[#662]: https://github.com/datalad-handbook/book/pull/662
[#663]: https://github.com/datalad-handbook/book/pull/663
[#665]: https://github.com/datalad-handbook/book/pull/665
[#666]: https://github.com/datalad-handbook/book/pull/666
[#667]: https://github.com/datalad-handbook/book/pull/667
[#669]: https://github.com/datalad-handbook/book/pull/669
[#670]: https://github.com/datalad-handbook/book/pull/670
[#671]: https://github.com/datalad-handbook/book/pull/671
[#672]: https://github.com/datalad-handbook/book/pull/672
[#675]: https://github.com/datalad-handbook/book/pull/675
[#678]: https://github.com/datalad-handbook/book/pull/678
[#679]: https://github.com/datalad-handbook/book/pull/679
[#682]: https://github.com/datalad-handbook/book/pull/682
[#684]: https://github.com/datalad-handbook/book/pull/684
[#685]: https://github.com/datalad-handbook/book/pull/685
[#694]: https://github.com/datalad-handbook/book/pull/694
[#759]: https://github.com/datalad-handbook/book/pull/759
[#680]: https://github.com/datalad-handbook/book/pull/680
[#691]: https://github.com/datalad-handbook/book/pull/691
[#693]: https://github.com/datalad-handbook/book/pull/693
[#703]: https://github.com/datalad-handbook/book/pull/703
[#704]: https://github.com/datalad-handbook/book/pull/704
[#707]: https://github.com/datalad-handbook/book/pull/707
[#717]: https://github.com/datalad-handbook/book/pull/717
[#721]: https://github.com/datalad-handbook/book/pull/721
[#722]: https://github.com/datalad-handbook/book/pull/722
[#723]: https://github.com/datalad-handbook/book/pull/723
[#724]: https://github.com/datalad-handbook/book/pull/724
[#743]: https://github.com/datalad-handbook/book/pull/743
