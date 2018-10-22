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
./run.sh solomon homberger_200
```

It will

- parse all instances `*.txt` files to generate `VROOM` input files in `json`
format
- solve all instances
- retrieve comparisons to best known solutions for all instances
- log global indicators

# Notes

## Costs evaluation

All results reported in the litterature for the above benchmarks use
double precision for costs and timing constraints. As no rounding
convention has ever been decided, different implementations might
actually rely on different costs values due to the joys of
floating-point arithmetic (there are even questions on some best known
costs validity!).

So on one hand, we need to compare to double precision values rounded
to 2 decimal places, and on the other hand `VROOM` only uses integer
values for costs. Our workaround is to round costs with the usual
TSPLIB convention **after** multiplying double precision values by
10000 to keep a fair amount of precision. Then this "scaling" is taken
into account while comparing our results to best known solutions.