import sys
import shutil
import os
from glob import glob

if len(sys.argv) != 3:
    print("The script expects 2 arguments (input and output folder).")
    quit()

input_folder = sys.argv[1]
output_folder = sys.argv[2]

files = [f for f in glob(os.path.join(input_folder, "*")) if os.path.isfile(f)]

if len(files) == 0:
    print("no files to move.")
else:
    print(f"moving {len(files)} files.")

for file in files:
    shutil.move(file, os.path.join(output_folder, os.path.basename(file)))
