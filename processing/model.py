d = """A script for converting folders with hold images into 3D models."""

import os
import argparse

from subprocess import Popen, DEVNULL

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

parser.add_argument("-i", "--input", help="The input folder. Defaults to 'scans/'.", default="scans")

arguments = parser.parse_args()

# TODO
# meshroom_batch -i out -o out2 -p Meshroom.mg
