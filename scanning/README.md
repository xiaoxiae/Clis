# Scanning

## `scan.py`
A script that takes the specified number of photos of the given hold. It expect to be connected to the turntable's Arduino (as described in the `turntable` directory), and a camera that is supported by [gphoto2](http://gphoto.org/) (see [supported cameras](http://gphoto.org/proj/libgphoto2/support.php)).

It requires:
- Python package `gphoto2` for camera control and
- Python package `pyserial` for turntable control.

## `scan-manual.py`
Same as `scan.py`, but doesn't expect an argument, nor an Arduino turntable. The photos are manually taken when enter is pressed and stopped when interrupted by the user.

## `convert.py`
Converts the RAW hold photos to JPEGs. Uses [Darktable](https://www.darktable.org/) to do so.

## `turntable/`
A folder containing the source code/documentation for the custom turntable used for turning the holds.

## `background/`
A folder containing scripts for generating hold backgrounds (the surface the holds are place on).

To scale the appropriate file for printing, `pdfjam` can be used:

```
pdfjam --no-tidy --paper a4 -- <file_name>
```

## `TUTORIAL.md`
Contais my notes about the setup that I used for scanning (lighting, background, number of photos, camera, etc.).
