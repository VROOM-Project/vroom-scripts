# -*- coding: utf-8 -*-
import json

def solution_indicators(file):
  with open(file, 'r') as sol_file:
    output = json.load(sol_file)
    if('solution' in output
       and 'computing_times' in output['solution']):
      return output['solution']
