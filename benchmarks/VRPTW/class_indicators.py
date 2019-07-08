# -*- coding: utf-8 -*-
import json, sys, os
import numpy as np

# Retrieve cumulated number of vehicle (CNV) and cumulated travel time
# (CTT) per class.

# See src/vrptw_to_json.py
VRPTW_PRECISION = 1000

CLASSES = ['C1', 'C2', 'R1', 'R2', 'RC1', 'RC2']

def s_round(v, d):
  if d == 0:
    return str(int(v))
  else:
    return str(round(v, d))

def get_class(file_name):
  number_index = 1

  if file_name[0:2].upper() == 'RC':
    number_index = 2

  return file_name[0:number_index].upper() + file_name[number_index]

def log_indicators(BKS, files):
  CNV = {}
  CTT = {}
  BKS_CNV = {}
  BKS_CTT = {}

  for c in CLASSES:
    CNV[c] = []
    CTT[c] = []
    BKS_CNV[c] = []
    BKS_CTT[c] = []

  computing_times = []

  for f in files:
    instance = f[0:f.rfind("_sol.json")]
    instance = instance[instance.rfind('/') + 1:]

    if instance not in BKS and instance + '_distance' not in BKS:
      continue

    with open(f, 'r') as sol_file:
      solution = json.load(sol_file)

    if solution['code'] != 0 or len(solution['unassigned']) > 0:
      continue

    instance_class = get_class(instance)

    if instance + '_distance' in BKS:
      # Specific entry for approach targeting distance as optimization
      # objective.
      indicators = BKS[instance + '_distance']
    else:
      indicators = BKS[instance]

    BKS_CNV[instance_class].append(indicators['solved_with_vehicles'])
    BKS_CTT[instance_class].append(indicators['best_known_cost'])

    CNV[instance_class].append(len(solution['routes']))
    CTT[instance_class].append(solution['summary']['cost'])

    computing_times.append(solution['summary']['computing_times']['loading'] + solution['summary']['computing_times']['solving'])

  # Output
  print(',' + ','.join(CLASSES) + ',' + 'Total')

  cumulated_BKS_CNV = 0
  bks_cnv_line = 'BKS CNV,'
  for c in CLASSES:
    bks_cnv_line += s_round(np.mean(BKS_CNV[c]), 2) + ','
    cumulated_BKS_CNV += sum(BKS_CNV[c])
  print(bks_cnv_line + s_round(cumulated_BKS_CNV, 0))

  cumulated_BKS_CTT = 0
  bks_ctt_line = 'BKS CTT,'
  for c in CLASSES:
    bks_ctt_line += s_round(np.mean(BKS_CTT[c]), 2) + ','
    cumulated_BKS_CTT += sum(BKS_CTT[c])
  print(bks_ctt_line + s_round(cumulated_BKS_CTT, 0))

  cumulated_CNV = 0
  cnv_line = 'CNV,'
  for c in CLASSES:
    cnv_line += s_round(np.mean(CNV[c]), 2) + ','
    cumulated_CNV += sum(CNV[c])
  print(cnv_line + s_round(cumulated_CNV, 0))

  cumulated_CTT = 0
  ctt_line = 'CTT,'
  for c in CLASSES:
    ctt_line += s_round(np.mean(CTT[c]) / VRPTW_PRECISION, 2) + ','
    cumulated_CTT += sum(CTT[c])
  print(ctt_line + s_round(cumulated_CTT / VRPTW_PRECISION, 0))

  # Computing time percentiles
  print(',')
  ct_percentiles = np.percentile(computing_times, [0, 10, 25, 50, 75, 90, 100])
  print(',Computing times')
  print('Average,' + s_round(np.mean(computing_times), 0))
  print(',')

  titles = ['Min', 'First decile', 'Lower quartile', 'Median', 'Upper quartile', 'Ninth decile', 'Max']
  for i in range(len(titles)):
    print(titles[i] + ',' + s_round(ct_percentiles[i], 0))

if __name__ == "__main__":
  # First argument if the best known solution file.
  with open(sys.argv[1], 'r') as sol_file:
    bks = json.load(sol_file)

  # Remaining arguments are computed solution files to use.
  log_indicators(bks, sys.argv[2:])
