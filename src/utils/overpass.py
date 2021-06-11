# -*- coding: utf-8 -*-
import requests


def node_coordinates_bb(key, values, bb):
    req = "http://overpass-api.de/api/interpreter"
    query = "[out:json];("
    for value in values:
        query += "node[" + key + "=" + value + "]"
        query += (
            "("
            + str(bb[0][1])
            + ","
            + str(bb[0][0])
            + ","
            + str(bb[1][1])
            + ","
            + str(bb[1][0])
            + ");"
        )

    query += ");out;"

    return requests.post(req, data=query).json()


def node_coordinates_city(key, values, city):
    req = "http://overpass-api.de/api/interpreter"
    query = "[out:json];"
    query += '( area[name="' + city + '"][admin_level=8]; )->.searchArea;('
    for value in values:
        query += "node[" + key + "=" + value + "]"
        query += "(area.searchArea);"
    query += ");out;"

    return requests.post(req, data=query).json()
