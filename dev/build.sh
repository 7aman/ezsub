#!/usr/bin/env bash
# -*- coding: utf-8 -*-

echo ""
echo "----- build: start"
echo "Clean dist and build directories..."
rm -rd build dist 2> /dev/null
python3 setup.py sdist bdist_wheel
echo "----- build: done"
echo ""
exit 0
