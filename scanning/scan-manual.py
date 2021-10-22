d = """A script for creating photos manually, using just the camera."""

import argparse
import gphoto2 as gp
import os

from subprocess import Popen, DEVNULL
from glob import glob
from time import sleep
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

parser.add_argument("--arduino-device", metavar="PATH", help="The Arduino device path (defaults to /dev/ttyACM0).", default='/dev/ttyACM0')

parser.add_argument("-o", "--output", help="The output directory. Defaults to 'scans/'.", default='scans')

arguments = parser.parse_args()

camera = gp.Camera()

print('Camera: \tconnecting to the camera...', end="", flush=True)
while True:
    try:
        camera.init()
    except gp.GPhoto2Error as ex:
        # this is not too pretty, but works...
        try:
            if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                sleep(2)
                continue
            raise
        except KeyboardInterrupt:
            print(" interrupted by the user, quitting.", flush=True)
            quit()
    break
print(" connected.", flush=True)


def take_photo():
    """Take a photo on the camera, returning its object."""
    print(f"Camera: \ttaking photo...", end="", flush=True)
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print(f" '{file_path.name}' taken.", flush=True)

    return file_path


directory = os.path.join(arguments.output, f"{datetime.now().strftime('%s')}")
os.mkdir(directory)

while True:
    try:
        input(f"Camera: \twaiting for enter press...")

        photo = take_photo()
        target = os.path.join(directory, photo.name)

        camera_file = camera.file_get(photo.folder, photo.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
    except KeyboardInterrupt:
        print()
        break

camera.exit()
