# CVRP benchmark classes

## CVRPLIB

The `A`, `B`, `E`, `F`, `M`, `P` and `X` folders contain all instances
described in
[CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/) using
euclidean distance (`EDGE_WEIGHT_TYPE = EUC_2D`).

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh A B E F M P X
./run.sh A B E F M P X
```

Includes:

- parsing all `*.vrp` files to generate `VROOM` input files in `json` format
- solving all instances
- retrieving comparisons to best known solutions for all instances
- logging global indicators
