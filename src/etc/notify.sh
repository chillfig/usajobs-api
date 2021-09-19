#!/usr/bin/env bash

cd "${0%/*}"
source ../../usajobs-venv/bin/activate
python notify.py
deactivate