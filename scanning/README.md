# Scanning

## `scan.py`
A script that takes the specified number of photos of the given hold. It expect to be connected to the turntable's Arduino (as described in the `turntable` directory), and a camera that is supported by [gphoto2](http://gphoto.org/) (see [supported cameras](http://gphoto.org/proj/libgphoto2/support.php)).

It requires:
- Python package `gphoto2` for camera control,
- Python package `pyserial` for turntable control and
- [Darktable](https://www.darktable.org/) for converting the RAW images into usable JPEGs.

## `turntable/`
A folder containing the documentation for the custom turntable used for turning the holds.
