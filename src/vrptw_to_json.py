#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
from utils.benchmark import get_matrix

# Generate a json-formatted problem from a TSPTW/VRPTW file.

# Those benchmarks use double precision for matrix costs (and input
# timings), and results are usually reported with 2 decimal places. As
# a workaround, we multiply all costs/timings by CUSTOM_PRECISION
# before performing the usual integer rounding. Comparisons in
# benchmarks/compare_to_BKS.py are adjusted accordingly.
CUSTOM_PRECISION = 1000

line_no = 0


def parse_meta(lines, meta):
    global line_no
    while len(lines) > 0:
        line = lines.pop(0).strip()
        line_no += 1
        if len(line) == 0:
            continue
        elif "CUSTOMER" in line or "CUST NO." in line:
            lines.insert(0, line)
            line_no -= 1
            break
        elif "NUMBER" in line:
            continue
        else:
            x = line.split()
            if len(x) < 2:
                print("Cannot understand line " + str(line_no) + ": too few columns.")
                exit(2)
            meta["VEHICLES"] = int(x[0])
            meta["CAPACITY"] = int(x[1])


def parse_jobs(lines, jobs, coords):
    global line_no
    location_index = 0
    while len(lines) > 0:
        line = lines.pop(0).strip()
        line_no += 1
        if len(line) == 0:
            continue
        elif "CUST " in line:
            continue
        else:
            x = line.split()
            if len(x) < 7:
                print("Cannot understand line " + str(line_no) + ": too few columns.")
                exit(2)
            # some guys use '999' entry as terminator sign and others don't
            elif "999" in x[0] and len(jobs) < 999:
                break
            coords.append([float(x[1]), float(x[2])])
            jobs.append(
                {
                    "id": int(x[0]),
                    "location": [float(x[1]), float(x[2])],
                    "location_index": location_index,
                    "delivery": [int(float(x[3]))],
                    "time_windows": [
                        [
                            CUSTOM_PRECISION * int(float(x[4])),
                            CUSTOM_PRECISION * int(float(x[5])),
                        ]
                    ],
                    "service": CUSTOM_PRECISION * int(x[6]),
                }
            )
            location_index += 1


def parse_vrptw(input_file):
    global line_no

    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = {}
    while len(lines) > 0:
        line = lines.pop(0).strip()
        line_no += 1
        if len(line) > 0:
            if "#NUM" in line:
                lines.insert(0, line)
                meta["NAME"] = input_file
            else:
                meta["NAME"] = line
            break

    coords = []
    jobs = []

    while len(lines) > 0:
        line = lines.pop(0)
        line_no += 1
        if "VEHICLE" in line:
            parse_meta(lines, meta)
        elif "CUSTOMER" in line or "CUST " in line or "#NUM" in line:
            parse_jobs(lines, jobs, coords)

    matrix = get_matrix(coords, CUSTOM_PRECISION)

    j = jobs.pop(0)

    total_demand = 0
    time_min = ~0
    time_max = 0
    for n in range(len(jobs)):
        total_demand += jobs[n]["delivery"][0]
        for t in jobs[n]["time_windows"]:
            if t[0] - matrix[0][n] < time_min:
                time_min = t[0] - matrix[0][n]
            if t[1] + matrix[n][0] > time_max:
                time_max = t[1] + matrix[n][0]

    if "VEHICLES" not in meta:
        meta["VEHICLES"] = 1
    if "CAPACITY" not in meta:
        meta["CAPACITY"] = total_demand
    meta["JOBS"] = len(jobs)
    meta["TIME WINDOW"] = [time_min, time_max]

    n_vehicles = meta["VEHICLES"]
    capacity = meta["CAPACITY"]
    # use TW for vehicle (first points entry) when explicitely defined
    tw = j["time_windows"]
    if [tw[0][1] != 0]:
        time_min = tw[0][0]
        time_max = tw[0][1]

    vehicles = []

    for n in range(n_vehicles):
        vehicles.append(
            {
                "id": n,
                "start": coords[0],
                "start_index": 0,
                "end": coords[0],
                "end_index": 0,
                "capacity": [capacity],
                "time_window": [time_min, time_max],
            }
        )

    return {
        "meta": meta,
        "vehicles": vehicles,
        "jobs": jobs,
        "matrices": {"car": {"durations": matrix}},
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".txt")] + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_vrptw(input_file)

    with open(output_name, "w") as out:
        json.dump(json_input, out)
