import os
import sys
import argparse

sys.path.append("..")
from config import *
from utilities import *

printer = Printer("retexture", silence_others=True)

cwd = os.path.dirname(os.path.abspath(__file__))

os.chdir(METASHAPE_KEY_DIRECTORY_PATH)
import Metashape

os.chdir(cwd)

parser = argparse.ArgumentParser()

parser.add_argument("model", help="The model to retexture.")
parser.add_argument("project", help="The Metashape project file to use to retexture.")

arguments = parser.parse_args()


try:
    doc = Metashape.Document()
    doc.open(arguments.project)

    # get the (only) active chunk
    chunk = doc.chunk

    printer.begin("importing the model")
    chunk.importModel(arguments.model)
    printer.end("done.")

    printer.begin("mapping texture")
    chunk.buildUV(mapping_mode=Metashape.GenericMapping)
    chunk.buildTexture(texture_size=TEXTURE_RESOLUTION, ghosting_filter=True)
    printer.end("done.")

    printer.begin("exporting final model and report")
    chunk.exportModel(model_modified_path)
    chunk.exportReport(os.path.join(output_folder, "report-retextured.pdf"))
    printer.end("done.")
except Exception as e:
    printer.full("an exception occurred while generating the model, writing to log.")
    with append_log_file(output_folder) as f:
        f.write(str(e))
