# -*- coding: utf-8 -*-
import json, os, sys
from utils.file import *

# Produce global indicators from a set of solutions in a given folder.

def global_indicators(files):
  all = {
    'cost': 0,
    'duration': 0,
    'distance': 0,
    'computing_times':{
      'loading': 0,
      'solving': 0,
      'routing': 0,
      'solving_details':{
        'heuristic': 0,
        'local_search': 0
      }
    }
  }

  # We only want to keep global solving details if they are always
  # present.
  has_solving_details = True

  for file in [f for f in files if f.endswith(".json")]:
    indicators = solution_indicators(file)
    if not indicators:
      # No a valid solution file.
      continue

    for key in ['cost', 'duration', 'distance']:
      all[key] += indicators[key]

    for key in ['loading', 'solving', 'routing']:
      if key in indicators['computing_times']:
        # Routing might be absent...
        all['computing_times'][key] += indicators['computing_times'][key]

    has_solving_details &= ('solving_details' in indicators['computing_times'])
    if has_solving_details:
      for key in ['heuristic', 'local_search']:
        all['computing_times']['solving_details'][key] += indicators['computing_times']['solving_details'][key]

  return all;

if __name__ == "__main__":
  folder = sys.argv[1]
  r = global_indicators(map(lambda f: os.path.join(sys.argv[1], f),
                            os.listdir(folder)))

  print folder
  print r

  # CSV values
  size = folder[:folder.find('/')]
  s = ','
  print size, s, r['computing_times']['loading'], s, r['computing_times']['solving'], s, r['computing_times']['routing'], s
