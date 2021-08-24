#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import sys
from utils.file import load_json
from utils.vroom import solve

# Parse a json-formatted input instance, then apply iterative solving
# strategies to come up with a solution minimizing completion time.


def dichotomy(data, first_solution):
    init_input = copy.deepcopy(data)
    solutions = [first_solution]

    end_dates = [r["steps"][-1]["arrival"] for r in first_solution["routes"]]
    earliest = min(end_dates)
    latest = max(end_dates)

    if len(first_solution["routes"]) < len(init_input["vehicles"]):
        # There is an unused vehicle in the initial solution so
        # current earliest is meaningless.
        earliest = 0

    for vehicle in init_input["vehicles"]:
        if "time_window" not in vehicle:
            vehicle["time_window"] = [0, latest]

    end_candidate = int(round(float(earliest + latest) / 2))
    while (end_candidate != earliest) and (end_candidate != latest):
        # Force end_candidate as new end date for all vehicles.
        current = copy.deepcopy(init_input)

        for v in range(len(current["vehicles"]) - 1, -1, -1):
            vehicle = current["vehicles"][v]
            if end_candidate < vehicle["time_window"][1]:
                if end_candidate < vehicle["time_window"][0]:
                    # Discard vehicle since its time window is past
                    # end_candidate.
                    current["vehicles"].pop(v)
                else:
                    # Reduce time window for vehicle.
                    vehicle["time_window"][1] = end_candidate

        # Solve updated variant
        current_sol = solve(current)

        if current_sol["summary"]["unassigned"] == 0:
            solutions.append(current_sol)
            latest = end_candidate
        else:
            earliest = end_candidate

        end_candidate = int(round(float(earliest + latest) / 2))

    return solutions


def solve_asap(data):
    init_solution = solve(data)

    if init_solution["code"] != 0:
        print(json.dumps(init_solution))
        exit(init_solution["code"])

    if init_solution["summary"]["unassigned"] != 0:
        print('{"code": 2, "error": "Can\'t solve problem with all jobs"}')
        exit(2)

    dichotomy_solutions = dichotomy(data, init_solution)

    print(
        [
            {
                "completion": max([r["steps"][-1]["arrival"] for r in sol["routes"]]),
                "cost": sol["summary"]["cost"],
            }
            for sol in dichotomy_solutions
        ]
    )


if __name__ == "__main__":
    input_file = sys.argv[1]

    data = load_json(input_file)
    solve_asap(data)
