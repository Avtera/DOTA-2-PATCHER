# DOTA-2-PATCHER
An utility for visual mod.

### What this tool do?
- Patch all wards to the default wards model
- Patch gameinfo.gi to inject the visual mod folder
- Build patched pak01_dir folder to a .vpk file
- Play cool music (you can turn it off)

### I dont left you guessing how
- 1: Select your pak01_dir.vpk from "\Steam\steamapps\common\dota 2 beta\game\dota" or your modded pak01_dir.vpk
- 2: (Change the mod folder name to any mod u using, then) Select your gameinfo.gi from "\Steam\steamapps\common\dota 2 beta\game\dota", Copy the new gameinfo.gi from "patched" folder to the same folder where you get it
- 3: Select the pak01_dir folder and copy the pak01_dir.vpk from "patched" folder to the mod folder (default: dota_tempcontent) located in "\Steam\steamapps\common\dota 2 beta\game"

### Some info
- The default folder name injected to gameinfo.gi is "dota_tempcontent", you can change this folder name inside /data/database.json with any text editor to any folder name you wish 😎
- Reminder for those want to rename the patched vpk to pak02_dir.vpk: If your installed mod pak01_dir.vpk is contains items_game.txt, the patch wards to default mod will not work because Dota 2 cant accept 2 items_games.txt inside 2 different .vpk
- Solution: Coming soon .vpk decompiler

### Screenshot
![image](https://user-images.githubusercontent.com/69560119/221392381-ddff5080-9436-4db9-93a0-43600e6300e4.png)

### To do list
- make a prompt to rename the folder
- add other visual mod patch
- idk give me suggestions

### Why the .exe file size is large?
Because i need to include library like vpk, json, shutil, tkinter, customtkinter, zlib, and crc-manipulator. To give you a pleasant and ease of use experience with this tool.

### Virustotal
https://www.virustotal.com/gui/file-analysis/N2RkNDRjZGEwYjNmY2Y4MzEwMWVkNGI2YWE2MmMxOTM6MTY3NzM4NjIyNg==
