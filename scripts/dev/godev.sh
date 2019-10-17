#!/usr/bin/env bash
# -*- coding: utf-8 -*-

python3 -m pip uninstall ezsub -y
python3 setup.py develop --user
exit 0
