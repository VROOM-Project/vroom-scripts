#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, sys, os
from utils.benchmark import *

# Generate a json-formatted problem from a PDPTW file.

# Those benchmarks use double precision for matrix costs (and input
# timings), and results are usually reported with 2 decimal places. As
# a workaround, we multiply all costs/timings by CUSTOM_PRECISION
# before performing the usual integer rounding. Comparisons in
# benchmarks/compare_to_BKS.py are adjusted accordingly.
CUSTOM_PRECISION = 1000


def parse_meta(line):
    x = line.split()
    if len(x) < 2:
        print("Cannot understand meta line: too few columns.")
        exit(2)

    return {"VEHICLES": int(x[0]), "CAPACITY": int(x[1])}


def parse_depot(line):
    x = line.split()
    if len(x) < 9:
        print("Cannot understand depot line: too few columns.")
        exit(2)

    return {
        "location": [int(x[1]), int(x[2])],
        "time_window": [CUSTOM_PRECISION * int(x[4]), CUSTOM_PRECISION * int(x[5])],
    }


def parse_job(line, pickups, deliveries, coords):
    x = line.split()
    if len(x) < 9:
        print("Cannot understand job line: too few columns.")
        exit(2)

    job = {
        "id": int(x[0]),
        "location": [float(x[1]), float(x[2])],
        "location_index": len(coords),
        "amount": [int(float(x[3]))],
        "time_windows": [
            [CUSTOM_PRECISION * int(float(x[4])), CUSTOM_PRECISION * int(float(x[5]))]
        ],
        "service": CUSTOM_PRECISION * int(float(x[6])),
    }
    coords.append([float(x[1]), float(x[2])])

    pickup_id = int(x[7])
    delivery_id = int(x[8])

    if pickup_id == 0:
        # This job is a pickup.
        job["matching_delivery"] = delivery_id
        pickups.append(job)
    else:
        if delivery_id != 0:
            print("Invalid pickup/delivery values.")
            exit(2)
        # This job is a delivery.
        job["matching_pickup"] = pickup_id
        deliveries[x[0]] = job


def parse_pdptw(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    meta = parse_meta(lines[0].strip())
    meta["NAME"] = input_file

    depot = parse_depot(lines[1].strip())

    coords = [depot["location"]]

    vehicles = []
    for v in range(meta["VEHICLES"]):
        vehicles.append(
            {
                "id": v,
                "start": depot["location"],
                "start_index": 0,
                "end": depot["location"],
                "end_index": 0,
                "capacity": [meta["CAPACITY"]],
                "time_window": depot["time_window"],
            }
        )

    # We want to access deliveries in constant time based on their id.
    pickups = []
    deliveries = {}

    for line in lines[2:]:
        parse_job(line, pickups, deliveries, coords)

    meta["JOBS"] = len(pickups) + len(deliveries)

    shipments = []

    for pickup in pickups:
        delivery = deliveries[str(pickup["matching_delivery"])]
        if (delivery["matching_pickup"] != pickup["id"]) or (
            delivery["amount"][0] != -pickup["amount"][0]
        ):
            print("Invalid matching between pickup and delivery.")
            exit(2)

        current = {"amount": pickup["amount"], "pickup": pickup, "delivery": delivery}
        del current["pickup"]["amount"]
        del current["pickup"]["matching_delivery"]
        del current["delivery"]["amount"]
        del current["delivery"]["matching_pickup"]

        shipments.append(current)

    matrix = get_matrix(coords, CUSTOM_PRECISION)

    return {
        "meta": meta,
        "vehicles": vehicles,
        "shipments": shipments,
        "matrix": matrix,
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".txt")] + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_pdptw(input_file)

    with open(output_name, "w") as out:
        json.dump(json_input, out)
