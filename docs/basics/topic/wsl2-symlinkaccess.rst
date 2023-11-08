If you are using WSL2 you have access to a Linux kernel and POSIX file system, including symlink support.
Your DataLad experience has therefore been exactly as it has been for macOS or Linux users.
But one thing that bears the need for additional information is sharing files in dataset between your Linux and Windows system.

It's fantastic that files created under Linux can be shared to Windows and used by Windows tools.
Usually, you should be able to open an explorer and type ``\\wsl$\<distro>\<path>`` in the address bar to navigate to files under Linux, or type ``explorer.exe`` into the WSL2 terminal.
Some core limitations of Windows can't be overcome, though: Windows usually isn't capable of handling symlinks.
So while WSL2 can expose your dataset filled with symlinked files to Windows, your Windows tools can fail to open them.
How can this be fixed?

.. index::
  pair: checkout; Git command
  pair: check out particular version; with Git

Whenever you need to work with files from your datasets under Windows, you should *unlock* with ``datalad unlock``.
This operation copies the file from the annex back to its original location, and thus removes the symlink (and also returns write :term:`permissions` to the file).
Alternatively, use `git-annex adjust --unlock <https://git-annex.branchable.com/git-annex-adjust>`_ to switch to a new dataset :term:`branch` in which all files are unlocked.
The branch is called ``adjusted/<branchname>(unlocked)`` (e.g., if the original branch name was ``main``, the new, adjusted branch will be called ``adjusted/main(unlocked)``).
You can switch back to your original branch using ``git checkout <branchname>``.
