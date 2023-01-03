# VRPB benchmark class

## VRPB

The `queiroga` folder contain all instances described in [Queiroga et
al. (2020)](https://hal.inria.fr/hal-02379008/file/Queiroga_etall_LOGIS19.pdf)
and available [from
VRP-REP](http://vrp-rep.org/datasets/item/2019-0003.html).

# Solving

Assuming the `vroom` command is somewhere in your path, just run the
provided scripts on the benchmark classes you want to use.

```
./generate.sh queiroga
./run.sh queiroga
```

Includes:

- parsing all `*.vrp` files to generate `VROOM` input files in `json` format
- solving all instances
- retrieving comparisons to best known solutions for all instances
- logging global indicators
