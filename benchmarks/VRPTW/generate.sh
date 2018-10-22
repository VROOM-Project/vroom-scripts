#!/bin/bash

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Move to ${class} class folder"
    cd ${class}
    mkdir limited_fleet

    # Generate json files from *.txt files on the first execution.
    echo "* Writing json input files"
    for file in `ls -rS *.txt`
    do
        json_file=${file%.txt}.json
        v_number=`jq .${file%.txt}.solved_with_vehicles ../BKS.json`
        [ -f ${json_file} ] || python ../../../src/vrptw_to_json.py ${file} $v_number
    done

    cd ../
done
