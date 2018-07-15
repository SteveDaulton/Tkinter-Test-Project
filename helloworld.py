#!/usr/bin/env python3

"""Experiments with tkinter in Python3"""

from tkinter import Tk, Frame, font, Button, Menu, TclError
from tkinter import filedialog as fd


class Application(Frame):    # pylint: disable=too-many-ancestors
    """Main application."""
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand=False)
        self.create_menu()
        self.create_widgets()
        self.filename = ""

    def create_menu(self):
        """Create menu"""
        # create a toplevel menu
        menubar = Menu(self)
        menubar.add_command(label="Hello!", command=print('hello'))
        menubar.add_command(label="Quit!", command=root.quit)
        # display the menu
        root.config(menu=menubar)

    def create_widgets(self):
        """Create widgets"""
        self.select_file = Button(self)
        self.select_file["text"] = "Select file"
        self.select_file["command"] = self.get_file
        self.select_file.pack(side="top")

        self.quit = Button(self, text="Quit", fg="red",
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


root = Tk()

# Hack to enable "show hidden files" button.
try:
    # call a dummy dialog with an impossible option to initialize the file
    # dialog without really getting a dialog window; this will throw a
    # TclError, so we need a try...except :
    try:
        root.tk.call('tk_getOpenFile', '-invalid')
    except TclError:
        pass
    # now set the magic variables accordingly
    root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
#The above calls are undocumented. They work on Linux now, but ...
except TclError as tke:
    print(tke)
    raise

# Set standard font sizes
font.nametofont("TkDefaultFont").configure(family='sans', size=10)
font.nametofont("TkTextFont").configure(family='sans', size=10)
font.nametofont("TkFixedFont").configure(family='monospace', size=10)
font.nametofont("TkMenuFont").configure(family='sans', size=10)
font.nametofont("TkHeadingFont").configure(family='sans', size=10)
font.nametofont("TkCaptionFont").configure(family='sans', size=10)
font.nametofont("TkSmallCaptionFont").configure(family='sans', size=8)
font.nametofont("TkTooltipFont").configure(family='sans', size=9)
font.nametofont("TkIconFont").configure(family='sans', size=10)

#Scaling the widgets does not appear to be necessary, so long as we set the default
#font size in points.
#Scale widgets. Tkinter seems to assume a screen height of about 600 px
#screen_height = root.winfo_screenheight()
#root.tkinter.call('tk', 'scaling', screen_height / 600)

app = Application(master=root)
app.mainloop()
