# Scanning

## Scripts
The following describes the order in which the scripts should be called and what they do.

### `01-scan.py`
Scans the hold either automatically using the turntable (in which case it expects to be connected to it), or manually.
It should also be connected to a camera that is supported by [gphoto2](http://gphoto.org/) (see [supported cameras](http://gphoto.org/proj/libgphoto2/support.php)).

### `02-copy.py`
Copies over the images from a local path or the camera itself.
Expects the path to be readable by the user, for or the camera to be connected via USB.

### `03-convert.py`
Converts the RAW hold photos to JPEGs. Uses [Darktable](https://www.darktable.org/) to do so.

## Turntable

### `markers/`
A folder containing

### `turntable/`
A folder containing the source code/documentation for the custom turntable used for turning the holds.

## `tutorials/`
Contais notes about scanning both the holds and the wall.
