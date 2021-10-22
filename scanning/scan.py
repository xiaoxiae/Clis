d = """A script for creating photos using the automatic camera + Arduino setup."""

import serial
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


try:
    print('Arduino: \testablishing serial connection...', end="", flush=True)
    ser = serial.Serial(arguments.arduino_device,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )

    if not ser.isOpen():
        ser.open()

    # give Arduino some time
    # important, *don't change this*
    sleep(2)

    print(" established.")
except serial.serialutil.SerialException as e:
    # TODO: this is probably not a good way
    if "Errno 13" in str(e):
        print(" failed with exit code 13, make sure the device is readable and writable.")
        quit()


def take_photo():
    """Take a photo on the camera, returning its object."""
    print(f"Camera: \ttaking photo...", end="", flush=True)
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    print(f" '{file_path.name}' taken.", flush=True)

    return file_path

def turn_by(angle: int):
    """Turn the turntable by an angle."""
    print(f"Arduino: \tturning...", end="", flush=True)

    ser.flushInput()
    ser.flushOutput()

    ser.write(str(angle).encode())

    while True:
        data = ser.readline().decode().strip()

        if data == str(angle):
            print(f" turned by {angle} degrees.", flush=True)
            break
        else:
            print(f" Arduino returned '{data}', exitting.")
            quit()


# rotate and save the pictures at the same time
directory = os.path.join(arguments.output, f"{datetime.now().strftime('%s')}-{arguments.count}")
os.mkdir(directory)

angle = int(360 / arguments.count)

for i in range(arguments.count):
    photo = take_photo()
    target = os.path.join(directory, photo.name)

    camera_file = camera.file_get(photo.folder, photo.name, gp.GP_FILE_TYPE_NORMAL)
    camera_file.save(target)

    if i != arguments.count - 1:
        turn_by(angle)


for file in glob(os.path.join(directory, "*")):
    print(f"Darktable: \tconverting photo {os.path.basename(file)}...", end="", flush=True)
    Popen(["darktable-cli", file, os.path.join(os.path.dirname(file), ".")], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL).communicate()
    print(f" done.", flush=True)

camera.exit()
