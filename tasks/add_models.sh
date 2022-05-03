#!/usr/bin/sh
cd "$(dirname "$(realpath $0)")"
pyenv exec python "../03-data/01-add-models.py"
