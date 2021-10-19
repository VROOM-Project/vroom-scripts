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
    "engine": "ors",
    "profiles": {
        "driving-car": {"host": "localhost", "port": "8080"},
        "driving-hgv": {"host": "localhost", "port": "8080"},
        "cycling-regular": {"host": "localhost", "port": "8080"},
        "cycling-mountain": {"host": "localhost", "port": "8080"},
        "cycling-road": {"host": "localhost", "port": "8080"},
        "cycling-electric": {"host": "localhost", "port": "8080"},
        "foot-walking": {"host": "localhost", "port": "8080"},
        "foot-hiking": {"host": "localhost", "port": "8080"},
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
