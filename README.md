# autoverif 
Auto verify NSP, NSZ, XCI, XCZ to check if they have a valid hash and signature, on Linux and Windows.

# Usage


```
  -h, --help            show help message and exit
  -c CONTRIB_PATH, --contrib-path CONTRIB_PATH
                        input folder (valid games are moved from here)
  -s STASH_PATH, --stash-path STASH_PATH
                        output folder (verified games)
  -w WEBHOOK_URL, --webhook-url WEBHOOK_URL
                        discord webhook url
  -t, --check-stash     check for games with invalid format
```
# Install
clone this repo, then:

```
cd autoverif
python3 -m venv .venv

#Windows:
.venv.\Scripts\activate.bat
#Linux:
source .venv/bin/activate

pip3 install -r requirements.txt
```

# Examples
```
python3 autoverify.py -c /path/to/unverified/games -s /path/to/stash
```

/path/to/unverified/games must contain folders named "Base", "UPD", and "DLC" (case sensitive). Only files in these folders will be checked.
If the folders in the contrib or stash directory do not exist, they will be created.
Files that pass the signature verification will be moved to their corresponding folder in the stash directory (ie, Base to Base, etc. Only the source folder is actually considered, not whether the file really is a Base nsp).
Files that do not pass the signature verification will be **PERMANENTLY DELETED** (they don't validate anyway why do you have them?). This may or may not include random non-verifiable files (eg: text files, photos of your cat, your hard drive's partition table) that happen to be there.
