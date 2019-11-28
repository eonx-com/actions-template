#!/usr/bin/env bash

# Get parameters from Github Actions workflow
PATH_TEMPLATES=$(echo ${1} | tr -s /)
PATH_CONFIGS=$(echo ${2} | tr -s /)
PATH_OUTPUT=$(echo ${3} | tr -s /)
OUTPUT_PREFIX=${4}
OUTPUT_SUFFIX=${5}

# Validate all paths specified can be found
if [[ ! -d "${PATH_TEMPLATES}" ]]; then
    echo "ERROR: The template path specified could not be found"
    exit 1;
fi
if [[ ! -d "${PATH_CONFIGS}" ]]; then
    echo "ERROR: The environment path specified could not be found"
    exit 2;
fi
if [[ ! -d "${PATH_OUTPUT}" ]]; then
    echo "ERROR: The output path specified could not be found"
    exit 3;
fi

# Setup PIP requirements
echo "Installing Python Dependencies"
pip install -r ./requirements.txt

# Iterate over each environment folder
for ENVIRONMENT_CURRENT in ${PATH_CONFIGS}/* ; do
    if [[ -d "${ENVIRONMENT_CURRENT}" ]]; then
        ENVIRONMENT_CODE=$(basename ${ENVIRONMENT_CURRENT})
        OUTPUT_FILENAME=$(echo "./${PATH_OUTPUT}/${OUTPUT_PREFIX}${ENVIRONMENT_CODE}${OUTPUT_SUFFIX}" | tr -s /)

        # Build the template
        echo "Building Template: ${OUTPUT_FILENAME}"
        python template.py \
          "${ENVIRONMENT_CODE}" \
          "${PATH_TEMPLATES}" \
          "${PATH_CONFIGS}" \
          "${OUTPUT_FILENAME}"
    fi
done
