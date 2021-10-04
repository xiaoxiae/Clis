import sys
import shutil
import os
from subprocess import call
from glob import glob

if len(sys.argv) != 3:
    print("The script expects 2 arguments (input and output folder).")
    quit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]

files = [f for f in glob(os.path.join(input_folder, "*")) if os.path.isfile(f)]

printed_message = False

if len(files) == 0:
    print("no files to move. ", end="", flush=True)

for file in files:
    try:
        shutil.move(file, os.path.join(output_folder, os.path.basename(file)))
    except PermissionError:
        call(["sudo", "-E", "pypy3"] + [os.path.abspath(a) for a in sys.argv])
        sys.exit()

    if not printed_message:
        printed_message = True
        print(f"moving {len(files)} files... ", end="", flush=True)
