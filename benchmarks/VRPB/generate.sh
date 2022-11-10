#!/bin/bash

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Move to ${class} class folder"
    cd ${class}

    # Generate json files from *.vrp files on the first execution.
    echo "* Writing json input files"
    for file in `ls -rS *.vrpb`
    do
        json_file=${file%vrpb}json
        [ -f ${json_file} ] || python3 ../../../src/cvrplib_to_json.py ${file}
    done

    cd ../
done
