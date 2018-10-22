#!/bin/bash

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Move to ${class} class folder"
    cd ${class}

    # Generate json files from *.tsp files on the first execution.
    echo "* Writing json input files"
    for file in `ls -rS *.tsp`
    do
        json_file=${file%tsp}json
        [ -f ${json_file} ] || python ../../../src/tsplib_to_json.py ${file}
    done
done
