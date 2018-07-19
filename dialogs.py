"""Dialog windows for EZ-Image application"""

from functools import partial

import tkinter as tk
from tkinter import font
import webbrowser


LINK_KWARGS = {'color': "red2", 'weight':"bold", 'underscore': False}
HOVER_KWARGS = {'color': "blue", 'weight':"normal", 'underscore': True}

class About(tk.Toplevel):
    """About... window"""
    URL = r"https://github.com/SteveDaulton/Tkinter-Test-Project"
    def __init__(self, version=None):
        tk.Toplevel.__init__(self)
        self.title("About EZ-Image")
        if version is None:
            self.version = "n/a"
        else:
            self.version = version
        self.display = tk.Label(self, text=self.message())
        self.display.pack(fill="both", expand=True, padx=10, pady=10)

        link = tk.Label(self, text="Home page", fg="blue", cursor="hand2")
        fnt = font.Font(link, link.cget("font"))
        fnt.configure(underline=True)
        link.configure(font=fnt)
        link.pack(pady=10)
        self.close = tk.Button(self, text="Close", command=self.destroy)
        self.close.pack(side="bottom")

        link.bind("<Button-1>",
                  lambda evt, url=self.URL: open_url(url, evt))

        link.bind("<Enter>", partial(self.mouseover, link,
                                     **LINK_KWARGS))
        link.bind("<Leave>", partial(self.mouseover, link,
                                     **HOVER_KWARGS))

    def message(self):
        """Message to display"""
        message = ("EZ-Image by Steve Daulton.\n"
                   "Version: %s") % self.version
        return message

    @staticmethod
    def mouseover(widget, event, **kwargs):  # pylint: disable=unused-argument
        """Modify the widget font on mouseover"""
        fnt = font.Font(widget, widget.cget("font"))
        fnt.configure(underline=kwargs['underscore'], weight=kwargs['weight'])
        widget.configure(fg=kwargs['color'], font=fnt)



def open_url(url, event):  # pylint: disable=unused-argument
    """Open web page
    The event object is not used, but required for
    binding the function to an event.
    """
    webbrowser.open_new(url)
