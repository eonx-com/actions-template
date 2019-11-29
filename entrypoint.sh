#!/usr/bin/env bash

# Get parameters from Github Actions workflow
ENVIRONMENT_SELECTED=$(echo ${1})
print "ENVIRONMENT_SELECTED: ${ENVIRONMENT_SELECTED}"
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
    echo "ERROR: The output path specified (${OUTPUT_PATH}) could not be found"
    exit 3;
fi

# Install Python requirements
pip install -r /opt/template/requirements.txt

if [[ "${ENVIRONMENT_SELECTED}" != "*" ]] && [[ ! -z "${ENVIRONMENT_SELECTED}" ]]; then
  echo "Building '${ENVIRONMENT_SELECTED}' Environment..."

  # Building a single environment from the config root folder
  OUTPUT_FILENAME=$(echo "${OUTPUT_PATH}/${OUTPUT_FILENAME_PREFIX}${ENVIRONMENT_SELECTED}${OUTPUT_FILENAME_SUFFIX}" | tr -s /)

  echo "Building:        '${ENVIRONMENT_SELECTED}'"
  echo "Output Filename: '${OUTPUT_FILENAME}'"
  echo "Template Root:   '${TEMPLATE_ROOT}'"
  echo "Config Root:     '${CONFIG_ROOT}'"
  echo "Output Path:     '${OUTPUT_PATH}'"
  echo "Output Prefix:   '${OUTPUT_FILENAME_PREFIX}'"
  echo "Output Suffix:   '${OUTPUT_FILENAME_SUFFIX}'"

  # Build the template
  python /opt/template/template.py \
    "${ENVIRONMENT}" \
    "${TEMPLATE_ROOT}" \
    "${CONFIG_ROOT}" \
    "${OUTPUT_FILENAME}"

else
  echo "Building All Environments..."

  # Building all environments in the config root folder
  for ENVIRONMENT_CURRENT in ${CONFIG_ROOT}/* ; do
      if [[ -d "${ENVIRONMENT_CURRENT}" ]]; then
          ENVIRONMENT_SELECTED=$(basename ${ENVIRONMENT_CURRENT})
          OUTPUT_FILENAME=$(echo "${OUTPUT_PATH}/${OUTPUT_FILENAME_PREFIX}${ENVIRONMENT_CODE}${OUTPUT_FILENAME_SUFFIX}" | tr -s /)

          echo "Building:        '${ENVIRONMENT_SELECTED}'"
          echo "Output Filename: '${OUTPUT_FILENAME}'"
          echo "Template Root:   '${TEMPLATE_ROOT}'"
          echo "Config Root:     '${CONFIG_ROOT}'"
          echo "Output Path:     '${OUTPUT_PATH}'"
          echo "Output Prefix:   '${OUTPUT_FILENAME_PREFIX}'"
          echo "Output Suffix:   '${OUTPUT_FILENAME_SUFFIX}'"

          # Build the template
          python /opt/template/template.py \
            "${ENVIRONMENT_SELECTED}" \
            "${TEMPLATE_ROOT}" \
            "${CONFIG_ROOT}" \
            "${OUTPUT_FILENAME}"
      fi
  done

fi
