#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import json
import sys
import matplotlib.pyplot as plt
from utils.file import load_json
from utils.vroom import solve

# Parse a json-formatted input instance, then apply iterative solving
# strategies to come up with a solution minimizing completion time.


def filter_dominated(solutions):
    indices = range(len(solutions))
    completion_times = []
    costs = []
    to_pop = []

    for i in indices:
        sol = solutions[i]
        completion_times.append(max([r["steps"][-1]["arrival"] for r in sol["routes"]]))
        costs.append(sol["summary"]["cost"])

    for i in indices:
        for j in indices:
            if j == i:
                continue
            if completion_times[j] < completion_times[i] and costs[j] < costs[i]:
                to_pop.append(i)
                break

    for i in reversed(to_pop):
        solutions.pop(i)


def dichotomy(data, first_solution):
    init_input = copy.deepcopy(data)
    solutions = []

    if len(first_solution["routes"]) > 0:
        sol = copy.deepcopy(first_solution)
        sol["origin"] = "dichotomy"
        solutions.append(sol)

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
            current_sol["origin"] = "dichotomy"
            solutions.append(current_sol)
            latest = end_candidate
        else:
            earliest = end_candidate

        end_candidate = int(round(float(earliest + latest) / 2))

    return solutions


def plot_pareto_front(indicators, pareto_file, full_Y_scale=False):
    fig, ax1 = plt.subplots(1, 1)
    plt.xlabel("Completion time")
    plt.ylabel("Cost")

    options = {
        "dichotomy": {"marker": "^", "edgecolor": "red", "linewidth": 0.7},
        "backward_search": {"marker": "o", "edgecolor": "blue", "linewidth": 0.5},
    }

    ymax = indicators[0]["cost"]

    for origin in ["backward_search", "dichotomy"]:
        costs = [i["cost"] for i in indicators if i["origin"] == origin]
        completions = [i["completion"] for i in indicators if i["origin"] == origin]
        ymax = max(ymax, max(costs))

        ax1.scatter(
            completions,
            costs,
            facecolor="none",
            edgecolor=options[origin]["edgecolor"],
            marker=options[origin]["marker"],
            linewidth=options[origin]["linewidth"],
        )

    if full_Y_scale:
        ax1.set_ylim(0, ymax * 1.05)

    plt.savefig(pareto_file, bbox_inches="tight")
    plt.show()
    plt.close()


def backward_search(data, first_solution):
    current = copy.deepcopy(data)
    current_sol = copy.deepcopy(first_solution)
    solutions = []

    end_dates = [r["steps"][-1]["arrival"] for r in first_solution["routes"]]
    latest = max(end_dates)

    for vehicle in current["vehicles"]:
        if "time_window" not in vehicle:
            vehicle["time_window"] = [0, latest]

    unassigned = first_solution["summary"]["unassigned"]

    while unassigned == 0:
        current_sol["origin"] = "backward_search"
        solutions.append(current_sol)

        # Reduce time window length for all vehicles.
        new_end = latest - 1
        for v in range(len(current["vehicles"]) - 1, -1, -1):
            vehicle = current["vehicles"][v]
            if new_end < vehicle["time_window"][1]:
                if new_end < vehicle["time_window"][0]:
                    # Discard vehicle since its time window is past
                    # new_end.
                    current["vehicles"].pop(v)
                else:
                    # Reduce time window for vehicle.
                    vehicle["time_window"][1] = new_end

        # Solve updated variant
        current_sol = solve(current)

        unassigned = current_sol["summary"]["unassigned"]
        if len(current_sol["routes"]) > 0:
            latest = max([r["steps"][-1]["arrival"] for r in current_sol["routes"]])

    return solutions


def solve_asap(data, pareto_file=""):
    init_solution = solve(data)

    if init_solution["code"] != 0:
        print(json.dumps(init_solution))
        exit(init_solution["code"])

    if init_solution["summary"]["unassigned"] != 0:
        print('{"code": 2, "error": "Can\'t solve problem with all jobs"}')
        exit(2)

    solutions = dichotomy(data, init_solution)
    solutions.extend(backward_search(data, init_solution))

    filter_dominated(solutions)

    indicators = [
        {
            "completion": max([r["steps"][-1]["arrival"] for r in sol["routes"]]),
            "cost": sol["summary"]["cost"],
            "origin": sol["origin"],
        }
        for sol in solutions
    ]

    plot_pareto_front(indicators, pareto_file)

    # Print solution with smallest completion time to standard output.
    best_rank = 0
    smallest_completion = indicators[0]["completion"]
    for i in range(1, len(indicators)):
        if indicators[i]["completion"] < smallest_completion:
            best_rank = i
            smallest_completion = indicators[i]["completion"]

    print(json.dumps(solutions[best_rank]))


if __name__ == "__main__":
    input_file = sys.argv[1]

    data = load_json(input_file)

    pareto_file = input_file[: input_file.rfind(".json")] + "_pareto.svg"
    solve_asap(data, pareto_file)
