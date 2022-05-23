#-*- coding: utf-8 -*-
import json
from xmlrpc.client import MAXINT
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import sys
import numpy as np

# Very simple plot for a VROOM solution file.

colors_blacklist = [
    "whitesmoke",
    "white",
    "snow",
    "mistyrose",
    "seashell",
    "linen",
    "bisque",
    "antiquewhite",
    "blanchedalmond",
    "papayawhip",
    "wheat",
    "oldlace",
    "floralwhite",
    "cornsilk",
    "lemonchiffon",
    "aliceblue",
    "ivory",
    "beige",
    "lightyellow",
    "lightgoldenrodyellow",
    "honeydew",
    "mintcream",
    "azure",
    "lightcyan",
    "aliceblue",
    "ghostwhite",
    "lavender",
    "lavenderblush",
]

def plot_schedules(sol_file_name):
    plot_file_name = sol_file_name[0 : sol_file_name.rfind(".json")] + "_gantt.svg"

    print("Parsing " + sol_file_name)
    with open(sol_file_name, "r") as sol_file:
        solution = json.load(sol_file)

    color_list = []
    for name, hex in clrs.cnames.items():
        if name not in colors_blacklist:
            color_list.append(name)
    
    fig, ax1 = plt.subplots(1, 1)
    fig.set_figwidth(15)
    plt.subplots_adjust(left=0.03, right=1, top=1, bottom=0.05, wspace=0.03)

    if "routes" not in solution:
        return

    t = 0
    dt = 0
    n = solution["routes"][-1]["vehicle"]

    for route in solution["routes"]:
        t = route["steps"][0]["arrival"]
        d1, d2 = 0, 0
        for step in route["steps"]:
            dt = step["waiting_time"]
            t += dt
            d1, d2 = d2, step["duration"]
            dt = d2 - d1
            ax1.hlines(y = route["vehicle"], xmin = t, xmax = t + dt, colors = color_list[route["vehicle"] % len(color_list)])
            t += dt
            dt = step["setup"]
            ax1.hlines(y = route["vehicle"], xmin = t, xmax = t + dt, colors = color_list[route["vehicle"] % len(color_list)], linewidth = 5)
            t += dt
            dt = step["service"]
            if step["type"] in ["job", "pickup", "delivery"]:
                ax1.vlines(x = t, ymin = (route["vehicle"])-0.5+5/(n+10), ymax = route["vehicle"]+0.5-5/(n+10), colors = color_list[route["vehicle"] % len(color_list)])
                ax1.hlines(y = route["vehicle"], xmin = t, xmax = t + dt, colors = color_list[route["vehicle"] % len(color_list)], linewidth = 5)
            t += dt

    computing_time = solution["summary"]["computing_times"]["loading"]
    computing_time += solution["summary"]["computing_times"]["solving"]
    if "routing" in solution["summary"]["computing_times"]:
        computing_time += solution["summary"]["computing_times"]["routing"]

    title = plot_file_name[: plot_file_name.rfind(".")]
    title += " ; cost: " + str(solution["summary"]["cost"])
    title += " ; computing time: " + str(computing_time)
    title += "ms"
    ax1.set_title(title)
    
    print("Plotting file " + plot_file_name)
    plt.savefig(plot_file_name, bbox_inches="tight")
    plt.close()
    # plt.show()

if __name__ == "__main__":
    # Argument is the name of the solution fils to plot.
    for f in sys.argv[1:]:
        plot_schedules(f)