#!/usr/bin/sh
pyenv exec python "$(dirname "$(realpath $0)")/../01-scanning/02-copy.py" path $1
