#!/bin/bash
declare -a folders=("small_postcard_colls" "RT66" "MonroeSports" "MonroeFantasy" "Monroe" "Lende" "Bossier")

for i in "${folders[@]}"
do
    mv -v --backup=numbered $i/*_cb.tif* cbfiles/
done
