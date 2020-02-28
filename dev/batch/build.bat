@echo off
echo ""
echo "----- build: start"
echo "Clean dist and build directories..."
DEL /Q /S /F build dist
python setup.py sdist bdist_wheel
echo "----- build: done"
echo ""
exit
