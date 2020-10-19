#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

cd $BASEDIR
cd ../..

echo $(pwd)

git add elec_bol20/datos_1_intermedios/2020/comp/*.csv

git commit -m "auto"

git push origin master
