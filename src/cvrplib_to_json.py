#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, sys
from utils.benchmark import *

# Generate a json-formatted problem from a CVRPLIB file.

CVRP_FIELDS = ['NAME',
               'TYPE',
               'COMMENT',
               'DIMENSION',
               'EDGE_WEIGHT_TYPE',
               'CAPACITY',
               'VEHICLES']

def parse_cvrp(input_file):
  with open(input_file, 'r') as f:
    lines = f.readlines()

  # Remember main fields describing the problem type.
  meta = {}
  for s in CVRP_FIELDS:
    data = get_value(s, lines)
    if data:
      meta[s] = data

  # Only support EUC_2D for now.
  if ('EDGE_WEIGHT_TYPE' not in meta) or (meta['EDGE_WEIGHT_TYPE'] != 'EUC_2D'):
    message = 'Unsupported EDGE_WEIGHT_TYPE'
    if ('EDGE_WEIGHT_TYPE' in meta):
      message += ': ' + meta['EDGE_WEIGHT_TYPE']
    message += '.'

    print message
    exit(0)

  meta['DIMENSION'] = int(meta['DIMENSION'])
  meta['CAPACITY'] = int(meta['CAPACITY'])

  # Find start of nodes descriptions.
  node_start = (i for i, s in enumerate(lines) if s.startswith('NODE_COORD_SECTION')).next()

  # Defining all jobs.
  jobs = []
  coords = []

  for i in range(node_start + 1, node_start + 1 + meta['DIMENSION']):
    coord_line = parse_node_coords(lines[i])

    if len(coord_line) < 3:
      # Reaching another section (like DEMAND_SECTION), happens when
      # only jobs are listed in NODE_COORD_SECTION but DIMENSION count
      # include jobs + depot.
      break

    coords.append([float(coord_line[1]), float(coord_line[2])])
    jobs.append({
      'id': int(coord_line[0]),
      'location': [float(coord_line[1]), float(coord_line[2])],
      'location_index': i - node_start - 1
    })

  # Add all job demands.
  total_demand = 0
  demand_start = (i for i, s in enumerate(lines) if s.startswith('DEMAND_SECTION')).next()
  for i in range(demand_start + 1, demand_start + 1 + meta['DIMENSION']):
    demand_line = parse_node_coords(lines[i])

    if len(demand_line) < 2:
      # Same as above in job parsing.
      break

    job_id = int(demand_line[0])
    current_demand = int(demand_line[1])

    for j in jobs:
      # Add demand to relevant job.
      if j['id'] == job_id:
        j['amount'] = [current_demand]
        total_demand += current_demand
        break

  # Find depot description.
  depot_start = (i for i, s in enumerate(lines) if s.startswith('DEPOT_SECTION')).next()

  depot_def = lines[depot_start + 1].strip().split(' ')
  if len(depot_def) == 2:
    # Depot coordinates are provided, we add them at the end of coords
    # list and remember their index.
    depot_loc = [float(depot_def[0]), float(depot_def[1])]
    depot_index = len(coords)
    coords.append(depot_loc)
  else:
    # Depot is one of the existing jobs, we retrieve loc and index in
    # coords, then remove the job.
    depot_id = int(depot_def[0])
    job_index =  (i for i, j in enumerate(jobs) if j['id'] == depot_id).next()
    depot_loc = jobs[job_index]['location']
    depot_index = jobs[job_index]['location_index']
    jobs.pop(job_index)

  matrix = get_matrix(coords)

  if 'VEHICLES' in meta:
    meta['VEHICLES'] = int(meta['VEHICLES'])
    nb_vehicles = meta['VEHICLES']
  else:
    nb_vehicles = 1 + (total_demand / meta['CAPACITY'])

  vehicles = []

  for i in range(nb_vehicles):
    vehicles.append({
      'id': i,
      'start': depot_loc,
      'start_index': depot_index,
      'end': depot_loc,
      'end_index': depot_index,
      'capacity': [meta['CAPACITY']]
    })

  return {'meta': meta, 'vehicles': vehicles, 'jobs': jobs, 'matrix': matrix}

if __name__ == "__main__":
  input_file = sys.argv[1]
  output_name = input_file[:input_file.rfind('.vrp')] + '.json'

  pbl_instance = parse_cvrp(input_file)

  with open(output_name, 'w') as out:
    print 'Writing problem ' + input_file + ' to ' + output_name
    json.dump(pbl_instance, out, indent = 2)

