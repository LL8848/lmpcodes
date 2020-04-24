#!/bin/bash

# Objective: Submit a batch of NEMD jobs
# Before executing this script
# You should create a directotry named "input"
# and put all the files needed into this folder


# set temperature [K], pressure [MPa]
T=340
P=50
# force field
ff=lopls2015

# loop through a list of shear rates [1/fs]
shearList="1e9 2e9 3e9 5e9 7e9"
#shearList="2e-7 3e-7 5e-7 7e-7 10e-7 2e-6 3e-6 5e-6 7e-6"

for srate in $shearList; do
    mkdir $srate
    cp input/*.* $srate
    cd $srate
    echo ------------------------------------------------
    echo "run job: shear rate = $srate [1/s]"
    sbatch sb_nemd.sh $T $srate $P
    cd ../
done
echo ------------------------------------------------