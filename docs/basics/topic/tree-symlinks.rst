First of all, the Windows ``tree`` command lists only directories by default, unless you parametrize it with ``/f``.
And, secondly, even if you list the individual files, you would not see the :term:`symlink`\s shown below.
Due to insufficient support of symlinks on Windows, git-annex does not use them.
Please read on for a basic understanding of how git-annex usually works -- a Windows Wit at the end of this section will then highlight the difference in functionality on Windows.
