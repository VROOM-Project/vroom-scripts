#!/bin/bash

# Retrieve global indicators by instance size for all solutions.

array_jobs=(20 50 100 250 500 750 1000 1500)

for size in "${array_jobs[@]}"
do
    folder=${size}/osrm-routed
    python ../../src/global_indicators.py $folder
    folder=${size}/libosrm
    python ../../src/global_indicators.py $folder
done
