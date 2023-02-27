from json import load as jsload
from webbrowser import open_new_tab
from time import sleep
import customtkinter as ctk
import tkinter as tk
import sys
import os

# avoid circular import, detects if this launches as main
if __name__ == "__main__":
    import av_dbm
    import av_mid
    import av_ward
    import av_patcher
    import av_build

# load the language
def load_language_file(lang):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "lang", f"strings_{lang}.json"), "r") as f:
        return jsload(f)

# directory determiner
def determine_dir():
    if getattr(sys, 'frozen', False):
        this_dir = os.path.dirname(sys.executable)
    else:
        this_dir = os.path.dirname(os.path.abspath(__file__))
    return this_dir

# default variable
this_dir = determine_dir()
root_dir = os.path.dirname(os.path.abspath(__file__))

# avoid unecessary import, detects if this launches as main
if __name__ == "__main__":
    eng = load_language_file("en")
    w = 500
    h = 345

class App(ctk.CTk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title(eng["title"])
        self.iconbitmap(os.path.join(root_dir, "data", "library", "icon", "av_icon.ico"))
        # self.wm_attributes("-topmost", True)
        self.geometry(f"{w}x{h}")
        self.maxsize(w, h)
        self.minsize(w, h)
        # widgets
        # self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.menu = Menu(self)
        self.credit = Credit(self)
        self.menu.pack(padx=20, pady=(20, 20), fill="both")
        self.credit.pack(padx=30, pady=0, fill="both")

        self.toplevel_window = None

# class InputTextWindow(ctk.CTkToplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.title(eng["namegi"])
#         self.iconbitmap(os.path.join(root_dir, "data", "library", "icon", "av_icon.ico"))
#         self.geometry("400x150")
#         self.maxsize(400, 150)
#         self.minsize(400, 150)
#         # define
#         self.lbl = ctk.CTkLabel(self, text="Edit mod folder name", width=0, height=0)
#         self.etry = ctk.CTkEntry(self, fg_color="transparent")
#         self.btn = ctk.CTkButton(self, text="Confirm", command=self.savemodfolder)
#         # props
#         self.etry.insert("0", av_dbm.dbread("folder_name"))
#         self.etry.focus()
#         # place
#         self.lbl.pack(padx=20, pady=20)
#         self.etry.pack(padx=20, fill="both")
#         self.btn.pack(padx=20, pady=20)

#     def savemodfolder(self):
#         av_dbm.dbwrite("folder_name", self.etry.get())
#         self.withdraw()

class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.entry = {}
        self.widgets()
        
    # def editmodfolder(self):
    #     if App().toplevel_window is None or not App().toplevel_window.winfo_exists():
    #         App().toplevel_window = InputTextWindow(App())  # create window if its None or destroyed
    #     else:
    #         App().toplevel_window.focus()  # if window exists focus it
            
        
    def widgets(self):
        # font
        bold = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        # grid
        self.grid_columnconfigure(1, weight=1)
        
        # widget 1
        self.label1 = ctk.CTkLabel(self, text=eng["tool1"], font=bold, anchor="s")
        self.entry1 = ctk.CTkEntry(self, border_color="#ED4337", fg_color="transparent")
        self.button1 = ctk.CTkButton(self, text="Browse", command=self.tool1)
        # place 1
        self.label1.grid(row=0, column=0, columnspan=3, padx=(20, 20), pady=(5, 5), sticky="w")
        self.entry1.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(5, 10), sticky="ew")
        self.button1.grid(row=1, column=2, padx=(20, 20), pady=(5, 10), sticky="ew")
        # properties 1
        self.update_entry(1)
        self.entry1.configure(state="disabled")
        
        # widget 2
        self.label2 = ctk.CTkLabel(self, text=eng["tool2"], font=bold, anchor="s")
        self.entry2 = ctk.CTkEntry(self, border_color="#ED4337", fg_color="transparent")
        self.button2 = ctk.CTkButton(self, text="Browse", command=self.tool2)
        # place 2
        self.label2.grid(row=2, column=0, columnspan=3, padx=(20, 20), pady=(0, 5), sticky="w")
        self.entry2.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=(5, 10), sticky="ew")
        self.button2.grid(row=3, column=2, padx=(20, 20), pady=(5, 10), sticky="ew")
        # properties 2
        self.update_entry(2)
        self.entry2.configure(state="disabled")
        
        # widget 3
        self.label3 = ctk.CTkLabel(self, text=eng["tool3"], font=bold, anchor="s")
        self.entry3 = ctk.CTkEntry(self, border_color="#ED4337", fg_color="transparent")
        self.button3 = ctk.CTkButton(self, text="Browse", command=self.tool3)
        # place 3
        self.label3.grid(row=4, column=0, columnspan=3, padx=(20, 20), pady=(0, 5), sticky="w")
        self.entry3.grid(row=5, column=0, columnspan=2, padx=(20, 0), pady=(5, 20), sticky="ew")
        self.button3.grid(row=5, column=2, padx=(20, 20), pady=(5, 20), sticky="ew")
        # properties 3
        self.update_entry(3)
        self.entry3.configure(state="disabled")
        
    # tool 1
    def tool1(self):
        result = av_ward.warder()
        self.update_entry(1)
        self.update_entry(3)
        if result:
            self.button1.configure(text="Patched!")
        else:
            self.button1.configure(text="Failed!")
    # tool 2
    def tool2(self):
        result = av_patcher.patcher()
        self.update_entry(2)
        if result:
            self.button2.configure(text="Patched!")
        else:
            self.button2.configure(text="Failed!")
    # tool 3
    def tool3(self):
        result = av_build.browsefldr()
        self.update_entry(3)
        if result:
            self.button3.configure(text="Builded!")
        else:
            self.button3.configure(text="Failed!")
    def update_entry(self, integer):
        if integer == 1:
            path = av_dbm.dbread("pak01dir_path")
            if path == None or not os.path.exists(path):
                self.entry1.delete(0, tk.END)
                self.entry1.insert("0", eng["tool1file"])
            else:
                self.entry1.configure(state="normal")
                self.entry1.delete(0, tk.END)
                self.entry1.insert(0, path)
                self.entry1.configure(border_color="#3f8f29")
                self.button1.configure(text="Patch")
            self.entry1.configure(state="disabled")
        elif integer == 2:
            path = av_dbm.dbread("gameinfo_path")
            if path == None or not os.path.exists(path):
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, eng["tool2file"])
            else:
                self.entry2.configure(state="normal")
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, path)
                self.entry2.configure(border_color="#3f8f29")
                self.button2.configure(text="Patch")
            self.entry2.configure(state="disabled")
        else:
            path = av_dbm.dbread("pakfolder_path")
            if path == None or not os.path.exists(path):
                self.entry3.delete(0, tk.END)
                self.entry3.insert(0, eng["tool3file"])
            else:
                self.entry3.configure(state="normal")
                self.entry3.delete(0, tk.END)
                self.entry3.insert(0, path)
                self.entry3.configure(border_color="#3f8f29")
                self.button3.configure(text="Build")
            self.entry3.configure(state="disabled")


