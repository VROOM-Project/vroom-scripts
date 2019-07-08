# -*- coding: utf-8 -*-
import json
from utils.csv_stuff import write_to_csv

def format_json_from_coordinates(lons, lats, names):
  # Set vehicle start and end.
  vehicles = [
    {
      'id': 0
    }
  ]
  start = [lons[0], lats[0]]
  vehicles[0]['start'] = start
  vehicles[0]['end'] = start
  if names[0] is not None:
    vehicles[0]['startDescription'] = names[0]
    vehicles[0]['endDescription'] = names[0]

  # Set jobs.
  jobs = []
  for i in range(1, len(lons)):
    current = {'id': i, 'location': [lons[i], lats[i]]}
    if names[i] is not None:
      current['description'] = names[i]
    jobs.append(current)

  return {'vehicles': vehicles, 'jobs': jobs}

def format_geojson_from_coordinates(lons, lats, names):
  geo_content = {
    'type': 'FeatureCollection',
    'features': []
  }
  for i in range(len(lons)):
    current = {
        'type': 'Feature',
        'properties': {
          'id': i,
          'status': 'job',
          'name': 'Job ' + str(i)
        },
        'geometry': {
          'type': 'Point',
          'coordinates': [lons[i], lats[i]],
        }
      }
    if names[i] is not None:
      # Override if name is known
      current['properties']['name'] = names[i]

    geo_content['features'].append(current)

  geo_content['features'][0]['properties']['status'] = 'start/end'

  return geo_content

def write_files(file_name, lons, lats, names, geojson, csv):
  json_input = format_json_from_coordinates(lons, lats, names)

  with open(file_name + '.json', 'w') as out:
    print('Writing problem to ' + file_name + '.json')
    json.dump(json_input,
              out,
              indent = 2)
  if geojson:
    with open(file_name + '.geojson', 'w') as out:
      print('Writing geojson file to ' + file_name + '.geojson')
      json.dump(format_geojson_from_coordinates(lons, lats, names), out, indent = 2)

  if csv:
    write_to_csv(file_name, json_input)
