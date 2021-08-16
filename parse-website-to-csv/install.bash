#!/bin/bash	

BASEDIR=$(dirname $0)

source "${BASEDIR}/bin/activate"
echo "${BASEDIR}/bin/activate"
pip install -r requirements.txt

$SHELL
