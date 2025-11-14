#!/bin/bash

#SCENARIO=$1
SCENARIO="Runs"

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/georgina.nouli/.mujoco/mujoco210/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/nvidia

# General Job-related configuration
export JOB_NAME="Final ${SCENARIO}"
export JOBLOG_NAME="${SCENARIO}"
export EMAIL="georgina.nouli@tum.de"
# Command to execute. Will be run with arguments from the
# run list file.

export EXECUTABLE="./executable"

# How many CPUs each run requires
export CPUS_PER_RUN=32
export MEMORY_PER_CPU="3G"

# Maximum time limit is 5h
export MINUTES_PER_RUN=5000
# Can be 1 or 0
export GPUS_PER_RUN=1
# Possible choices: urgent > normal
export QOS="normal"
# On which nodes to run, possible values: CPU_ONLY, GPU_ONLY, ANY
export NODE_TYPE="GPU_NEW_ONLY"

# Set up your environment here, e.g., load modules, activate virtual environments
source "miniconda3/etc/profile.d/conda.sh"
module load python/3.10.2
conda activate rlenv

export CPATH=$CONDA_PREFIX/include:$CPATH
export LIBRARY_PATH=$CONDA_PREFIX/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

# Defaults for other run-related variables.
# These can be ignored in most cases
export BASE_DIR=$(pwd)
#RUN_LIST="./args/${SCENARIO}/run_list.csv"
RUN_LIST="./args/run_list.csv"
export RESULTS_DIRECTORY="results"
export LOGS_DIRECTORY="logs"
export ERROR_LOGS_DIRECTORY="error-logs"
export SCRIPTS_DIRECTORY="scripts"
export CONSOLE_LOG_NAME="console.log"
export ERROR_CONSOLE_LOG_NAME="console-error.log"

RUN_LIST_DESCRIPTION="./args/run_list_description.csv"
export RUN_LIST_DESCRIPTION
