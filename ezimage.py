#!/usr/bin/env python3

"""Experiments with tkinter in Python3
The Application class inherits from tk.Frame since we will be putting all of the
widgets in a frame.

Initial setup for the application occurs in Main(), which then launches the app.
"""

import os
import configparser
from functools import partial

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
        self.style = ttk.Style()
        self.selected_style = tk.IntVar()
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

        # Style selection
        stylemenu = tk.Menu(optmenu, tearoff=0)
        themes = self.style.theme_names()
        val = 0
        for theme in themes:
            # ttk default may not be the app default
            if theme == 'default':
                theme_name = 'ttk default'
            else:
                theme_name = theme
            stylemenu.add_radiobutton(label=theme_name, value=val,
                                      variable=self.selected_style,
                                      command=partial(self.set_theme, theme))
            if self.style.theme_use() == theme:
                # Set current style as selected_style
                self.selected_style.set(val)
            val += 1
        optmenu.add_cascade(label="Style Selection", menu=stylemenu)

        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help...")
        helpmenu.add_command(label="About...", command=about_dialog)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.master.config(menu=menubar)

    def gui_options(self):  # pylint: disable=no-self-use
        """This is a dummy placeholder"""
        print("GUI Options")

    def set_theme(self, theme_name):
        """Set selected theme"""
        print("Loading '%s' theme" % theme_name)
        write_config('GUI', 'Theme', theme_name)
        self.style.theme_use(theme_name)

    def select_file(self):
        """File selector dialog/"""
        self.filename = fd.askopenfilename(initialdir="~/",
                                           title="Select file",
                                           filetypes=(("PNG files", "*.png"),
                                                      ("JPEG files", "*.jpg"),
                                                      ("GIF files", "*.gif"),
                                                      ("All files", "*.*")))
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


def read_config(section, key):
    """Return value saved in config object"""
    config = configparser.ConfigParser()
    config.read(config_file())
    value = None
    if section in config:
        try:
            value = (config[section][key])
        except KeyError:
            print("'%s' not found. Using default." % key)
        except configparser.Error:
            print("Config parser error. Using defaults")
        except Exception as exc:
            raise RuntimeError("Unknown error") from exc
    else:
        print("Using default %s settings." % section)
    return value

def write_config(section, key, value):
    """Write a value to the application config file"""
    config = configparser.ConfigParser()
    # Get existing data
    config.read(config_file())
    if section in config:
        settings = config[section]
        settings[key] = value
    else:
        config[section] = {}
        config[section][key] = value
    try:
        with open(config_file(), 'w') as configfile:
            config.write(configfile)
    except IOError:
        print("Unable to write configuration file")

def config_file():
    """Return fully qualified config file name"""
    home = os.path.expanduser("~")
    return os.path.join(home, ".config/AudioNyq/EZImage.conf")


def main():
    """Initiate app and run it"""
    root = tk.Tk()          # Create the root window
    # Application icon
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='icon.gif'))  # pylint: disable=protected-access

    root.resizable(0, 0)    #Disable resizing with mouse
    root.minsize("500", 0)

    # Scale widgets. Tkinter seems to assume a screen height of about 600 px
    screen_height = root.winfo_screenheight()
    root.tk.call('tk', 'scaling', screen_height / 600)

    # Default fonts are tiny on high dpi displays
    set_fonts()

    # Set style
    style = ttk.Style()
    theme = read_config('GUI', 'Theme')
    if theme is not None:
        style.theme_use(theme)
    elif 'clam' in style.theme_names():
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
