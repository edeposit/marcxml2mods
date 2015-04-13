#! /usr/bin/env sh
PYTHONPATH="src:$PYTHONPATH"

py.test tests $@