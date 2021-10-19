#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.osrm import table

# Compute durations matrix using OSRM for each required profile, then
# add the matrix and all relevant indices to the input problem.


def round_to_cost(d):
    return int(d + 0.5)


def get_index(locations, locations_indices, loc):
    new_index = len(locations)

    lon_str = str(loc[0])
    lat_str = str(loc[1])

    if lon_str in locations_indices:
        if lat_str in locations_indices[lon_str]:
            return locations_indices[lon_str][lat_str]
        else:
            locations_indices[lon_str][lat_str] = new_index
    else:
        locations_indices[lon_str] = {lat_str: new_index}

    # loc is not already listed in locations.
    locations.append(loc)
    return new_index


def add_matrix(data, routing):
    # Retrieve all problem locations in the same order as in
    # input_parser.cpp.
    locs = []
    index_of_known_locations = {}

    profiles = set()

    for v in data["vehicles"]:
        if "profile" in v:
            profiles.add(v["profile"])
        else:
            profiles.add("car")

        if ("start" not in v) and ("end" not in v):
            raise ValueError("Missing coordinates for vehicle.")

        if "start" in v:
            v["start_index"] = get_index(locs, index_of_known_locations, v["start"])
        if "end" in v:
            v["end_index"] = get_index(locs, index_of_known_locations, v["end"])

    if "jobs" in data:
        for job in data["jobs"]:
            if "location" not in job:
                raise ValueError("Missing coordinates for job.")
            else:
                job["location_index"] = get_index(
                    locs, index_of_known_locations, job["location"]
                )

    if "shipments" in data:
        for shipment in data["shipments"]:
            if "location" not in shipment["pickup"]:
                raise ValueError("Missing coordinates for shipment pickup.")
            else:
                shipment["pickup"]["location_index"] = get_index(
                    locs, index_of_known_locations, shipment["pickup"]["location"]
                )

            if "location" not in shipment["delivery"]:
                raise ValueError("Missing coordinates for shipment delivery.")
            else:
                shipment["delivery"]["location_index"] = get_index(
                    locs, index_of_known_locations, shipment["delivery"]["location"]
                )

    # Get matrices from OSRM.
    data["matrices"] = {}
    for p in profiles:
        if p not in routing["profiles"]:
            raise ValueError("Invalid profile: " + p)

        matrix = table(
            locs, routing["profiles"][p]["host"], routing["profiles"][p]["port"]
        )["durations"]
        data["matrices"][p] = {"durations": []}

        # Round all durations to the nearest integer (same behavior as
        # in osrm_wrapper.h)
        for line in matrix:
            data["matrices"][p]["durations"].append([round_to_cost(d) for d in line])
