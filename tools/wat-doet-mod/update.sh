#!/bin/bash

[ ! -d env ] && exit 0

source env/bin/activate
python3 collect.py > data.json
git add data.json

