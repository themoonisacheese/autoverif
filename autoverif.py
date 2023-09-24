import os
import json
import requests
import verif  
import shutil
import re

import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--contrib-path", help="input folder (games)")
parser.add_argument("-s", "--stash-path", help="output folder (valid games are moved here)")
parser.add_argument("-w", "--webhook-url", help="discord webhook url", required=False)
parser.add_argument("-t", "--check-stash", action="store_true", help="check for games with invalid format", required=False)
args = parser.parse_args()
config = vars(args)

CONTRIB_PATH = config["contrib_path"]
STASH_PATH = config["stash_path"]
DISCORD_WEBHOOK_URL = config["webhook_url"]
CHECK_STASH = config["check_stash"]

def send_hook(message_content):
    try:
        print(message_content)
        payload = {
            "username": "Contributions",
            "content": message_content
        }
        headers = {"Content-type": "application/json"}
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except: pass

def handle_folder(folder_name):
    final_path = os.path.join(CONTRIB_PATH, folder_name)
    try:
        if not os.path.exists(final_path):
            os.makedirs(final_path)
            print("Please put your game files in: " + final_path + " and run this script again.") 

        for filename in os.listdir(final_path):
            file_path = os.path.join(final_path, filename)
            send_hook(f"new file found: {filename}")
            
            if verif.verify(file_path):
                send_hook("Signature valid, moving to stash...")
                stash_folder = os.path.join(STASH_PATH, folder_name)
                os.makedirs(stash_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(stash_folder, filename))
                send_hook("Done")
            else:
                send_hook("Signature Invalid! deleting...")
                os.remove(file_path)
    except Exception as e:
        send_hook(f"An error occurred: {str(e)}")

def check_folder(folder_name):
    final_path = os.path.join(STASH_PATH, folder_name)
    if not os.path.exists(final_path):
        os.makedirs(final_path)
        print("Please put your game files in: " + final_path + " and run this script again.") 

    print(f"\nFiles found in {folder_name} : {len(os.listdir(final_path))}")

    if len(os.listdir(final_path)) == 0:
        return print("No files found, skipping folder")
    
    print("Checking for invalid files...\n")
    for filename in os.listdir(final_path):
        try:
            file_path = str(os.path.join(final_path, filename))
            send_hook(f"\nnew file found: {filename}")
            if not file_path.endswith(("nsp", "nsz", "xci", "xcz")):
                send_hook("Not a valid file extension. Skipping file...")
            
            else:
                titleid = None
                ver = None
                filetype = None

                send_hook("Checking syntax...")
                res = re.findall(r'\[([A-Za-z0-9_. ]+)\]',filename)

                for arg in res:
                    if len(arg) == 16:
                        titleid = arg
                    if arg.upper() in ["BASE", "UPD", "DLC", "UPDATE"] :
                        filetype = arg
                    if arg.lower().startswith("v") or (arg[:1].isdigit() and len(arg) < 16):
                        ver = arg

                print(f"\nTitleID: {titleid}\nVersion: {ver}\nFiletype: {filetype}\n")

                if not titleid or not ver:
                    send_hook("Syntax invalid! Writing that down...")
                    with open("invalid.txt", "a") as f:
                        if titleid == None and ver == None:
                            f.write(f"\nFOLDER: {folder_name}\n{filename}: MISSING TITLEID AND VERSION\n")
                        else:
                            if titleid == None:
                                f.write(f"\nFOLDER: {folder_name}\n{filename}: MISSING TITLEID\n")
                            if ver == None:
                                f.write(f"\nFOLDER: {folder_name}\n{filename}: MISSING VERSION\n")

                else:
                    send_hook("Syntax valid!")
    
        except Exception as e:
            send_hook(f"An error occurred: {str(e)}") 
    print("done! for invalid files check invalid.txt")     

        

if __name__ == "__main__":
    if CONTRIB_PATH and STASH_PATH:
        handle_folder("DLC")
        handle_folder("Base")
        handle_folder("UPD")
    elif STASH_PATH and CHECK_STASH:
        check_folder("DLC")
        check_folder("UPD")
        check_folder("Base")
        
    else: 
        parser.print_help()