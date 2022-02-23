<p align="center" width="100%">
<img width="50%" src="https://raw.githubusercontent.com/Climber-Apps/Clis/master/logo.svg">
</p>

<p align="center" width="100%">
The <strong>cli</strong>mber's <strong>s</strong>canner – efficient 3D scanning of climbing holds and climbing gym interiors.
</p>

## Setting up
1. `python3 -m venv venv` (create a virtual environment)
2. `. venv/bin/activate` (activate it)
3. `pip install -r requirements.txt` (install requirements)

## Usage
When using the scripts in each of the respective directories, don't forget to activate the virtual environment using `. venv/bin/activate`. Before running each script, it is advisable to check `config.py`, since a lot of the values will likely differ from their default values.

Each of the respective folders contain a `README.md` that further explains the usage of each of the scripts.

### `01-scanning/`
Contains tools for scanning the holds.

### `02-processing/`
Contains tools for processing the hold images into 3D models.

### `03-data/`
Contains the hold data format specification and the scans of the holds and the wall themselves.
