#!/usr/bin/sh
cd "$(dirname "$(realpath $0)")"
pyenv exec python "../01-scanning/02-copy.py" camera
