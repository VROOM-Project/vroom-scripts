#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys
import numpy.random as npr
import json
from utils.format_input import write_files

# Generate a random problem to feed vroom for solving.

def generate_random_problem(size, sw, ne, file_name, uniform, geojson, csv):
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

  write_files(file_name, lons, lats, geojson, csv)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate random problem')
  parser.add_argument('-j', '--jobs', metavar = 'JOBS',
                      help = 'number of jobs to generate',
                      type = int,
                      default = '50')
  parser.add_argument('-o', '--output', metavar = 'OUTPUT',
                      help = 'output file name',
                      default = None)
  parser.add_argument('--top', metavar = 'TOP',
                      help = 'bounding box max latitude',
                      type = float,
                      default = 49.5),
  parser.add_argument('--bottom', metavar = 'BOTTOM',
                      help = 'bounding box min latitude',
                      type = float,
                      default = 48),
  parser.add_argument('--left', metavar = 'LEFT',
                      help = 'bounding box min longitude',
                      type = float,
                      default = 1.4),
  parser.add_argument('--right', metavar = 'RIGHT',
                      help = 'bounding box max longitude',
                      type = float,
                      default = 3.5),
  parser.add_argument('-s', '--seed', metavar = 'SEED',
                      help = 'number used for seeding the random generation',
                      type = int,
                      default = None)
  parser.add_argument('--uniform', action='store_true',
                      help = 'use an uniform distribution (default is normal)',
                      default = False)
  parser.add_argument('--geojson', action='store_true',
                      help = 'also write a geojson file with all generated points',
                      default = False)
  parser.add_argument('--csv', action='store_true',
                      help = 'also write a csv file with coordinates for all generated points',
                      default = False)

  args = parser.parse_args()

  # Set random seed for generation.
  if not args.seed:
    seed = npr.randint(10000)
  else:
    # Avoid troubles with command-line args.
    seed = args.seed
  npr.seed(seed)

  file_name = args.output;
  if not file_name:
    file_name = 'jobs_' + str(args.jobs) + '_seed_' + str(seed)

  generate_random_problem(args.jobs,
                          [args.left, args.bottom],
                          [args.right, args.top],
                          file_name,
                          args.uniform,
                          args.geojson,
                          args.csv)
