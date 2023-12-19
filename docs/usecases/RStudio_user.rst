.. _usecase_Rstat:

DataLad and RStudio: First steps
--------------------------------

.. index:: ! Usecase; R users quickstart

This use case sketches typical entry points for R and `Rstudio <https://en.wikipedia.org/wiki/RStudio>`_ users. 

#. A repository having submodules for data and code is cloned.
#. R scripts are developed in Rstudio
#. R scripts are run using ``datalad run``

(This is a `hello world` type of analysis, used only for demonstration purposes.)

The Challenge
^^^^^^^^^^^^^

Max has been using Rstudio together with :term:`GitHub` for a long time. They know how :term:`Git`
works. Max has learned that Git will not work with their new project,
because there will be too many files and some dataset files will be too large.
Max read the DataLad :ref:`Handbook Basics <basics-intro>` and has decided to use DataLad.
They indeed want to version control larger files, and spread files across several repositories, linked as "DataLad dataset hierarchies".
Max still wants to use Rstudio and a combination of R and Python scripts for the
data analysis.

Bobby is a data manager who already learned (the hard way), how to handle DataLad
using Rstudio. 
He provides Max with a repository with submodules, that should be ready to be used.
He is happy to help Max, as he knows this will allow them to record analysis provenance.





Setting up
^^^^^^^^^^

Max follows the handbook and installs DataLad on his computer.
He already has SSH keys installed, as he was using it to work with Git repositories before (if you do not know SSH refers to the handbood section on installation or the `Rstudio tutorial <https://support.posit.co/hc/en-us/articles/200532077-Version-Control-with-Git-and-SVN>`_ ). 
Max first want to clone the repository on their computer, they use the Rstudio 
`create a new project` function using the SSH address of the parent repository.


.. figure:: ../artwork/src/rstudio/Rstudio-create.png
   :scale: 80 %
   :alt: screenshots patchwork of Rstudio new project creation.

   Figures of several screenshots demonstrating the creation of new projects on Rstudio.

Max can't see submodules content and comes to Bobby.

Bobby comes and run ``datalad get . -n -r`` in the terminal window of Rstudio. 

.. figure:: ../artwork/src/rstudio/Rstudio-terminal.png
   :scale: 80 %
   :alt: screenshot of Rstudio terminal tab.

   Using Rstudio terminal window to give DataLad commands


They then explain:
  - Rstudio can only use simple Git commands, which do not clone submodule content.
  - DataLad command are run in the terminal window. DataLad does not have a R package and do not run in the console.
  - This specific function :command:`datalad get .` will download all files, it has two options:
     - ``-n`` option means annexed files will not be downloaded
     - ``-r`` option (short for ``--recursive``) means that the function is run in all submodules, recursively.

Max is thanking Bobby for the insights.
Before leaving, Bobby gives an additional advice: Our template uses "pure Git" repositories, DataLad functions will work but they will not use git-annex. 
Looking at Max incredulous stare, they explain further: you will now be able to use DataLad to manage the submodules and save them all at once, but big files will be added to Git, this will make it unusable very fast. 
So you need to turn this pure Git repository into proper :term:`DataLad dataset` (meaning a Git repository with additional features from :term:`git-annex` and DataLad).

Max is a bit puzzled and read the basics chapter of the handbook again.
Then, they see that :command:`datalad create --force` is the correct command  to create a DataLad dataset.
when the folder already exist, so they  run 
``datalad create --force -r`` in the parent repository.
Now they are sure they set up DataLad to work in the repository and all submodules,
since they used the ``-r``  option.
Max also now understand what Bobby meant when he said that annexed files are not downloaded, and this is further explained in the next section.

