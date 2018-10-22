# VRPTW benchmark classes

## VRPLIB

The `solomon` and `homberger` folders contain all VRPTW instances
described in [Solomon](http://web.cba.neu.edu/~msolomon/problems.htm)
and [Gehring &
Homberger](https://www.sintef.no/projectweb/top/vrptw/homberger-benchmark/).

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
