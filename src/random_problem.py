#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys
import numpy.random as npr
import json

# Generate a random problem to feed vroom for solving.

def get_coordinates(input):
  return map(lambda x: float(x), input.split(','))

def generate_random_problem(size, sw, ne, file_name, uniform):
  # Avoid troubles with command-line args.
  size = int(size)

  vehicles = [
    {
      'id': 0
    }
  ]

  if uniform:
    # Using uniform distribution with bounding box coordinates.
    lons = map(lambda x: round(x, 5), npr.uniform(sw[0], ne[0], size + 1))
    lats = map(lambda x: round(x, 5), npr.uniform(sw[1], ne[1], size + 1))
  else:
    # Using normal distribution, with mean centered wrt the bounding
    # box.
    mu_lon = (sw[0] + ne[0]) / 2
    mu_lat = (sw[1] + ne[1]) / 2
    # Define sigma so that the bounding box correspond to the interval
    # [mu - 3 * sigma ; mu + 3 * sigma], where 99.7% of the random
    # generated data lies.
    sigma_lon = (ne[0] - mu_lon) / 3
    sigma_lat = (ne[1] - mu_lat) / 3

    lons = map(lambda x: round(x, 5), npr.normal(mu_lon, sigma_lon, size + 1))
    lats = map(lambda x: round(x, 5), npr.normal(mu_lat, sigma_lat, size + 1))

  # Set vehicle start and end.
  start = [lons[0], lats[0]]
  vehicles[0]['start'] = start
  vehicles[0]['end'] = start

  # Set jobs.
  jobs = []
  for i in range(1, len(lons)):
    jobs.append({'id': i, 'location': [lons[i], lats[i]]})

  # Write output file
  with open(file_name + '.json', 'w') as out:
    print 'Writing problem to ' + file_name
    json.dump({'vehicles': vehicles, 'jobs': jobs},
              out,
              indent = 2)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate random problem')
  parser.add_argument('-j', '--jobs', metavar = 'JOBS',
                      help = 'number of jobs to generate',
                      default = '50')
  parser.add_argument('-o', '--output', metavar = 'OUTPUT',
                      help = 'output file name',
                      default = None)
  parser.add_argument('--sw', metavar = 'SW',
                      help = 'south-west coords for desired bounding box',
                      default = '1.4,48')
  parser.add_argument('--ne', metavar = 'SW',
                      help = 'north-east coords for desired bounding box',
                      default = '3.5,49.5')
  parser.add_argument('-s', '--seed', metavar = 'SEED',
                      help = 'number used for seeding the random generation',
                      default = None)
  parser.add_argument('--uniform', action='store_true',
                      help = 'use an uniform distribution (default is normal)',
                      default = False)

  args = parser.parse_args()

  sw = get_coordinates(args.sw)
  ne = get_coordinates(args.ne)

  # Set random seed for generation.
  if not args.seed:
    seed = npr.randint(10000)
  else:
    # Avoid troubles with command-line args.
    seed = int(args.seed)
  npr.seed(seed)

  file_name = args.output;
  if not file_name:
    file_name = 'jobs_' + str(args.jobs) + '_seed_' + str(seed)

  generate_random_problem(args.jobs,
                          sw,
                          ne,
                          file_name,
                          args.uniform)
