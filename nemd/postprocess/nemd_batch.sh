#!/bin/bash

# Objective: Submit a batch of NEMD jobs
# Before executing this script
# You should create a directotry named "input"
# and put all the files needed into this folder


# set temperature [K]
T=$1

# set density [g/cm3]. use average of EMD simulations.
rho=$2

# loop through a list of shear rates [1/fs]
shearList="2e-7"
# shearList="3e-7 4e-7 5e-7 6e-7 7e-7 8e-7 9e-7 10e-7"
for srate in $shearList; do
    mkdir $srate
    cp input/*.* $srate
    cd $srate
    echo ------------------------------------------------
    echo "run job: shear rate = $srate [1/fs]"
    sbatch sb_nemd.sh $T $rho $srate
    cd ../
done
echo ------------------------------------------------