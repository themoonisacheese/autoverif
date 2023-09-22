#!/bin/bash

#run this as a cron job every 5 minutes

CONTRIB_PATH="/home/themoon/googledrive/perso"
STASH_PATH="/home/themoon/googledrive/contrib"

cd "$(dirname "$0")"

send_hook() {
    #args:
    # message content
    json='{"username": "Contributions", "content":"'
    json=$json$1
    json=$json'"}'
    curl -H "Content-type:application/json" -d "$json" <discord webhook url>
}


handle_folder() {
    #args:
    #   Folder name (DLC, Base, Update)
    #only include folder name and not path, path is constructed from script variables
    finalpath=$CONTRIB_PATH/$1/
    shopt -s nullglob #enable nullglob to prevent running the loop on an empty folder
    for file in "$finalpath"*
    do
        filename=$(basename "$file")
        echo "new file found : $filename"
        send_hook "new file found: $filename"
        if  .venv/bin/python verif.py "$file"; then
            send_hook "Signature valid, moving to stash..."
            mv "$file" "$STASH_PATH/$1"
            send_hook "Done"
        else
            send_hook "Signature Invalid! deleting..."
            rm "$file"
        fi
    done
    shopt -u nullglob #disable nullglob after loop
}


handle_folder DLC
handle_folder Base
handle_folder Update

