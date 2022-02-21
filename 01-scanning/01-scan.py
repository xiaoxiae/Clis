d = """A script for creating photos automatically using a camera and optionally a turntable."""

from datetime import datetime
from time import sleep
import os
import gphoto2 as gp
import argparse
import serial

from config import *


os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

save_path = os.path.join(CAMERA_SAVE_PATH, IMAGE_SAVE_PATH.lstrip("/"))

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
    help=f"The Arduino device path (defaults to {ARDUINO_PATH}).",
    default=ARDUINO_PATH,
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
    """Connect to the camera."""
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

def set_camera_config(key, value):
    config = camera.get_config()
    focus = config.get_child_by_name(key)
    focus.set_value(value)
    camera.set_config(config)

def focus():
    """Focus the camera."""
    # thanks https://www.cmcguinness.com/2015/11/using-python-and-gphoto2-to-control-the-focus-of-a-canon-t3i-eos-600d/
    set_camera_config('autofocusdrive', 1)

def set_save_to_card():
    """Set saving of the pictures to the SD card."""
    set_camera_config('capturetarget', '1')

def take_photo():
    """Take a photo on the camera, returning its object."""
    print(f"Camera: \tfocusing...", end="", flush=True)
    print(f" taking photo...", end="", flush=True)
    print(f" image taken.", flush=True)


connect_to_camera()
set_save_to_card()

automatic = arguments.mode == "automatic"

if automatic:
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
                f" failed with exit code 13, make sure the device ({ARDUINO_PATH}) is readable and writable."
            )
            quit()


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


if automatic:
    angle = int(360 / arguments.count)
else:
    # a bit of a hack to take a lot of pictures manually
    arguments.count = 999

# the photos before the start of the shooting
initial_photos = list(camera.folder_list_files(save_path))

for i in range(arguments.count):
    print("Camera: \ttaking a photo: focusing... ", end="", flush=True)
    try:
        while True:
            try:
                focus()
                break
            except gp.GPhoto2Error:
                print("unable to focus, retrying... ", end="", flush=True)
    except KeyboardInterrupt:
        print("\nCamera: \tInterrupted by the user, taking no more pictures.", flush=True)
        break

    try:
        print("capturing... ", end="", flush=True)
        camera.trigger_capture()
        print("done.", flush=True)

        # don't move on the very last photo (or if we're not in automatic)
        if automatic:
            if i != arguments.count - 1:
                turn_by(angle)
        else:
            print("Camera: \tPress enter when the hold has been turned.", end="")
            input()
    except gp.GPhoto2Error as e:
        print(f" camera error! Attempt to reconnect? (y/n): ", flush=True, end="")

        answer = input().strip().lower()

        if answer == "y":
            connect_to_camera()
        else:
            break
    except KeyboardInterrupt:
        print("\nCamera: \tInterrupted by the user, taking no more pictures.", flush=True)
        break

camera.exit()

sleep(2)

# the photos after the shooting
current_photos = list(camera.folder_list_files(save_path))

count = len(current_photos) - len(initial_photos)

# don't create any folders or files if no photos were taken
if count == 0:
    quit()

directory = os.path.join(arguments.output, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} - {count}")
os.mkdir(directory)

# save the names of the shot photos to download them later
with open(os.path.join(directory, "images.txt"), "w") as file:
    for f in current_photos:
        if f not in initial_photos:
            name, _ = f

            file.write(f"{name}\n")
