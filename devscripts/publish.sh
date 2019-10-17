#!/usr/bin/env bash
# -*- coding: utf-8 -*-

version=`ls dist/*.tar.gz | cut -d"-" -f2 | cut -d"." -f1,2,3`
run_zsub="yes"


if [[ $1 = "final" ]];
then

    echo ""
    echo "----- final publish: start"
    echo "You are going to publish ezsub version '$version'."
    read -p "continue? y/[n]: " -r
    if [[ $REPLY =~ ^[Yy]$ ]];
    then
        echo ""
        python3 -m twine upload dist/*
    else
        echo "skipped."
        echo "----- final publish: done"
        echo ""
        exit 0
    fi

else

    echo ""
    echo "----- test publish: start"
    echo "You are going to publish ezsub version '$version' to test repository."
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    echo "----- test publish: done"
    echo ""

fi

echo ""
read -p "Do you want install uploaded version? y/[n]: " -r
if [[ $REPLY =~ ^[Yy]$ ]];
then
    cd ~ > /dev/null
    python3 -m pip uninstall ezsub -y
    if [[ $1 = "final" ]];
    then
        python3 -m pip install --user --upgrade ezsub==$version
    else
        python3 -m pip install --user --index-url https://test.pypi.org/simple/ ezsub==$version
    fi
    cd - > /dev/null
else
    echo ""
    exit 0
fi

echo ""
read -p "Do you want to run new version? y/[n]: " -r
if [[ $REPLY =~ ^[Yy]$ ]];
then
    echo ""
    echo "----- run ezsub: start"
    ezsub
    echo "----- run ezsub: done"
    echo ""
else
    echo ""
    exit 0
fi

exit 0
