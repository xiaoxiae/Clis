import os
import sys
from glob import glob
from subprocess import Popen, PIPE, DEVNULL

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("model", silence_others=True)

cwd = os.path.dirname(os.path.abspath(__file__))

os.chdir(METASHAPE_KEY_DIRECTORY_PATH)
import Metashape

os.chdir(cwd)


def append_log_file(output_folder):
    """Open the model's log file in append mode."""
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    return open(os.path.join(output_folder, "model.log"), "a")


for image_folder in glob(os.path.join(SCAN_PATH, "*")):
    try:
        output_folder = os.path.join(MODEL_PATH, os.path.basename(image_folder))

        if os.path.exists(output_folder):
            printer.full(f"{output_folder} not generated, folder already exists.")
            continue

        printer.full(f"generating {image_folder}:")

        photos = glob(os.path.join(image_folder, "*"))

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

        for m in MARKERS:
            m_str = f"target {m}"

            if m_str not in markers:
                with append_log_file(output_folder) as f:
                    f.write(f"Non-existent marker '{m_str}' found.")

            markers[m_str].reference.location = Metashape.Vector(MARKERS[m])
            del markers[m_str]

        if len(markers) != 0:
            with append_log_file(output_folder) as f:
                f.write(f"Markers {markers.keys()} not found, terminating.")
            break

        chunk.updateTransform()
        printer.end("done.")

        printer.begin("matching photos")
        chunk.matchPhotos(
            keypoint_limit=40000,
            tiepoint_limit=10000,
            generic_preselection=True,
            reference_preselection=True,
        )
        printer.end(f"done.")

        printer.begin("aligning cameras")
        chunk.alignCameras()
        printer.end("done.")

        # check if all cameras are aligned (and possibly warn)
        aligned_cameras = [c for c in chunk.cameras if c.transform]
        if len(aligned_cameras) != 0:
            with append_log_file(output_folder) as f:
                f.write(f"Not all cameras aligned ({len(aligned_cameras)}/{len(photos)}): {[c for c in chunk.cameras if not c.transform]}")

        printer.begin("building depth maps")
        chunk.buildDepthMaps(downscale=2, filter_mode=Metashape.MildFiltering)
        printer.end("done.")

        printer.begin("building model")
        chunk.buildModel(source_data=Metashape.DepthMapsData)
        printer.end("done.")

        model_original_path = os.path.join(output_folder, f"{MODEL_FILE_NAME}_original.obj")
        model_modified_path = os.path.join(output_folder, f"{MODEL_FILE_NAME}.obj")

        printer.begin("exporting original model")
        chunk.exportModel(model_original_path)
        printer.end("done.")

        printer.begin("removing floor and simplifying")
        Popen(["python", "02-remove-ground.py", model_original_path, model_modified_path]).communicate()
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
    except Exception as e:
        printer.full("an exception occurred while generating the model, writing to log.")
        with append_log_file(output_folder) as f:
            f.write(str(e))
