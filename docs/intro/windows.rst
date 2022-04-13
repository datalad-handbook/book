.. _ohnowindows:

So... Windows... eh?
--------------------


DataLad and its underlying tools work different on Windows machines.
This makes the user experience less fun than on other operating systems -- an honest assessment.

.. figure:: ../artwork/src/warning.svg


Many software tools for research or data science are first written and released for Linux, then for Mac, and eventually Windows.
TensorFlow for Windows was `released only a full year after it became open source <https://developers.googleblog.com/2016/11/tensorflow-0-12-adds-support-for-windows.html>`_, for example, and Python only became easy to install on Windows in `2019 <https://devblogs.microsoft.com/python/python-in-the-windows-10-may-2019-update/>`_.
The same is true for DataLad and its underlying tools.
There *is* Windows support and user documentation, but it isn't as far developed as for Unix-based systems.
This page summarizes core downsides and deficiencies of Windows, DataLad on Windows, and the user documentation.

Windows-Deficiencies
^^^^^^^^^^^^^^^^^^^^

Windows works fundamentally different than macOS or Linux-based operating systems.
This results in missing dependencies, altered behavior, and inconvenient workarounds.
Beyond this, Windows uses a different file system than Unix based systems.
Given that DataLad is a data management software, it is heavily affected by this, and the Basics part of the handbook is filled with "Windows-Wits", dedicated sections that highlight different behavior on native Windows installations of DataLad, or provide adjusted commands -- nevertheless, standard DataLad operations on Windows can be much slower than on other operating systems.

A major annoyance and problem is that some tools that DataLad or :term:`datalad extension`\s use are not available on Windows.
If you are interested in adding :term:`software container`\s to your DataLad dataset (with the ``datalad-container`` extension), for example, you will likely not be able to do so on a native Windows computer -- :term:`Singularity`, a widely used containerization software, doesn't exit for Windows, and while there *is* some support for :term:`Docker` on Windows, it does not apply to most private computers [#f1]_.

Windows also has insufficient support for :term:`symlink`\ing and locking files (i.e., revoking write :term:`permissions`), which alters how :term:`git-annex` works, and may make interoperability of datasets between Windows and non-Windows operating systems not as smooth as between various flavours of Unix-like operating systems.

