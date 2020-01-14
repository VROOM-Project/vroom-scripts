# PDPTW benchmark classes

## Li & Lim

The `li_lim_*` folders contain all instances described in [Li &
Lim](https://doi.org/10.1142/S0218213003001186) and available from
[https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/](https://www.sintef.no/projectweb/top/pdptw/li-lim-benchmark/).

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh li_lim_100 li_lim_200
./run.sh li_lim_100 li_lim_200
```

Includes:

- parsing all `*.txt` files to generate `VROOM` input files in `json` format
- solving all instances
- retrieving comparisons to best known solutions for all instances
- logging global indicators

# Notes

## Optimization objective(s)

### Benchmarks comparison limitation

For all instances in the above benchmarks, the number of provided
vehicles is way larger than what is required to handle all jobs. Most
implementations from the literature aim at first minimizing the number
of vehicles used and then the total travel time, and most of the best
known solutions listed in `BKS.json` comply with this view. On the
other hand, VROOM aims at first maximizing the number of handled jobs
(with fixed fleet) and then minimizing total travel time. As a result,
direct cost comparisons with stored best known solutions are
meaningless if the number of vehicles used are different. For example
VROOM might provide a solution that is way cheaper in term of travel
time than the "best known solution", but uses one more vehicle.

## Costs evaluation

All results reported in the literature for the above benchmarks use
double precision for costs and timing constraints. As no rounding
convention has ever been decided, different implementations might
actually rely on different costs values due to the joys of
floating-point arithmetic (there are even doubts on some best known
costs validity!).

So on one hand, we need to compare to double precision values rounded
to 2 decimal places, and on the other hand VROOM only uses integer
values for costs. Our workaround is to round costs with the usual
TSPLIB convention **after** multiplying double precision values by
1000 to keep a fair amount of precision. Then this "scaling" is taken
into account while comparing our results to best known solutions.