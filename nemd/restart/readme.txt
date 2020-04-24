Procedure to restart a NEMD job in ref_flam partition:

1. create a folder named "r.input".

2. copy the "pec5.lopls2015.settings", "r.sb_nemd.sh", and "r.nemd.in" to the folder.

3. You're recommended to use the original "nemd.in" by renaming it with "r.nemd.in" and making the following changes:
change "read_restart pec5_125.equi${T}K" to "read_restart    ${res}" 
comment out the line "reset_timestep	0"
change "run 100000000" to "run 100000000 upto"
(may be OK to copy the backup r.nemd.in file to it)

4. Generally "r.sb_nemd.sh" doesn't need modification

5. copy the "r.nemd_batch.sh" to the upper directory, change the tempearture and srate if to desired conditions

6. run the jobs with the command "sh r.nemd_batch.sh"


Debug:
1. ERROR: Triclinic box skew is too large (src/domain.cpp:193)
Solution: see which restart file was used *.restart.B or *.restart.A.  Copy the other file to the folder and manually submit the sbatch job. Use command like "sbatch r.sb_nemd.sh 340 3e-6 lopls2015 340K.restart.B"  

2. "Warning: Inconsistent image flags"    can be ignored.

