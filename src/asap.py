#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
from utils.asap_helpers import solve_asap
from utils.matrix import add_matrices

# Parse a json-formatted input instance, then apply iterative solving
# strategies to come up with a solution minimizing completion time.


def get_cl_args(args):
    all_args = []
    if args.a:
        for a in args.a:
            all_args.append("-a" + a[0])
    if args.g:
        all_args.append("-g")
    if args.l is not None:
        all_args.append("-l" + str(args.l))
    if args.p:
        for p in args.p:
            all_args.append("-p" + p[0])
    if args.r:
        all_args.append("-r" + args.r)
    if args.t is not None:
        all_args.append("-t " + str(args.t))
    if args.x is not None:
        all_args.append("-x " + str(args.x))

    return all_args


def get_routing(args):
    routing = {"engine": args.r, "profiles": {}}
    if args.a:
        for a in args.a:
            kv = a[0].split(":")
            profile = kv[0]
            host = kv[1]
            if profile not in routing["profiles"]:
                routing["profiles"][profile] = {"host": host}
            else:
                routing["profiles"][profile]["host"] = host

    if args.p:
        for p in args.p:
            kv = p[0].split(":")
            profile = kv[0]
            port = kv[1]
            if profile not in routing["profiles"]:
                routing["profiles"][profile] = {"port": port}
            else:
                routing["profiles"][profile]["port"] = port

    if len(routing["profiles"]) == 0:
        routing["profiles"] = {"car": {"host": "0.0.0.0", "port": "5000"}}

    return routing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        metavar="PROFILE:HOST (=car:0.0.0.0)",
        help="routing server",
        nargs="+",
        action="append",
    )
    parser.add_argument(
        "-g",
        action="store_true",
        help="add detailed route geometry and indicators",
        default=False,
    )
    parser.add_argument(
        "-i",
        metavar="FILE",
        help="read input from FILE rather than from stdin",
        type=argparse.FileType("r"),
        default="-",
    )
    parser.add_argument(
        "-l",
        metavar="LIMIT",
        help="stop solving process after LIMIT seconds",
        type=float,
    )
    parser.add_argument(
        "-o",
        metavar="OUTPUT",
        help="output file name",
        type=argparse.FileType("w"),
        default="-",
    )
    parser.add_argument(
        "-p",
        metavar="PROFILE:PORT (=car:5000)",
        help="routing server port",
        nargs="+",
        action="append",
    )
    parser.add_argument(
        "--pareto-front",
        action="store_true",
        help="generate an array of solutions representing various trade-offs"
        + " between cost and completion time",
        default=False,
    )
    parser.add_argument(
        "--pareto-front-more-solutions",
        action="store_true",
        help="reach out to even more solutions than with --pareto-front",
        default=False,
    )
    parser.add_argument(
        "--pareto-plot-file",
        metavar="PLOT FILE",
        help="plot file name",
        type=str,
        default="",
    )
    parser.add_argument(
        "-r",
        metavar="ROUTER (=osrm)",
        help="osrm or ors",
        type=str,
        default="osrm",
    )
    parser.add_argument(
        "-t",
        metavar="THREADS (=4)",
        help="number of threads to use",
        type=int,
        default=4,
    )
    parser.add_argument(
        "-x",
        metavar="EXPLORE (=5)",
        help="exploration level (0..5)",
        type=int,
        default=5,
    )

    args = parser.parse_args()

    # Read input from file or stdin.
    try:
        data = json.load(args.i)
        # pareto_file = input_file[: input_file.rfind(".json")] + "_pareto.svg"
        try:
            if "matrices" not in data:
                # Embed required matrices prior to solving to avoid
                # duplicate matrix computations.
                add_matrices(data, get_routing(args))

            # Iterative solving approach.
            response = solve_asap(
                {
                    "instance": data,
                    "return_pareto_front": args.pareto_front
                    or args.pareto_front_more_solutions,
                    "pareto_front_more_solution": args.pareto_front_more_solutions,
                    "cl_args": get_cl_args(args),
                    "pareto_plot_file": args.pareto_plot_file,
                }
            )
        except OSError as e:
            response = {"code": e.errno, "error": e.strerror}
    except ValueError as e:
        response = {"code": 2, "error": str(e)}

    json.dump(response, args.o)
    exit(response["code"] if "code" in response else 0)
