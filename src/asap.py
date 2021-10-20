#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
from utils.asap_helpers import solve_asap

# Parse a json-formatted input instance, then apply iterative solving
# strategies to come up with a solution minimizing completion time.


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
    data = json.load(args.i)

    # pareto_file = input_file[: input_file.rfind(".json")] + "_pareto.svg"
    try:
        response = solve_asap(data)
    except OSError as e:
        response = {"code": e.errno, "error": e.strerror}

    json.dump(response, args.o)
    exit(response["code"])
