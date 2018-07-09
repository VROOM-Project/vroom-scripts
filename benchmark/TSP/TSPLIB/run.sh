#!/bin/bash

# Generate json files from *.tsp files on the first execution.
echo "* Writing json input files"
for file in `ls -rS *.tsp`
do
    json_file=${file%tsp}json
    [ -f ${json_file} ] || python ../../../src/tsplib_to_json.py ${file}
done

# Number of threads for solving.
t=8
folder="solutions_t_${t}"

echo "* Solving with ${t} threads, output written to ${folder}"
mkdir ${folder}

for file in `ls -rS *.json`
do
    if [ "${file}" = "BKS.json" ]
    then
        continue
    fi
    sol_file=${folder}/${file%.json}_sol.json
    [ -f ${sol_file} ] || echo "Solving ${file%.json}"
    [ -f ${sol_file} ] || vroom -i ${file} -o ${sol_file} -t ${t}
done

echo "* Compare all results to best known solutions."
python compare_to_BKS.py BKS.json ${folder}/*json > ${folder}.csv
echo "  - output written to ${folder}.csv"
