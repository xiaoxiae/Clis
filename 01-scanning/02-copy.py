d = """A script for copying over images from the SD card."""

import argparse
import os
import tempfile
import shutil
import gphoto2 as gp

from subprocess import Popen, PIPE
from glob import glob

from config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser(description=d)

save_path = os.path.join(CAMERA_SAVE_PATH, IMAGE_SAVE_PATH.lstrip("/"))

subparsers = parser.add_subparsers(help="copy mode", dest="mode", required=True)

camera_parser = subparsers.add_parser("camera", help="from camera")

sd_parser = subparsers.add_parser("card", help="from SD card")

arguments = parser.parse_args()

camera = gp.Camera()

if arguments.mode == "camera":
    def connect_to_camera():
        """Connect to the camera."""
        print("Copy: \tConnecting to the camera...", end="", flush=True)
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

    for folder in glob("*"):
        for file in [f for f in glob(os.path.join(folder, "**", "images.txt"))]:
            dest_folder = os.path.dirname(file)

            print(f"Copy: \tcopying images from '{file}':")
            with open(file) as f:
                photos = f.read().splitlines()
                for photo in photos:
                    print(f"Copy: \tcopying '{photo}':", flush=True, end="")
                    gp_file = camera.file_get(save_path, photo, gp.GP_FILE_TYPE_NORMAL)
                    result_path = os.path.join(dest_folder, photo)
                    gp_file.save(result_path)
                    print(" copied.")

            os.remove(file)
else:
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
