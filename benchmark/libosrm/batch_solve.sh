#!/bin/bash

# Run this in the right folder to solve all problems. Toogle commented
# part to use libosrm over osrm-routed.

FOLDER="osrm-routed"
LIBOSRM_FLAG=""

# FOLDER="libosrm"
# LIBOSRM_FLAG="-l"

mkdir $FOLDER
for f in *.json
do
    echo "Solving ${f}"
    vroom -i $f -g $LIBOSRM_FLAG -o ${FOLDER}/${f%.json}_sol.json
done
