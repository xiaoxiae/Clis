# Processing

## `01-model.py`
A script that converts sets of photos to models using [Agisoft Metashape Pro](https://www.agisoft.com/).
Only converts sets that don't yet have corresponding model folder.

## `02-clean.py`
A script that takes the model produced by Metashape and outputs the same model with the ground removed and simplified to a reasonable size.
It is _not meant to be called alone_ and is instead used in `01-model.py`.

## `03-retexture.py`
A script that takes the model and retextures it by reimporting it back to Metashape.
