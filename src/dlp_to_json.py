#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

# Generate a json-formatted problem from a DLP file.

# Those benchmarks use double precision for matrix costs and results
# are usually reported with 2 decimal places. As a workaround, we
# multiply all costs by CUSTOM_PRECISION before performing the usual
# integer rounding. Comparisons in benchmarks/compare_to_BKS.py are
# adjusted accordingly.
CUSTOM_PRECISION = 1000

FIRST_LINE = 5


def parse_meta(line):
    meta = line.split()
    return {"JOBS": int(meta[0]), "VEHICLE_TYPES": int(meta[1])}


def parse_depot(line):
    depot = line.split()
    return int(depot[0])


def parse_matrix(lines):
    N = len(lines)
    matrix = []
    for line in lines:
        current_line = [int(v) for v in line.split()]
        if len(current_line) != N:
            print("Matrix problem")
            exit(1)

        matrix.append(current_line)
    return matrix


def parse_jobs(lines, jobs):
    for i in range(len(lines)):
        customer = lines[i].split()
        if len(customer) < 2:
            print("Too few columns in customer line.")
            exit(2)

        index = int(customer[0])

        jobs.append(
            {"id": index, "location_index": index, "delivery": [int(customer[1])]}
        )


def parse_dlp(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = parse_meta(lines[FIRST_LINE])

    instance_name = input_file[: input_file.rfind(".txt")]
    BKS = {
        instance_name: {
            "class": "DLP",
            "best_known_cost": 0,
            "jobs": meta["JOBS"],
            "total_demand": 0,
            "total_capacity": 0,
            "vehicles": 0,
        }
    }

    depot_index = parse_depot(lines[FIRST_LINE + meta["VEHICLE_TYPES"] + 1])

    matrix_start = FIRST_LINE + meta["VEHICLE_TYPES"] + 2

    # No custom precision here as it appears matrix values are already
    # scaled, presumably provided in meters while global cost is km.
    matrix = parse_matrix(lines[matrix_start : matrix_start + meta["JOBS"] + 1])

    # Handle vehicles.
    vehicles = []

    for v_type in range(1, meta["VEHICLE_TYPES"] + 1):
        line = lines[FIRST_LINE + v_type]
        vehicle = line.split()

        v_number = int(vehicle[0])
        v_capacity = int(vehicle[1])
        v_fixed_cost = int(CUSTOM_PRECISION * float(vehicle[2]))
        v_du_cost = float(vehicle[3])

        BKS[instance_name]["vehicles"] += v_number
        BKS[instance_name]["total_capacity"] += v_number * v_capacity

        for n in range(v_number):
            vehicles.append(
                {
                    "id": v_type * 1000 + n,
                    "start_index": depot_index,
                    "end_index": depot_index,
                    "capacity": [v_capacity],
                    "costs": {"fixed": v_fixed_cost, "per_hour": int(3600 * v_du_cost)},
                    "description": str(v_type),
                }
            )

    # Handle jobs
    jobs = []
    jobs_start = matrix_start + meta["JOBS"] + 2

    parse_jobs(lines[jobs_start : jobs_start + meta["JOBS"]], jobs)

    for n in range(len(jobs)):
        BKS[instance_name]["total_demand"] += jobs[n]["delivery"][0]

    meta["VEHICLES"] = len(vehicles)

    for n in range(len(jobs)):
        BKS[instance_name]["total_demand"] += jobs[n]["delivery"][0]

    # print(json.dumps(BKS))
    # exit(0)

    return {
        "meta": meta,
        "vehicles": vehicles,
        "jobs": jobs,
        "matrices": {"car": {"durations": matrix}},
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    instance_name = input_file[: input_file.rfind(".txt")]
    output_name = instance_name + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_dlp(input_file)

    json_input["meta"]["NAME"] = instance_name

    with open(output_name, "w") as out:
        json.dump(json_input, out)