class Credit(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.widgets()
    def widgets(self):
        link = ctk.CTkFont(family="Segoe UI", size=12)
        linku = ctk.CTkFont(family="Segoe UI", size=12, underline=True)
        # credit widget
        self.cr_link = ctk.CTkButton(self, text=eng["credit2"],
                                     command=self.openmygithub, font=link,
                                     text_color="#4682B4", corner_radius=0, width=0, height=0, fg_color="transparent", hover=False)
        self.cr_label = ctk.CTkLabel(self, text=eng["credit1"], font=link, width=0, height=0, justify="left")
        # credit placement
        self.cr_link.grid(padx=(0, 0), pady=(0, 0), row=0, column=0, sticky="w")
        self.cr_label.grid(padx=(3, 0), pady=(0, 0), row=1, column=0, sticky="w")
        def on_enter(e):
            self.cr_link.configure(font=linku)
        def on_leave(e):
            self.cr_link.configure(font=link)
        self.cr_link.bind("<Enter>", on_enter)
        self.cr_link.bind("<Leave>", on_leave)
        # play the music!
        self.checkbox = ctk.CTkCheckBox(self, text="Music", command=av_mid.toggle_music, border_width=2, width=0, height=0, checkbox_height=20, checkbox_width=20)
        self.checkbox.grid(padx=(0, 3), pady=(5, 0), row=0, rowspan=2, column=1)
        self.checkbox.select()
    def openmygithub(self):
        open_new_tab(eng["credit2"])


if __name__ == "__main__":
    app = App()
    if Credit(app).checkbox.get() == 1:
        av_mid.play_music()
    app.protocol("WM_DELETE_WINDOW", sys.exit)
    app.mainloop()