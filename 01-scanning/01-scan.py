import argparse
import os
import sys
from datetime import datetime
from time import sleep

import serial

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("scan")

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser()

parser.add_argument(
    "-n",
    "--number",
    help="The number of holds to scan; defaults to 1, -1 means infinite.",
    metavar="N",
    default=1,
    type=int,
)

subparsers = parser.add_subparsers(help="scanning mode", dest="mode", required=True)

auto_parser = subparsers.add_parser("automatic", help="automatic mode")

auto_parser.add_argument(
    "count",
    type=int,
    help="How many images of a hold to take.",
)

auto_parser.add_argument(
    "--arduino-device",
    metavar="PATH",
    help=f"The Arduino device path (defaults to {ARDUINO_PATH}).",
    default=ARDUINO_PATH,
)


manual_parser = subparsers.add_parser("manual", help="manual mode")


arguments = parser.parse_args()


def set_camera_config(key, value):
    config = camera.get_config()
    focus = config.get_child_by_name(key)
    focus.set_value(value)
    camera.set_config(config)


def focus():
    """Focus the camera."""
    # thanks https://www.cmcguinness.com/2015/11/using-python-and-gphoto2-to-control-the-focus-of-a-canon-t3i-eos-600d/
    set_camera_config("autofocusdrive", 1)


def set_save_to_card():
    """Set saving of the pictures to the SD card."""
    set_camera_config("capturetarget", "1")


camera = initialize_camera(printer=printer)
set_save_to_card()

automatic = arguments.mode == "automatic"

if automatic:
    try:
        printer.begin("establishing Arduino serial connection")
        ser = serial.Serial(
            arguments.arduino_device,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )

        if not ser.isOpen():
            ser.open()

        # give Arduino some time to connect
        # important, *don't change this*
        sleep(1)

        printer.end("established.")
    except serial.serialutil.SerialException as e:
        # TODO: this is probably not a good way
        if "Errno 13" in str(e):
            printer.end(
                f"failed with exit code 13, make sure the device ({ARDUINO_PATH}) is readable and writable."
            )
            sys.exit(1)


def turn_by(angle: int):
    """Turn the turntable by an angle."""
    printer.begin("turning")

    ser.flushInput()
    ser.flushOutput()

    ser.write(str(angle).encode())

    while True:
        data = ser.readline().decode().strip()

        if data == str(angle):
            printer.end(f"turned by {angle} degrees.")
            break
        else:
            printer.end(f"Arduino returned invalid response '{data}', exitting.")
            sys.exit(1)


if automatic:
    angle = int(360 / arguments.count)
else:
    # a bit of a hack to take a lot of pictures manually
    arguments.count = 999


n = 0
while True:
    # called here to work for 0 photos
    if n == arguments.number:
        break

    if n != 0:
        printer.begin("waiting for enter to scan the next hold")
        try:
            input()
        except KeyboardInterrupt:
            printer.end("scanning no more holds.")
            break

    n += 1

    try:
        # the photos before the start of the shooting
        initial_photos = list(camera.folder_list_files(camera_path))
    except gphoto2.GPhoto2Error:
        printer.full(
            f"the path '{camera_path}' not found on the camera, make sure that it is correct and that the camera is turned on."
        )
        sys.exit(1)


    for i in range(arguments.count):
        printer.begin("taking a photo: focusing")
        try:
            while True:
                try:
                    focus()
                    break
                except gp.GPhoto2Error:
                    printer.mid("unable to focus, retrying")
        except KeyboardInterrupt:
            printer.full("\nInterrupted by the user, taking no more pictures.")
            break

        try:
            printer.mid("capturing")
            camera.trigger_capture()
            printer.end("done.")

            # don't move on the very last photo (or if we're not in automatic)
            if automatic:
                if i != arguments.count - 1:
                    turn_by(angle)
            else:
                printer.full("press enter when the hold has been turned.", end="")
                input()
        except gp.GPhoto2Error as e:
            printer.end("camera error! Attempt to reconnect? (y/n): ", end="")
            answer = input().strip().lower()

            if answer == "y":
                connect_to_camera()
            else:
                break
        except KeyboardInterrupt:
            printer.full("Interrupted by the user, taking no more pictures.")
            break

    camera.exit()

    # important, *don't change this* (otherwise camera.folder_list_files won't work)
    printer.begin("waiting for camera to save changes")
    sleep(1)
    printer.end("done.")

    # the photos after the shooting
    current_photos = list(camera.folder_list_files(camera_path))

    count = len(current_photos) - len(initial_photos)

    # don't create any folders or files if no photos were taken
    if count == 0:
        printer.full("No photos were taken, not saving anything!")
        sys.exit(1)

    directory = os.path.join(SCAN_PATH, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    os.mkdir(directory)

    # save the names of the shot photos to download them later
    with open(os.path.join(directory, "images.txt"), "w") as file:
        for f in sorted(current_photos):
            if f not in initial_photos:
                name, _ = f

                file.write(f"{name}\n")

    printer.full(f"Saved {count} photos.")
