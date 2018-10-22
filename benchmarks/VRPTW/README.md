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
provided script on the benchmark classes you want to use.

```
./generate.sh solomon homberger_200
./run.sh solomon homberger_200
```

It will

- parse all instances `*.txt` files to generate `VROOM` input files in `Jason`
format
- solve all instances
- retrieve comparisons to best known solutions for all instances
- log global indicators

# Notes

## Optimization objective(s)

### Single or bi-objective?

For all instances in the above benchmarks, the number of provided
vehicles is way larger than what is required to handle all jobs. Most
implementations from the literature aim at first minimizing the number
of vehicles used and then the total travel time, and our best known
solution compilation comply with this view. On the other hand, VROOM
aims at first maximizing the number of handled jobs (with fixed fleet)
and then minimizing total travel time. As a result, direct cost
comparisons with stored best known solutions are meaningless if the
number of vehicles used are different. For example VROOM might provide
a solution that is way cheaper in term of travel time than the "best
known solution", but uses one more vehicle.

### Limited fleet instances

To overcome the above limitation, an alternative set of instances is
generated. The instances contain the same set of jobs but have a
number of available vehicles that matches the minimal number of used
vehicles observed in stored best known results. Thus we transform the
"try to do everything with less vehicles" view into "try to handle all
jobs with a small fleet". Then in case VROOM manages to handle all
jobs, comparisons and gaps to best known solutions are relevant.

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
10000 to keep a fair amount of precision. Then this "scaling" is taken
into account while comparing our results to best known solutions.