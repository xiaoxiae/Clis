import os
import sys
import argparse
import shutil

from glob import glob
from subprocess import Popen, PIPE, DEVNULL

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("model", silence_others=True)


cwd = os.path.dirname(os.path.abspath(__file__))

os.chdir(METASHAPE_KEY_DIRECTORY_PATH)

import Metashape

if not Metashape.License().valid:
    printer.full("Metashape license not activated, quitting.")
    quit()

os.chdir(cwd)

parser = argparse.ArgumentParser()

parser.add_argument(
    "-m",
    "--no-markers",
    help="Ignore when not enough markers are found (skipping the clean.py script).",
    action="store_true",
)

parser.add_argument(
    "-c",
    "--cameras",
    help="The Metashape camera position file to use.",
)

parser.add_argument(
    "-f",
    "--force",
    help="Force model generation, even if the folder exists (removing it before).",
    action="store_true",
)

arguments = parser.parse_args()


def append_to_log_file(output_folder, string):
    """Open the model's log file in append mode."""
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    with open(os.path.join(output_folder, "model.log"), "a") as f:
        f.write(string)


for image_folder in sorted(glob(os.path.join(SCAN_PATH, "*"))):
    output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

    if os.path.exists(output_folder):
        if arguments.force:
            printer.full(f"{output_folder} exists, forcing removal.")
            shutil.rmtree(output_folder)
        else:
            printer.full(f"{output_folder} not generated, folder already exists.")
            continue

    printer.full(f"generating {image_folder}:")

    try:
        photos = glob(os.path.join(image_folder, f"*.{CONVERTED_IMAGE_EXTENSION}"))

        if len(photos) == 0:
            printer.full(f"no photos with the {CONVERTED_IMAGE_EXTENSION} extension found, were they converted?")
            continue

        doc = Metashape.Document()
        doc.open("metashape-template/Template.psx")

        # get the (only) active chunk
        chunk = doc.chunk

        chunk.addPhotos(photos)
        printer.full(f"{str(len(chunk.cameras))} images loaded.")

        printer.begin("configuring markers: detecting")
        chunk.detectMarkers(target_type=Metashape.CircularTarget12bit, tolerance=50)

        printer.mid("setting positions")

        markers = {marker.label: marker for marker in chunk.markers}
        found_markers = 0

        for m in sorted(MARKERS):
            m_str = f"target {m}"

            if m_str not in markers:
                append_to_log_file(output_folder, f"Marker '{m_str}' not found in the images, skipping.\n")
            else:
                found_markers += 1
                markers[m_str].reference.location = Metashape.Vector(MARKERS[m])

                del markers[m_str]

        if found_markers < 3:
            if arguments.no_markers:
                append_to_log_file(output_folder, "Less than 3 markers found, generating regardless.\n")
                printer.end(f"less than 3 markers found, generating regardless.")
            else:
                append_to_log_file(output_folder, "Less than 3 markers found, not generating the model.\n")
                printer.end(f"less than 3 markers found, not generating the model.")
            if not arguments.no_markers:
                continue
        else:
            chunk.updateTransform()
            printer.end("done.")

        printer.begin("matching photos")
        chunk.matchPhotos(
            keypoint_limit=40000,
            tiepoint_limit=10000,
            generic_preselection=False,
            reference_preselection=False,
        )
        printer.end(f"done.")

        if arguments.cameras:
            # TODO: this works really poorly
            printer.begin("importing cameras")
            chunk.importCameras(arguments.cameras)
            printer.end(f"done.")

            printer.begin("triangulating points")
            chunk.triangulatePoints()
            printer.end("done.")
        else:
            printer.begin("aligning cameras")
            chunk.alignCameras()
            printer.end("done.")

        # check if all cameras are aligned (and possibly warn)
        aligned_cameras = [c for c in chunk.cameras if c.transform]
        if len(aligned_cameras) - len(photos) != 0:
            append_to_log_file(output_folder, f"Not all cameras aligned ({len(aligned_cameras)}/{len(photos)}): {[c for c in chunk.cameras if not c.transform]}\n")

        printer.begin("building depth maps")
        chunk.buildDepthMaps()
        printer.end("done.")

        printer.begin("building dense cloud")
        chunk.buildDenseCloud()
        printer.end("done.")

        printer.begin("building model")
        chunk.buildModel(source_data=Metashape.DepthMapsData)
        printer.end("done.")

        model_original_path = os.path.join(output_folder, f"{MODEL_FILE_NAME}_original.obj")
        model_modified_path = os.path.join(output_folder, f"{MODEL_FILE_NAME}.obj")

        # if not enough markers are found but we still want to generate the model, don't do cleanup
        if found_markers >= 3:
            printer.begin("exporting original model")
            chunk.exportModel(model_original_path)
            printer.end("done.")

            printer.begin("removing floor and simplifying")
            Popen(["python", "02-clean.py", model_original_path, model_modified_path]).communicate()
            printer.end("done.")

            printer.begin("importing back")
            chunk.importModel(model_modified_path)
            printer.end("done.")

        printer.begin("mapping texture")
        chunk.buildUV(mapping_mode=Metashape.GenericMapping)
        chunk.buildTexture(texture_size=TEXTURE_RESOLUTION, ghosting_filter=True)
        printer.end("done.")

        printer.begin("exporting final model and report")
        chunk.exportModel(model_modified_path)
        chunk.exportReport(os.path.join(output_folder, "report.pdf"))
        printer.end("done.")

        printer.begin("saving Metashape project file")
        doc.save(path=os.path.join(output_folder, "model.psx"))
        printer.end("done.")

        printer.begin("saving configuration")
        shutil.copy(
            os.path.join("..", "config.py"),
            os.path.join(output_folder, "model_config.py"),
        )
        printer.end("done.")
    except KeyboardInterrupt:
        printer.full(f"interrupted by the user, cleaning up.")
        shutil.rmtree(output_folder)
    except Exception as e:
        printer.full(f"an exception occurred while generating the model, writing to log: {e}")
        append_to_log_file(output_folder, str(e))
