#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys
import numpy.random as npr
import json
from utils.format_input import write_files

# Generate a random problem to feed vroom for solving.

def generate_random_problem(j, s, v, sw, ne, file_name, uniform, geojson, csv):
  locations = {}

  if uniform:
    # Using uniform distribution with bounding box coordinates.
    v_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
    v_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
    locations['vehicles'] = {
      'coordinates': [[v_lon, v_lat]] * v
    }

    locations['jobs'] = {'coordinates': []}
    for i in range(j):
      j_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
      j_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
      locations['jobs']['coordinates'].append([j_lon, j_lat])

    locations['shipments'] = {'coordinates': []}
    for i in range(2 * s):
      s_lon = round(npr.uniform(sw[0], ne[0], 1)[0], 5)
      s_lat = round(npr.uniform(sw[1], ne[1], 1)[0], 5)
      locations['shipments']['coordinates'].append([s_lon, s_lat])
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

    v_lon = round(npr.normal(mu_lon, sigma_lon, 1)[0], 5)
    v_lat = round(npr.normal(mu_lat, sigma_lat, 1)[0], 5)
    locations['vehicles'] = {
      'coordinates': [[v_lon, v_lat]] * v
    }

    locations['jobs'] = {'coordinates': []}
    for i in range(j):
      j_lon = round(npr.normal(mu_lon, sigma_lon, 1)[0], 5)
      j_lat = round(npr.normal(mu_lat, sigma_lat, 1)[0], 5)
      locations['jobs']['coordinates'].append([j_lon, j_lat])

    locations['shipments'] = {'coordinates': []}
    for i in range(2 * s):
      s_lon = round(npr.normal(mu_lon, sigma_lon, 1)[0], 5)
      s_lat = round(npr.normal(mu_lat, sigma_lat, 1)[0], 5)
      locations['shipments']['coordinates'].append([s_lon, s_lat])

  write_files(file_name, locations, geojson, csv)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate random problem')
  parser.add_argument('-c', '--center', action='store_true',
                      help = 'center vehicles location in the bbox',
                      default = False)
  parser.add_argument('-j', '--jobs', metavar = 'JOBS',
                      help = 'number of jobs to generate',
                      type = int,
                      default = '50')
  parser.add_argument('-s', '--shipments', metavar = 'SHIPMENTS',
                      help = 'number of shipments to generate',
                      type = int,
                      default = '0')
  parser.add_argument('-v', '--vehicles', metavar = 'VEHICLES',
                      help = 'number of vehicles to generate',
                      type = int,
                      default = '5')
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
  parser.add_argument('-r', '--random_seed', metavar = 'RANDOM_SEED',
                      help = 'number used for seeding the random generation',
                      type = int,
                      default = 14)
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
  npr.seed(args.random_seed)

  file_name = args.output;
  j = args.jobs
  s = args.shipments
  v = args.vehicles

  if not file_name:
    file_name = ''
    if(j > 0):
      file_name += 'j_' + str(j) + '_'
    if(s > 0):
      file_name += 's_' + str(s) + '_'

    file_name += 'v_' + str(v) + '_seed_' + str(args.random_seed)

  generate_random_problem(j,
                          s,
                          v,
                          [args.left, args.bottom],
                          [args.right, args.top],
                          file_name,
                          args.uniform,
                          args.geojson,
                          args.csv)
