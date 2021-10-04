import sys
import os
import shutil
from PIL import Image, ImageStat

from glob import glob

THRESHOLD = 8

def brightness(file):
   im = Image.open(file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]

if len(sys.argv) != 2:
    print("The script expects 1 arguments (the input folder).")
    quit()

current_dirs = []
i = 1
for file in glob(os.path.join(sys.argv[1], "*")):
    b = brightness(file)

    # ship t
    if b <= THRESHOLD:
        dir_name = os.path.join(sys.argv[1], str(i).rjust(2, "0"))
        os.mkdir(dir_name)

        # move the collected files
        for f in current_dirs:
            shutil.move(f, os.path.join(dir_name, os.path.basename(f)))

        current_dirs = []

        # move the current file
        shutil.move(file, os.path.join(dir_name, "mask" + os.path.splitext(file)[1]))

        i += 1
    else:
        current_dirs.append(file)

