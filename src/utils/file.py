# -*- coding: utf-8 -*-
import json

def load_json(file):
  with open(file, 'r') as input_file:
    return json.load(input_file)

def solution_indicators(file):
  output = load_json(file)
  if('summary' in output
     and 'computing_times' in output['summary']):
    return output['summary']
