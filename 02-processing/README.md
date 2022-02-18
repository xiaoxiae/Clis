# Processing

## `model.py`
A script that takes a single argument - the folder containing the folders with the photos of the scanned holds. It then calls `meshroom_batch` from [MeshroomCL](https://github.com/openphotogrammetry/meshroomcl) using the `Meshroom.mg` pipeline on each of the folders, creating their 3D models.

It requires [MeshroomCL](https://github.com/openphotogrammetry/meshroomcl). _Regular [Meshroom](https://github.com/alicevision/meshroom) could also be used, but the pipeline would have to be changed and I can't test this because I don't have a graphics card with Cuda support._

Note that:
- **it takes a LONG time* for each of the holds to be modeled (like an hour or three).
- MeshroomCL works natively under Windows, so you'll need to install it there, and under Wine on Linux
	- for Linux: you'll have to install some OpenCL package for Meshroom to recognize your GPU. Also, the support is pretty bad (out of the box), I would recommend just using Windows
	- for Windows: don't forget to add `meshroom_batch` to the path and install Python 3 to run the script
