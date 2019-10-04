#!/bin/bash

#SBATCH --nodes=1

##SBATCH --constraint=broadwell
##SBATCH --ntasks-per-node=36

##SBATCH --constraint=rack-Z12,broadwell
##SBATCH --ntasks-per-node=36

#SBATCH -p ref_flam
#SBATCH --ntasks-per-node=24

#SBATCH -t 30-00:00
#SBATCH -J anneal
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=lingnan.lin@nist.gov


export OMP_NUM_THREADS=1

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

mpirun -np $SLURM_NTASKS --mca btl tcp,vader,self /share/sw/lammps/5Jun19/bin/lmp -pk omp $OMP_NUM_THREADS -sf omp -var ff $1 -var T0 $2 -in anneal.in
