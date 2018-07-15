#!/usr/bin/env python3

"""Experiments with tkinter in Python3"""

import tkinter as tk
import tkinter.font as fnt
from tkinter import filedialog as fd


class Application(tk.Frame):    # pylint: disable=too-many-ancestors
    """Main application."""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.filename = ""

    def create_widgets(self):
        """Create widgets"""
        self.select_file = tk.Button(self)
        self.select_file["text"] = "Select file"
        self.select_file["command"] = self.get_file
        self.select_file.pack(side="top")

        self.quit = tk.Button(self, text="Quit", fg="red",
                              overrelief="groove",
                              command=root.destroy)
        self.quit["activebackground"] = "red"
        self.quit["activeforeground"] = "#fff"
        self.quit.pack(side="bottom")

    def get_file(self):
        """File selector dialog/"""
        self.filename = fd.askopenfilename(initialdir="~/",
                                           title="Select file",
                                           filetypes=(("jpeg files", "*.jpg"),
                                                      ("all files", "*.*")))
        print(self.filename)


root = tk.Tk()

# Hack to enable "show hidden files" button.
try:
    # call a dummy dialog with an impossible option to initialize the file
    # dialog without really getting a dialog window; this will throw a
    # TclError, so we need a try...except :
    try:
        root.tk.call('tk_getOpenFile', '-invalid')
    except tk.TclError:
        pass
    # now set the magic variables accordingly
    root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
#The above calls are undocumented. They work on Linux now, but ...
except tk.TclError as tke:
    print(tke)
    raise

# Set standard font sizes
fnt.nametofont("TkDefaultFont").configure(family='sans', size=10)
fnt.nametofont("TkTextFont").configure(family='sans', size=10)
fnt.nametofont("TkFixedFont").configure(family='monospace', size=10)
fnt.nametofont("TkMenuFont").configure(family='sans', size=10)
fnt.nametofont("TkHeadingFont").configure(family='sans', size=10)
fnt.nametofont("TkCaptionFont").configure(family='sans', size=10)
fnt.nametofont("TkSmallCaptionFont").configure(family='sans', size=8)
fnt.nametofont("TkTooltipFont").configure(family='sans', size=9)
fnt.nametofont("TkIconFont").configure(family='sans', size=10)

#Scaling the widgets does not appear to be necessary, so long as we set the default
#font size in points.
#Scale widgets. Tkinter seems to assume a screen height of about 600 px
#screen_height = root.winfo_screenheight()
#root.tkinter.call('tk', 'scaling', screen_height / 600)

app = Application(master=root)
app.mainloop()
