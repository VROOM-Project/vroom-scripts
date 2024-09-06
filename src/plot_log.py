# -*- coding: utf-8 -*-
from plot import plot_routes

import json
import math
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import sys

START = "Start"
JOB_ADDITION = "JobAddition"
LOCAL_MINIMA = "LocalMinima"
RUIN = "Ruin"
RECREATE = "Recreate"
ROLLBACK = "Rollback"


def get_title(ls_search, best_score):
    return (
        ";".join(
            [
                ls_search["heuristic"],
                ls_search["init"],
                str(round(ls_search["regret"], 2)),
                ls_search["sort"],
            ]
        )
        + " / assigned: "
        + str(best_score["assigned"])
        + " / cost: "
        + str(best_score["cost"])
    )


def is_smaller_score(a, b):
    return (-a["priority"], -a["assigned"], a["cost"]) < (
        -b["priority"],
        -b["assigned"],
        b["cost"],
    )


def is_equal_score(a, b):
    return (a["priority"], a["assigned"], a["cost"]) == (
        b["priority"],
        b["assigned"],
        b["cost"],
    )


def is_cost_comparable(a, b):
    return (a["priority"], a["assigned"]) == (
        b["priority"],
        b["assigned"],
    )


def generate_log_plot(steps, assigned_values, max_assigned, assigned_boundary, fig, ax):
    specific_ranks = {"start": [], "job_addition": [], "recreate": [], "rollback": []}

    best_score = steps[0]["score"]
    best_score_rank = 0

    min_cost = min([s["score"]["cost"] for s in steps if s["event"] != RUIN])
    max_cost = max([s["score"]["cost"] for s in steps])

    use_colormap = len(assigned_values) != 1

    if use_colormap:
        cmap = mpl.cm.viridis
        norm = mpl.colors.BoundaryNorm(
            assigned_boundary + [assigned_boundary[-1] + 1], cmap.N
        )
        color_map = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

        fig.colorbar(
            color_map,
            ax=ax,
            orientation="vertical",
            label="Missing tasks",
        )

    plot_times = []
    plot_costs = []
    plot_colors = []

    # First pass through steps to store most data.
    for i, s in enumerate(steps):
        # Update best score.
        current_score = s["score"]
        current_cost = current_score["cost"]

        if is_smaller_score(current_score, best_score) or (
            is_equal_score(current_score, best_score) and s["event"] == LOCAL_MINIMA
        ):
            best_score = current_score
            best_score_rank = i

        # First filter high-level LS modification.
        event = s["event"]
        if event == RECREATE:
            specific_ranks["recreate"].append(i)
        if event == ROLLBACK:
            specific_ranks["rollback"].append(i)
        if event == START:
            specific_ranks["start"].append(i)
        if event == JOB_ADDITION:
            specific_ranks["job_addition"].append(i)

        if event != RUIN:
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

    # Materialize R&R phase.
    for i in specific_ranks["recreate"]:
        assert i > 1
        previous_time = steps[i - 2]["time"]
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
        ax.plot(
            [time, time],
            [min_cost, max_cost],
            color="orange",
            linewidth=0.8,
        )
        ax.plot(
            [time],
            [steps[i]["score"]["cost"]],
            "o",
            ms=6,
            markerfacecolor="None",
            markeredgecolor="darkgoldenrod",
            markeredgewidth=0.8,
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

    ax.scatter(plot_times, plot_costs, s=5, c=plot_colors, linewidths=0)

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
        markeredgecolor="limegreen",
        markeredgewidth=1.5,
    )

    ax.xaxis.set_major_formatter(lambda x, pos: str(int(float(x) / 1000)))

    return best_score, best_score_rank


def log_plot(log_data, plot_base_name):
    nb_plots = len(log_data)
    fig, axes = plt.subplots(
        nb_plots, 1, sharex=True, squeeze=False, constrained_layout=True
    )
    fig.set_figwidth(10)
    fig.set_figheight(2 * nb_plots)

    # Decide range for assigned tasks.
    assigned_ranges = [
        sorted(
            set(
                [s["score"]["assigned"] for s in ls_data["steps"] if s["event"] != RUIN]
            ),
            reverse=True,
        )
        for ls_data in log_data
    ]
    merged_ranges = []
    for r in assigned_ranges:
        merged_ranges += r

    common_assigned_ranges = sorted(set(merged_ranges), reverse=True)
    max_assigned = common_assigned_ranges[0]
    assigned_boundary = [max_assigned - v for v in common_assigned_ranges]

    # Handle individual plots and get best scores per search.
    best_scores = []
    best_scores_ranks = []
    for i, ls_data in enumerate(log_data):
        best_score, best_score_rank = generate_log_plot(
            ls_data["steps"],
            assigned_ranges[i],
            max_assigned,
            assigned_boundary,
            fig,
            axes[i][0],
        )

        best_scores.append(best_score)
        best_scores_ranks.append(best_score_rank)

        # axes[i][0].tick_params(axis="both", reset=True)

    # Handle things related to best overall score.
    best_score_overall = best_scores[0]

    for i, score in enumerate(best_scores):
        if is_smaller_score(score, best_score_overall):
            best_score_overall = score
            best_score_rank = i

    for i, ls_data in enumerate(log_data):
        axes[i][0].plot(
            [ls_data["steps"][0]["time"], ls_data["steps"][-1]["time"]],
            [best_score_overall["cost"], best_score_overall["cost"]],
            color="red",
            linewidth=0.5,
        )

        reaches_best = is_equal_score(best_scores[i], best_score_overall)

        gap_str = ""
        if not reaches_best and is_cost_comparable(best_scores[i], best_score_overall):
            gap = 100 * (float(best_scores[i]["cost"]) / best_score_overall["cost"] - 1)
            gap_str = " (+" + str(round(gap, 1)) + "%)"

        axes[i][0].set_title(
            get_title(ls_data, best_scores[i]) + gap_str,
            color="red" if reaches_best else "black",
        )

        if reaches_best:
            axes[i][0].plot(
                [ls_data["steps"][best_scores_ranks[i]]["time"]],
                [best_scores[i]["cost"]],
                "o",
                ms=12,
                markerfacecolor="None",
                markeredgecolor="red",
                markeredgewidth=1.5,
            )

    print("Plotting file " + plot_base_name + ".svg")
    plt.savefig(plot_base_name + ".svg", bbox_inches="tight")
    # plt.show()
    plt.close()


def plot_intermediate_solutions(log_data, plot_base_name):
    for ls_data in log_data:
        h_description = (
            ls_data["heuristic"].lower()
            + "_"
            + ls_data["init"].lower()
            + "_"
            + str(round(ls_data["regret"], 1))
        )
        max_time_ms = ls_data["steps"][-1]["time"]
        nb_digits = math.floor(math.log10(max_time_ms) + 1)
        for step in ls_data["steps"]:
            if "solution" in step:
                sol_base_name = (
                    plot_base_name
                    + "_"
                    + h_description
                    + "_"
                    + str(round(step["time"])).zfill(nb_digits)
                    + "_"
                    + step["event"].lower()
                )
                plot_routes(step["solution"], sol_base_name)


if __name__ == "__main__":
    # Argument is the name of the VROOM log file to plot.
    log_file = "vroom_ls_log.json"
    if len(sys.argv) > 1:
        log_file = sys.argv[1]

    plot_base_name = log_file[0 : log_file.rfind(".json")]

    print("Parsing " + log_file)
    with open(log_file, "r") as data_file:
        log_data = json.load(data_file)

    log_plot(log_data, plot_base_name)

    plot_intermediate_solutions(log_data, plot_base_name)
