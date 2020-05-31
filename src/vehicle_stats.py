# -*- coding: utf-8 -*-
import json, sys, numpy

# Report simple stats on vehicle usage in a solution.

def generate_stats(input_file, sol_file):
  with open(input_file, 'r') as data:
    problem = json.load(data)

  with open(sol_file, 'r') as data:
    solution = json.load(data)

  print(','.join(["vehicle", "start", "end", "working_time", "service_rate", "travel_rate", "waiting_rate", "working_ratio"]))

  starts = []
  ends = []
  working_times = []
  service_rates = []
  travel_rates = []
  waiting_rates = []
  working_ratios  = []

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
      current.append(str(round(working_ratio, 1)))
      working_ratios.append(working_ratio)
    else:
      current.append("")

    print(','.join(current))

if __name__ == "__main__":
  # Arguments are the name of the input and solution files.
  input_file = sys.argv[1]
  sol_file = sys.argv[2]
  generate_stats(input_file, sol_file)
