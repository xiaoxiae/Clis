"""Add holds that were not yet added to the dictionary."""
import os
import sys
import hashlib
import math
from glob import glob

sys.path.append("..")
from config import *
from utilities import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper

printer = Printer("model")

def get_file_hashsum(path):
    """Return the hashsum of the file contents."""
    with open(path) as f:
        return hashlib.sha256(f.read().encode('utf-8')).hexdigest()

def infer_obj_color(path):
    """Infer a color from an obj file if it contains it, else return None."""
    def hex_to_tuple(color):
        """Return an (r, g, b) tuple from a hex string."""
        return tuple([int(color[1:][i*2:(i+1)*2], 16) for i in range(3)])

    def color_distance(c1, c2):
        """Return the distance between two colors (in Euclidean distance)."""
        return math.sqrt(sum([(x1 - x2) ** 2 for x1, x2 in zip(c1, c2)]))

    with open(path) as f:
        average_color = [0, 0, 0]
        total_vertices = 0

        # determine the average color by parsing the file
        for line in f.read().splitlines():
            contents = line.strip().split()

            if len(contents) == 0:
                continue

            if contents[0] == 'v':
                try:
                    _, _, _, _, r, g, b = contents
                except:
                    return

                for i, c in enumerate(map(float, [r, g, b])):
                    average_color[i] += c

                total_vertices += 1

        for i in range(len(average_color)):
            average_color[i] = average_color[i] / total_vertices * 256

        # return the closest named color
        min_color_distance = float('inf')
        min_color = None
        for name, color in NAMED_COLORS.items():
            distance = color_distance(hex_to_tuple(color), average_color)
            if distance < min_color_distance:
                min_color_distance = distance
                min_color = name

        return min_color

if not os.path.exists(MODEL_YAML_NAME):
    data = {}
else:
    with open(MODEL_YAML_NAME) as f:
        # if the file is empty, None is read; we want an empty dict instead
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
        data[id] = {}

        # infer color by parsing the obj file, since it contains the vertex colors
        # this is not standardized but Metashape does this, which is nice
        color = infer_obj_color(hold_path)

        if color is None:
            printer.mid("no color information")
        else:
            data[id]['color'] = color
            printer.mid(f"color {color} inferred")

        printer.end(f"added.")
    else:
        printer.end(f"already added, skipping.")

with open(MODEL_YAML_NAME, "w") as f:
    f.write(dump(data, Dumper=Dumper))
