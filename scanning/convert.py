d = """A script for converting photos from RAW to JPGs using darktable."""

import argparse
import os

from subprocess import Popen, DEVNULL
from glob import glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

parser.add_argument("-i", "--input", help="The input directory. Defaults to 'scans/'.", default='scans')
parser.add_argument("-f", "--format", help="The RAW format. Defaults to 'nef'.", default='nef')

arguments = parser.parse_args()


for folder in glob(os.path.join(arguments.input, "*")):
    for file in [f for f in glob(os.path.join(folder, "*")) if f.lower().endswith(arguments.format)]:
        print(f"Darktable: \tconverting file {os.path.basename(file)}...", end="", flush=True)
        Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()
        print(f" done.", flush=True)