.. gitusernote:: Pushing and GIN-Tonic

  The scenario  does not present the use of remotes (server version of the resitory) and :command:`datalad push`, as it is indeed not different for R or Rstudio users.
  One *only* needs to use DataLad commands (in the terminal tab) instead of Git (integration in Rstudio-GUI or shell).
  
  While the original repositories are described as pure Git repositories here,
  most of the scenario was actually tested
  using a :term:`GIN` repository with git-annex, with :term:`submodule`\s 
  for data and for code, that were created using the `Tonic tool and templates <https://gin-tonic.netlify.app>`_ . 
  Note that the template itself `was ported from a single GitHub repository into DataLad datasets <https://gin-tonic.netlify.app/installation/template_repository/>`_ . 
  
  
  
    
Working on the code
^^^^^^^^^^^^^^^^^^^

Max starts to write one script that he saves in the analysis submodule, and use :command:`datalad save` typing ``datalad save -r -m "this is a first draft of the script"`` command in the terminal (in the parent repository). 
The commit history of the parent and the analysis repositories shows the message and Max things everything works fine.
Max change the script, but Rstudio does not want to save the changes.
Max save a copy of the script file and call Bobby for help.

Bobby start to explain what happened:
DataLad saved the script using Git-annex.
This means that the file was moved somewhere else, and the content was replaced by a code linking to the file location. 
Because it is :term:`symlink`, Rstudio still read the content of the original file when clicking on it, but it cannot overwrite the file: that file is in read-only mode.
This is explained in detail in the :ref:`Handbook chapters on Git-annex <chapter_gitannex>`.

One could overwrite the file by first unlocking it (using ``datalad unlock .``), but that would not be very practical, and it would save the script as a binary file, making the version control very inefficient.
You do not want to use Git-annex for scripts, as they are text files which version should be handled by Git.
Bobby then shows how to tell DataLad to use git for text files and he runs: ``datalad create -c text2git --force``. 

Max can now work on its script as he used to, but commit changes using the ``datalad save -r`` command.




.. gitusernote:: The dangers of text2git

  Note that all text files will be added to git using this option, so if you have large text files (.csv or .json files) that you want to be added via Git-annex, you will need to be more precise in what text file should not be annexed. 
  This may be quite important if you want to be able to *drop* files to keep space on your computer harddrive.
  See :ref:`Handbook chapters <procedures>` for details on how text2git change `.gitattributes` to achieve that.

Running code
^^^^^^^^^^^^

The code use relative path starting in the parent repository, as they are used to do in normal projects, and since the code is run from there in Rstudio.
 (Later on, Max realize he can also use git commands from inside the analysis submodule, and he creates a second Rstudio project in that submodule, just to use the git functions he is used to. Code is run from the parent Rstudio project.)

Max is now happy and start working on his code. 
In order to test everything, Max put a text file in the data submodule, and write a script that read the file and produce a pdf writing the text as an image.
He runs the code and it works!
He know save it with ``datalad save -r``.
He runs the code again and... ups it fails.

Max thinks a bit about it and remember what he learned before: the pdf file has been annexed and cannot be overwritten.
Max therefore runs ``datalad unlock . -r`` and then runs the code, and it works.
Max realize also that using ``datalad save . -r`` lock the files again, 
it does it also if there is no change in the repository (and therefore no commit made).

At the coffee break, Max meets Bobby and complain about the process.
Bobby use the occasion to say that another problem can arise: if you drop the input files (erase GIT-annex data from your computer once they are on the server), you would also need to download the input files before running the code (using the ``datalad get`` command).

Bobby tells Max it is time to learn about ``datalad run``.

DataLad run with Rscripts
^^^^^^^^^^^^^^^^^^^^^^^^^^

Bobby starts with the basics of running R code via :command:`datalad run`:

Because datalad runs in the terminal, it needs a terminal command to run the script.
For R, that command is "Rscript": ``datalad run Rscript "<path-to-script.r>"``.
The path is relative to where the terminal is, the terminal tab is per default in the working directory of the project. If your code is in a submodule and the data is in another one, you should run this command from the parent repository.

