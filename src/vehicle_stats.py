# -*- coding: utf-8 -*-
import json, sys
import numpy as np

# Report simple stats on vehicle usage in a solution.

def s_round(v, d):
  if d == 0:
    return str(int(v))
  else:
    return str(round(v, d))

def generate_stats(input_file, sol_file):
  with open(input_file, 'r') as data:
    problem = json.load(data)

  with open(sol_file, 'r') as data:
    solution = json.load(data)

  amount_size = 0
  if 'delivery' in solution['summary']:
    amount_size = len(solution['summary']['delivery'])

  headers = [
    "vehicle",
    "start",
    "end",
    "working_time",
    "service_rate",
    "travel_rate",
    "waiting_rate",
    "working_ratio"
  ]
  if (amount_size > 0):
    headers.append("max_load")

  if (amount_size > 1):
    headers += (amount_size - 1) * [""]
  if (amount_size > 0):
    headers.append("max_load_ratio")

  if (amount_size > 1):
    headers += (amount_size - 1) * [""]

  print(','.join(headers))

  starts = []
  ends = []
  working_times = []
  service_rates = []
  travel_rates = []
  waiting_rates = []
  working_ratios  = []
  max_loads  = []
  max_load_ratios  = []

  for route in solution['routes']:
    v_id = route['vehicle']
    current = [str(v_id)]

    start = route['steps'][0]['arrival']
    current.append(str(start))
    starts.append(start)

    end = route['steps'][-1]['arrival']
    if ('service' in route['steps'][-1]):
      end += route['steps'][-1]['service']
    current.append(str(end))
    ends.append(end)

    working_time = end - start
    current.append(str(working_time))
    working_times.append(working_time)

    service_rate = 100 * float(route['service']) / working_time
    current.append(str(round(service_rate, 1)))
    service_rates.append(service_rate)

    travel_rate = 100 * float(route['duration']) / working_time
    current.append(str(round(travel_rate, 1)))
    travel_rates.append(travel_rate)

    waiting_rate = 100 * float(route['waiting_time']) / working_time
    current.append(str(round(waiting_rate, 1)))
    waiting_rates.append(waiting_rate)

    v = next(v for v in problem['vehicles'] if v['id'] == v_id)
    if ('time_window' in v):
      available_time = v['time_window'][1] - v['time_window'][0]
      working_ratio = 100 * float(working_time) / available_time
      current.append(s_round(working_ratio, 1))
      working_ratios.append(working_ratio)
    else:
      current.append("")

    if (amount_size > 0):
      max_load = amount_size * [0]
      for step in route['steps']:
        for i in range(amount_size):
          if (max_load[i] < step['load'][i]):
            max_load[i] = step['load'][i]
      current += map(lambda l: str(l), max_load)
      max_loads.append(max_load)

      max_load_ratio = []
      for i in range(amount_size):
        max_load_ratio.append(100 * float(max_load[i]) / v['capacity'][i])

      current += map(lambda r: s_round(r, 1), max_load_ratio)
      max_load_ratios.append(max_load_ratio)

    print(','.join(current))

  print(',')
  averages = [
    'Average',
    s_round(np.mean(starts), 0),
    s_round(np.mean(ends), 0),
    s_round(np.mean(working_time), 0),
    s_round(np.mean(service_rate), 1),
    s_round(np.mean(travel_rate), 1),
    s_round(np.mean(waiting_rate), 1),
    s_round(np.mean(working_ratio), 1)
  ]

  if (amount_size > 0):
    for i in range(amount_size):
      averages.append(s_round(np.mean([load[i] for load in max_loads]), 0))
    for i in range(amount_size):
      averages.append(s_round(np.mean([load[i] for load in max_load_ratios]), 1))

  print(','.join(averages))

if __name__ == "__main__":
  # Arguments are the name of the input and solution files.
  input_file = sys.argv[1]
  sol_file = sys.argv[2]
  generate_stats(input_file, sol_file)
