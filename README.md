# autoverif 
Auto verify NSP, NSZ, XCI, XCZ to check if they have a valid hash and signature

# Usage

```
  -h, --help            show this help message and exit
  -c CONTRIB_PATH, --contrib-path CONTRIB_PATH
                        input folder (valid games are moved from here)
  -s STASH_PATH, --stash-path STASH_PATH
                        output folder (verified games)
  -w WEBHOOK_URL, --webhook-url WEBHOOK_URL
                        discord webhook url
```

# Examples

## Windows
```
.\venv-windows\Scripts\python.exe autoverif.py -s "/path/to/your/unverified/games/folder" -c "/path/to/output/foler"
```

## Linux
```
./venv-linux/bin/python autoverif.py -s "/path/to/your/unverified/games/folder" -c "/path/to/output/foler"
```
