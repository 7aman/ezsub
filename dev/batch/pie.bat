@echo off
python -m pip uninstall ezsub -y
REM "in case of both editable and released are installed"
python -m pip uninstall ezsub -y
python -m pip install --editable .
exit 0
