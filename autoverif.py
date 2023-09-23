import os
import json
import requests
import verif  
import shutil

import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--contrib-path", help="input folder (games)")
parser.add_argument("-s", "--stash-path", help="output folder (valid games are moved to here)")
parser.add_argument("-w", "--webhook-url", help="discord webhook url", required=False)
args = parser.parse_args()
config = vars(args)

CONTRIB_PATH = config["contrib_path"]
STASH_PATH = config["stash_path"]
DISCORD_WEBHOOK_URL = config["webhook_url"]

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
            print(filename)
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
        raise e

if __name__ == "__main__":
    if CONTRIB_PATH and STASH_PATH:
        handle_folder("DLC")
        handle_folder("Base")
        handle_folder("Update")
    else: 
        parser.print_help()