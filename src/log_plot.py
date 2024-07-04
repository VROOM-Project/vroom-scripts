# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import sys

JOB_ADDITION = "JobAddition"
RUIN = "Ruin"
ROLLBACK = "Rollback"


def get_hierarchical_cost(score, cumulated_delta):
    return score["cost"] + cumulated_delta[score["assigned"]]


def log_plot(log_file):
    # log_plot_name = log_file[0 : log_file.rfind(".json")] + ".svg"

    print("Parsing " + log_file)
    with open(log_file, "r") as data_file:
        data = json.load(data_file)

    fig, ax1 = plt.subplots(1, 1)
    fig.set_figwidth(15)

    steps = data[0]["steps"]
    specific_ranks = {"job_addition": [], "ruin": [], "rollback": []}

    ranks_chunks = [[]]

    best_score = steps[0]["score"]
    best_score_rank = 0

    max_time = steps[-1]["time"]

    # For all possible number of assigned tasks, store cost range as
    # [min, max].
    cost_range_per_assigned = {}

    # First pass through steps to store most data.
    for i, s in enumerate(steps):
        # Update best score.
        current_score = s["score"]
        current_cost = current_score["cost"]
        if (
            -current_score["priority"],
            -current_score["assigned"],
            current_cost,
        ) < (-best_score["priority"], -best_score["assigned"], best_score["cost"]):
            best_score = current_score
            best_score_rank = i

        # Update cost ranges.
        if current_score["assigned"] not in cost_range_per_assigned:
            cost_range_per_assigned[current_score["assigned"]] = [
                current_cost,
                current_cost,
            ]
        else:
            cost_range_per_assigned[current_score["assigned"]][0] = min(
                cost_range_per_assigned[current_score["assigned"]][0],
                current_cost,
            )
            cost_range_per_assigned[current_score["assigned"]][1] = max(
                cost_range_per_assigned[current_score["assigned"]][1],
                current_cost,
            )

        # First filter high-level LS modification.
        event = s["event"]
        if (event == RUIN) or (event == ROLLBACK):
            if event == RUIN:
                specific_ranks["ruin"].append(i)
            else:
                specific_ranks["rollback"].append(i)

            # Start new chunk for plotting.
            ranks_chunks.append([])
            continue

        # Moving on into current LS step.
        if event == JOB_ADDITION:
            specific_ranks["job_addition"].append(i)

        ranks_chunks[-1].append(i)

    print(specific_ranks)

    # Compute cost delta for all solutions with the same number of
    # assigned tasks.
    cost_delta_per_assigned = {}
    for nb_tasks in cost_range_per_assigned:
        cost_range = cost_range_per_assigned[nb_tasks]
        cost_delta_per_assigned[nb_tasks] = cost_range[1] - cost_range[0]

    # Compute cumulated cost deltas to use for vertical offsets.
    cumulated_delta = {}
    for nb_tasks in cost_range_per_assigned:
        cumulated_delta[nb_tasks] = 0
        for assigned in cost_delta_per_assigned:
            if assigned > nb_tasks:
                cumulated_delta[nb_tasks] += cost_delta_per_assigned[assigned]

    print(cost_delta_per_assigned)
    print(cumulated_delta)

    for chunk in ranks_chunks:
        chunk_times = []
        hierarchical_costs = []
        for r in chunk:
            chunk_times.append(steps[r]["time"])

            s = steps[r]["score"]
            hierarchical_costs.append(get_hierarchical_cost(s, cumulated_delta))

        ax1.plot(chunk_times, hierarchical_costs, color="blue")

    ax1.plot(
        [steps[0]["time"], steps[-1]["time"]],
        [best_score["cost"], best_score["cost"]],
        color="green",
        linewidth=2,
    )

    # Materialize job addition events
    for i in specific_ranks["job_addition"]:
        time = steps[i]["time"]
        ax1.plot(
            [time, time],
            [
                best_score["cost"],
                get_hierarchical_cost(steps[i]["score"], cumulated_delta),
            ],
            color="red",
            linewidth=2,
        )

    print(best_score_rank)
    print(best_score)
    ax1.scatter(
        [steps[best_score_rank]["time"]],
        [best_score["cost"]],
        color="green",
        linewidth=10,
    )

    for nb_tasks in cost_range_per_assigned:
        hierarchical_min_cost = get_hierarchical_cost(
            {"assigned": nb_tasks, "cost": cost_range_per_assigned[nb_tasks][0]},
            cumulated_delta,
        )
        ax1.plot(
            [0, max_time],
            [hierarchical_min_cost, hierarchical_min_cost],
            color="gray",
            linewidth=0.5,
        )

    # print("Plotting file " + log_plot_name)
    # plt.savefig(log_plot_name, bbox_inches="tight")
    # plt.close()
    plt.show()


if __name__ == "__main__":
    # Argument is the name of the VROOM log file to plot.
    log_file = "vroom_ls_log.json"
    if len(sys.argv) > 1:
        log_file = sys.argv[1]

    log_plot(log_file)
