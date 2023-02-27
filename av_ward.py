import os
import re
import vpk
import json
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import av_dbm
import av_main

# load the languages
def load_language_file(lang):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "lang", f"strings_{lang}.json"), "r") as f:
        return json.load(f)
eng = load_language_file("en") # eng["key"]

# some necessary default variable
this_dir = av_main.determine_dir()
root_dir = os.path.dirname(os.path.abspath(__file__))
vmdl_path = os.path.join(root_dir, "data", "library", "ward", "default_ward.vmdl_c")
txt_temp = os.path.join(root_dir, "data", "temp", "temp.txt")
vpk_extracted = False
vpk_input = None
if av_dbm.dbread("pak01dir_path") != None:
    vpk_input = os.path.join(av_dbm.dbread("pak01dir_path"))

# regex pattern to search
rx_search = r'"models/items/wards/[^"]*"' #inital search
str_replace = '"models/props_gameplay/default_ward.vmdl"' #replacement string
rx_search_vmdl = r'"models/items/wards/([^/]+)' #file name search

# core functions
def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    file_size_kb = round(os.path.getsize(file_path) / 1024, 3)
    return file_name, file_size_kb, file_dir
def warder():
    browse = browsevpk(eng["namewrd"])
    if browse:
        if os.path.exists(vpk_input):
            patched = patchwards()
            if patched:
                return True
def browsevpk(string):
    global vpk_input
    firsttime = True
    while True:
        # detects wether is pak01_dir.vpk or other .vpk file is exists
        if vpk_input == None or not os.path.exists(vpk_input) or ".vpk" not in os.path.splitext(vpk_input)[1]:
            if firsttime == True:
                message = "The file pak01_dir.vpk is not detected. \nPlease locate the file."
                result = messagebox.showinfo(string, message)
                firsttime = False
            vpk_input = filedialog.askopenfilename(title="Select pak01_dir.vpk", filetypes=(("Valve Pak file", "*.vpk"), ("All files", "*.*")))
            # selected file is invalid
            if os.path.exists(vpk_input) and ".vpk" not in os.path.splitext(vpk_input)[1]:
                message = "Invalid file is selected. Please try again."
                result = messagebox.askretrycancel(string, message)
                if result:
                    continue # select the file again
                else:
                    return False # quit
            # selected file is valid
            elif ("pak" in vpk_input and "_dir" in vpk_input) or ".vpk" not in os.path.splitext(vpk_input)[1]:
                continue # continue loop and go to else
            # detects wether any file is selected
            else:
                message = "No file is selected. Please try again."
                result = messagebox.askretrycancel(string, message)
                if result:
                    continue # select the file again
                else:
                    return False # quit
        else: # goes here if the file is valid
            firsttime = False
            file_name, file_size_kb, file_dir = get_file_info(vpk_input)
            confirm = "Please confirm that the file is correct."
            message = f"File Details:\n- Name: {file_name}\n- Size: {file_size_kb} KB\n\nFile Location:\n- {file_dir} \n\n{confirm}"
            result = messagebox.askyesno(string, message)
            if result:
                av_dbm.dbwrite("pak01dir_path", vpk_input)
                return True # stop the loop then continue the process
            else:
                vpk_input = None
                continue # select the file again
def extractvpk():
    try:
        pak01_dir = vpk.open(av_dbm.dbread("pak01dir_path"))
        file_inside_vpk = pak01_dir.get_file("scripts/items/items_game.txt")
        file_inside_vpk.save(txt_temp)
        # file_inside_vpk.save("./items_game.txt")
        # shutil.move("items_game.txt", txt_temp)
        # ask if user want to extract all of the vpk01_dir content
        vpk_name = os.path.basename(av_dbm.dbread("pak01dir_path"))
        vpk_name_o = os.path.splitext(vpk_name)[0]
        message = f"Do you want to extract all of contents of the {vpk_name} to the patched folder?"
        result = messagebox.askyesno(eng["namewrd"], message)
        if result:
            global vpk_extracted
            this_path = os.path.join(this_dir, "patched", vpk_name_o)
            os.makedirs(this_path, exist_ok=True) if not os.path.exists(this_path) else None
            try:
                for path in pak01_dir:
                    file = pak01_dir.get_file(path)
                    full_path = this_path + "/" + path
                    if not os.path.exists(full_path):
                        dir = path.split("/")[:-1]
                        file_dir = ""
                        for folder in dir:
                            file_dir += folder + "/"
                            if not os.path.exists(f"{this_path}/{file_dir}"):
                                os.makedirs(f"{this_path}/{file_dir}", exist_ok=True) if not os.path.exists(f"{this_path}/{file_dir}") else None
                        # print(f"Extracting: {vpk_name}/{path} to {this_path}/{path}")
                        # status = os.path.exists(this_path+'/'+file_dir)
                        # print(f"Status: {status}", end = "\n\n")
                        file.save(f"{this_path}/{path}")
                    else:
                        # print(f"File: {vpk_name}/{path}")
                        # print(f"Exists: {os.path.exists(full_path)}")
                        # print(f"Path: {full_path}")
                        file.save(f"{this_path}/{path}")
                vpk_extracted = True
            except Exception as e:
                message = f"Error: could not extract {vpk_name}\n\nDetails: {str(e)}"
                messagebox.showerror(eng["namewrd"], message)
        return True
    except Exception as e:
        message = f"Error: could not extract items_game.txt\n\nDetails: {str(e)}"
        messagebox.showerror(eng["namewrd"], message)
        return False
