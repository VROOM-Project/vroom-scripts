# TSP benchmark classes

## TSPLIB

TSPLIB is the
[reference benchmark for TSP](https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/). The
`TSPLIB` folder contains all instances described using euclidean
distance (`EDGE_WEIGHT_TYPE = EUC_2D`).

## National TSP

A set of instances put together by William Cook on the
[University of Waterloo TSP page](http://www.math.uwaterloo.ca/tsp/world/countries.html),
ranging in size from 29 cities in Western Sahara to 71,009 cities in
China.

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh TSPLIB national_TSP
./run.sh TSPLIB national_TSP
```

Includes:

- parsing all `*.tsp` files to generate `VROOM` input files in `json` format
- solving all instances
- retrieving comparisons to best known solutions for all instances
- logging global indicators

## Warning

For huge instances, parsing input files **and** solving are both a
long and memory-intensive process. If running low on memory or
patience, one might want to rule out some of the biggest instances...
