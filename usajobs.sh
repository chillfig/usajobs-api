#!/usr/bin/env bash

cd "${0%/*}"
source usajobs-venv/bin/activate
python src/main.py
deactivate