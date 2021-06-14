#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from utils.benchmark import get_matrix

# Generate a json-formatted problem from a MDVRP file.

# Those benchmarks use double precision for matrix costs and results
# are usually reported with 2 decimal places. As a workaround, we
# multiply all costs by CUSTOM_PRECISION before performing the usual
# integer rounding. Comparisons in benchmarks/compare_to_BKS.py are
# adjusted accordingly.
CUSTOM_PRECISION = 1000

FIRST_LINE = 0


def parse_meta(line):
    meta = line.split()
    if len(meta) < 1 or int(meta[0]) != 2:
        print("Not a MDVRP!")
        exit(2)

    return {
        "VEHICLES_PER_DEPOT": int(meta[1]),
        "JOBS": int(meta[2]),
        "DEPOTS": int(meta[3]),
    }


def parse_jobs(lines, jobs, coords):
    for i in range(len(lines)):
        customer = lines[i].split()
        if len(customer) < 5:
            print("Too few columns in customer line.")
            exit(2)

        current_coords = [float(customer[1]), float(customer[2])]
        jobs.append(
            {
                "id": int(customer[0]),
                "location": current_coords,
                "location_index": len(coords),
                "service": CUSTOM_PRECISION * int(customer[3]),
                "delivery": [int(customer[4])],
            }
        )
        coords.append(current_coords)


def parse_mdvrp(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = parse_meta(lines[FIRST_LINE])

    coords = []

    # Handle capacity per depot.
    first_values = lines[FIRST_LINE + 1].split()
    meta["MAX_ROUTE_DURATION"] = int(first_values[0])
    meta["CAPACITY"] = int(first_values[1])
    for line in lines[FIRST_LINE + 2 : FIRST_LINE + 1 + meta["DEPOTS"]]:
        if meta["MAX_ROUTE_DURATION"] != int(line.split()[0]):
            print("Inconsistent max route duration!")
            exit(1)
        if meta["CAPACITY"] != int(line.split()[1]):
            print("Inconsistent capacity!")
            exit(1)

    # Handle customer lines
    jobs = []

    jobs_start = FIRST_LINE + meta["DEPOTS"] + 1
    parse_jobs(lines[jobs_start : jobs_start + meta["JOBS"]], jobs, coords)

    # Handle depots and vehicles
    vehicles = []
    depots_start = jobs_start + meta["JOBS"]

    for d in range(meta["DEPOTS"]):
        depot = lines[depots_start + d].split()
        if len(depot) < 5:
            print("Too few columns in depot line.")
            exit(2)

        depot_id = int(depot[0])
        depot_coords = [float(depot[1]), float(depot[2])]
        location_index = len(coords)
        coords.append(depot_coords)

        for v in range(1, 1 + meta["VEHICLES_PER_DEPOT"]):
            vehicles.append(
                {
                    "id": 100 * depot_id + v,
                    "profile": "euc_2D",
                    "start": depot_coords,
                    "start_index": location_index,
                    "end": depot_coords,
                    "end_index": location_index,
                    "capacity": [meta["CAPACITY"]],
                }
            )

    meta["VEHICLES"] = len(vehicles)

    if meta["MAX_ROUTE_DURATION"] != 0:
        for vehicle in vehicles:
            vehicle["time_window"] = [0, CUSTOM_PRECISION * meta["MAX_ROUTE_DURATION"]]

    matrix = get_matrix(coords, CUSTOM_PRECISION)

    return {
        "meta": meta,
        "vehicles": vehicles,
        "jobs": jobs,
        "matrices": {"euc_2D": {"durations": matrix}},
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    instance_name = input_file[: input_file.rfind(".txt")]
    output_name = instance_name + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_mdvrp(input_file)

    json_input["meta"]["NAME"] = instance_name

    with open(output_name, "w") as out:
        json.dump(json_input, out)
