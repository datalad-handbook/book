By default, Windows does not show common file extensions when you view directory contents with a file explorer.
Instead, it only displays the base of the file name and indicates the file type with the display icon.
You can see if this is the case for you, too, by opening the ``books\`` directory in a file explorer, and checking if the file extension (``.pdf``) is a part of the file name displayed underneath its PDF icon.

Hidden file extensions can be a confusing source of errors, because some Windows editors (for example, Notepad) automatically add a ``.txt`` extension to your files -- when you save the script above under the name ``list_titles.sh``, your editor may add an extension (``list_titles.sh.txt``), and the file explorer displays your file as ``list_titles.sh`` (hiding the ``.txt`` extension).

To prevent confusion, configure the file explorer to always show you the file extension.
For this, open the Explorer, click on the "View" tab, and tick the box "File name extensions".

Beyond this, double check the correct naming of your file, ideally in the terminal.
