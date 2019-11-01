#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# Install editable mode

cd ~
python3 -m pip uninstall ezsub -y
# in case of both editable and released are installed.
python3 -m pip uninstall ezsub -y
cd -
python3 -m pip install --user --editable .
exit 0
