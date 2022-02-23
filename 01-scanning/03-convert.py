import argparse
import os
import sys
from glob import glob
from subprocess import DEVNULL, Popen

sys.path.append("..")
from config import *
from utilities import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

printer = Printer("convert")


for folder in glob(os.path.join(SCAN_PATH, "*")):
    for file in glob(os.path.join(folder, "*")):
        if not file.lower().endswith(IMAGE_EXTENSION):
            continue

        printer.begin(f"converting file {os.path.basename(file)}")
        Popen(
            ["darktable-cli", file, os.path.join(os.path.dirname(file), ".")],
            stdin=DEVNULL,
            stdout=DEVNULL,
            stderr=DEVNULL,
        ).communicate()
        printer.mid("removing the original")
        os.remove(file)
        printer.end("done.")
