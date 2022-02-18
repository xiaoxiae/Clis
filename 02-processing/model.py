d = """A script for converting folders with hold images into 3D models."""

import os
import argparse
from subprocess import Popen, PIPE
from glob import glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

parser.add_argument("-i", "--input", help="The input folder. Defaults to 'scans/'.", default="scans")
parser.add_argument("-o", "--output", help="The output folder. Defaults to 'models/'.", default="models")

arguments = parser.parse_args()

for folder in glob(os.path.join(arguments.input, "*")):
    output_folder = os.path.join(arguments.output, os.path.os.path.basename(folder) + "-out")

    os.makedirs(output_folder, exist_ok=True)

    process = Popen(["meshroom_batch", "-i", folder, "-o", output_folder, "-p", "Meshroom.mg"], stdout=PIPE, stderr=PIPE)
    result = process.communicate()
