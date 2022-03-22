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

sd_parser = subparsers.add_parser("path", help="from path")
sd_parser.add_argument("path", help="the path")

arguments = parser.parse_args()

# TODO: this code is not too nice
if arguments.mode == "camera":
    camera = initialize_camera()

    try:
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
    except Exception as e:
        printer.full(f"A fatal error occurred while copying the files: {e}")
else:
    try:
        for folder in glob("*"):
            for file in [f for f in glob(os.path.join(folder, "**", "images.txt"))]:
                dest_folder = os.path.dirname(file)

                printer.full(f"copying images from '{file}':")
                with open(file) as f:
                    photos = f.read().splitlines()
                    for photo in photos:
                        photo_src = os.path.join(
                            arguments.path, CAMERA_IMAGE_PATH.lstrip("/"), photo
                        )
                        photo_dest = os.path.join(dest_folder, photo)

                        printer.begin(f"copying '{photo}'")
                        shutil.copyfile(photo_src, photo_dest)
                        printer.end("copied.")
    except Exception as e:
        printer.full(f"A fatal error occurred while copying the files: {e}")
