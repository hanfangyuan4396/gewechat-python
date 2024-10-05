#!/bin/bash

set -e

rm -rf build dist *.egg-info

pip install setuptools wheel
python setup.py sdist bdist_wheel