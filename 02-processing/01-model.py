d = """A script for converting folders with hold images into 3D models."""

import argparse
import os
import sys
import tempfile
import time
from glob import glob

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("model")

os.chdir(METASHAPE_KEY_DIRECTORY_PATH)
import Metashape

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# TODO masking by color (black background)
# TODO use some automated photo editing software and then tell metashape that it's masked
# TODO maybe gimp? (automatic black background removal)

parser = argparse.ArgumentParser(description=d)

arguments = parser.parse_args()

for image_folder in glob(os.path.join(SCAN_PATH, "*")):
    output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

    if os.path.exists(output_folder):

        printer.full(f"{image_folder} not generated, folder already exists.")
        continue

    printer.full(f"generating {image_folder}:")

    photos = glob(os.path.join(image_folder, "*"))

    tmp_file_name = os.path.join(
        tempfile._get_default_tempdir(), next(tempfile._get_candidate_names())
    )

    doc = Metashape.Document()
    doc.save(tmp_file_name)

    chunk = doc.addChunk()
    chunk.addPhotos(photos)
    doc.save()

    printer.full(f"{str(len(chunk.cameras))} images loaded.")

    printer.begin("matching photos")
    chunk.matchPhotos(
        keypoint_limit=40000,
        tiepoint_limit=10000,
        generic_preselection=True,
        reference_preselection=True,
    )
    doc.save()
    printer.end(f"done.")

    printer.begin("aligning cameras")
    chunk.alignCameras()
    doc.save()
    printer.end("done.")

    # TODO: cry when not enough cameras are aligned
    # TODO: save the name of this file somewhere

    printer.begin("building depth maps")
    chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
    doc.save()
    printer.end("done.")

    printer.begin("building model and textures")
    chunk.buildModel(source_data=Metashape.DepthMapsData)
    doc.save()
    chunk.buildUV(page_count=2, texture_size=4096)
    doc.save()
    chunk.buildTexture(texture_size=4096, ghosting_filter=True)
    doc.save()
    printer.end("done.")

    # TODO scaling to real size by using markers
    # TODO documentation page 12
    # TODO test for checking markers
    # chunk.detectMarkers()
    # doc.save()
    # TODO actually use it to resize

    printer.begin("exporting")
    chunk.exportReport(os.path.join(output_folder, "report.pdf"))

    if chunk.model:
        chunk.exportModel(os.path.join(output_folder, "model.obj"))
        printer.end("done.")
    else:
        printer.end("failed!")

        # TODO: cry
        # TODO: save the name of this file somewhere
