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

# where the scans of the holds are saved
SCAN_PATH = "scans"

# where the generated models are stored
MODEL_PATH = "models"

# the path to the Metashape license file
METASHAPE_KEY_DIRECTORY_PATH = "/home/xiaoxiae/Downloads/metashape-pro"

# a marker id:position dictionary (in meters):
#
#                 z+
#                 |
#                 *-- y+
#                /
#               x+
#
# note that the origin of the hold should be at (0, 0, 0)
MARKERS = {
    1: (-1, 0, 0),
    2: (1, 0, 0),
    3: (0, 1, 0),
}
