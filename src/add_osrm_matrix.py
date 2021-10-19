#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from utils.file import load_json
from utils.matrix import add_matrix

# Parse a json-formatted input instance, add the matrix using OSRM for
# each required profile, then write a "standalone" problem instance
# that can be further solved even without an OSRM server handy.

ROUTING = {
    "engine": "osrm",
    "profiles": {
        "car": {"host": "0.0.0.0", "port": "5000"},
        "bike": {"host": "0.0.0.0", "port": "5001"},
        "foot": {"host": "0.0.0.0", "port": "5002"},
    },
}


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".json")] + "_matrix.json"

    data = load_json(input_file)

    add_matrix(data, ROUTING)

    with open(output_name, "w") as out:
        print("Writing problem with matrix to " + output_name)
        json.dump(data, out, indent=2)
