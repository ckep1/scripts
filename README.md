# scripts

## Install Instructions
All scripts are Python files and can be run in the directory using the Python launcher or via CLI.
I personally created aliases in my terminal to access these quickly from my working directory.
Python must be installed. These do not require outside dependencies to be installed.

## filetree.py
This script outputs your current file tree similar to `ls` but with a few changes:
- It is recursive
- If there is a .gitignore file present in the directory, the patterns will be matched.
- .git folders are also ignored (requires .gitignore to be present currently).
- The files are output in a hierarchal format.
### Usage:
- Output current working directory files to terminal `python filetree.py`
- Specify a Directory via an Argument `python filetree.py /path/to/dir`
- Save to file instead of printing to terminal `python filetree.py -savefile`
- Both `python filetree.py /path/to/dir -savefile`

## playlist-from-dir.py
  This script is used to create an m3u8 playlist from either the current working directory or the directory passed in as an argument. 
I currently use this for Flacbox on Mac and iPhone (the script is run on Mac) but it should work with any music playlist manager that accepts m3u8 files.
It is not recursive currently but this option may be added soon if anyone wants it.
### Usage:
- Output current working directory song files to an m3u8 playlist file `python filetree.py`
- Specify a Directory via an Argument `python playlist-from-dir.py /path/to/dir`

## more soon...
