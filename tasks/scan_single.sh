#!/usr/bin/sh
cd "$(dirname "$(realpath $0)")"
pyenv exec python "../01-scanning/01-scan.py" -n 1 automatic 12
