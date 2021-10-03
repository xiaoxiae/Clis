import sys
import os
import shutil
from PIL import Image
from glob import glob

extension = "jpg"
n = 9

threshold = 20

in_folder = "in"
out_folder = "out"

deltas = [i - n // 2 for i in range(n)]

def value_function(pixel):
    r, g, b = pixel
    return r + g + b

if len(sys.argv) != 2:
    print("The script expects a single argument (the hot pixel mask).")
    exit()

mask_path = sys.argv[1]

if not os.path.exists(mask_path):
    print("Mask not found.")
    exit()

if os.path.exists("out"):
    shutil.rmtree("out")
os.mkdir("out")

with Image.open(mask_path) as mask_image:
    mask_pixels = mask_image.load()

    w, h = mask_image.width, mask_image.height

    for file in glob(f"*.{extension}"):
        if file == mask_path:
            continue

        with Image.open(file) as clean_image:
            clean_pixels = clean_image.load()
            exif = clean_image.info['exif']

            # remove dead pixel using the mask
            for x in range(w):
                for y in range(h):
                    if value_function(mask_pixels[(x, y)]) > threshold:
                        values = []

                        for dx in deltas:
                            for dy in deltas:
                                nx, ny = x + dx, y + dy

                                if not (nx >= 0 and ny >= 0 and nx < w and ny < h):
                                    continue

                                if value_function(mask_pixels[(nx, ny)]) <= threshold:
                                    values.append(clean_pixels[(nx, ny)])

                        # TODO: tohle je docela ošklivé, bylo by fajn to udělat lépe
                        # TODO: zakomponovat barvu pozadí do toho, zda se to bude filtrovat nebo ne
                        average = [0, 0, 0]
                        for value in values:
                            average[0] += value[0]
                            average[1] += value[1]
                            average[2] += value[2]

                        average[0] //= len(values)
                        average[1] //= len(values)
                        average[2] //= len(values)

                        clean_pixels[(x, y)] = tuple(average)

            clean_image.save(f"out/{file}", exif=exif)
