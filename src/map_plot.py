#!/usr/bin/env python
# -*- coding: utf-8 -*-
from folium.features import DivIcon
import folium
import json
import sys

# Given a VROOM solution with latlng locations, generates a map of the paths of the vehicles (up to 15 vehicles)
def plot_map_solution(filepath):
    f = open(filepath, 'r+')
    vroom_res = json.load(f)

    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen']
    
    first_step = vroom_res['routes'][0]['steps'][0]
    center_lat = first_step['location'][1]
    center_lng = first_step['location'][0]

    map_center = [center_lat, center_lng]
    map = folium.Map(location=map_center, zoom_start=10)

    for i, path in enumerate(vroom_res['routes']):
        steps = path['steps']        
        coords = []
        for j, point in enumerate(steps):
            current_lat = point['location'][1]
            current_lng = point['location'][0]
            
            folium.Marker(
                    location=(current_lat, current_lng),
                    icon=DivIcon(icon_size=(20,20),
                                icon_anchor=(0,0),
                                html=f'<div style="font-size: 12pt">{(j+1) if j != 0 else "START"}</div>')
                    ).add_to(map)
            
            coords.append((current_lat, current_lng))

        folium.PolyLine(locations=coords, color=colors[i]).add_to(map)

    return map

if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(f"Plotting {f}...")
        mymap = plot_map_solution(f)
        filename = f.split('.')[0]
        mymap.save(f"{filename}_map_plot.html")


