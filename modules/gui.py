import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename

from ttkbootstrap import Style

class GUI(tk.Tk):
    def __init__(self, app) -> None:
        super().__init__("Antimonium")
        self.app = app

        style = Style("darkly")

        self.title("Antimonium")
        self.resizable(False, False)

        self.menu = tk.Menu(self)
        self.list_menu = tk.Menu(self.menu, tearoff=0)
        self.list_menu.add_command(label="Import list...",underline=0)
        self.list_menu.add_command(label="Export list...",underline=0)
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About",command=self.about,underline=0)
        self.help_menu.add_command(label="License",command=self.license,underline=0)
        self.menu.add_cascade(label="List", menu=self.list_menu, underline=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu, underline=0)
        self.config(menu=self.menu)

        self.bind("<Button-1>", self.unfocus)

        self.left_frame = LeftFrame(self)
        self.frame_separator = Separator(self, orient="vertical")
        self.right_frame = RightFrame(self)
        
        self.left_frame.grid(row=0, column=0, padx=3, pady=3, sticky="ns")
        self.frame_separator.grid(row=0, column=1, padx=3, pady=3, sticky="ns")
        self.right_frame.grid(row=0, column=2, padx=3, pady=3, sticky="ns")

    def unfocus(self, event=None):
        self.focus()
    
    def about(*args):
        messagebox.showinfo(title="About",message="about...")

    def license(*args):
        messagebox.showinfo(title="License",message="license goes here...")

class LeftFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.font1 = font.Font(self, size=18)
        
        self.sort_btn = Button(self, text="Sort A-Z")
        self.app_list = tk.Listbox(self, width=18, height=15, font=self.font1)
        self.app_scroll = Scrollbar(self, 
            orient="vertical", 
            command=self.app_list.yview
        )

        self.sort_btn.grid(row=0, column=0, pady=(1,2))
        self.app_list.grid(row=1, column=0)
        self.app_scroll.grid(row=1, column=1, sticky="ns")

        self.app_list.config(yscrollcommand=self.app_scroll.set)
        self.app_list.bind("<<ListboxSelect>>", self.onSelect)

    def updateList(self, items):
        self.app_list.delete(0, "end")
        self.app_list.insert("end", *items)

    def getSelectedLabelname(self):
        try:
            return self.app_list.get(self.app_list.curselection())
        except: return

    def onSelect(self, event=None):
        labelname = self.getSelectedLabelname()
        self.parent.app.gui_updateInfo(labelname)

class RightFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.options_frame = OptionsFrame(self)
        self.info_frame = InfoFrame(self)
        self.start_frame = StartFrame(self)

        self.options_frame.pack()
        self.info_frame.pack(fill="x", pady=(10,0))
        self.start_frame.pack(side="bottom", fill="x")

class OptionsFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.grid_rowconfigure(0, minsize=31)

        self.add_btn = Button(self, text="Add a program", width=25, command=self.openFile)
        self.rename_btn = Button(self, text="Rename selected")
        self.remove_btn = Button(self, text="Remove selected", command=self.removeItem)

        self.add_btn.grid(row=1, column=0, sticky="ew", pady=1)
        self.rename_btn.grid(row=2, column=0, sticky="ew", pady=1)
        self.remove_btn.grid(row=3, column=0, sticky="ew", pady=1)

    def openFile(self):
        filepath = askopenfilename(filetypes=(("Executables", "*.exe"),))
        if filepath:
            self.parent.parent.app.gui_addProgram(filepath)

    def removeItem(self):
        if (labelname := self.parent.parent.left_frame.getSelectedLabelname()):
            self.parent.parent.app.gui_removeProgram(labelname)

class InfoFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        LabelFrame.__init__(self, parent, text="App Info", *args, **kwargs)

        self.info1_label = Label(self, text="Path: File not selected.")
        self.info2_label = Label(self, text="Date created: File not selected.")
        self.info3_label = Label(self, text="Size: File not selected.")

        self.info1_label.grid(row=0, column=0, sticky="w")
        self.info2_label.grid(row=1, column=0, sticky="w")
        self.info3_label.grid(row=2, column=0, sticky="w")

    def setInfo(self, filepath, size, creation):
        if len(filepath) > 35:
            filepath = filepath[:33] + "..."
        self.info1_label["text"] = f"Path: {filepath}"
        self.info2_label["text"] = f"Date created: {creation}"
        self.info3_label["text"] = f"Size: {size}"

class StartFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.close_check = Checkbutton(self, text="Close antimonium")
        self.start_btn = Button(self, text="START", width=35, command=self.runItem)

        self.close_check.grid(row=0, column=0, sticky="w", pady=5)
        self.start_btn.grid(row=1, column=0, sticky="ew", ipady=5)

    def runItem(self):
        if (labelname := self.parent.parent.left_frame.getSelectedLabelname()):
            self.parent.parent.app.gui_runProgram(labelname)