In addition, Windows has a (default) `maximum path length limitation of only 260 characters <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation>`_.
However, DataLad (or rather, :term:`git-annex`) relies on `file content hashing <https://en.wikipedia.org/wiki/Hash_function>`_ to ensure file integrity.
Usually, the *longer* the `hash` that is created, the more fail-safe it is.
For a general idea about the length of hashes, consider that many tools including :term:`git-annex` use ``SHA256`` (a 256 characters long hash) as their default.
As git-annex represents files with their content hash as a name, though, a secure 256 character file name is too long for Windows.
Datasets thus adjust this default to a 128 character hash [#f2]_, but still, if you place a DataLad dataset into a deeply nested directory location, you may run into issues due to hitting the path length limit [#f3]_.
You *can* enable long paths in recent builds of Windows 10, `but it requires some tweaking <https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation#enable-long-paths-in-windows-10-version-1607-and-later>`_.

Windows also doesn't really come with a decent :term:`terminal`.
It is easy to get a nice and efficient terminal set up on macOS or Linux, it is harder on Windows.
For example, its :term:`tab completion` is deemed inefficient by many, it takes some `poking and clicking <https://www.howtogeek.com/353200/how-to-enable-copy-and-paste-keyboard-shortcuts-in-windows-10s-bash-shell/>`_ to enable copy-pasting, most standard command line tools are not pre-installed, and many aren't even available or easy to access from the terminal.
Usually, Windows users aren't bothered much by this, but DataLad is a command line tool, and with a command line that is difficult to use, command line tools become difficult to use, too.
Are you a Windows user and have tips for setting up a decent terminal?
`Please tell us, we're eager to learn from you <https://github.com/datalad/datalad>`_.

Sadly, even the non-commandline parts of Windows bear inconveniences.
Windows' File Explorer does not display common file extensions by default, and some editors (such as notepad) add their own file extensions to files, even when they already have an extension.
This can cause confusion.


Unfortunately, issues that affect Windows itself are out of our hands.
We can adapt to limitations, but in many cases it is not possible to overcome them.
That sucks, and we're really sorry for this.
Its not that we pick dependencies that only work on Unix-based systems -- we try to use tools that are as cross-platform-compatible as possible, but certain tools, functions, or concepts simply don't (yet) work on Windows:

- As there is no way to install :term:`Singularity` or :term:`Docker` on regular Windows machines, none of the functionality that the ``datalad-container`` extension provides can be used.
- As there is insufficient support for symlinking and locking, datasets will have a higher disk usage on Windows machines. Section :ref:`symlink` has the details on this.
- The Windows terminals are much less user friendly, and errors that are thrown on Windows systems are typically much more complex.
- DataLad and its underlying tools are slower on Windows.


DataLad-on-Windows-Deficiencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DataLad is developed and predominantly used on Linux-based operating systems.
There is a broad suite of `unit tests <https://en.wikipedia.org/wiki/Unit_testing>`_ and `continuous integration <https://en.wikipedia.org/wiki/Continuous_integration>`_ to ensure that functions and commands work under Windows, but given that development and user base is mostly not Windows-based, many bugs that would only surface during complete workflows (as opposed to atomic unit testing) or on machines with specific configurations, versions, or software environments (as opposed to the simplistic and isolated Windows test environments on continuous integration) have not been discovered yet.
And a typical Windows user may also use their computer differently than a Linux-based developer imagines computers to be used.

Thus, when using DataLad under Windows it is likely that you encounter bugs.
We're trying to prevent this, but it is a normal part of (scientific) software development.
What you can do to help us improve your experience is to talk to us at `github.com/datalad/datalad <https://github.com/datalad/datalad>`_ about problems or bugs you ran into, about your typical workflows, and the usecases you are trying to achieve.

User documentation deficiencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DataLad Handbook is tested on :term:`Debian` and predominantly created by Unix users [#f4]_.
Being written by many converted Linux users, is filled with start-to-end instructions and tips for Unix systems that have sufficient detail to help Unix newcomers to get started, and it aims to be accessible to everyone -- you don't need to be a Linux crank to be able to use the handbook.

However, you may need to be a Windows crank (or a fearless experimentalist) if you want to use all of the handbook on a Windows computer, though.
There hasn't been nearly as much time invested into finding, describing, and solving caveats or edge cases, and there isn't enough "daily Windows usage" expertise to be able to give all of the advice that may be needed to identify or prevent problems or improve the user experience to the maximum.

The workflow-based and user-centric narrative of the Basics has been developed on a Unix-based system -- Windows-related enhancements are solely adjustments or workarounds.
So far, only the :ref:`basics-intro` have been tested with a Windows computer (Windows 10, build-version 2004) and adjusted where necessary.
We're working on more adjustments, testing, and general improvements, but its a process.
You can help us prioritize Windows by getting in touch to voice general interest, discover and report bugs, or contribute to the user documentation with your own advice and experiences.

So, overall...
^^^^^^^^^^^^^^

You won't get the best possible DataLad experience on a Windows computer.
While basic functionality is ensured, it is smoother and more fail-safe to use DataLad on anything but a Native Windows installation, at least for the time being.
When sticking to Windows, though, you could find out about interesting aspects of your operating system and help us improve Windows functionality if you tell us about your workflows or report bugs.


Are there feasible alternatives?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to use DataLad, but fear problems when on Windows, what is there that you can do?
Should you switch your operating system?

Its quite easy to say "Just use Linux" but tough to do when you have no experience, support, or spare time and are hence reluctant to completely overhaul your operating system and reduce your productivity while you get a hang on it -- or if you rely on software that is native to Windows, such as Microsoft or Adobe products.
Its also easy to say "Just use a Mac, its much more user-friendly *and* Unix-based" when an Apple product is a very expensive investment that only few people can or want to afford.
Its a bit like recommending a MatLab user (proprietary, expensive, closed-source software) to switch to Python, R, Julia, or a similar open source alternative.
Yes, there are real benefits to it that make the change worthwhile to many, but that doesn't change the fact that it is effortful and may be frustrating.
But how about switching from MatLab to `Octave <https://www.gnu.org/software/octave/>`_, an open source programming language, made to be compatible to MatLab?
There definitely is work and adjustment involved, but much less work than when trying to rewrite your analyses in Go or C++.
It is tough if you have been using "a thing" for decades without much hassle and now someone tells you to change.
If you feel that you lack the time, resources, support, or knowledge, then throwing yourself into cold water and making a harsh change not only sucks, but its also not likely to succeed.
If you're juggling studies (or the general publish-or-perish-work-life-misery that Academia too often is), care-giving responsibilities, and surviving a pandemic, all while being in a scientific lab that advocates using Windows and works exclusively with Microsoft Excel, then switching to Arch Linux would widely be seen as a bad idea.

But is there a middle-ground, the "Octave" of switching Operating Systems or alternative solutions?
It depends on what you need and what you want to do.
Below, we have listed solutions that may be feasible for you as an alternative to native Windows so that you can debate individual pros and cons of each alternative with yourself.



Use a compute cluster
"""""""""""""""""""""

If you are a researcher, chances are that your institution runs a large compute cluster.
Those things run on Linux distributions, they have knowledgeable system administrators, and typically institute-internal documentation.
Even if you are on a Windows computer, you can log into such a cluster (if you have an account), and use tools made for Unix-like operating systems there -- without having to deal with any of the set-up, installation, or maintenance, and with access to documentation and experienced users.
The section :ref:`install` also contains installation instructions for such shared compute clusters ("Linux machines with no root access").


The Windows Subsystem for Linux (version 2)
"""""""""""""""""""""""""""""""""""""""""""

If you want to have a taste of Unix on your own computer, but in the most safe and reversible way, or have essential software that only runs under Windows and really need to keep a Windows Operating System, then the Windows Subsystem for Linux (WSL2) may be a solution.
`Microsoft acknowledges that a lot of software is assuming that the environment in which they run behaves like Linux, and has added a real Linux kernel to Windows with the WSL2 <https://docs.microsoft.com/en-us/windows/wsl/faq>`_.
If you enable WSL2 on your Windows 10 computer, you have access to a variety of Linux distributions in the Microsoft store, and you can install them with a single click.
The Linux distribution(s) of your choice becomes an icon on your task bar, and you can run windows and Linux in parallel.


**What should you be mindful of?** WSL is a minimalist tool in that it is made to run :term:`bash` or core Linux commands.
It does not support graphical user (GUI) interfaces or applications.
So while common Linux distributions have GUIs for various software, in WSL2 you will only be able to use a terminal.
Also, it is important to know that `older versions of WSL did not allow accessing or modifying Linux files via Windows <https://devblogs.microsoft.com/commandline/do-not-change-linux-files-using-windows-apps-and-tools/>`_.
Recent versions (starting with Windows 10 version 1903) `allow accessing Linux files with Windows tools <https://devblogs.microsoft.com/commandline/whats-new-for-wsl-in-windows-10-version-1903/>`_, although some tweaking, explained in :ref:`wslfiles`, is necessary.

**How do I start?**
Microsoft has detailed installation instructions `here <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_.

Linux Mint
""""""""""

There isn't much that holds you to Windows?
The software you use is either already open source or available on Linux or easily replaceable by available alternatives (e.g., libre office instead of Microsoft Word, the Spotify player in a web browser instead of as an App)?
But you're reluctant to undergo huge changes when switching operating systems?
Then Linux Mint may be a good starting point.
Its user interface is not identical to Windows, but also not that far away, it is a mature operating system, its very user-friendly, there is a helpful and welcoming community behind it, and -- like all Linux distributions -- it is free.

**What should I be mindful of?** If you're changing your operating system, **create a backup** of your data (unless you do it on a new computer of course). You can't install a new OS and have all data where you left it -- pull it onto an external drive, and copy it back to your new OS later.
Also, take a couple of minutes and google whether the hardware of your computer is compatible with Linux.
Go to your system's settings and find out the name and version of your computer, your graphics card and CPU, and put all of it into a Google search that starts with "Install Linux on <hardware specifications>".
Some hardware may need additional configuration or be incompatible with Linux, and you would want to know about this upfront.
And don't be afraid to ask or look for help.
The internet is a large place and filled with helpful posts and people.
Take a look at user forums such as `forums.linuxmint.com/ <https://forums.linuxmint.com/>`_ -- they likely contain the answers to the questions you may have.

**How do I start?** A nice and comprehensive overview is detailed in `this article <https://uk.pcmag.com/adobe-photoshop-cc/124238/how-to-make-the-switch-from-windows-to-linux>`_.

.. rubric:: Footnotes

.. [#f1] If you are thinking, "Well, why would you use :term:`Singularity`, :term:`Docker` is available on Windows!": True, and ``datalad-container`` can indeed use Docker. But Docker can only be installed on Windows Pro or Enterprise, but not on Windows Home. Eh. :(

.. [#f2] The path length limitation on Windows is the reason that DataLad datasets always use hashes based on `MD5 <https://en.wikipedia.org/wiki/MD5>`_, a hash function that produces a 128 character hash value. This wouldn't be necessary on Unix-based operating systems, but is required to ensure portability of datasets to Windows computers.

.. [#f3] The path length limitation certainly isn't only a problem for DataLad and its underlying tools. Many users run into a Path length related problems at least once, by accident. Downloading or copying files with long names into a folder that itself has a long name, for example, can become an unexpected issue (especially if you are not aware of the limit). Imagine transferring pictures from your friends camera into ``C:\Users\"Bob McBobface"\Desktop\Pictures\"Vacation Pictures"\2020\Saint-Remy-en-Bouzemont-Saint-Genest-et-Isson\"From Alice and Sasha"\Camera\`` -- those file names shouldn't be too long to fit in the limit. Likewise, when ``git clone``\ing a :term:`Git` repository that was created on a Unix computer and contains very long file names could fail.

.. [#f4] Its not written by Windows-lynching ideologists and Linux cranks, though. The lead author switched from Windows to Debian 1.5 years before starting to write the handbook, coming from more than a decade of happy Windows experience. She doesn't regret having made the change at all, but she respects and understands reluctance to switch.
