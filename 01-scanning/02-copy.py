import argparse
import os
import shutil
import sys
import tempfile
from glob import glob
from subprocess import PIPE, Popen

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("copy")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help="copy mode", dest="mode", required=True)

camera_parser = subparsers.add_parser("camera", help="from camera")

sd_parser = subparsers.add_parser("card", help="from SD card")

arguments = parser.parse_args()


if arguments.mode == "camera":
    camera = initialize_camera()

    for folder in glob("*"):
        for file in [f for f in glob(os.path.join(folder, "**", "images.txt"))]:
            dest_folder = os.path.dirname(file)

            printer.full(f"copying images from '{file}':")
            with open(file) as f:
                photos = f.read().splitlines()
                for photo in photos:
                    printer.begin(f"copying '{photo}'")

                    gp_file = camera.file_get(
                        camera_path, photo, gp.GP_FILE_TYPE_NORMAL
                    )
                    result_path = os.path.join(dest_folder, photo)
                    gp_file.save(result_path)

                    printer.end("copied.")

            os.remove(file)
else:
    if not os.geteuid() == 0:
        printer.full("must be run as root.")
        quit()

    mount_folder = tempfile.TemporaryDirectory()

    def unmount():
        printer.begin(f"unmounting {SD_PATH}")
        Popen(["sudo", "umount", mount_folder.name]).communicate()
        printer.end("unmounted.")

    try:
        # mount the SD path
        printer.begin(f"mounting {SD_PATH}")
        Popen(["sudo", "mount", SD_PATH, mount_folder.name]).communicate()
        printer.end("mounted.")

        for folder in glob("*"):
            for file in [f for f in glob(os.path.join(folder, "**", "images.txt"))]:
                dest_folder = os.path.dirname(file)

                printer.full(f"copying images from '{file}':")
                with open(file) as f:
                    photos = f.read().splitlines()
                    for photo in photos:
                        photo_src = os.path.join(
                            mount_folder.name, IMAGE_SAVE_PATH.lstrip("/"), photo
                        )
                        photo_dest = os.path.join(dest_folder, photo)

                        printer.begin(f"copying '{photo}'")
                        shutil.copyfile(photo_src, photo_dest)
                        printer.end("copied.")

                os.remove(file)

        unmount()

        mount_folder.cleanup()

    except Exception as e:
        printer.full(f"A fatal error occurred while copying the files: {e}")

        unmount()

    username = Popen(["logname"], stdout=PIPE).communicate()[0].decode().strip()

    Popen(["sudo", "chown", "-R", f"{username}:{username}", SCAN_PATH]).communicate()
