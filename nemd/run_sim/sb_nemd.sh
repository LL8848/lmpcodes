#!/bin/bash

#SBATCH --nodes=1

##SBATCH --constraint=broadwell
##SBATCH --ntasks-per-node=36

#SBATCH --constraint=rack-Z12,broadwell
#SBATCH --ntasks-per-node=36

##SBATCH --constraint=skylake
##SBATCH --ntasks-per-node=24

#SBATCH -t 30-00:00
#SBATCH -J nemd
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=lingnan.lin@nist.gov

export OMP_NUM_THREADS=2

module purge
module load intel/2017
module load openmpi/4.0.1/intel2017

# set environment for LAMMPS and msi2lmp executables
# to find potential and force field files
source /share/sw/lammps/5Jun19/etc/profile.d/lammps.sh

echo "working directory = "$SLURM_SUBMIT_DIR
echo "SLURM_SUBMIT_HOST = "$SLURM_SUBMIT_HOST
echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURM_NTASKS"=$SLURM_NTASKS

# set temperature [K]
#export T=313
# set density [g/cm3]
#export rho=0.9
# set shear rate [1/fs]
#export srate=2e-7

mpirun -np $SLURM_NTASKS --mca btl '^openib' /share/sw/lammps/5Jun19/bin/lmp -pk omp $OMP_NUM_THREADS -var T $1 -var rho $2 -var srate $3 -in pec6.in
