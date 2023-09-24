# autoverif 
Auto verify NSP, NSZ, XCI, XCZ to check if they have a valid hash and signature

# RUN SETUP.PY IF YOU'RE ON WINDOWS

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
# Examples

## Windows
```
.\venv-windows\Scripts\python.exe autoverif.py -c "/path/to/your/unverified/games/folder" -s "/path/to/output/folder"
```

## Linux
```
./venv-linux/bin/python autoverif.py -c "/path/to/your/unverified/games/folder" -s "/path/to/output/folder"
```

