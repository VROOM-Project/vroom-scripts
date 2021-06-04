# -*- coding: utf-8 -*-
import json
from utils.file import load_json


def coord_to_csv(array):
    return str(array[1]) + "," + str(array[0]) + "\n"


def write_to_csv(file_name, json_input):
    lines = []

    for v in json_input["vehicles"]:
        if "start" in v:
            lines.append(coord_to_csv(v["start"]))
        if "end" in v:
            lines.append(coord_to_csv(v["end"]))

    if "jobs" in json_input:
        for job in json_input["jobs"]:
            lines.append(coord_to_csv(job["location"]))

    if "shipments" in json_input:
        for shipment in json_input["shipments"]:
            lines.append(coord_to_csv(shipment["pickup"]["location"]))
            lines.append(coord_to_csv(shipment["delivery"]["location"]))

    print("Writing csv file to " + file_name + ".csv")
    with open(file_name + ".csv", "w") as output_file:
        for l in lines:
            output_file.write(l)
