#!/usr/bin/env python3

"""Experiments with tkinter in Python3
The Application class inherits from tk.Frame since we will be putting all of the
widgets in a frame.

Initial setup for the application occurs in Main(), which then launches the app.
"""

import tkinter as tk
import tkinter.font             # pylint: disable=unused-import
from tkinter import ttk
from tkinter import filedialog as fd

import dialogs


VERSION = "0.0.1"

class Application(tk.Frame):    # pylint: disable=too-many-ancestors
    """Main application."""
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()
        self.pack()
        self.filename = ""

    def configure_gui(self):
        """Configuration options"""
        self.master.title("Hello World Example")

    def create_widgets(self):
        """Create widgets"""
        self.create_menu()

        self.label = tk.Label(self.master, text="A very simple GUI!")
        self.label.pack()

        # Buttons
        self.quit = ttk.Button(self, text="Quit", command=self.master.quit)
        self.quit.pack(side="left")

    def create_menu(self):
        """Create menu"""
        # Toplevel menu
        menubar = tk.Menu(self)

        # File menu pulldown
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Select image file...", command=self.select_file)
        filemenu.add_command(label="Save", command=None)
        filemenu.add_command(label="Save As...", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Options menu
        optmenu = tk.Menu(menubar, tearoff=0)
        optmenu.add_command(label="Interface...", command=self.gui_options)
        menubar.add_cascade(label="Options", menu=optmenu)

        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help...")
        helpmenu.add_command(label="About...", command=about_dialog)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.master.config(menu=menubar)

    def gui_options(self):
        print("GUI Options")

    def select_file(self):
        """File selector dialog/"""
        self.filename = fd.askopenfilename(initialdir="~/",
                                           title="Select file",
                                           filetypes=(("jpeg files", "*.jpg"),
                                                      ("gif files", "*.gif"),
                                                      ("all files", "*.*")))
        print(self.filename)


def about_dialog():
    """Call 'About' dialog"""
    dialogs.About(VERSION)

def set_fonts(base_size=None):
    """Configure Tkinter's standard fonts"""
    if base_size is None:
        base_size = 10
    elif base_size < 6:
        base_size = 6
    tk.font.nametofont("TkDefaultFont").configure(family='sans', size=base_size)
    tk.font.nametofont("TkTextFont").configure(family='sans', size=base_size)
    tk.font.nametofont("TkFixedFont").configure(family='monospace', size=base_size)
    tk.font.nametofont("TkMenuFont").configure(family='sans', size=base_size)
    tk.font.nametofont("TkHeadingFont").configure(family='sans', size=base_size)
    tk.font.nametofont("TkCaptionFont").configure(family='sans', size=base_size)
    tk.font.nametofont("TkSmallCaptionFont").configure(family='sans', size=(base_size - 2))
    tk.font.nametofont("TkTooltipFont").configure(family='sans', size=(base_size - 1))
    tk.font.nametofont("TkIconFont").configure(family='sans', size=base_size)


def main():
    """Initiate app and run it"""
    root = tk.Tk()          # Create the root window
    root.resizable(0, 0)    #Disable resizing with mouse
    root.minsize("500", 0)

    # Scale widgets. Tkinter seems to assume a screen height of about 600 px
    screen_height = root.winfo_screenheight()
    root.tk.call('tk', 'scaling', screen_height / 600)

    # Default fonts are tiny on high dpi displays
    set_fonts()

    # Set style
    #TODO: This is not portable
    style = ttk.Style()
    style.theme_use('clam')
    

    # Hack to enable "show hidden files" button.  This is an undocumented
    # 'feature' so wrap it all in try...except in case it throws in the future.
    try:
        # Call a dummy dialog with an impossible option to initialize the file
        # dialog without really getting a dialog window; this will throw a
        # TclError, so we need a try...except :
        try:
            root.tk.call('tk_getOpenFile', '*invalid*')
        except tk.TclError:
            pass
        # Now set the magic variables.
        root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
        root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    except tk.TclError as tke:
        print(tke)
        raise

    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
