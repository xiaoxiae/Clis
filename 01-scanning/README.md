# Scanning

## Scripts
The following describes the order in which the scripts should be called and what they do.

### `01-scan.py`
Scans the hold either automatically using the turntable (in which case it expects to be connected to it), or manually.
It must be connected to a camera that is supported by [gphoto2](http://gphoto.org/) (see [supported cameras](http://gphoto.org/proj/libgphoto2/support.php)).

### `02-copy.py`
Copies over the images from a local (user-readable) path, or the camera itself (connected via USB).

### `03-convert.py`
Converts the RAW hold photos to an image format (likely JPG) used for creating the models.
Uses [Darktable](https://www.darktable.org/)-CLI to do so.

### `04-mask.py`
Masks the images using the green color of the turntable.
Expects the list of files to do this to as a parameter.
Uses [OpenCV](https://pypi.org/project/opencv-python/) and [pyexiv2](https://github.com/LeoHsiao1/pyexiv2) (for metadata perservation).

## Turntable

### `markers/`
A folder containing a PDF with all 12-bit markers used for the scanning, along with their 3D models.

### `turntable/`
A folder containing the source code/documentation for the custom turntable used for turning the holds.

## `tutorials/`
Contais notes about scanning both the holds and the wall.
