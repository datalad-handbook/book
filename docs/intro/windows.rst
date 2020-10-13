.. _ohnowindows:

So... Windows... eh?
--------------------


DataLad and its underlying tools work different on Windows machines.
This makes the user experience less fun than on other operating systems -- an honest assessment.

.. figure:: ../artwork/src/warning.svg


Why is that?
For one, many software tools for research or data science are first written and released for Linux, then for Mac, and eventually Windows.
TensorFlow for Windows was `released only a full year after it became open source <https://developers.googleblog.com/2016/11/tensorflow-0-12-adds-support-for-windows.html>`_, for example, and Python only became easy to install on Windows in `2019 <https://devblogs.microsoft.com/python/python-in-the-windows-10-may-2019-update/>`_.
The same is true for DataLad and its underlying tools.
There *is* Windows support and user documentation, but it isn't as far developed as for Unix-based systems.

Some tools that DataLad or :term:`datalad extension`\s use are not available on Windows.
If you are interested in adding :term:`software container`\s to your DataLad dataset, for example, you will not be able to do so on a native Windows computer -- :term:`Singularity`, a widely used containerization software and dependency of the ``datalad-container`` extension, doesn't exit for Windows.
That sucks, and we're really sorry for this.
Its not that we pick dependencies that only work on Unix-based systems -- we try to use tools that are as cross-platform-compatible as possible.
But certain tools or functions simply don't (yet) work on Windows.
Take :term:`Docker`, another popular containerization software that has existed for far longer than Singularity: It can only be installed on Windows Pro or Enterprise, but not on Windows Home. Eh. :(

Beyond this, Windows uses a different file system than Unix based systems.
Given that DataLad is a data management software, it is heavily affected by this, and the Basics part of the handbook is filled with "Windows-Workarounds", expandable sections that highlight different behavior on native Windows installations of DataLad, or provide adjusted commands.
A quick example: Unix-based systems provide support for identifying the type of a file (e.g., text files) via "mime encoding" -- Windows instead relies on file extensions, and this requires adjustment.
Likewise, Windows has insufficient support for symlinking and locking files, which alters how :term:`git-annex` works, and may make interoperability of datasets between Windows and non-Windows operating systems not as smooth as between various flavours of Unix-like operating systems.

This section is for Windows users and entails an honest assessment of what is possible and what is not with DataLad on native Windows systems to prevent bad surprises or unmet expectations.
We try to keep a rough tracker of current issues and development goals on this page, and test the workflows depicted in the handbook on Windows machines.
Here is what **works** on Windows 10 with DataLad version 0.13.5 or higher:

- Create datasets
- Version control for arbitrary files
- Retrieving contents on demand and dropping them
- Pushing, cloning, and updating datasets
- Reproducible execution with ``datalad run``

Here are known issues that we are working on:

- The user documentation is not as well maintained and tested for Windows users
- The datalad-archives-special remote isn't happy on Windows
- Collaborative workflows with nested datasets with Windows and Non-Windows users are not smooth

Here are problems that are out of our hands:

- As there is no way to install :term:`Singularity` or :term:`Docker` on regular Windows machines, none of the functionality that the ``datalad-container`` extension provides can be used.
- As there is insufficient support for symlinking and locking, datasets will have a higher disk usage on Windows machines. Section :ref:`symlink` has the details on this.
- The Windows terminals are much less user friendly, and errors that are thrown on Windows systems are typically much more complex.
- DataLad and its underlying tools are slower on Windows.

While basic functionality is ensured, if you have access to an alternative set-up, using DataLad on anything but a Native Windows installation is smoother and more fail-safe, at least for the time being, and it will give more (and better tested) DataLad functionality.


What are feasible alternatives?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Its quite easy to say "Just use Linux" when you have no experience, support, or spare time and are hence reluctant to completely overhaul your operating system and reduce your productivity while you get a hang on it -- or if you rely on software that is native to Windows, such as Microsoft or Adobe products.
Its also easy to say "Just use a Mac, its much more user-friendly *and* Unix-based" when an Apple product is a very expensive investment that only few people can or want to afford.
Its a bit like recommending a MatLab user (proprietary, expensive, closed-source software) to switch to Python, R, Julia, or a similar open source alternative.
Yes, there are real benefits to it that make the change worthwhile to many, but that doesn't change the fact that it is effortful and may be frustrating.
But how about switching from MatLab to `Octave <https://www.gnu.org/software/octave/>`_, an open source programming language, made to be compatible to MatLab?
There definitely is work and adjustment involved, but much less work than when trying to rewrite your analyses in Go or C++.

It is tough if you have been using "a thing" for decades without much hassle and now someone tells you to change.
If you feel that you lack the time, resources, support, or knowledge, then throwing yourself into cold water and making a harsh change not only sucks, but its also not likely to succeed.
If you're juggling studies (or the general publish-or-perish-work-life-misery that Academia too often is), care-giving responsibilities, and surviving a pandemic, all while being in a scientific lab that advocates using Windows and works exclusively with Microsoft Excel, then switching to Arch Linux would widely be seen as a bad idea.

But is there a middle-ground, the "Octave" of Operating Systems?
It depends on what you need and what you want to do.
But you should at least consider possible alternatives and debate your individual pros and cons with yourself.
Below, we have listed solutions that may be feasible for you.


Use a compute cluster
"""""""""""""""""""""

If you are a researcher, chances are that your institution runs a large compute cluster.
Those things run on Linux distributions, they have knowledgeable system administrators, and typically institute-internal documentation.
Even if you are on a Windows computer, you can log into such a cluster (if you have an account), and use tools made for Unix-like operating systems there -- without having to deal with any of the set-up, installation, or maintenance, and with access to documentation and experienced users.
The section :ref:`install` also contains installation instructions for such shared compute clusters ("Linux machines with no root access").


The Windows Subsystem for Linux (version 2)
"""""""""""""""""""""""""""""""""""""""""""

You want to have a taste of Unix on your own computer, but in the most safe and reversible way.
Or you have essential software that only runs under Windows and you really need to keep a Windows Operating System.
Then the Windows Subsystem for Linux (WSL2) may be a solution.
`Microsoft acknowledges that a lot of software is assuming that the environment in which they run behaves like Linux, and has added a real Linux kernel to Windows with the WSL2 <https://docs.microsoft.com/en-us/windows/wsl/faq>`_.
If you enable WSL2 on your Windows 10 computer, you have access to a variety of Linux distributions in the Microsoft store, and you can install them with a single click.
The Linux distribution(s) of your choice becomes an icon on your task bar, and you can run windows and Linux in parallel.


**What should you be mindful of?** WSL is a minimalist tool in that it is made to run :term:`bash` or core Linux commands.
It does not support graphical user (GUI) interfaces or applications.
So while common Linux distributions have GUIs for various software, in WSL2 you will only be able to use a terminal.
Also, it is important to know that `older versions of WSL did not allow accessing or modifying Linux files via Windows <https://devblogs.microsoft.com/commandline/do-not-change-linux-files-using-windows-apps-and-tools/>`_.
Recent versions (starting with Windows 10 version 1903) `allow accessing Linux files with Windows tools <https://devblogs.microsoft.com/commandline/whats-new-for-wsl-in-windows-10-version-1903/>`_.

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