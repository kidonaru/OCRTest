#!/bin/bash -ex

cd `dirname $0`

skip_key_wait=$1

python3.10 -m venv venv
source ./venv/bin/activate

pip3 install --upgrade -r requirements-osx.txt

pip freeze

if [ "$skip_key_wait" != "true" ]; then
  read -p "All complate!!! plass any key..."
fi

deactivate
