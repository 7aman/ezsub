@echo off

if "%1" == "final" (
    echo "upload to pypi repository"
    python -m twine upload dist/*

) else (
    echo "upload to test repository"
    python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
)

echo "Done!"
