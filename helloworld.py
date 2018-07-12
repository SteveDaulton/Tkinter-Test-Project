#!/usr/bin/env python3

import tkinter as tk
import tkinter.font

class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)
      self.pack()
      self.create_widgets()

   def create_widgets(self):
      self.hi_there = tk.Button(self)
      self.hi_there["text"] = "Hello World\n(click me)"
      self.hi_there["command"] = self.say_hi
      self.hi_there.pack(side="top")

      self.quit = tk.Button(self, text="QUIT", fg="red",
                           command=root.destroy)
      self.quit.pack(side="bottom")

   def say_hi(self):
      print("hi there, everyone!")

root = tk.Tk()
# Increase default font size to 10px
default_font = tk.font.nametofont("TkDefaultFont")
default_font.configure(family='sans-serif', size=10)
#Scale widgets to 144 dpi (default scaling of x1 = 72 dpi)
root.tk.call('tk', 'scaling', 2.0)
app = Application(master=root)
app.mainloop()