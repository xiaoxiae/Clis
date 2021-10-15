d = """A script for controlling the automatic camera + Arduino setup."""

import argparse
import gphoto2 as gp
import os

from subprocess import Popen, DEVNULL
from glob import glob
from time import sleep
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)
parser.add_argument("count", type=int, help="How many images to take.")
arguments = parser.parse_args()

camera = gp.Camera()

print('Camera: Connecting to the camera...')
while True:
    try:
        camera.init()
    except gp.GPhoto2Error as ex:
        if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
            sleep(2)
            continue
        raise
    break

print("Camera: Connected!")


photos = []

def take_photo():
    """Take a photo on the camera, storing its name."""
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

    print(f"Camera: taken photo '{file_path.name}'")
    photos.append(file_path)

def turn_by(angle: int):
    """Turn the turntable by an angle."""
    pass # TODO: communicate with Arduino


angle = int(360 / arguments.count)

for i in range(arguments.count):
    take_photo()

    if i != arguments.count - 1:
        turn_by(angle)


directory = datetime.now().strftime('%s')
os.mkdir(directory)

# copy files over
for photo in photos:
    target = os.path.join(directory, photo.name)
    camera_file = camera.file_get(photo.folder, photo.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)

for file in glob(os.path.join(directory, "*")):
    Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()

camera.exit()

