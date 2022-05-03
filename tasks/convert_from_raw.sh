#!/usr/bin/sh
cd "$(dirname "$(realpath $0)")"
pyenv exec python "../01-scanning/03-convert.py"
