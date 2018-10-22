#!/bin/bash

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Move to ${class} class folder"
    cd ${class}

    # Generate json files from *.vrp files on the first execution.
    echo "* Writing json input files"
    for file in `ls -rS *.vrp`
    do
        json_file=${file%vrp}json
        [ -f ${json_file} ] || python ../../../src/cvrplib_to_json.py ${file}
    done

    cd ../
done
