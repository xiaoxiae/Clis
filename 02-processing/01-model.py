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


for image_folder in glob(os.path.join(SCAN_PATH, "*")):
    output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

    if os.path.exists(output_folder):
        printer.full(f"{image_folder} not generated, folder already exists.")
        continue

    printer.full(f"generating {image_folder}:")

    photos = glob(os.path.join(image_folder, "*"))

    # manually create the tempfile name, since we have to feed it to metashape
    tmp_file_name = os.path.join(
        tempfile._get_default_tempdir(),
        next(tempfile._get_candidate_names())
    )

    doc = Metashape.Document()
    doc.save(tmp_file_name)

    chunk = doc.addChunk()
    chunk.addPhotos(photos)
    doc.save()

    printer.full(f"{str(len(chunk.cameras))} images loaded.")

    printer.begin("matching photos")
    # TODO: what do these parameters do?
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

    # TODO: warn when not all cameras are aligned
    # TODO: create a log file to models/ folder

    printer.begin("configuring markers: detecting")
    chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=50)
    doc.save()

    printer.mid("setting positions")
    for m in MARKERS:
        try:
            chunk.findMarker(m).location = Metashape.Vector(MARKERS[m])
        except:
            pass # TODO cry when a marker is not found

    chunk.updateTransform()
    printer.end("done.")

    printer.begin("building depth maps")
    # TODO: what do these parameters do?
    chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
    doc.save()
    printer.end("done.")

    printer.begin("building model")
    chunk.buildModel(source_data=Metashape.DepthMapsData)
    doc.save()
    printer.end("done.")

    printer.begin("removing floor")
    # TODO: use some tool to edit obj
    # TODO: Popen the Blender script, since it gives exceptions
    printer.mid("importing back")
    # TODO: import back
    printer.end("done.")

    printer.begin("mapping texture")
    chunk.buildTexture(texture_size=4096, ghosting_filter=True)
    doc.save()
    printer.end("done.")

    printer.begin("exporting")
    chunk.exportReport(os.path.join(output_folder, "report.pdf"))

    chunk.exportModel(os.path.join(output_folder, "model.obj"))
    printer.end("done.")
