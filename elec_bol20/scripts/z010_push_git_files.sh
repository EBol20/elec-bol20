#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

cd $BASEDIR
cd ../..

echo $(pwd)

while true; do


git add \
elec_bol20/datos_1_intermedios/2020/comp/*.csv \
elec_bol20/datos_0_crudos/2020/comp/*.xlsx

git commit -m "auto" \
elec_bol20/datos_1_intermedios/2020/comp/*.csv \
elec_bol20/datos_0_crudos/2020/comp/*.xlsx

git push origin master


sleep 600

done