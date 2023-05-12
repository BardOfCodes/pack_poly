#!/bin/bash

#SBATCH -J polyomino
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=6g
#SBATCH -t 24:00:00
#SBATCH --export=CXX=g++
#SBATCH --array=0-31
#SBATCH -o /users/amaesumi/logs/polyomino%a.out
#SBATCH -e /users/amaesumi/logs/polyomino%a.err

cd /users/amaesumi/pack_poly
module load anaconda/2022.05
module load gcc/10.2
source /gpfs/runtime/opt/anaconda/2020.02/etc/profile.d/conda.sh
conda activate systems

NUM_THREADS=32

python stability.py --stage preproc --nthreads $NUM_THREADS --thread_id $SLURM_ARRAY_TASK_ID
