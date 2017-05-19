#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, sys
from utils.format_input import write_files
from utils.overpass import amenity_coordinates_bb

def name_if_present(n):
  if('name' in n['tags']):
    return n['tags']['name']
  else:
    return None

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate problem from an overpass query')
  parser.add_argument('-a', '--amenity', metavar = 'AMENITY',
                      help = 'tag value to use in overpass query',
                      default = "cafe")
  parser.add_argument('-o', '--output', metavar = 'OUTPUT',
                      help = 'output file name',
                      default = None)
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
  if not file_name:
    file_name = args.amenity + '_' + str(args.bottom) + '_' + str(args.left) + '_' + str(args.top) + '_' + str(args.right)

  nodes = amenity_coordinates_bb(args.amenity,
                                 [[args.left, args.bottom],
                                  [args.right, args.top]])['elements']

  if len(nodes) < 2:
    print "Too few nodes to format a problem!"
    sys.exit(0)

  lons = map(lambda n: n['lon'], nodes)
  lats = map(lambda n: n['lat'], nodes)
  names = map(lambda n: name_if_present(n), nodes)

  write_files(file_name, lons, lats, names, args.geojson, args.csv)
