#!/bin/bash	

BASEDIR=$(dirname $0)

cd ~
cd "${BASEDIR}"
source ./bin/activate
python3 ./main.py

$SHELL
