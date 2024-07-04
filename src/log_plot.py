# -*- coding: utf-8 -*-
import json
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import sys

START = "Start"
JOB_ADDITION = "JobAddition"
RUIN = "Ruin"
ROLLBACK = "Rollback"


def generate_log_plot(steps, fig, ax):
    specific_ranks = {"start": [], "job_addition": [], "ruin": [], "rollback": []}

    best_score = steps[0]["score"]
    best_score_rank = 0

    min_cost = min([s["score"]["cost"] for s in steps])
    max_cost = max([s["score"]["cost"] for s in steps])

    assigned_values = sorted(set([s["score"]["assigned"] for s in steps]), reverse=True)
    use_colormap = len(assigned_values) != 1

    if use_colormap:
        max_assigned = max(assigned_values)
        cmap = mpl.cm.viridis
        norm = mpl.colors.BoundaryNorm(
            [max_assigned - v for v in assigned_values], cmap.N
        )
        color_map = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

        fig.colorbar(
            color_map,
            ax=ax,
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
        if event == RUIN:
            specific_ranks["ruin"].append(i)
        if event == ROLLBACK:
            specific_ranks["rollback"].append(i)
        if event == START:
            specific_ranks["start"].append(i)
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

    # Materialize job addition events.
    for i in specific_ranks["job_addition"]:
        time = steps[i]["time"]
        ax.plot(
            [time, time],
            [
                best_score["cost"],
                steps[i]["score"]["cost"],
            ],
            color="gray",
            linewidth=0.5,
        )

    # Materialize rollback events and depth levels.
    for i in specific_ranks["rollback"]:
        time = steps[i]["time"]
        ax.plot(
            [time],
            [steps[i]["score"]["cost"]],
            "o",
            ms=6,
            markerfacecolor="None",
            markeredgecolor="black",
            markeredgewidth=0.8,
        )
        ax.plot(
            [time, time],
            [min_cost, max_cost],
            color="black",
            linewidth=1,
        )

    # Materialize ruin events.
    for i in specific_ranks["ruin"]:
        assert i > 0
        previous_time = steps[i - 1]["time"]
        time = steps[i]["time"]
        ax.add_patch(
            patches.Rectangle(
                (previous_time, min_cost),
                time - previous_time,
                max_cost - min_cost,
                linewidth=0,
                facecolor="oldlace",
            )
        )

    ax.scatter(plot_times, plot_costs, s=4, c=plot_colors, linewidths=0)

    # Best cost
    ax.plot(
        [steps[0]["time"], steps[-1]["time"]],
        [best_score["cost"], best_score["cost"]],
        color="gray",
        linewidth=0.5,
    )

    ax.plot(
        [steps[best_score_rank]["time"]],
        [best_score["cost"]],
        "o",
        ms=12,
        markerfacecolor="None",
        markeredgecolor="green",
        markeredgewidth=1.2,
    )


def log_plot(log_file):
    # log_plot_name = log_file[0 : log_file.rfind(".json")] + ".svg"

    print("Parsing " + log_file)
    with open(log_file, "r") as data_file:
        data = json.load(data_file)

    nb_plots = len(data)
    fig, axes = plt.subplots(
        nb_plots, 1, sharex=True, squeeze=False, figsize=(15, 10 * nb_plots)
    )

    for i, ls_data in enumerate(data):
        generate_log_plot(ls_data["steps"], fig, axes[i][0])
        axes[i][0].tick_params(axis="both", reset=True)

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
