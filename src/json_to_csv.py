# -*- coding: utf-8 -*-
import json, os, sys
from utils.file import load_json

# Parse a json-formatted input instance and produce a csv file with
# all involved coordinates.

def coord_to_csv(array):
  return str(array[0]) + ',' + str(array[1]) + '\n'

def write_to_csv(input_file):
  input = load_json(input_file)

  lines = []

  for v in input['vehicles']:
    if 'start' in v:
      lines.append(coord_to_csv(v['start']))
    if 'end' in v:
      lines.append(coord_to_csv(v['end']))

  for job in input['jobs']:
    lines.append(coord_to_csv(job['location']))

  output_name = input_file[:input_file.rfind('.json')] + '.csv'
  with open(output_name, 'w') as output_file:
    for l in lines:
      output_file.write(l)

if __name__ == "__main__":
  write_to_csv(sys.argv[1])
