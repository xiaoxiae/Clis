"""A script for creating photos automatically using a camera and optionally a turntable."""
from datetime import datetime
from time import sleep
from glob import glob
from subprocess import Popen, DEVNULL
import os
import gphoto2 as gp
import argparse
import serial


os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(
    description="A script for creating photos automatically using a camera and optionally a turntable."
)

subparsers = parser.add_subparsers(help="scanning mode", dest="mode", required=True)

auto_parser = subparsers.add_parser("automatic", help="automatic mode")

auto_parser.add_argument(
    "count",
    type=int,
    help="How many images to take.",
)

auto_parser.add_argument(
    "--arduino-device",
    metavar="PATH",
    help="The Arduino device path (defaults to /dev/ttyACM0).",
    default="/dev/ttyACM0",
)

manual_parser = subparsers.add_parser("manual", help="manual mode")

parser.add_argument(
    "-o",
    "--output",
    help="The output directory. Defaults to 'scans/'.",
    default="scans",
)


arguments = parser.parse_args()

camera = gp.Camera()


def connect_to_camera():
    global camera

    print("Camera: \tconnecting to the camera...", end="", flush=True)
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


connect_to_camera()

if arguments.mode == "automatic":
    try:
        print("Arduino: \testablishing serial connection...", end="", flush=True)
        ser = serial.Serial(
            arguments.arduino_device,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
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
            print(
                " failed with exit code 13, make sure the device (likely /dev/ttyACM0) is readable and writable."
            )
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
directory = os.path.join(
    arguments.output, f"{datetime.now().strftime('%s')}-{arguments.count}"
)
os.mkdir(directory)

angle = int(360 / arguments.count)

for i in range(arguments.count):
    try:
        photo = take_photo()

        target = os.path.join(directory, photo.name)

        camera_file = camera.file_get(photo.folder, photo.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)

        if i != arguments.count - 1 and arguments.mode == "automatic":
            turn_by(angle)
    except gp.GPhoto2Error:
        print(f" failed! Retry? (y/n): ", flush=True, end="")

        answer = input().strip().lower()

        if answer == "y":
            connect_to_camera()
        else:
            quit()
    except KeyboardInterrupt:
        print("interrupted by the user, quitting.", flush=True)
        quit()


# for file in glob(os.path.join(directory, "*")):
#    print(
#        f"Darktable: \tconverting photo {os.path.basename(file)}...", end="", flush=True
#    )
#    Popen(
#        ["darktable-cli", file, os.path.join(os.path.dirname(file), ".")],
#        stdin=DEVNULL,
#        stdout=DEVNULL,
#        stderr=DEVNULL,
#    ).communicate()
#    print(f" done.", flush=True)

camera.exit()
