import os
import shutil
import vpk
import json
from tkinter import filedialog, messagebox

import av_main
import av_dbm
import av_ward

# load the languages
def load_language_file(lang):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "lang", f"strings_{lang}.json"), "r") as f:
        return json.load(f)
eng = load_language_file("en") # eng["key"]

this_dir = av_main.determine_dir()
output_dir = os.path.join(this_dir, "patched")
output_vpk_dir = os.path.join(output_dir, "pak01_dir")

folder_input = av_dbm.dbread("pakfolder_path")
if folder_input == None:
    folder_input = output_vpk_dir
    if not os.path.exists(folder_input):
        os.makedirs(folder_input)

def browsefldr():
    global folder_input
    firsttime = True
    while True:
        # detects wether is pak01_dir folder is exists
        if folder_input == None or not os.path.exists(folder_input):
            if firsttime == True:
                message = "The pak01_dir folder is not detected. \nPlease locate the folder."
                result = messagebox.showinfo(eng["namefldr"], message)
                firsttime = False
            folder_input = filedialog.askdirectory(title="Select pak01_dir folder", initialdir=output_dir)
            # selected file is invalid
            if not os.path.exists(folder_input):
                message = "Invalid folder is selected. Please try again."
                result = messagebox.askretrycancel(eng["namefldr"], message)
                if result:
                    continue # select the file again
                else:
                    return # quit
            # selected file is valid
            elif "pak" in folder_input or "_dir" in folder_input:
                continue # continue loop and go to else
            # detects wether any file is selected
            else:
                message = "No folder is selected. Please try again."
                result = messagebox.askretrycancel(eng["namefldr"], message)
                if result:
                    continue # select the file again
                else:
                    return # quit
        else: # goes here if the file is valid
            firsttime = False
            folder_name = os.path.basename(folder_input)
            confirm = "Please confirm that the folder is correct."
            message = f"Folder Name: {folder_name}\n\nFolder Directory: {folder_input} \n\n{confirm}"
            result = messagebox.askyesno(eng["namefldr"], message)
            if result:
                av_dbm.dbwrite("pakfolder_path", folder_input)
                break # stop the loop then continue the process
            else:
                folder_input = None
                continue # select the file again
    if os.path.exists(folder_input):
        result = buildfolder()
        if result:
            return result
        else:
            return result
def buildfolder():
    global folder_input
    folder_name = os.path.basename(folder_input)
    newpak = vpk.new(folder_input)
    newpak.save(os.path.join(output_dir, f"{folder_name}.vpk"))
    message = f"Patcher report:\nVPK Name: {folder_name}.vpk\nVPK Output: {output_dir}\n\nThe build operation was successful."
    messagebox.showinfo(eng["namefldr"], message)
    while True:
        input_vpk_path = av_dbm.dbread("pak01dir_path")
        if input_vpk_path != None:
            message = f"Would you like to replace the input pak01_dir.vpk file with the newly built one?"
            result = messagebox.askyesno(eng["namefldr"], message)
            if result:
                try:
                    shutil.copy2(os.path.join(output_dir, f"{folder_name}.vpk"), input_vpk_path)
                    # status = os.path.exists(input_vpk_path)
                    # if status:
                    message = "Copied! operation was successful."
                    messagebox.showinfo(eng["namefldr"], message)
                except Exception as e:
                    message = "Oops, unable to copy the file!"
                    messagebox.showerror(eng["namefldr"], message)
            break
        else:
            result = av_ward.browsevpk(eng["namefldr"])
            if result:
                continue
            else:
                break
    return True