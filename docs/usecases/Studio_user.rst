.. \_usecase_Rstat:

My first steps as a R users
---------------------------

.. index:: ! Usecase; R users quickstart

This use case sketches typical entry points for R users, who know
nothing about bash, but still want to leverage the power of git-annex
and datalad. I will list here issues I needed some testing before
understanding. Hopefully this will help you quickstart your journey. 

1.  Code and data: git and git-annex
2.  Using `datalad run` ?
3.  Dealing with (relative) path
4.  oups, how to undo `datalad save` done on the wrong repository ?

This use case take for granted you know how git works, but are not
familiar with git-annex and datalad. This is the results of multiple
tests and looking into what happened using sourcetree, as well as actually reading the `datalad run` chapter of the handbook a couple of time.

.. gitusernote:: Take home messages:
  
  datalad commands run in the terminal, not the Console.
  
  The simplest way to tell datalad not to use git-annex for your code
files is to use `datalad create -c text2git --force` command.

  the `datalad run Rscript "path-to-script.r"` will run your script.
  
  Use additional options to read or write annexed files (and give more
info for commit message).

  in your R script, use path relative to the project, not relative to the code position.

Why git-annex
-------------

As you probably know if you read this, git
does not work well with large or numerous files, and I want to use
datalad to circonvent the issues. The rough idea is that data files
should be annexed, while the code should use the normal git
workflow, which is more powerful and convenient for text files.

.. gitusernote:: annexed files

  When files are added via git-annex, they are moved somewhere eles and the file is now a kind of link to the real content. Using the Rstudio file system, clicking on the simlink will actually open the file content, but that file is in read-only mode. So if you git-annex your code, you will not be able to make changes and save them directly in Rstudio. In addition, the advantage of git for text files are lost, as annexed content is treated as binary files: each new version is saved in its entirety.

  To save changes to an annexed file, one needs to unlock the file in question (using the `datalad unlock <filename>` command) first. Then you can overwrite the file and save its new state.    

Datalad default: all annexed !?
--------------------------------

I am used to write code, and version control it using git (all inside
Rstudio), my usual workflow is to modify files, save them, and then
commit all the changes at once. I would push these changes to a remote
repository from time to time. 

My first reflex was to keep the workflow but running `datalad save` in
the terminal window of Rstudio, instead of the commit step. This does
not work, because datalad will use git-annex per default for all files
(see detail box if you do not get why it fails). It also will use
git-annex on files that were previously added via `git add`. Therefore,
one should tell datalad not to use git-annex for your code files, to
keep your usual workflow.



The simplest way to tell datalad not to use git-annex for your code
files is to use `datalad create -c text2git --force` command (force is
necessary if you change an existing repository). Note that all text
files will be added to git using this, so if you have large text files
(.csv or .json files), you will need to be more precise in what text
file should not be annexed. See
<http://handbook.datalad.org/en/inm7/basics/101-124-procedures.html#>
for details on how text2git change `.gitattributes` to achieve that.

Using Datalad run ?
---------------------

### Do I have to use datalad run?

In theory, you can run your R script the way you are used to, as long as all files are present locally, and you are not overwriting files. If you need to access files that are only on the server (because you dropped them), you need to run `datalad get` to download them first. If you need to overwrite files which were saved via git-annex (that is that are not text files), you need to unlock them. You can unlock all your repository, including submodules files, running `datalad unlock -r .`

.. gitusernote:: locking

  to lock the files again, you can use `datalad save` (and derivates), this will not create a new commit (unless they are other changes made than the unlock). 




### how to use datalad run

Because datalad runs in the terminal, it needs a terminal command to run the script, for R, that command is "Rscript": `datalad run Rscript "<path-to-script.r>"`. Not the path is relative to where the terminal is, if you are using Rstudio projects, the terminal tab is per default in the working directory of the project. If your code is in a submodule and the data is in another one, you should run this command from the parent repository.

To access annexed files, we need to use the input and output options:

.. code-block:: bash

    
    $ datalad run Rscript \
      --input "file1.csv" \
      --input "data/file2.json" \
      --output "figures/*.png" \
      --explicit \
      "<path-to-script.r>" {inputs} {outputs}
  
  

Behavior explained :

- Input: To be read, files are downloaded if not present. Note that they are not unlocked (no need for reading them) and that they will not be dropped again after being read.
- Output: files are unlocked so they can be overwritten. If the files are not present (dropped), they will not be downloaded. This may make your code fail: if it does, either get the files manually before running `datalad run`, or remove them in the R code (`r file.remove()`). In other case, it will work and it will even detect when the file has not been modified and make no commit.
- explicit: datalad runs normally only in clean repositories, this includes all submodules. By adding --explicit, datalad will only test that the output files are clean, and only output files will be saved. Please use with care, as the script and data you use will not be tested and provenance information can be lost.
- {inputs} {outputs} If you add the placeholders, the terminal will actually gives the input and output text as argument to the Rscript bash function. One can access them in the R script with `args <- commandArgs(trailingOnly = TRUE)` (then get them with `args[i]`, with i starts at 1).
- At the end, datalad usually runs `datalad save -r` so that modification made by the code in the whole repository, including submodules will be done (exception when --explicit is given, see above.) This will include any intermediate file created by your code in bash mode, that is using `Rscript "path-to-code.R "` in the terminal (it can happen that bash mode creates more files than running the code directly)  



On can set as many input and output files, one can use `*` to define several files with a similar ending (in the example all .png figures will be unlocked), one can list files who are not annexed to give more information in the commit message.

.. gitusernote:: using datalad run

  unlocking the files will make its state "unclean", so if you use datalad run, you need to set output options in the function, you cannot unlock files manually before.

  The commit message will only look at the options, whether the code use these input and output files is not checked.

  One can write these datalad commands in a shell script file in Rstudio, and push the run button will run them in the terminal.
   
  Using `datalad run` correctly is sometimes tricky, and since it does save each time, it can make the repository history quite messy. Make sure to give good commit messages. 


The advantage of using datalad run and not running the code directly is that R code cannot access directly annexed files, that might even be only present in the server but not on the computer. For each input and output files, one would need to get it or unlock it manually before running the code, then save it again. Datalad run can do all that automatically.

In addition, datalad run write specific comments in the commit message, so that it is easy to understand what was done, and so that the `datalad rerun` command can be used.


Dealing with (relative) path
----------------------------

You may work on your code in a submodule using your usual git workflow. It is still best practice to write your code as run from the parent repository in term of path. You may run them there too.

My current workflow is to have 2 Rstudio projects open. I work in the parent repository, but make commits and push in the code repository.

Undo`datala d save` 
-------------------

Sometimes one goes to fast and make a `datalad save` in a repository that was not ready to be saved, or one runs the `datalad run` command and one would want to undo it. This is a bit complex and needs some manual interventions.

The handbook explain what to do well: https://handbook.datalad.org/en/0.17/basics/101-137-history.html#untracking-accidentally-saved-contents-stored-in-git-annex:

- You need to manually check what is the hash of the commit you want to go back to, and what was changed in git-annex since then. You can do that in Rstudio via the history button of the git tab, and patience if you want to go far back.
- unlock all files that were created with `datalad unlock <filename>`
- Then you go back git commits with `git reset --mixed <hash>`

The save (but not the run) has been undone, and the files are present as untracked content (both the files that were put in git-annex and the file put in git). 

