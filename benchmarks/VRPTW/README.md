# VRPTW benchmark classes

## VRPLIB

The benchmark instances represented here are described in:
- [VRPTW](https://www.sintef.no/projectweb/top/vrptw)
- [TSPTW](http://homepages.dcc.ufmg.br/~rfsilva/tsptw)

# Downloading

Just run:
```
./download.sh
```
It will retrieve and aggregate everything needed.

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided script on the benchmark classes you want to use.
```
./run.sh [VRPTW|TSPTW|VRPTW TSPTW(default)]
```
It will
- parse all instances `*.txt` files to generate `VROOM` input files in `json`
format
- solve all instances
- retrieve comparisons to best known solutions for all instances
- log global indicators
