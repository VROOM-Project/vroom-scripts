# MDVRP benchmark classes

## Cordeau

The `cordeau` folder contain all MDVRP instances described in [Cordeau
et al. (1997)](http://vrp-rep.org/datasets/item/2017-0010.html).

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh cordeau
./run.sh cordeau
```

Includes:

- parsing all `*.txt` files to generate `VROOM` input files in `json` format
- solving all instances
- retrieving comparisons to best known solutions for all instances
- logging global indicators

# Notes

## Costs evaluation

All results reported in the literature for the above benchmarks use
double precision for costs.

Our workaround is to round costs with the usual TSPLIB convention
**after** multiplying double precision values by 1000 to keep a fair
amount of precision. Then this "scaling" is taken into account while
comparing our results to best known solutions.
