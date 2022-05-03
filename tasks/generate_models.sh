#!/usr/bin/sh
cd "$(dirname "$(realpath $0)")"
pyenv exec python "../02-processing/01-model.py"
