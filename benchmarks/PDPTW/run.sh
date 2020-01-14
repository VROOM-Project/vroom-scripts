#!/bin/bash

# Number of threads for solving.
t=4
# Exploration level.
x=5
sol_folder="solutions_t_${t}_x_${x}"

solutions=()

# Loop over list of folder in input.
for class in "$@"
do
    echo "* Solving with ${t} threads and exploration level ${x}, output written to ${class}/${sol_folder}"
    mkdir ${class}/${sol_folder}

    for file in `ls ${class}/*.json`
    do
        base_file=`basename ${file}`
        sol_file=${class}/${sol_folder}/${base_file%.json}_sol.json
        solutions+=($sol_file)
        [ -f ${sol_file} ] || echo "Solving ${file%.json}"
        [ -f ${sol_file} ] || vroom -i ${file} -o ${sol_file} -t ${t} -x ${x}
    done
done

echo "* Compare all results to best known solutions."
python ../compare_to_BKS.py BKS.json ${solutions[@]} > ${sol_folder}.csv
echo "  - output written to ${sol_folder}.csv"
