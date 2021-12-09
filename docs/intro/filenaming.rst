.. _filenaming:

How to name a file: Interoperability considerations
---------------------------------------------------

One of the most fundamental data management tasks is naming files.

.. figure:: https://imgs.xkcd.com/comics/documents.png

This may sound mundane to some --- "yeah, I guess I can't manage data if it doesn't have a file name, but what's the big deal? I already know that `I shouldn't use spaces in file names <https://superuser.com/questions/29111/what-technical-reasons-exist-for-not-using-space-characters-in-file-names>`_".
Other people take it to the edge of `bikeshedding <https://en.wiktionary.org/wiki/bikeshedding>`_ an beyond: "Let's start each file name with the ISO 8601 date format of its first modification for better sorting!"
But between the two extremes, there are a surprising amount of *interoperability* considerations --- practices and tips to ensure cross-platform compatibility --- in order to create file names that work on your own as well as on anyone else's machine.

This matters because the files, directories, or repositories that you may at some point share with friends, colleagues, or the entire internet should successfully make it to those other people's computers, and on those computers they should be usable for their intended purpose.
As you will see in some examples below, having a completely fail-safe file name is the first step in ensuring this.
Coincidentally, a short deep-dive into interoperability hacks for file names will probably also teach you some fascinating facts about your own or other operating systems, file systems, or common tools that you may not have known yet.

Oh no, normalization!
^^^^^^^^^^^^^^^^^^^^^

Different operating systems, file systems, or tools normalize names given to files, and this can go wrong in many ways:

Don't create files that differ only in case
===========================================

While many Unix systems save file names exactly as provided, and are able to differentiate between ``example.txt`` and ``Example.txt``, this won't work on other systems.
Filesystems such as File Allocation Table (FAT) or Extended File Allocation Table (EXFAT) always convert filenames to uppercase: ``example.txt`` will be stored as ``EXAMPLE.TXT``, as will ``Example.txt``, or ``exaMple.txt``.
That's really bad news if you were to share a folder filled with ``example.txt`` files with different casing variations from your Linux computer with a USB stick.
But also if you happen to have both a ``README`` and a ``readme`` file in your directory, or save important observations from scientific field work on mating bonobos in capital-cased files for females and lower-cased files for males.

New Technology File System (NTFS) and Apple's Hierarchical File System (HFS) Plus, on the other hand, usually preserve case when storing files, *but are case insensitive when retrieving them*.
A file saved as ``Example.txt`` will be retrieved by that name but will also be  retrieved as ``EXAMPLE.TXT``, ``example.txt``, etc.
If you are on a Mac, chances are high that you can fascinate your friends [#f1]_ with these simple magic tricks:

.. code-block:: bash

	me@mymac ~ % touch a A
	me@mymac ~ % ls -l a A
	-rw-r--r--  1 me  staff  0 Aug 31 13:06 A
	-rw-r--r--  1 me  staff  0 Aug 31 13:06 a
	me@mymac ~ % rm a
	me@mymac ~ % ls -l a A
	ls: A: No such file or directory
	ls: a: No such file or directory
	*flying doves*

	me@mymac ~ % touch a A
	me@mymac ~ % ls -l a A
	-rw-r--r--  1 me  staff  0 Aug 31 13:06 A
	-rw-r--r--  1 me  staff  0 Aug 31 13:06 a
	me@mymac ~ % echo 123 > a
	me@mymac ~ % ls -l a A   
	-rw-r--r--  1 me  staff  4 Aug 31 13:06 A
	-rw-r--r--  1 me  staff  4 Aug 31 13:06 a
	me@mymac ~ % cat A
	123
	*rabbit emerges from hat*

If you can, try to avoid trouble with unicode
=============================================

Lucky are the people with boring names without accents and special characters.
The others may have an extra bit of fun in their lives when software can not handle their names.

Even though certain names look identical across file system or operating systems, their underlying unicode character sequences can differ.
For example, the character "é" can be represented as the single Unicode character u+00E9 (latin small letter e with acute), or as the two Unicode characters u+0065 and u+0301 (the letter "e" plus a combining acute symbol).
This is called `canonical equivalence <https://en.wikipedia.org/wiki/Unicode_equivalence>`_ and can be  confusing: While file names are visually indistinguishable, certain tools, operating systems, or file systems can normalize their underlying unicode differently and cause errors in the process.
It becomes a problem, potentially even leading to permanent data loss, when `one tool or filesystem won't recognize a file anymore that has been normalized by a different tool or filesystem <https://web.archive.org/web/20100109162824/http://forums.macosxhints.com/archive/index.php/t-99344.html>`_.

Apple's HFS Plus filesystem always normalizes file names to a `fully decomposed form <https://developer.apple.com/library/archive/technotes/tn/tn1150.html#UnicodeSubtleties>`_.
"é" would be represented as two Unicode characters u+0065 and u+0301, in that order.
Windows treats filenames as opaque character sequences and will store and return the encoded bytes exactly as provided.
Linux and other common Unix systems are generally similar to Windows in storing and returning opaque byte streams, but this behavior is technically dependent on the filesystem.
And utilities used for file management, transfer, and archiving may ignore this issue, apply an arbitrary normalization form, or allow the user to control how normalization is applied.
Having special characters in your file names thus is a bit like a data management version of russian roulette.
Most things will likely be fine, but at some point, with some tool, sharing to some system, things could just blow up.

Illegal in certain systems
^^^^^^^^^^^^^^^^^^^^^^^^^^

While normalization differences between systems may make it impossible to disambiguate different files or cause different representations of identical files, there are also file names that aren't allowed.
And places that ban certain file names will not be able to create, receive, or use such such files.

Avoid illegal characters
========================

Different operating system disallow certain characters in file names, and things will be messy if you were to share a file with a character that works on your machine with a machine that regards it as illegal.
Let's start easy and with characters that you can actually find on your keyboard:

On Unix systems, the forward slash ``/`` can not be used in file names.
This is because this character is used to denote directory boundaries.
On Windows systems, on the other hand, there is quite a long list of characters:

.. code-block::

    < (less than)
    > (greater than)
    : (colon)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)

