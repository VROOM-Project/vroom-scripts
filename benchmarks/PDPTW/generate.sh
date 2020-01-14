#!/bin/bash

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Move to ${class} class folder"
    cd ${class}

    # Generate json files from *.txt files on the first execution.
    echo "* Writing json input files"
    for file in `ls -rS *.txt`
    do
        json_file=${file%.txt}.json
        [ -f ${json_file} ] || python ../../../src/pdptw_to_json.py ${file}
    done

    cd ../
done
