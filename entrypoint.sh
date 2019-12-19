#!/bin/bash

# Get parameters from Github Actions workflow
ENVIRONMENT_SELECTED=${1}
TEMPLATE_ROOT=$(echo "${GITHUB_WORKSPACE}/${2}" | tr -s /)
CONFIG_ROOT=$(echo "${GITHUB_WORKSPACE}/${3}" | tr -s /)
OUTPUT_PATH=$(echo "${GITHUB_WORKSPACE}/${4}" | tr -s /)
OUTPUT_FILENAME_PREFIX=${5}
OUTPUT_FILENAME_SUFFIX=${6}

# Validate all paths specified can be found
if [[ ! -d "${TEMPLATE_ROOT}" ]]; then
    echo "ERROR: The template path specified (${TEMPLATE_ROOT}) could not be found"
    exit 1;
fi
if [[ ! -d "${CONFIG_ROOT}" ]]; then
    echo "ERROR: The config path specified (${CONFIG_ROOT}) could not be found"
    exit 2;
fi
if [[ ! -d "${OUTPUT_PATH}" ]]; then
    echo "WARNING: Output path did not exist, creating..."
    echo "Creating path: ${OUTPUT_PATH}"
    mkdir -p ${OUTPUT_PATH};
fi

# Install Python requirements
pip install -r /opt/template/requirements.txt

if [[ "${ENVIRONMENT_SELECTED}" != "*" ]] && [[ ! -z "${ENVIRONMENT_SELECTED}" ]]; then
  echo "Building ${ENVIRONMENT_SELECTED}..."
  echo "Output Path: ${OUTPUT_PATH}"
  python /opt/template/template.py \
    "${ENVIRONMENT_SELECTED}" \
    "${TEMPLATE_ROOT}" \
    "${CONFIG_ROOT}" \
    "${OUTPUT_PATH}" \
    "${OUTPUT_FILENAME_PREFIX}" \
    "${OUTPUT_FILENAME_SUFFIX}"

else
  echo "Building All Environments..."
  echo "Output Path: ${OUTPUT_PATH}"
  for ENVIRONMENT_CURRENT in ${CONFIG_ROOT}/* ; do
      if [[ -d "${ENVIRONMENT_CURRENT}" ]]; then
          echo ${ENVIRONMENT_CURRENT}
          ENVIRONMENT_SELECTED=$(basename ${ENVIRONMENT_CURRENT})
          python /opt/template/template.py \
            "${ENVIRONMENT_SELECTED}" \
            "${TEMPLATE_ROOT}" \
            "${CONFIG_ROOT}" \
            "${OUTPUT_PATH}" \
            "${OUTPUT_FILENAME_PREFIX}" \
            "${OUTPUT_FILENAME_SUFFIX}"
      fi
  done

fi
