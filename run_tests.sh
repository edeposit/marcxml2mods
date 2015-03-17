#! /usr/bin/env bash

PYTHONPATH="$PYTHONPATH:src"
TEST_PATH="tests"

py.test "$TEST_PATH"