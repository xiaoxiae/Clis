d = """A script for copying over images from the SD card."""

import argparse
import os
import tempfile
import shutil

from subprocess import Popen, PIPE
from glob import glob

from config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser(description=d)

parser.add_argument("--sd-path", help=f"The path to the SD card. Defaults to '{SD_PATH}'.", default=SD_PATH)

arguments = parser.parse_args()

if not os.geteuid() == 0:
    print("Copy: \tmust be run as root.")
    quit()

mount_folder = tempfile.TemporaryDirectory()

def unmount():
    print(f"Copy: \tunmounting {SD_PATH}...", flush=True, end=" ")
    Popen(["sudo", "umount", mount_folder.name]).communicate()
    print("unmounted.")

try:
    # mount the SD path 
    print(f"Copy: \tmounting {SD_PATH}...", flush=True, end=" ")
    Popen(["sudo", "mount", SD_PATH, mount_folder.name]).communicate()
    print("mounted.")

    for folder in glob("*"):
        for file in [f for f in glob(os.path.join(folder, "**", "images.txt"))]:
            dest_folder = os.path.dirname(file)

            print(f"Copy: \tcopying images from '{file}':")
            with open(file) as f:
                photos = f.read().splitlines()
                for photo in photos:
                    photo_src = os.path.join(mount_folder.name, IMAGE_SAVE_PATH.lstrip("/"), photo)
                    photo_dest = os.path.join(dest_folder, photo)

                    print(f"Copy: \tcopying '{photo}':", flush=True, end="")
                    shutil.copyfile(photo_src, photo_dest)
                    print(" copied.")

            os.remove(file)

    unmount()

    mount_folder.cleanup()

except Exception as e:
    print(f"Copy: \tA fatal error occurred while copying the files: {e}")

    unmount()

username = Popen(["logname"], stdout=PIPE).communicate()[0].decode().strip()

Popen(["sudo", "chown", "-R", f"{username}:{username}", SCAN_PATH]).communicate()
