#!/bin/bash

iList="2"
# iList="1 2 3 4 5 6 7 8 9"

for i in $iList; do
    mkdir $i
    cp input/*.* $i
    cd $i
    echo ------------------------------------------------
    echo "run job: # $i"
    sbatch sb_bw_emd.sh
    cd ../
done
echo ------------------------------------------------
