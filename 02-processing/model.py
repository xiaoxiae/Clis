d = """A script for converting folders with hold images into 3D models."""

import os
import argparse
import sys, time
import tempfile
import Metashape
from glob import glob

from config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


parser = argparse.ArgumentParser(description=d)

arguments = parser.parse_args()

for image_folder in glob(os.path.join(SCAN_PATH, "*")):
    print(f"Model: \tgenerating {image_folder}:", flush=True)
    output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

    photos = glob(os.path.join(image_folder, "*"))

    tmp_file_name = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))

    doc = Metashape.Document()
    doc.save(tmp_file_name)

    chunk = doc.addChunk()
    chunk.addPhotos(photos)
    doc.save()

    print(f"Model: \t{str(len(chunk.cameras))} images loaded.", flush=True)

    print(f"Model: \tmatching photos...", flush=True, end="")
    chunk.matchPhotos(keypoint_limit = 40000, tiepoint_limit = 10000, generic_preselection = True, reference_preselection = True)
    doc.save()
    print(f" done.", flush=True)

    print(f"Model: \taligning cameras...", flush=True, end="")
    chunk.alignCameras()
    doc.save()
    print(f" done.", flush=True)

    print(f"Model: \tbuilding depth maps...", flush=True, end="")
    chunk.buildDepthMaps(downscale = 2, filter_mode = Metashape.MildFiltering)
    doc.save()
    print(f" done.", flush=True)

    print(f"Model: \tbuilding model...", flush=True, end="")
    chunk.buildModel(source_data = Metashape.DepthMapsData)
    doc.save()
    print(f" done.", flush=True)

    print(f"Model: \texporting...", flush=True, end="")
    chunk.exportReport(output_folder + '/report.pdf')
    if chunk.model:
        chunk.exportModel(output_folder + '/model.obj')
    print(f" done.", flush=True)
