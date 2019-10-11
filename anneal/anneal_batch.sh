#!/bin/bash

# Objective: Submit a batch of annealing jobs
# Before executing this script
# You should create a directotry named "input"
# and put all the files needed into this folder


# force field
ff=lopls2015

# loop through a list of temperatures [K]
TList="258 273"
# TList="273 298 313 343 373"
for T in $TList; do
    mkdir $T
    cp input/*.* $T
    cd $T
    echo ------------------------------------------------
    echo "run job: T = $T [K]"
    sbatch sb_anneal.sh $ff $T
    cd ../
done
echo ------------------------------------------------
