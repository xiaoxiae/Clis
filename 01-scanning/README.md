# Scanning

## Script workflow
The following describes the order in which the scripts should be called and what they do.

### `01-scan.py`
Scans the hold either automatically using the turntable (in which case it expects to be connected to it), or manually. It should also be connected to a camera that is supported by [gphoto2](http://gphoto.org/) (see [supported cameras](http://gphoto.org/proj/libgphoto2/support.php)).

### `02-copy.py`
Copies over the images from the SD card of the camera. Expects the SD card from the camera to be connected to `/dev/sdX` (see `config.py` for the appropriate `X`).

### `03-convert.py`
Recursively converts the RAW hold photos to JPEGs. Uses [Darktable](https://www.darktable.org/) to do so.

## Turntable

### `turntable/`
A folder containing the source code/documentation for the custom turntable used for turning the holds.

### `background/`
A folder containing scripts for generating hold backgrounds (the surface the holds are place on).

To scale the appropriate file for printing, `pdfjam` can be used:

```
pdfjam --no-tidy --paper a4 -- <file_name>
```

## `TUTORIAL.md`
Contais my notes about the setup that I used for scanning (lighting, background, number of photos, camera, etc.).
