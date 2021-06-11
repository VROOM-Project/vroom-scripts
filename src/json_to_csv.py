#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from utils.file import load_json
from utils.csv_stuff import write_to_csv

# Parse a json-formatted input instance and produce a csv file with
# all involved coordinates in Lat,Lng order.

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = input_file[: input_file.rfind(".json")]

    write_to_csv(output_name, load_json(input_file))
