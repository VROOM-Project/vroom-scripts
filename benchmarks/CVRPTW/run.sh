#!/bin/bash

# Number of threads for solving.
t=8
# Exploration level.
x=1
sol_folder="solutions_t_${t}_x_${x}"

TOP=`dirname $0`

# Generate json files from *.txt files on the first execution.
echo "* Writing json input files"
for file in `find "$@" . -name '*.txt'`
do
    json_file=${file%.txt}.json
    [ -f ${json_file} ] || python $TOP/../../src/cvrptw_to_json.py ${file}
done

echo "* Solving with ${t} threads and exploration level ${x}, output written to ${class}/${sol_folder}"
mkdir -p ${sol_folder}

for file in `find "$@" -name '*.txt'`
do
    json_file=${file%.txt}.json
    base=`basename $file`
    sol_file=${sol_folder}/${base%.txt}_sol.json
    [ -f ${sol_file} ] || echo "Solving ${json_file}"
    [ -f ${sol_file} ] || vroom -i ${json_file} -o ${sol_file} -t ${t} -x ${x}
done

echo "* Compare all results to best known solutions."
[ -f $TOP/BKS.json ] || python $TOP/build_BKS.py
python $TOP/../CVRP/compare_to_BKS.py $TOP/BKS.json `find $TOP -name '*_sol.json'` > ${sol_folder}.csv
echo "  - output written to ${sol_folder}.csv"
