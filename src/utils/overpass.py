# -*- coding: utf-8 -*-
import json, requests

def amenity_coordinates_bb(amenity, bb):
  req = 'http://overpass-api.de/api/interpreter'
  query = '[out:json];'
  query += 'node[amenity=' + amenity + ']'
  query += '(' + str(bb[0][1]) + ',' + str(bb[0][0]) + ',' + str(bb[1][1]) + ',' + str(bb[1][0]) + ');out;'

  return requests.post(req, data = query).json()

def amenity_coordinates_area(amenity, area):
  req = 'http://overpass-api.de/api/interpreter'
  query = '[out:json];'
  query += '( area[name="' + area + '"][admin_level=8]; )->.searchArea;'
  query += '(node[amenity=' + amenity + ']'
  query += '(area.searchArea);'
  query += ');out;'

  return requests.post(req, data = query).json()

