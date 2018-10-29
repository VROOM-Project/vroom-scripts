# VRPTW benchmark classes

## Solomon

The `solomon` folder contain all 100-jobs VRPTW instances described in
[Solomon](http://web.cba.neu.edu/~msolomon/problems.htm).

## Gehring & Homberger

The `homberger_*` folders contain all VRPTW instances described in
[Gehring &
Homberger](https://www.sintef.no/projectweb/top/vrptw/homberger-benchmark/),
with sizes ranging from 200 to 1000 jobs.

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh solomon homberger_200
./run.sh solomon homberger_200
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

### Travel-time oriented best known solutions

The best known solutions when minimizing the total travel time (and
not the number of vehicles) are provided for Solomon instances, based
on best results gathered from 1., 2. and 3. They are described in
`BKS.json` with a key ending with `_distance`.

1. O. Bräysi, M. Gendreau (2005). Vehicle Routing Problem with Time Windows, Part II: Metaheuristics.
2. S. Jung, B.R. Moon (2002). A Hybrid Genetic Algorithm for the Vehicle Routing Problem with Time Windows.
3. K. Tan, T. Lee, K. Ou, and L. Lee (2001). A messy genetic algorithm
for the vehicle routing problem with time window constraints.

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