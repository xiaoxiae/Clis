"""Add holds that were not yet added to the dictionary."""
import os
import sys
import hashlib
import math
import datetime
from PIL import Image, ImageEnhance
from glob import glob

sys.path.append("..")
from config import *
from utilities import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper

printer = Printer("model")


def get_file_hashsum(path, characters=12):
    """Return the hashsum of the file contents."""
    with open(path) as f:
        return hashlib.sha256(f.read().encode("utf-8")).hexdigest()[:12]


def infer_texture_color(path):
    """Infer a color from an jpg texture of the file."""

    def hex_to_tuple(color):
        """Return an (r, g, b) tuple from a hex string."""
        return tuple([int(color[1:][i * 2 : (i + 1) * 2], 16) for i in range(3)])

    def get_average_color(path, enhance=4):
        """Given a path to image, return average value of color as (r, g, b).
        Also saturates it for the color to be more vivid."""
        i_orig = Image.open(path)

        converter = ImageEnhance.Color(i_orig)
        i = converter.enhance(enhance)
        h = i.histogram()

        # split into red, green, blue
        r = h[0:256]
        g = h[256:256*2]
        b = h[256*2: 256*3]

        # perform the weighted average of each channel:
        # the *index* is the channel value, and the *value* is its weight
        return (
            sum( i*w for i, w in enumerate(r) ) / sum(r),
            sum( i*w for i, w in enumerate(g) ) / sum(g),
            sum( i*w for i, w in enumerate(b) ) / sum(b)
        )

    def color_distance(c1, c2):
        """Return the distance between two colors (in Euclidean distance)."""
        return math.sqrt(sum([(x1 - x2) ** 4 for x1, x2 in zip(c1, c2)]))

    average_color = get_average_color(path)

    # return the closest named color
    min_color_distance = float("inf")
    min_color = None
    for name, color in NAMED_COLORS.items():
        distance = color_distance(hex_to_tuple(color), average_color)
        if distance < min_color_distance:
            min_color_distance = distance
            min_color = name

    return min_color


def file_modification_date(path):
    """Get the file modification time."""
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))


model_yaml_path = os.path.join(MODEL_PATH, MODEL_YAML_NAME)

if not os.path.exists(MODEL_PATH):
    os.mkdir(MODEL_PATH)

if not os.path.exists(model_yaml_path):
    data = {}
else:
    with open(model_yaml_path) as f:
        # if the file is empty, None is read; we want an empty dict instead
        data = load(f.read(), Loader=Loader) or {}

for model_folder in sorted(glob(os.path.join(MODEL_PATH, "*"))):
    if not os.path.isdir(model_folder):
        continue

    hold_path = os.path.join(model_folder, MODEL_FILE_NAME + ".obj")
    texture_path = os.path.join(model_folder, MODEL_FILE_NAME + ".jpg")

    printer.begin(f"reading '{hold_path}'")
    try:
        id = get_file_hashsum(hold_path)
    except FileNotFoundError:
        printer.end(f"doesn't contain {MODEL_FILE_NAME + '.obj'}, skipping.")
        continue

    if id not in data:
        data[id] = {}

        # infer color by parsing the texture file
        color = infer_texture_color(texture_path)

        if color is None:
            printer.mid("no color information")
        else:
            data[id]["color"] = color
            printer.mid(f"color {color} inferred")

        data[id]["date"] = file_modification_date(hold_path)

        printer.end(f"added.")
    else:
        printer.end(f"already added, skipping.")

with open(model_yaml_path, "w") as f:
    f.write(dump(data, Dumper=Dumper))
