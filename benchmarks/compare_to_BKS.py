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

def nb_jobs(solution):
  jobs = 0
  for r in solution['routes']:
    for s in r['steps']:
      if s['type'] == 'job':
        jobs += 1

  return jobs

def log_comparisons(BKS, files):
  print ','.join(["Instance", "Jobs", "Vehicles", "tightness", "Best known cost", "Assigned jobs", "Used vehicles", "Solution cost", "Unassigned jobs", "Gap (%)", "Computing time (ms)"])

  jobs = []
  vehicles = []
  assigned = []
  unassigned = []
  tightnesses = []
  gaps = []
  computing_times = []
  assigned_jobs = 0
  total_files = len(files)
  job_ok_files = 0
  optimal_sols = 0

  for f in files:
    instance = f[0:f.rfind("_sol.json")]
    instance = instance[instance.rfind('/') + 1:]

    if instance not in BKS:
      total_files -= 1
      continue

    indicators = BKS[instance]

    BK_cost = indicators['best_known_cost']
    nb_job = indicators['jobs']
    jobs.append(nb_job)
    nb_vehicle = indicators['vehicles']
    vehicles.append(nb_vehicle)
    tightness = round(float(indicators['total_amount']) / (nb_vehicle * indicators['capacity']), 3)
    tightnesses.append(tightness)
    line = [
      instance,
      nb_job,
      nb_vehicle,
      tightness,
      BK_cost
    ]

    with open(f, 'r') as sol_file:
      solution = json.load(sol_file)

    if solution['code'] != 0:
      continue

    sol_jobs = nb_jobs(solution)
    assigned.append(sol_jobs)

    line.append(sol_jobs)
    line.append(len(solution['routes']))

    cost = solution['summary']['cost']
    line.append(cost)
    line.append(nb_job - sol_jobs)
    unassigned.append(nb_job - sol_jobs)

    if sol_jobs == nb_job:
      job_ok_files += 1
      gap = 100 * (float(cost) / BK_cost - 1)
      line.append(round(gap, 2))
      gaps.append(gap)
      if cost == BK_cost:
        optimal_sols += 1
    else:
      line.append('')

    computing_time = solution['summary']['computing_times']['loading'] + solution['summary']['computing_times']['solving']
    line.append(computing_time)
    computing_times.append(computing_time)

    print ','.join(map(lambda x: str(x), line))

  print 'Average,' + s_round(np.mean(jobs), 1) + ',' + s_round(np.mean(vehicles), 1) + ',' + s_round(np.mean(tightnesses), 2) + ',' + s_round(np.mean(assigned), 1) + ',,,,' + s_round(np.mean(unassigned), 1) + ',' + s_round(np.mean(gaps), 2) + ',' + s_round(np.mean(computing_times), 0)

  total_jobs = np.sum(jobs)
  assigned_jobs = np.sum(assigned)
  print ','
  print 'Total jobs,' + s_round(total_jobs, 0)
  print 'Total jobs assigned,' + s_round(assigned_jobs, 0) + ',' + s_round(100 * float(assigned_jobs) / total_jobs, 2) + '%'
  print ','
  print 'Instances,' + s_round(total_files, 0)
  print 'All jobs solutions,' + s_round(job_ok_files, 0) + ',' + s_round(100 * float(job_ok_files) / total_files, 2) + '%'
  print 'Optimal solutions,' + s_round(optimal_sols, 0) + ',' + s_round(100 * float(optimal_sols) / total_files, 2) + '%'

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
