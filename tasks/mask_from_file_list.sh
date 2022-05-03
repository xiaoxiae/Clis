#!/usr/bin/sh
for line in `cat $1`
do
    pyenv exec python "../01-scanning/04-mask.py" $line
done
