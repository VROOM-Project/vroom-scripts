#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys
from utils.format_input import write_files
from utils.overpass import node_coordinates_bb, node_coordinates_city

def name_if_present(n):
  if('name' in n['tags']):
    return n['tags']['name']
  else:
    return None

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate problem from an overpass query')
  parser.add_argument('-c', '--city', metavar = 'CITY',
                      help = 'city to restrict overpass query to',
                      default = None)
  parser.add_argument('-o', '--output', metavar = 'OUTPUT',
                      help = 'output file name',
                      default = None)
  parser.add_argument('-k', '--key', metavar = 'KEY',
                      help = 'key value to use in overpass query',
                      default = "amenity")
  parser.add_argument('-v', '--value', metavar = 'VALUE',
                      help = 'comma-separated list of value(s) to use in overpass query',
                      default = "cafe")
  parser.add_argument('--top', metavar = 'TOP',
                      help = 'bounding box max latitude',
                      type = float,
                      default = 48.86),
  parser.add_argument('--bottom', metavar = 'BOTTOM',
                      help = 'bounding box min latitude',
                      type = float,
                      default = 48.85),
  parser.add_argument('--left', metavar = 'LEFT',
                      help = 'bounding box min longitude',
                      type = float,
                      default = 2.37),
  parser.add_argument('--right', metavar = 'RIGHT',
                      help = 'bounding box max longitude',
                      type = float,
                      default = 2.39),
  parser.add_argument('--geojson', action='store_true',
                      help = 'also write a geojson file with all generated points',
                      default = False)
  parser.add_argument('--csv', action='store_true',
                      help = 'also write a csv file with coordinates for all generated points',
                      default = False)

  args = parser.parse_args()

  file_name = args.output;

  values = args.value.split(',')
  values_name = '_'.join(values)

  if args.city is not None:
    if not file_name:
      file_name = args.key + '_' + values_name + '_' + args.city
    nodes = node_coordinates_city(args.key,
                                  values,
                                  args.city)['elements']
  else:
    if not file_name:
      file_name = args.key + '_' + values_name + '_' + str(args.bottom) + '_' + str(args.left) + '_' + str(args.top) + '_' + str(args.right)

    nodes = node_coordinates_bb(args.key,
                                values,
                                [[args.left, args.bottom],
                                 [args.right, args.top]])['elements']

  if len(nodes) < 2:
    print("Too few nodes to format a problem!")
    sys.exit(0)

  lons = map(lambda n: n['lon'], nodes)
  lats = map(lambda n: n['lat'], nodes)
  names = map(lambda n: name_if_present(n), nodes)

  write_files(file_name, lons, lats, names, args.geojson, args.csv)
