"""Add holds that were not yet added to the dictionary."""
import os
import sys
import hashlib
from glob import glob

sys.path.append("..")
from config import *
from utilities import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper

printer = Printer("model")

def get_file_hashsum(path):
    with open(path) as f:
        return hashlib.sha256(f.read().encode('utf-8')).hexdigest()

with open(MODEL_YAML_NAME) as f:
    data = load(f.read(), Loader=Loader) or {}

for model_folder in glob(os.path.join(MODEL_PATH, "*")):
    hold_path = os.path.join(model_folder, MODEL_FILE_NAME + ".obj")

    printer.begin(f"reading '{hold_path}'")
    try:
        id = get_file_hashsum(hold_path)

    except FileNotFoundError:
        printer.end(f"doesn't contain {MODEL_FILE_NAME + '.obj'}, skipping.")
        continue

    if id not in data:
        printer.end(f"added.")

        data[id] = {}
    else:
        printer.end(f"already added, skipping.")

with open(MODEL_YAML_NAME, "w") as f:
    f.write(dump(data, Dumper=Dumper))
