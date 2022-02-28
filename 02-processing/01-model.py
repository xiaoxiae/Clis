import argparse
import os
import sys
import tempfile
from glob import glob

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("model", silence_others=True)

cwd = os.path.dirname(os.path.abspath(__file__))

os.chdir(METASHAPE_KEY_DIRECTORY_PATH)
import Metashape

os.chdir(cwd)

# TODO: put the entire thing into try-catch and cry if it doesn't work
for image_folder in glob(os.path.join(SCAN_PATH, "*")):
    output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

    if os.path.exists(output_folder):
        printer.full(f"{image_folder} not generated, folder already exists.")
        continue

    printer.full(f"generating {image_folder}:")

    photos = glob(os.path.join(image_folder, "*"))

    doc = Metashape.Document()
    doc.open("metashape-template/Template.psx")

    # get the (only) active chunk
    chunk = doc.chunk

    chunk.addPhotos(photos)
    printer.full(f"{str(len(chunk.cameras))} images loaded.")

    printer.begin("matching photos")
    # TODO: what do these parameters do?
    chunk.matchPhotos(
        keypoint_limit=40000,
        tiepoint_limit=4000,
        generic_preselection=True,
        reference_preselection=True,
    )
    printer.end(f"done.")

    printer.begin("aligning cameras")
    chunk.alignCameras()
    printer.end("done.")

    # TODO: warn when not all cameras are aligned
    # TODO: create a log file to models/ folder

    printer.begin("configuring markers: detecting")
    chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=50)


    printer.mid("setting positions")

    markers = {marker.label:marker for marker in chunk.markers}

    for m in MARKERS:
        m_str = f"target {m}"

        if m_str not in markers:
            pass # TODO: cry

        markers[m_str].reference.location = Metashape.Vector(MARKERS[m])
        del markers[m_str]

    if len(markers) != 0:
        pass # TODO: cry

    chunk.updateTransform()
    printer.end("done.")

    printer.begin("building depth maps")
    # TODO: what do these parameters do?
    chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
    printer.end("done.")

    printer.begin("building model")
    chunk.buildModel(source_data=Metashape.DepthMapsData)
    printer.end("done.")

    printer.begin("removing floor")
    # TODO: use some tool to edit obj
    # TODO: Popen the Blender script, since it gives exceptions
    printer.mid("importing back")
    # TODO: import back
    printer.end("done.")

    printer.begin("mapping texture")
    chunk.buildUV(mapping_mode=Metashape.GenericMapping)
    chunk.buildTexture(texture_size=4096, ghosting_filter=True)
    printer.end("done.")

    printer.begin("exporting")
    chunk.exportReport(os.path.join(output_folder, "report.pdf"))

    chunk.exportModel(os.path.join(output_folder, "model.obj"))
    printer.end("done.")
