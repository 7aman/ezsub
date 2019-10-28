#!/usr/bin/env bash
# -*- coding: utf-8 -*-

cd ~
python3 -m pip uninstall ezsub -y
cd -
python3 -m pip install --user --editable .
exit 0
