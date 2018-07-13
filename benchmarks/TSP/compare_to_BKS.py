# -*- coding: utf-8 -*-
import json, sys, os
import numpy as np

# Compare a set of computed solutions to best known solutions on the
# same problems.

def s_round(v, d):
  if d == 0:
    return str(int(v))
  else:
    return str(round(v, d))

def log_comparisons(BKS, files):
  print ','.join(["Instance", "Jobs", "Vehicles", "Best known cost", "Solution cost", "Gap (%)", "Computing time (ms)"])

  jobs = []
  gaps = []
  computing_times = []

  for f in files:
    instance = f[0:f.rfind("_sol.json")]
    instance = instance[instance.rfind('/') + 1:]

    if instance not in BKS:
      continue

    indicators = BKS[instance]

    BK_cost = indicators['best_known_cost']
    nb_job = indicators['jobs']
    jobs.append(nb_job)

    line = [
      instance,
      nb_job,
      indicators['vehicles'],
      BK_cost
    ]

    with open(f, 'r') as sol_file:
      solution = json.load(sol_file)

    if solution['code'] != 0:
      continue

    cost = solution['summary']['cost']
    line.append(cost)

    gap = 100 * (float(cost) / BK_cost - 1)
    line.append(round(gap, 2))
    gaps.append(gap)

    computing_time = solution['summary']['computing_times']['loading'] + solution['summary']['computing_times']['solving']
    line.append(computing_time)
    computing_times.append(computing_time)

    print ','.join(map(lambda x: str(x), line))

  print ','

  print 'Average,' + s_round(np.mean(jobs), 1) + ',,,,' + s_round(np.mean(gaps), 2) + ',' + s_round(np.mean(computing_times), 0)

  # Percentiles
  print ','
  gaps_percentiles = np.percentile(gaps, [0, 10, 25, 50, 75, 90, 100])
  ct_percentiles = np.percentile(computing_times, [0, 10, 25, 50, 75, 90, 100])
  print ',Gaps,Computing times'
  titles = ['Min', 'First decile', 'Lower quartile', 'Median', 'Upper quartile', 'Ninth decile', 'Max']
  for i in range(len(titles)):
    print titles[i] + ',' + s_round(gaps_percentiles[i], 2) + ',' + s_round(ct_percentiles[i], 0)

if __name__ == "__main__":
  # First argument if the best known solution file.
  with open(sys.argv[1], 'r') as sol_file:
    bks = json.load(sol_file)

  # Remaining arguments are computed solution files to use.
  log_comparisons(bks, sys.argv[2:])
