#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os
from bs4 import BeautifulSoup

def get_vehicles_data(lines, data):
  while len(lines) > 0:
    l = lines.pop(0).strip()
    if len(l) == 0 or 'NUMBER' in l:
      continue
    elif 'CUSTOMER' in l or 'CUST NO.' in l:
      lines.insert(0, l)
      break
    else:
      x = l.split()
      if len(x) < 2:
        print "Cannot understand line: " + l + ": too few columns."
        exit(2)
      data['n_vehicles'] = int(x[0]);
      data['capacity'] = int(x[1]);

def get_amounts(lines):
  amounts = []
  while len(lines) > 0:
    l = lines.pop(0).strip()
    if len(l) == 0 or 'CUST' in l:
      continue
    else:
      x = l.split()
      if len(x) < 7:
        print "Cannot understand line: " + l + ": too few columns."
        exit(2)
      #some guys use '999' entry as terminator sign and others don't
      elif '999' in x[0] and len(amounts) < 999:
        break
      amounts.append(int(float(x[3])))
  return amounts

def get_problem_data(input_file):
  with open(input_file, 'r') as f:
    lines = f.readlines()

  data = {}

  while len(lines) > 0:
    l = lines.pop(0);
    if 'VEHICLE' in l:
      get_vehicles_data(lines, data)
    elif 'CUSTOMER' in l or 'CUST ' in l or '#NUM' in l:
      break

  amounts = get_amounts(lines)
  amounts.pop(0)

  total_amount = 0
  for a in amounts:
    total_amount += a;

  if 'n_vehicles' not in data:
    data['n_vehicles'] = 1
  if 'capacity' not in data:
    data['capacity'] = total_amount
  data['n_jobs'] = len(amounts)
  data['total_amount'] = total_amount

  return data

def build_homberger(problem_dir, file):
  print 'Building BKS from ' + problem_dir + ' and ' + file + '...'

  with open(file) as f:
    doc = BeautifulSoup(f, "lxml")

  rows = doc.tbody.find_all('tr')
  rows.pop(0)

  bks = {}

  for r in rows:
    #print r
    td = r.find_all('td')

    if len(td) == 6 or len(td) == 5:
      name = td[0].text
      if not name[-1].isdigit():
        name = name[:-1]

      problem_file = problem_dir + '/' + name + ".txt"
      pd = get_problem_data(problem_file)

      bks[name] = {
        'jobs': pd['n_jobs'],
        'vehicles': pd['n_vehicles'],
        'capacity': pd['capacity'],
        'total_amount': pd['total_amount'],
        'best_known_cost': float(td[2].text.replace(',', '.')),
        'solved_with_vehicles': int(td[1].text),
        'comment': td[-1].text.strip(),
        'problem_file': problem_file
        #'class': 'noname',
        #'proven_optimal': True
      }

      if td[0].a:
        href = td[0].a.get('href')
      elif td[-1].a:
        href = td[-1].a.get('href')

      if href:
        p = href.split('/')
        bks[name]['solution_file'] = problem_dir + '-solutions/' + p[-1] + '.solution'

  #print json.dumps(bks, indent=4, separators=(',', ': '))
  return bks

def build_solomon(problem_dir, file):
  print 'Building BKS from ' + problem_dir + ' and ' + file + '...'

  with open(file) as f:
    doc = BeautifulSoup(f, "lxml")

  rows = doc.table.find_all('tr')
  rows.pop(0)

  bks = {}

  def make_bks(problem_dir, name, nv, bk_cost, comment):
    name = name.strip()
    nv = nv.strip()

    if len(nv) == 0:
      return

    problem_file = problem_dir + '/' + name + ".txt"
    pd = get_problem_data(problem_file)

    bks[name] = {
      'jobs': pd['n_jobs'],
      'vehicles': pd['n_vehicles'],
      'capacity': pd['capacity'],
      'total_amount': pd['total_amount'],
      'best_known_cost': float(bk_cost.strip()),
      'solved_with_vehicles': int(nv),
      'comment': comment.strip(),
      'problem_file': problem_file
    }

  for r in rows:
    #print r
    td = r.find_all('td')

    if len(td) == 8:
      make_bks(problem_dir, td[0].text, td[1].text, td[2].text, td[3].text)
      make_bks(problem_dir, td[4].text, td[5].text, td[6].text, td[7].text)

  #print json.dumps(bks, indent=4, separators=(',', ': '))
  return bks

def build_tsptw(problem_dir, solution_dir):
  print 'Building BKS from ' + problem_dir + ' and ' + solution_dir + '...'

  bks = {}

  files = os.listdir(solution_dir)

  for f in files:
    name = os.path.splitext(f)[0]

    problem_file = problem_dir + '/' + name
    solution_file = solution_dir + '/' + name + '.solution'

    pd = get_problem_data(problem_file)

    with open(solution_file, 'r') as f:
      lines = f.readlines()

    comment = lines[0]
    bk_cost = lines[-1]

    bks[name] = {
      'jobs': pd['n_jobs'],
      'vehicles': pd['n_vehicles'],
      'capacity': pd['capacity'],
      'total_amount': pd['total_amount'],
      'best_known_cost': float(bk_cost.strip()),
      'solved_with_vehicles': 1,
      'comment': comment.strip(),
      'problem_file': problem_file,
      'solution_file': solution_file
    }

  #print json.dumps(bks, indent=4, separators=(',', ': '))
  return bks

if __name__ == "__main__":

  bks = {}

  bks.update(build_tsptw('TSPTW/ins', 'TSPTW/solution'))

  bks.update(build_solomon('VRPTW/solomon', 'VRPTW/solomon_r1r2-solutions.html'))
  bks.update(build_solomon('VRPTW/solomon', 'VRPTW/solomon_c1c2-solutions.html'))
  bks.update(build_solomon('VRPTW/solomon', 'VRPTW/solomon_rc12-solutions.html'))
  bks.update(build_solomon('VRPTW/solomon', 'VRPTW/solomon_heuristi-solutions.html'))

  bks.update(build_homberger('VRPTW/homberger', 'VRPTW/homberger_200-solutions.html'))
  bks.update(build_homberger('VRPTW/homberger', 'VRPTW/homberger_400-solutions.html'))
  bks.update(build_homberger('VRPTW/homberger', 'VRPTW/homberger_600-solutions.html'))
  bks.update(build_homberger('VRPTW/homberger', 'VRPTW/homberger_800-solutions.html'))
  bks.update(build_homberger('VRPTW/homberger', 'VRPTW/homberger_1000-solutions.html'))

  #print json.dumps(bks, indent=4, separators=(',', ': '))
  #exit(0)

  output_name = 'BKS.json'
  with open(output_name, 'w') as out:
    out.write(json.dumps(bks, indent=2, separators=(',', ': ')))
