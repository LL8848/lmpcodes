#!/bin/bash

# Objective: Submit a batch of NEMD jobs
# Before executing this script
# You should create a directotry named "input"
# and put all the files needed into this folder


# set temperature [K]
T=298
# force field
ff=opls2015

# loop through a list of shear rates [1/fs]
shearList="10e-7"
# shearList="2e-7 3e-7 4e-7 5e-7 6e-7 7e-7 8e-7 9e-7"
for srate in $shearList; do
    mkdir ${srate}_2
    cp r.input/*.* ${srate}_2
    # find the newer restart file (A or B ?)
    if [ ${srate}/*.restart.A -nt ${srate}/*.restart.B ]
    then
        r=A
    else
        r=B
    fi
    # copy restart file
    cp -f ${srate}/${T}K.restart.${r} ${srate}_2
    # copy .settings file
    cp ${srate}/*.*.settings ${srate}_2
    cd ${srate}_2
    echo ------------------------------------------------
    echo "run restart job: shear rate = ${srate}_2 [1/fs]"
    sbatch r.sb_nemd.sh $T $srate $ff ${T}K.restart.${r}
    cd ../
done
echo ------------------------------------------------
