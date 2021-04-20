# HVRP benchmark classes

## Instances

The `VFMP_V` folder contains instances available
[here](http://fc.isima.fr/~lacomme/hvrp/hvrp.html). See
[Prins](https://dl.acm.org/doi/abs/10.1016/j.engappai.2008.10.006) for
a description of this class of problem.

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh VFMP_V
./run.sh VFMP_V
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
