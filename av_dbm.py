import json
import os

import av_main

this_dir = av_main.determine_dir()
db_path = os.path.join(this_dir, "data", "database.json")

# Check if JSON file exists, create it if it doesn't
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))
if not os.path.exists(db_path):
    with open(db_path, 'w') as f:
        json.dump({}, f)
        
# Load existing JSON data
def dbread(string):
    with open(db_path, 'r') as f:
        data = json.load(f)
    # print("one:", data.get(string))
    return data.get(string)

# Store and write JSON data
def dbwrite(key, value):
    with open(db_path, 'r+') as f:
        data = json.load(f)
        if key in data:
            data[key] = value
            update = True
        else:
            data.update({key: value})
            update = False
        f.seek(0)
        f.truncate()
        json.dump(data, f)
    return update

