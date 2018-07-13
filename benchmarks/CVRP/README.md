# CVRP benchmark classes

## CVRPLIB

The `A`, `B`, `E`, `F`, `M`, `P` and `X` folders contain all instances
described in
[CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/) using
euclidean distance (`EDGE_WEIGHT_TYPE = EUC_2D`).

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided script on the benchmark classes you want to use.

```
./run.sh A B E F M P X
```

It will

- parse all `*.vrp` files to generate `VROOM` input files in `json` format
- solve all instances
- retrieve comparisons to best known solutions for all instances
- log global indicators
