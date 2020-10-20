#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

cd $BASEDIR
cd ../..

echo $(pwd)
conda activate ebol20

while true; do

python -u ./elec_bol20/nb_2020/z050_plot_contados.py

git add \
elec_bol20/datos_1_intermedios/2020/comp/*.csv \
elec_bol20/datos_0_crudos/2020/comp/*.xlsx \
docs/Ejemplos/z050_panel.html \

git commit -m "auto" \
elec_bol20/datos_1_intermedios/2020/comp/*.csv \
elec_bol20/datos_0_crudos/2020/comp/*.xlsx \
docs/Ejemplos/z050_panel.html \

git pull --no-edit
git push origin master


sleep 600

done