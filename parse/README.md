# `parse/`
This directory contains various scripts for parsing the hold photos.

## `parse.py`
The main script -- splits and parses the photos into usable datasets.

## `move.py <input folder> <output folder>`
Moves the photos from the specified folder to the output folder.

## `split.py <input folder>`
Splits the hold photos into separate folders. The splits are performed automatically when a dark photo is spotted, which is then used as a mask for that directory (and named as such).

## `clean.py <input file> <mask file> <output file>`
Cleans hot pixels from a photo using a mask (a black photo containing only the hot pixels, taken by covering the lens).
