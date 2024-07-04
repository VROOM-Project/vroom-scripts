# -*- coding: utf-8 -*-
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
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
    specific_ranks = {"job_addition": [], "ruin": [], "rollback": []}

    best_score = steps[0]["score"]
    best_score_rank = 0

    assigned_values = sorted(set([s["score"]["assigned"] for s in steps]), reverse=True)
    use_colormap = len(assigned_values) != 1

    if use_colormap:
        print(assigned_values)
        max_assigned = max(assigned_values)
        cmap = mpl.cm.viridis
        norm = mpl.colors.BoundaryNorm(
            [max_assigned - v for v in assigned_values], cmap.N
        )
        color_map = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

        fig.colorbar(
            color_map,
            ax=ax1,
            orientation="vertical",
            label="Missing tasks vs best score",
        )

    plot_times = []
    plot_costs = []
    plot_colors = []

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

        # First filter high-level LS modification.
        event = s["event"]
        if (event == RUIN) or (event == ROLLBACK):
            if event == RUIN:
                specific_ranks["ruin"].append(i)
            else:
                specific_ranks["rollback"].append(i)
            continue

        # Moving on into current LS step.
        if event == JOB_ADDITION:
            specific_ranks["job_addition"].append(i)

        plot_times.append(s["time"])
        plot_costs.append(current_cost)
        current_color = (
            color_map.to_rgba(max_assigned - current_score["assigned"])
            if use_colormap
            else "blue"
        )
        plot_colors.append(current_color)

    # Materialize job addition events
    for i in specific_ranks["job_addition"]:
        time = steps[i]["time"]
        ax1.plot(
            [time, time],
            [
                best_score["cost"],
                steps[i]["score"]["cost"],
            ],
            color="gray",
            linewidth=0.5,
        )

    ax1.scatter(plot_times, plot_costs, s=4, c=plot_colors, linewidths=0)

    # Best cost
    ax1.plot(
        [steps[0]["time"], steps[-1]["time"]],
        [best_score["cost"], best_score["cost"]],
        color="gray",
        linewidth=0.5,
    )

    ax1.plot(
        [steps[best_score_rank]["time"]],
        [best_score["cost"]],
        "o",
        ms=10,
        markerfacecolor="None",
        markeredgecolor="green",
        markeredgewidth=1,
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
