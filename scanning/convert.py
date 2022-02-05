d = """A script for recursively converting all photos from RAW to JPGs in a given folder using darktable."""

import argparse
import os

from subprocess import Popen, DEVNULL
from glob import glob

from config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

parser.add_argument("-i", "--input", help=f"The input folder. Defaults to '{SCAN_PATH}'.", default=SCAN_PATH)
parser.add_argument("-f", "--format", help=f"The image format. Defaults to '{IMAGE_EXTENSION}'.", default=IMAGE_EXTENSION)

arguments = parser.parse_args()


for folder in glob(os.path.join(arguments.input, "*")):
    for file in [f for f in glob(os.path.join(folder, "*")) if f.lower().endswith(arguments.format)]:
        print(f"Darktable: \tconverting file {os.path.basename(file)}...", end="", flush=True)
        Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()
        print(f" done.", flush=True)
