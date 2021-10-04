import sys
import os
import shutil
from PIL import Image
from glob import glob

N = 3

threshold = 20

def value_function(pixel):
    r, g, b = pixel
    return r + g + b

if len(sys.argv) != 3:
    print("The script expects two arguments (the input and the mask file).")
    exit()

file = sys.argv[1]
mask_path = sys.argv[2]

with Image.open(mask_path) as mask_image:
    mask_pixels = mask_image.load()

    w, h = mask_image.width, mask_image.height

    with Image.open(file) as clean_image:
        clean_pixels = clean_image.load()
        exif = clean_image.info['exif']

        # remove dead pixel using the mask
        for x in range(w):
            for y in range(h):
                if value_function(mask_pixels[(x, y)]) > threshold:
                    n = N
                    values = []
                    while len(values) == 0:
                        deltas = [i - n // 2 for i in range(n)]
                        for dx in deltas:
                            for dy in deltas:
                                nx, ny = x + dx, y + dy

                                if not (nx >= 0 and ny >= 0 and nx < w and ny < h):
                                    continue

                                if value_function(mask_pixels[(nx, ny)]) <= threshold:
                                    values.append(clean_pixels[(nx, ny)])

                        n += 2

                    # TODO: this is ugly
                    average = [0, 0, 0]
                    for value in values:
                        average[0] += value[0]
                        average[1] += value[1]
                        average[2] += value[2]

                    average[0] //= len(values)
                    average[1] //= len(values)
                    average[2] //= len(values)

                    clean_pixels[(x, y)] = tuple(average)

        clean_image.save(file, exif=exif)
