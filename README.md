<p align="center" width="100%">
<img width="50%" src="https://raw.githubusercontent.com/Climber-Apps/Clis/master/logo.svg">
</p>

<p align="center" width="100%">
The <strong>cli</strong>mber's <strong>s</strong>canner – efficient 3D scanning of climbing holds and climbing gym interiors.
</p>

## Setting up
For the setup, you'll need to first install `pyenv`:

```
curl https://pyenv.run | bash
```

and configure your shell's environment: https://github.com/pyenv/pyenv#basic-github-checkout

You'll then need to install Python `3.7.x` (due to Metashape and Blender working only with older Python versions):

```
pyenv install -v 3.7.12
```

To set up the virtual environment, do (in this directory)

```
pyenv virtualenv 3.7.12 clis
pyenv local clis
pyenv activate clis
pyenv exec pip install -r requirements.txt
pyenv exec bpy_post_install
```

## Usage
To activate the environment, use `pyenv activate clis`. Before running each script (using `pyenv exec`), it is advisable to check `config.py`, since a lot of the values will likely differ from their default values. Each of the respective folders contain a `README.md` that further explains the usage of each of the scripts.

### `01-scanning/`
Contains tools for scanning the holds.

### `02-processing/`
Contains tools for processing the hold images into 3D models.

### `03-data/`
Contains the hold data format specification and the scans of the holds and the wall themselves.
