#!/bin/bash

# Number of threads for solving.
t=8
# Exploration level.
x=1
sol_folder="solutions_t_${t}_x_${x}"

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

    echo "* Solving with ${t} threads and exploration level ${x}, output written to ${class}/${sol_folder}"
    mkdir ${sol_folder}

    for file in `ls -rS *.json`
    do
        sol_file=${sol_folder}/${file%.json}_sol.json
        [ -f ${sol_file} ] || echo "Solving ${file%.json}"
        [ -f ${sol_file} ] || vroom -i ${file} -o ${sol_file} -t ${t} -x ${x}
    done

    cd ../
done

echo "* Compare all results to best known solutions."
python compare_to_BKS.py BKS.json */${sol_folder}/*_sol.json > ${sol_folder}.csv
echo "  - output written to ${sol_folder}.csv"
