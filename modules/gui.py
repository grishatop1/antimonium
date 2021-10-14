import tkinter as tk
from tkinter.ttk import *

from ttkbootstrap import Style

class GUI(tk.Tk):
    def __init__(self, app) -> None:
        super().__init__("Antimonium")
        self.app = app

        style = Style("darkly")

        self.title("Antimonium")
        self.resizable(False, False)

        self.left_frame = LeftFrame(self)
        self.frame_separator = Separator(self, orient="vertical")
        self.right_frame = RightFrame(self)
        
        self.left_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ns")
        self.frame_separator.grid(row=0, column=1, padx=3, pady=3, sticky="ns")
        self.right_frame.grid(row=0, column=2, padx=3, pady=3, sticky="ns")

class LeftFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.sort_btn = Button(self, text="Sort A-Z")
        self.app_list = tk.Listbox(self, width=35, height=25)

        self.sort_btn.grid(row=0, column=0, pady=(1,2))
        self.app_list.grid(row=1, column=0)

class RightFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.options_frame = OptionsFrame(self)
        self.info_frame = InfoFrame(self)
        self.start_frame = StartFrame(self)

        self.options_frame.pack()
        self.info_frame.pack(fill="x", pady=(10,0))
        self.start_frame.pack(side="bottom", fill="x")

class OptionsFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.grid_rowconfigure(0, minsize=31)

        self.add_btn = Button(self, text="Add a program", width=25)
        self.rename_btn = Button(self, text="Rename")
        self.remove_btn = Button(self, text="Remove")

        self.add_btn.grid(row=1, column=0, sticky="ew", pady=1)
        self.rename_btn.grid(row=2, column=0, sticky="ew", pady=1)
        self.remove_btn.grid(row=3, column=0, sticky="ew", pady=1)

class InfoFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        LabelFrame.__init__(self, parent, text="App Info", *args, **kwargs)

        self.info1_label = Label(self, text="info1 - label")
        self.info2_label = Label(self, text="info2 - label")
        self.info3_label = Label(self, text="info3 - label")
        self.info4_label = Label(self, text="info4 - label")

        self.info1_label.grid(row=0, column=0)
        self.info2_label.grid(row=1, column=0)
        self.info3_label.grid(row=2, column=0)
        self.info4_label.grid(row=3, column=0)

class StartFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.close_check = Checkbutton(self, text="Close antimonium")
        self.start_btn = Button(self, text="START", width=30)

        self.close_check.grid(row=0, column=0, sticky="w", pady=5)
        self.start_btn.grid(row=1, column=0, sticky="ew", ipady=5)