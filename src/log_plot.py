# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import sys

JOB_ADDITION = "JobAddition"
RUIN = "Ruin"
ROLLBACK = "Rollback"


def log_plot(log_file):
    # log_plot_name = log_file[0 : log_file.rfind(".json")] + ".svg"

    print("Parsing " + log_file)
    with open(log_file, "r") as data_file:
        data = json.load(data_file)

    fig, ax1 = plt.subplots(1, 1)
    fig.set_figwidth(15)

    steps = data[0]["steps"]
    specific_times = {"job_addition": [], "ruin": [], "rollback": []}

    times_chunks = [[]]
    costs_chunks = [[]]

    best_score = steps[0]["score"]
    best_score_rank = 0

    for i, s in enumerate(steps):
        # Update best score.
        current_score = s["score"]
        if (
            -current_score["priority"],
            -current_score["assigned"],
            current_score["cost"],
        ) < (-best_score["priority"], -best_score["assigned"], best_score["cost"]):
            best_score = current_score
            best_score_rank = i

        # First filter high-level LS modification.
        event = s["event"]
        if (event == RUIN) or (event == ROLLBACK):
            if event == RUIN:
                specific_times["ruin"].append(s["time"])
            else:
                specific_times["rollback"].append(s["time"])

            # Start new chunk for plotting.
            times_chunks.append([])
            costs_chunks.append([])
            continue

        # Moving on into current LS step.
        if event == JOB_ADDITION:
            specific_times["job_addition"].append(s["time"])

        times_chunks[-1].append(s["time"])
        costs_chunks[-1].append(s["score"]["cost"])

    assert len(times_chunks) == len(costs_chunks)

    print(specific_times)

    for i in range(len(times_chunks)):
        ax1.plot(times_chunks[i], costs_chunks[i], color="blue")

    ax1.plot(
        [steps[0]["time"], steps[-1]["time"]],
        [best_score["cost"], best_score["cost"]],
        color="green",
    )

    # Materialize job addition events
    for i in specific_times["job_addition"]:
        time = steps[i]["time"]
        low = min(best_score["cost"], steps[i]["score"]["cost"])
        high = max(best_score["cost"], steps[i]["score"]["cost"])
        ax1.plot([time, time], [low, high], color="red")

    print(best_score_rank)
    print(best_score)
    ax1.scatter(
        [steps[best_score_rank]["time"]],
        [best_score["cost"]],
        color="green",
        linewidth=10,
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
