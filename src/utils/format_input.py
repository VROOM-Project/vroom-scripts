# -*- coding: utf-8 -*-
import json
from utils.csv_stuff import write_to_csv

def format_json_from_coordinates(lons, lats):
  # Set vehicle start and end.
  vehicles = [
    {
      'id': 0
    }
  ]
  start = [lons[0], lats[0]]
  vehicles[0]['start'] = start
  vehicles[0]['end'] = start

  # Set jobs.
  jobs = []
  for i in range(1, len(lons)):
    jobs.append({'id': i, 'location': [lons[i], lats[i]]})

  return {'vehicles': vehicles, 'jobs': jobs}

def format_geojson_from_coordinates(lons, lats):
  geo_content = {
    'type': 'FeatureCollection',
    'features': []
  }
  for i in range(len(lons)):
    geo_content['features'].append(
      {
        'type': 'Feature',
        'properties': {
          'id': i,
          'name': 'Job ' + str(i)
        },
        'geometry': {
          'type': 'Point',
          'coordinates': [lons[i], lats[i]],
        }
      })
  geo_content['features'][0]['properties']['name'] = 'Vehicle start/end'

  return geo_content

def write_files(file_name, lons, lats, geojson, csv):
  json_input = format_json_from_coordinates(lons, lats)

  with open(file_name + '.json', 'w') as out:
    print 'Writing problem to ' + file_name + '.json'
    json.dump(json_input,
              out,
              indent = 2)
  if geojson:
    with open(file_name + '.geojson', 'w') as out:
      print 'Writing geojson file to ' + file_name + '.geojson'
      json.dump(format_geojson_from_coordinates(lons, lats), out, indent = 2)

  if csv:
    write_to_csv(file_name, json_input)
