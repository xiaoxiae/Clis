import argparse
import os
from glob import glob
from subprocess import DEVNULL, Popen

sys.path.append("..")
from config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


for folder in glob(os.path.join(SCAN_PATH, "*")):
    for file in glob(os.path.join(folder, "*")):
        if not file.lower().endswith(IMAGE_EXTENSION):
            continue

        print(
            f"Darktable: \tconverting file {os.path.basename(file)}...",
            end="",
            flush=True,
        )
        Popen(
            ["darktable-cli", file, os.path.join(os.path.dirname(file), ".")],
            stdin=DEVNULL,
            stdout=DEVNULL,
            stderr=DEVNULL,
        ).communicate()
        print(f" removing the original...", end="", flush=True)
        os.remove(file)
        print(f" done.", flush=True)
