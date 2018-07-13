#!/bin/bash

# Generate 50 random instances for each chosen size in respective
# folders.

array_jobs=(20 50 100 250 500 750 1000 1500)

for size in "${array_jobs[@]}"
do
    mkdir $size
    for i in {1..50}
    do
        ../../src/random_problem.py --left 1 --right 3.5 --bottom 48 --top 49.5 --jobs $size --seed $i
    done
    mv *.json ${size}/
done
