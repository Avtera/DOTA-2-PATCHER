from re import search as research, finditer as refinditer
from os import path as ospath, makedirs as osmakedirs
from zlib import crc32
from json import load as jsload
from time import sleep
from subprocess import Popen as spPopen, PIPE as spPIPE
from tkinter import messagebox
from tkinter import filedialog

import av_dbm
import av_main

# some necessary default variable
this_dir = av_main.determine_dir()
root_dir = ospath.dirname(ospath.abspath(__file__))
crcmanip_dir = ospath.join(root_dir, "data", "library", "crcmanip", "crcmanip-cli.exe")
gameinfo_temp = ospath.join(root_dir, "data", "temp", "temp.gi")
gameinfo_output = ospath.join(this_dir, "patched", "gameinfo.gi")
offset = 2

# data and path value, so there is no existential crisis
if not ospath.exists(ospath.dirname(gameinfo_temp)):
    osmakedirs(ospath.dirname(gameinfo_temp))
if av_dbm.dbread("gameinfo_path") != None:
    gameinfo_input = ospath.join(av_dbm.dbread("gameinfo_path"))
if av_dbm.dbread("folder_name") != None:
    mod_folder = av_dbm.dbread("folder_name")
else:
    av_dbm.dbwrite("folder_name", "dota_tempcontent")
    mod_folder = av_dbm.dbread("folder_name")

# load the languages
def load_language_file(lang):
    with open(ospath.join(ospath.dirname(ospath.abspath(__file__)), "data", "lang", f"strings_{lang}.json"), "r") as f:
        return jsload(f)
eng = load_language_file("en")

# core functions
def get_file_info(file_path):
    file_name = ospath.basename(file_path)
    file_dir = ospath.dirname(file_path)
    file_size_kb = round(ospath.getsize(file_path) / 1024, 3)
    return file_name, file_size_kb, file_dir
def get_crc32(input_data):
    if ospath.isfile(input_data):
        with open(input_data, 'rb') as f:
            data = f.read()
    else:
        data = input_data.encode()
    return hex(crc32(data) & 0xffffffff)[2:]
def patcher():
    browse = browsegi()
    if browse:
        if ospath.exists(gameinfo_input):
            patched = patchgi()
            if patched:
                return True
def browsegi():
    global gameinfo_input
    global gameinfo_temp
    global gameinfo_output
    firsttime = True
    while True:
        # detects wether is gameinfo.gi or other .gi file is exists
        if 'gameinfo_input' not in globals() or not ospath.exists(gameinfo_input) or ".gi" not in ospath.splitext(gameinfo_input)[1]:
            if firsttime == True:
                message = "The file gameinfo.gi is not detected. \nPlease locate the file."
                result = messagebox.showinfo(eng["namegi"], message)
                firsttime = False
            gameinfo_input = filedialog.askopenfilename(title="Select gameinfo.gi", filetypes=(("Game Info file", "*.gi"), ("All files", "*.*")))
            # selected file is invalid
            if ospath.exists(gameinfo_input) and ".gi" not in ospath.splitext(gameinfo_input)[1]:
                message = "Invalid file is selected. Please try again."
                result = messagebox.askretrycancel(eng["namegi"], message)
                if result:
                    continue # select the file again
                else:
                    return False # quit
            # selected file is valid
            elif "gameinfo" in gameinfo_input or ".gi" in ospath.splitext(gameinfo_input)[1]:
                continue
            # detects wether any file is selected
            else:
                message = "No file is selected. Please try again."
                result = messagebox.askretrycancel(eng["namegi"], message)
                if result:
                    continue # select the file again
                else:
                    return False # quit
        # goes here if the file is exists
        else:
            firsttime = False
            file_name, file_size_kb, file_dir = get_file_info(gameinfo_input)
            agree = "Please confirm that the file is correct."
            message = f"File Details:\n- Name: {file_name}\n- Size: {file_size_kb} KB\n- CRC-32: {get_crc32(gameinfo_input)}\n\nFile Location:\n- {file_dir} \n\n{agree}"
            result = messagebox.askyesno(eng["namegi"], message)
            if result:
                av_dbm.dbwrite("gameinfo_path", gameinfo_input)
                return True # stop the loop then continue the process
            else:
                del gameinfo_input
                continue # select the file again
