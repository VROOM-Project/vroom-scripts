# -*- coding: utf-8 -*-
import json
from utils.csv_stuff import write_to_csv

def format_json_from_locations(locations):
  # Set vehicles.
  instance = {'vehicles': []}
  for i in range(len(locations['vehicles']['coordinates'])):
    instance['vehicles'].append({
      'id': i + 1,
      'start': locations['vehicles']['coordinates'][i],
      'end': locations['vehicles']['coordinates'][i]
    })

    if ('names' in locations['vehicles']) and (locations['vehicles']['names'][i] is not None):
      instance['vehicles'][-1]['startDescription'] = locations['vehicles']['names'][i]
      instance['vehicles'][-1]['endDescription'] = locations['vehicles']['names'][i]

  # Set jobs.
  job_coords = []
  if ('jobs' in locations) and (len(locations['jobs']['coordinates']) > 0):
    job_coords = locations['jobs']['coordinates']
    instance['jobs'] = []

  j = len(job_coords)
  for i in range(j):
    current = {
      'id': i + 1,
      'location': job_coords[i]
    }
    if ('names' in locations['jobs']) and (locations['jobs']['names'][i] is not None):
      current['description'] = locations['jobs']['names'][i]
    instance['jobs'].append(current)

  # Set shipments.
  shipment_coords = []
  if ('shipments' in locations) and (len(locations['shipments']['coordinates']) > 0):
    shipment_coords = locations['shipments']['coordinates']
    instance['shipments'] = []

  s = len(shipment_coords) / 2
  for i in range(s):
    current = {
      'pickup': {
        'id': j + 2 * i + 1,
        'location': shipment_coords[2 * i]
      },
      'delivery': {
        'id': j + 2 * i + 2,
        'location': shipment_coords[2 * i + 1]
      }
    }
    if 'names' in locations['shipments']:
      if locations['shipments']['names'][2 * i] is not None:
        current['pickup']['description'] = locations['shipments']['names'][2 * i]
      if locations['shipments']['names'][2 * i + 1] is not None:
        current['delivery']['description'] = locations['shipments']['names'][2 * i + 1]

    instance['shipments'].append(current)

  return instance

def format_geojson_from_locations(locations):
  geo_content = {
    'type': 'FeatureCollection',
    'features': []
  }

  for key in locations:
    for i in range(len(locations[key]['coordinates'])):
      current = {
        'type': 'Feature',
        'properties': {
          'id': i,
          'status': key,
          'name': key + ' ' + str(i)
        },
        'geometry': {
          'type': 'Point',
          'coordinates': locations[key]['coordinates'][i]
        }
      }
      if ('names' in locations[key]) and (locations[key]['names'][i] is not None):
        # Override if name is known
        current['properties']['name'] = locations[key]['names'][i]

      geo_content['features'].append(current)

  return geo_content

def write_files(file_name, locations, geojson, csv):
  json_input = format_json_from_locations(locations)

  with open(file_name + '.json', 'w') as out:
    print('Writing problem to ' + file_name + '.json')
    json.dump(json_input,
              out,
              indent = 2)
  if geojson:
    with open(file_name + '.geojson', 'w') as out:
      print('Writing geojson file to ' + file_name + '.geojson')
      json.dump(format_geojson_from_locations(locations), out, indent = 2)

  if csv:
    write_to_csv(file_name, json_input)
