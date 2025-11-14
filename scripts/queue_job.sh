#!/bin/bash

export TARGET_DIR_NAME=$1
export PYTHONUNBUFFERED=1

# Set up unique compile dir for Pytensor to avoid parallelization issues G
RUN_ID=$1
#COMPILE_BASE="${BASE_DIR}/.pytensor_tmp"
#mkdir -p "${COMPILE_BASE}"

#COMPILE_DIR="${COMPILE_BASE}/compiledir_${RUN_ID}"
#export COMPILE_DIR

#If zombie folder exists clean it. G
# if [ -d "${COMPILE_DIR}" ]; then
#    rm -rf "${COMPILE_DIR}"
# fi

# if [ ! -d "${COMPILE_DIR}" ]; then
#     mkdir -p "${COMPILE_DIR}"
#     cp -a ~/.pytensor/compiledir_Linux-5.4--generic-x86_64-with-glibc2.31-x86_64-3.11.9-64/"*" "${COMPILE_DIR}"
# fi


# export PYTENSOR_FLAGS="base_compiledir=${COMPILE_BASE},compiledir_format=compiledir_${RUN_ID}"


# Set up directories for this run
export TARGET_LOG_DIRECTORY="${BASE_DIR}/${LOGS_DIRECTORY}/${TARGET_DIR_NAME}"
export TARGET_RESULTS_DIRECTORY="${BASE_DIR}/${RESULTS_DIRECTORY}/${TARGET_DIR_NAME}"
export TARGET_ERROR_LOG_DIRECTORY="${BASE_DIR}/${ERROR_LOGS_DIRECTORY}/${TARGET_DIR_NAME}"

for dir in "${TARGET_LOG_DIRECTORY}" "${TARGET_RESULTS_DIRECTORY}" "${TARGET_ERROR_LOG_DIRECTORY}"; do
    if ! [ -e "${dir}" ]; then
        mkdir -p "${dir}"
    fi
done

export TARGET_STDOUT_LOG="${TARGET_LOG_DIRECTORY}/${CONSOLE_LOG_NAME}"
export TARGET_STDERR_LOG="${TARGET_LOG_DIRECTORY}/${ERROR_CONSOLE_LOG_NAME}"

case ${NODE_TYPE} in
    "GPU_NEW_ONLY")
        _NODES="--exclude=osm-cpu-[1-6],osm-gpu-[1-2]"
        ;; 
    "GPU_ONLY")
        _NODES="--exclude=osm-cpu-[1-6]"
        ;;
    "CPU_ONLY")
        _NODES="--exclude=osm-gpu-[1-5]"
        ;;
    "ANY")
        _NODES=""
        ;;
    *)
        echo "Error, unknown node type: ${NODE_TYPE}"
        ;;
esac

# Run
srun -n 1 \
  --job-name="${TARGET_DIR_NAME}" \
  --cpus-per-task=${CPUS_PER_RUN} \
  --gpus-per-task=${GPUS_PER_RUN} \
  --mem-per-cpu=${MEMORY_PER_CPU} \
  --time=${MINUTES_PER_RUN} \
  --qos="${QOS}" \
  ${_NODES} \
  --export=ALL,PYTENSOR_FLAGS="${PYTENSOR_FLAGS}" \
  --output="${TARGET_STDOUT_LOG}" \
  --error="${TARGET_STDERR_LOG}" \
  "${BASE_DIR}/${SCRIPTS_DIRECTORY}/dispatch_instance.sh" "$@"

slurm_status_code=$? 

if [ $slurm_status_code -ne 0 ]; then
	cp -a "${TARGET_LOG_DIRECTORY}/." "${TARGET_ERROR_LOG_DIRECTORY}/"
fi

## Clean up compiledir after run G
# COMPILE_DIR="${COMPILE_BASE}/compiledir_${RUN_NAME}"
# if [ -n "${COMPILE_DIR}" ]; then
#     echo "Cleaning up compiledir: ${COMPILE_DIR}"
#     rm -rf "${COMPILE_DIR}"
# fi

exit ${slurm_status_code}
