import os
import json
import requests
import verif  
import shutil

CONTRIB_PATH = "/home/themoon/Downloads/mhr/switch games/West of Loathing [NSZ]/"
STASH_PATH = "/home/themoon/googledrive/contrib"
DISCORD_WEBHOOK_URL = "https://discord.com/aksdpanf"  # Replace with your actual webhook URL

def send_hook(message_content):
    payload = {
        "username": "Contributions",
        "content": message_content
    }
    headers = {"Content-type": "application/json"}
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    response.raise_for_status()

def handle_folder(folder_name):
    final_path = os.path.join(CONTRIB_PATH, folder_name)
    try:
        os.makedirs(final_path, exist_ok=True)  # Create the folder if it doesn't exist
        for filename in os.listdir(final_path):
            file_path = os.path.join(final_path, filename)
            print(f"new file found: {filename}")
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

if __name__ == "__main__":
    handle_folder("DLC")
    handle_folder("Base")
    handle_folder("Update")