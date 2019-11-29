#!/usr/bin/env bash

# Get parameters from Github Actions workflow
ENVIRONMENT=$(echo ${1})
TEMPLATE_ROOT=$(echo ${2} | tr -s /)
CONFIG_ROOT=$(echo ${3} | tr -s /)
OUTPUT_PATH=$(echo ${4} | tr -s /)
OUTPUT_FILENAME_PREFIX=${5}
OUTPUT_FILENAME_SUFFIX=${6}

# Validate all paths specified can be found
if [[ ! -d "${TEMPLATE_ROOT}" ]]; then
    echo "ERROR: The template path specified could not be found"
    exit 1;
fi
if [[ ! -d "${CONFIG_ROOT}" ]]; then
    echo "ERROR: The environment path specified could not be found"
    exit 2;
fi
if [[ ! -d "${OUTPUT_PATH}" ]]; then
    echo "ERROR: The output path specified could not be found"
    exit 3;
fi

# Install Python requirements
pip install -r ./requirements.txt

if [[ "${ENVIRONMENT}" != "*" ]]; then

  # Building a single environment from the config root folder
  OUTPUT_FILENAME=$(echo "./${OUTPUT_PATH}/${OUTPUT_FILENAME_PREFIX}${ENVIRONMENT}${OUTPUT_FILENAME_SUFFIX}" | tr -s /)

  # Build the template
  echo "Building: ${OUTPUT_FILENAME}"
  python template.py \
    "${ENVIRONMENT}" \
    "${TEMPLATE_ROOT}" \
    "${CONFIG_ROOT}" \
    "${OUTPUT_FILENAME}"

else

  # Building all environments in the config root folder
  for ENVIRONMENT_CURRENT in ${CONFIG_ROOT}/* ; do
      if [[ -d "${ENVIRONMENT_CURRENT}" ]]; then
          ENVIRONMENT_CURRENT=$(basename ${ENVIRONMENT_CURRENT})
          OUTPUT_FILENAME=$(echo "./${OUTPUT_PATH}/${OUTPUT_FILENAME_PREFIX}${ENVIRONMENT_CODE}${OUTPUT_FILENAME_SUFFIX}" | tr -s /)

          # Build the template
          echo "Building: ${OUTPUT_FILENAME}"
          python template.py \
            "${ENVIRONMENT_CURRENT}" \
            "${TEMPLATE_ROOT}" \
            "${CONFIG_ROOT}" \
            "${OUTPUT_FILENAME}"
      fi
  done

fi
