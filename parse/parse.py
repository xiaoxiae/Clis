import os
import shutil

from subprocess import Popen, PIPE, DEVNULL
from glob import glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
BACKUP_FOLDER = "backup"

OUTPUT_FORMAT = ".jpg"

if os.path.exists(BACKUP_FOLDER):
    result = ""
    while result not in ("yes", "no"):
        result = input("Backup exists. Delete? (yes/no): ")

        if result == "yes":
            shutil.rmtree(BACKUP_FOLDER)
        elif result == "no":
            print("Exitting.")
            quit()

if os.path.exists(OUTPUT_FOLDER):
    shutil.rmtree(OUTPUT_FOLDER)
os.mkdir(OUTPUT_FOLDER)

print("move.py: ", end="", flush=True)
print(Popen(["pypy3", "move.py", INPUT_FOLDER, OUTPUT_FOLDER], stdin=PIPE, stdout=PIPE).communicate()[0].decode(), end="")
print("done.")

print("backing up the moved photos... ", end="", flush=True)
shutil.copytree(OUTPUT_FOLDER, BACKUP_FOLDER)
print("done.")

print("converting to a simpler format... ", end="", flush=True)
files = glob(os.path.join(OUTPUT_FOLDER, "*"))
for file in files:
    Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()
print(" done.")

print("removing the older photos... ", end="", flush=True)
for file in files:
    os.remove(file)
print("done.")

print("split.py: splitting the folder... ", end="", flush=True)
print(Popen(["pypy3", "split.py", OUTPUT_FOLDER], stdin=PIPE, stdout=PIPE).communicate()[0].decode(), end="")
print("done.")

print("clean.py: cleaning photos... ", end="", flush=True)
for folder in glob(os.path.join(OUTPUT_FOLDER, "*")):
    for file in glob(os.path.join(folder, "*")):
        mask_name = glob(os.path.join(folder, "mask*"))[0]
        Popen(["pypy3", "clean.py", file, mask_name], stdin=PIPE, stdout=PIPE).communicate()
print("done.")
