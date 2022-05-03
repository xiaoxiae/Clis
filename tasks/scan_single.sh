#!/usr/bin/sh
pyenv exec python "$(dirname "$(realpath $0)")/../01-scanning/01-scan.py" -n 1 automatic 12