And in addition, its also not possible to end a file name with a period (``.``) or a space on Windows.

Especially Unix users can thus inadvertently create files that a Windows system couldn't handle.
But in the case of files with illegal names being committed into Git repositories, the consequences are actually more sever than just a single file that can't be used or copied.
A dataset with a file with invalid characters likely fails to be cloned, because a checkout of that file will fail.
If a file with an invalid character exists on the non-default :term:`branch`, then that branch likely can't be checked out.
So while having invalid characters in your files is 1) a considerably convoluted way of keeping a Git repository private from that one co-worker who uses Windows, it is mostly 2) a `major interoperability hassle <https://dwheeler.com/essays/fixing-unix-linux-filenames.html>`_, even more so in the context of version control.


.. find-out-more:: What about file names with "invisible" characters?

	There are also illegal characters that you can't find on your keyboard: Control characters.
	Those are characters that do not represent written symbols, but cause particular actions on a system.
	The ASCII code `7 (bell) <https://en.wikipedia.org/wiki/Bell_character>`_, for example, can cause the device to emit a warning.
	On Unix systems, its illegal to use the `0 (NUL) <https://en.wikipedia.org/wiki/Null_character>`_ control character in a file name.
	On Windows systems, its also illegal to use any control character between ``0-31``.
	Relevant in the case that, you know, you wanted to have a file with non-printable characters.
	Why not, right?

Avoid illegal file names
========================

Windows has the fun concept of `reserved file names <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN#win32-file-namespaces>`_, which are names that referred to system actions or devices in OS versions predating current versions of Windows.
These names are

.. code-block::

	CON (used to access the computer console)
	PRN (used to print)
	AUX (used to access auxiliary devices)
	NUL (a special file that discards data written to it, often used to hide output)
	COM1-COM9 (serial communication ports)
	LPT1-LPT9 (parallel ports)

Just like with illegal characters, any file with those names, or any repository that includes a file with those names, will be an interoperability issue for Windows users, and Linux users should thus be mindful not to use those file names [#f2]_.


Impossibilities and inconveniences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You already know that you *could* create a file name with only control characters on Linux systems, but shouldn't do so to ensure interoperability.
Here are more examples on how to be nice to the system that receives your files:

Keep file names below 260 characters
====================================

If you want to annoy a foe with a Windows-based machine, or convince a Windows-friend to switch to Unix, send them files that exceed Window's (default) maximum path length limitation of 260 characters, or make them copy files with acceptable length into a too long, nested directory hierarchy [#f3]_.
This limit exists for all machines running Windows before Windows 10 version 1607, and for all later versions of Windows if the maximum path limit has not been manually removed in the settings.
For more gotchas that Windows users may run into, take a look at the section :ref:`ohnowindows`.

Prevent paths to be interpreted as command line arguments
=========================================================

While its not "illegal" to start a directory of file name with a hyphen (``-``) its a bad idea and disallowed by certain tools due to security risks.
In theory, a file name with a hyphen can clash with a command line argument, and a tool called to operate on that file may then misinterpret it as an argument.
If you were to create a file called ``-n`` on a Unix system, an ``ls`` or ``cat`` on this file (unless you would add a ``./`` prefix to indicate a file in the current directory) would behave different than expected, parametrizing the command line tool instead of displaying any file information.
Because this can be a security hazard, for example leading to remote code execution, `Git will refuse to operate on submodules that start with a hyphen (CVE-2018-17456) <https://www.exploit-db.com/exploits/45631>`_.

Other hassles
=============

While it is technically not illegal, try to keep the ``%`` symbol out of file names.
Tools that try to handle a name with it may mistake it as an escape urlencoded sequence and behave unpredictably.

Resources
^^^^^^^^^


Much information and some general structure of this page is taken from `RFC 8493 <https://datatracker.ietf.org/doc/html/rfc8493#section-6.1>`_.
The links used throughout this overview provide details and further information for particular issues.
A good general overview on how to name files can be found at `psychoinformatics-de.github.io/rdm-course/02-structuring-data/index.html <https://psychoinformatics-de.github.io/rdm-course/02-structuring-data/index.html>`_.

Do you know more? `We're eager to include your advice <github.com/datalad-handbook/book/issues/new/>`_!

.. rubric:: Footnotes

.. [#f1] or bore them to death -- depends on your friends

.. [#f2] If you are on Windows, you can try and go out of your way to create a file with that name. Windows does everything in its power to prevent you from doing it, but you can succeed. But be mindful - should you succeed, you won't get rid of this file, nor of any folder hierarchy it may be contained in.

.. [#f3] Copying vacation snapshots into ``C:\Users\"Bob McBobface"\Desktop\Pictures\"Vacation Pictures"\2020\Saint-Remy-en-Bouzemont-Saint-Genest-et-Isson\"From Alice and Sasha"\Camera\`` is as doomed to fail. Sorry. Better just dump those straight onto your Desktop or somthing...