(Bobby needs here to make sure Rscript is a recognized command and set the PATH variable accordingly.)

"What are the advantages of using this command", asks Max.

There are twofold (at least), answers Bobby.
First, this command will take care of obtaining input files and unlocking output files for you.
Second, and most importantly, the command will record what has been done in the commit message automatically: what input, what script, what output was used.
This code therefore records **provenance**: you will always be able to find what workflow and data version was used to create your figures.

Since Bobby looks very enthusiastic about provenance, Max reads a little more about it in the handbook: usecases/provenance_tracking, https://handbook.datalad.org/en/latest/basics/101-108-run.html#run

Then, Max create a bash script in Rstudio and run it using the usual button (This runs the bash script in the terminal). After some practice and tests,
Max finds his way between testing/developing code on training data (as he has been used to, while using :command:`datalad unlock` and :command:`datalad get` when needed), and running ready code on real data in a reproducible way using :command:`datalad run`. 

 

.. code-block:: bash

    
  $ datalad run  \
  --input "file1.csv" \
  --input "data/file2.json" \
  --output "figures/*.png" \
  --explicit \
  Rscript "<path-to-script.r>" {inputs} {outputs}

.. figure:: ../artwork/src/rstudio/Rstudio-dataladrun.png
   :scale: 80 %
   :alt: screenshot of Rstudio bash code window

   Figures of bash code running the DataLad run command


One can set as many input and output files, one can use `*` to define several files with a similar ending (in the example all .png figures will be unlocked). It is good practice to list files in input and output even if they do not need to be handled by DataLad, in order to give more information in the commit message.

.. gitusernote:: Behavior explained

  - Input: To be read, files are downloaded if not present. Note that they are not unlocked (no need for reading them) and that they will not be dropped again after being read.
  - Output: files are unlocked so they can be overwritten. If the files are not present (dropped), they will not be downloaded. This may make your code fail: if it does, either get the files manually before running `datalad run`, or remove them in the R code (`r file.remove()`). In other case, it will work and it will even detect when the file has not been modified and make no commit.
  - explicit: :command:`datalad run` runs normally only in clean repositories, this includes all submodules. By adding --explicit, DataLad will only test that the output files are clean, and only output files will be saved. Please use with care, as the script and data you use will not be tested and provenance information can be lost.
  - {inputs} {outputs}: If you add the placeholders, the terminal will actually gives the input and output text as argument to the Rscript bash function. One can access them in the R script with `args <- commandArgs(trailingOnly = TRUE)` (then get them with `args[i]`, with i starts at 1).
  - At the end, DataLad usually runs `datalad save -r` so that modification made by the code in the whole repository, including submodules will be recorded and committed (exception when --explicit is given, see above.) This will include any intermediate file created by your code in bash mode, that is using `Rscript "path-to-code.R "` in the terminal (it can happen that bash mode creates more files than running the code directly).  




.. gitusernote:: Advanced tips for the DataLad run command

  unlocking the files will make its state "unclean", so if you use DataLad run, you need to set output options in the function, you cannot unlock files manually before.

  The commit message will only look at the options, whether the code use these input and output files is not checked.
   
  Using :command:`datalad run` correctly is sometimes tricky, and since it does save each time, it can make the repository history quite messy. Make sure to give good commit messages by adding a `-m` variable to it. 







.. importantnote:: Take home messages
  
  DataLad commands run in the terminal, not the R Console.
  
  The simplest way to tell DataLad not to use git-annex for your code files is to use ``datalad create -r -c text2git --force`` command.

  the ``datalad run Rscript "path-to-script.r"`` command will run your script.
  
  Use additional options to command: `datalad run` to read or write annexed files (and give more info for commit messages).

  In your R script, use path relative to the project, not relative to the code position.
  
  An understanding of how Git-annex works and why, makes it easier to understand the workflow, refer to :ref:`Handbook Git-annex Basics <chapter_gitannex>`.  
