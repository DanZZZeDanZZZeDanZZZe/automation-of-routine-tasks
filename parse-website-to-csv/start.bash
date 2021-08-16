#!/bin/bash	

BASEDIR=$(dirname $0)

source "${BASEDIR}/bin/activate"
python3 "${BASEDIR}/main.py"

$SHELL