def patchgi():
    global mod_folder
    if ospath.exists(gameinfo_input): 
        with open(gameinfo_input, "r") as f:
            gi_data = f.read()
        originalfilelength = len(gi_data)
        for match in refinditer(r'\bGame\s+dota\b', gi_data):
            SearchPaths_start = gi_data.rfind("{", 0, match.start()) + 1
            SearchPaths = gi_data[SearchPaths_start:gi_data.find("}", match.start())]
        if 'SearchPaths' in locals():
            game_pos = research(r'\bGame\s+dota\b', SearchPaths)
        if 'game_pos' in locals():
            if not research(fr'\bGame\s+{mod_folder}\b', SearchPaths) and not research(fr'\bMod\s+{mod_folder}\b', SearchPaths):
                gi_crc32 = get_crc32(gameinfo_input)
                inject = game_pos.group().replace("dota", mod_folder)
                temp_sp = SearchPaths[:game_pos.start()] + inject + "\n" + SearchPaths[game_pos.start()-3:]
                mod_pos = research(r'\bMod\s+dota\b', temp_sp)
                inject = mod_pos.group().replace("dota", mod_folder)
                temp_sp = temp_sp[:mod_pos.start()] + inject + "\n" + temp_sp[mod_pos.start()-3:]
                gi_data = gi_data.replace(SearchPaths, temp_sp, 1)
                mod_data_crc32 = get_crc32(gi_data)
                # Find the number of excess characters and remove comments to make file size the same as the original
                excess_count = len(gi_data) - originalfilelength + offset + 4  # Additional 4 bytes(dummy crc bytes)
                # Debug
                while excess_count > 0:
                    # Find the first comment section
                    xpos = gi_data.find("//")
                    # Find the second comment section
                    pos = gi_data.find("//", xpos + offset)
                    if pos == -1:
                        break
                    # Find the end of the detected comment
                    end_pos = gi_data.find("\n", pos)
                    comment = gi_data[pos:end_pos]
                    comment_length = end_pos - pos
                    excess_count -= comment_length
                    if excess_count >= 0:
                        gi_data = gi_data.replace(comment, '', 1)
                    else:
                        gi_data = gi_data.replace(comment, comment[:-excess_count], 1)
                # Find the first comment section
                comment_offset = gi_data.find("//", xpos + 1)
                # Write temp file to the disk
                with open(gameinfo_temp, "w") as f:
                    f.write(gi_data)
                message = f'{eng["p_po_1"]}\n\n{eng["p_po_2"]}\n{eng["p_po_3"]}'
                result = messagebox.askyesno(eng["namegi"], message)
                if result:
                    gameinfo_output = filedialog.askopenfilename(
                        title="Select the original gameinfo.gi",
                        filetypes=(("Gameinfo files", "*.gi"), ("All files", "*.*")))
                else:
                    if not ospath.exists(ospath.dirname(gameinfo_output)):
                        osmakedirs(ospath.dirname(gameinfo_output))
                # CRC32 Manipulation
                cmd = [crcmanip_dir, "patch", gameinfo_temp, gameinfo_output, str(gi_crc32), "-p", str(comment_offset), "-a", "CRC32"]
                # Use subprocess to execute the command and capture the output
                process = spPopen(cmd, stdout=spPIPE, stderr=spPIPE)
                # output, error = process.communicate()
                # if process.returncode != 0:
                #     print(f"Error executing command: {cmd}")
                #     print(f"Output: {output.decode('utf-8')}")
                #     print(f"Error: {error.decode('utf-8')}")
                sleep(1)
                gi_manip_crc32 = get_crc32(gameinfo_output)
                if gi_crc32 == gi_manip_crc32:
                    message = f"Patcher report:\nOriginal CRC32: {gi_crc32}\nModified CRC32: {gi_manip_crc32}\n\nHex codes match! The patch operation was successful."
                    messagebox.showinfo(eng["namegi"], message)
                    return True
                else:
                    message = f"Patcher report:\nOriginal CRC32: {gi_crc32}\nModified CRC32: {gi_manip_crc32}\n\nThe hexadecimal codes do not match. The operation has failed."
                    messagebox.showerror(eng["namegi"], message)
            else:
                message = "The patch operation failed as the selected file has already been modified."
                messagebox.showerror(eng["namegi"], message)
        else:
            message = "Please verify the integrity of game files through Steam, as the selected file appears to be corrupted or invalid."
            messagebox.showerror(eng["namegi"], message)
    else:
        message = "Please try again as the selected file could not be detected."
        messagebox.showerror(eng["namegi"], message)

# Debug
# browsegi()
# patchgi()