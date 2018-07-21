"""Dialog windows for EZ-Image application"""

from functools import partial

import tkinter as tk
from tkinter import font
from tkinter import ttk
import webbrowser


LINK_KWARGS = {'color': "red2", 'weight':"bold", 'underscore': False}
HOVER_KWARGS = {'color': "blue", 'weight':"normal", 'underscore': True}


class About(tk.Toplevel):
    """Toplevel window for the 'About...' dialog

    Args:
        version (str): Application version string

    Attributes:
        URL (str): The project home page URL

    """
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
        self.close = ttk.Button(self, text="Close", command=self.destroy)
        self.close.pack(side="bottom")

        # Bind web link label
        link.bind("<Button-1>", lambda event: webbrowser.open_new(self.URL))
        link.bind("<Enter>", partial(self.mouseover, link, **LINK_KWARGS))
        link.bind("<Leave>", partial(self.mouseover, link, **HOVER_KWARGS))

    def message(self):
        """Body text of 'About' dialog

        Returns:
            Body text for 'About' dialog

        """
        message = ("EZ-Image version: %s\n"
                   "by Steve Daulton.\n\n"
                   "Released under the terms of GPL v3.") % self.version
        return message

    @staticmethod
    def mouseover(widget, event, color="blue", weight="normal", underscore=True):  # pylint: disable=unused-argument
        """Modify the widget font on mouseover

        Args:
            widget (widget): The widget to be modified.
            event (event): Unused - required to bind to event.
            color (str): Font color.
            weight (str): Font weight.
            underscore (bool): Underscore.

        """
        fnt = font.Font(widget, widget.cget("font"))
        fnt.configure(underline=underscore, weight=weight)
        widget.configure(fg=color, font=fnt)
