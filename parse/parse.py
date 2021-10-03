import os
import shutil

from subprocess import Popen, PIPE, DEVNULL
from glob import glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

OUTPUT_FORMAT = ".jpg"

#print("move.py: ", end="")
#print(Popen(["python3", "move.py", INPUT_FOLDER, OUTPUT_FOLDER], stdin=PIPE, stdout=PIPE).communicate()[0].decode())
#
#print("converting to a simpler format...", end="", flush=True)
#
#files = glob(os.path.join(OUTPUT_FOLDER, "*"))
#for file in files:
#    Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()
#print(" done.")
#
#print("removing the older photos...", end="", flush=True)
#for file in files:
#    os.remove(file)
#print(" done.")
#
#print("split.py: splitting the folder...", end="")
#print(Popen(["python3", "split.py", OUTPUT_FOLDER], stdin=PIPE, stdout=PIPE).communicate()[0].decode(), end="")
#print(" done.")
#

# TODO: clean!