def patchwards():
    result = extractvpk()
    if result:
        # read string from the vpk_temp
        with open(txt_temp, "r", encoding="utf-8") as f:
            file_contents = f.read()
        # replace all occurrences of the regex pattern in the file_contents/items_game.txt with the replacement string
        try:
            new_file_contents = ""
            num_replacements = 0
            num_regex = 0
            match_iterator = re.finditer(rx_search, file_contents)
            total_matches = len(list(match_iterator))
            match_iterator = re.finditer(rx_search, file_contents)
            for i, match in enumerate(match_iterator):
                new_file_contents += file_contents[num_replacements:match.start()]
                new_file_contents += str_replace
                num_replacements = match.end()
                num_regex += 1
            new_file_contents += file_contents[num_replacements:]
        except Exception as e:
            message = f"Error: could not patch items_game.txt\n\nDetails: {str(e)}"
            messagebox.showerror(eng["namewrd"], message)
            return False
        if num_replacements == 0:
            message = 'Error: could not patch items_game.txt\n\nDetails: The items_game.txt inside selected pak01_dir.vpk is already patched!'
            messagebox.showerror(eng["namewrd"], message)
            return False
        else: # Set the output directory and filename
            vpk_name = os.path.basename(av_dbm.dbread("pak01dir_path"))
            vpk_name_o = os.path.splitext(vpk_name)[0]
            output_path = os.path.join(this_dir, "patched", f"{vpk_name_o}", "scripts", "items", "items_game.txt")
            os.makedirs(os.path.dirname(output_path), exist_ok=True) if not os.path.exists(os.path.dirname(output_path)) else None
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(new_file_contents)
        # duplicating vmdl from below here
        try:
            global vmdl_path
            matches = re.findall(rx_search_vmdl, file_contents)
            num_copies = 0
            # Iterate over the matches and copy/rename the default_ward.vmdl file
            for match in matches:
                # Build the source and destination paths
                output_dir_vmdl = os.path.join(this_dir, "patched", f"{vpk_name_o}", "models", "items", "wards", match)
                output_path_vmdl = os.path.join(output_dir_vmdl, f"{match}.vmdl_c")
                # Create the destination directory if it doesn't exist
                os.makedirs(output_dir_vmdl, exist_ok=True) if not os.path.exists(output_dir_vmdl) else None
                # Copy the file to the destination path
                if not os.listdir(output_dir_vmdl):
                    shutil.copy2(vmdl_path, output_path_vmdl)
                    num_copies += 1 # count wards model is copied
            # print(f"+ Total {num_copies} wards model is succesfully linked!")
        except Exception as e:
            message = f"Error: could not duplicate the vmdl\n\nDetails: {str(e)}"
            messagebox.showerror(eng["namewrd"], message)
            return False
        cod = f"Replaced {num_regex} lines of code"
        vmd = f"Duplicated {num_copies} vmdl_c file"
        if num_copies == 0:
            vmd = f"No vmdl_c file duplicated (possibly it's already patched)"
        dir = os.path.join(this_dir, "patched", f"{vpk_name_o}")
        if vpk_extracted:
            ext = f"Extracted all contents from {vpk_name}"
            message = f"{ext}\n{cod}\n{vmd}\n\nOutput directory:\n{dir}"
        else:
            message = f"{cod}\n{vmd}\n\nOutput directory:\n{dir}"
        messagebox.showinfo(eng["namewrd"], message)
        return True
    else:
        return False