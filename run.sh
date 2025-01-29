#!/bin/bash -e

cd `dirname $0`

input_path=$1

source ./venv/bin/activate

pip freeze

python3 ./launch.py $input_path

deactivate
