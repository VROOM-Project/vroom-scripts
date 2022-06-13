#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from utils.benchmark import get_value, get_matrix, parse_node_coords

# Generate a json-formatted problem from a tsplib file.

TSP_FIELDS = ["NAME", "TYPE", "COMMENT", "DIMENSION", "EDGE_WEIGHT_TYPE"]


def parse_tsp(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Remember main fields describing the problem type.
    meta = {}
    for s in TSP_FIELDS:
        data = get_value(s, lines)
        if data:
            meta[s] = data

    # Only support EUC_2D for now.
    if ("EDGE_WEIGHT_TYPE" not in meta) or (meta["EDGE_WEIGHT_TYPE"] != "EUC_2D"):
        print("  - Unsupported EDGE_WEIGHT_TYPE: " + meta["EDGE_WEIGHT_TYPE"] + ".")
        exit(0)

    meta["DIMENSION"] = int(meta["DIMENSION"])

    # Find start of nodes descriptions.
    node_start = next(
        (i for i, s in enumerate(lines) if s.startswith("NODE_COORD_SECTION"))
    )

    # Use first line as vehicle start/end.
    coord_line = parse_node_coords(lines[node_start + 1])

    coords = [[float(coord_line[1]), float(coord_line[2])]]

    vehicle = {
        "id": int(coord_line[0]),
        "start": [float(coord_line[1]), float(coord_line[2])],
        "start_index": 0,
        "end": [float(coord_line[1]), float(coord_line[2])],
        "end_index": 0,
    }

    # Remaining lines are jobs.
    jobs = []

    for i in range(node_start + 2, node_start + 1 + meta["DIMENSION"]):
        coord_line = parse_node_coords(lines[i])

        coords.append([float(coord_line[1]), float(coord_line[2])])
        jobs.append(
            {
                "id": int(coord_line[0]),
                "location": [float(coord_line[1]), float(coord_line[2])],
                "location_index": i - node_start - 1,
            }
        )

    matrix = get_matrix(coords)

    return {
        "meta": meta,
        "vehicles": [vehicle],
        "jobs": jobs,
        "matrices": {"car": {"durations": matrix}},
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".tsp")] + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_tsp(input_file)

    with open(output_name, "w") as out:
        json.dump(json_input, out)
