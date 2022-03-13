# NOTE: all relative paths are to the directory of the script being called

# where the images are stored on the camera
# see `gphoto2 --list-files` for both
CAMERA_ROOT_PATH = "/store_00010001"
CAMERA_IMAGE_PATH = "/DCIM/102NZ_50"

camera_path = CAMERA_ROOT_PATH + CAMERA_IMAGE_PATH

# path to Arduino's serial port
ARDUINO_PATH = "/dev/ttyACM0"

# the extension of the images
IMAGE_EXTENSION = "nef"

# the path to the SD card from which to copy photos
SD_PATH = "/dev/sdc"

# folder where the scans of the holds are saved
SCAN_PATH = "scans"

# folders where the generated models are stored (and what each of their names are)
MODEL_PATH = "models"
MODEL_FILE_NAME = "model"

# the name of the file containing all the hold information
MODEL_YAML_NAME = "holds.yaml"

# the path to the Metashape license file
METASHAPE_KEY_DIRECTORY_PATH = "/home/xiaoxiae/Downloads/metashape-pro"

# a marker id:position dictionary (in meters):
#
#                 z+
#                 |
#                 o-- y+
#                /
#               x+
#
# the origin of the hold should be at (0, 0, 0)
MARKERS = {
    94: (-0.0633, -0.0695, 0),
    91: (0.1087, -0.0695, 0),
    92: (0.0217, 0.0869, 0),
}

# the resolution of the texture file
TEXTURE_RESOLUTION = 1024
