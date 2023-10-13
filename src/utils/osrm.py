#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = "5000"


def format_request(service, locs, ip=DEFAULT_IP, port=DEFAULT_PORT):
    req = "http://" + ip + ":" + port + "/"
    req += service + "/v1/car/"
    for loc in locs:
        req += str(loc[0]) + "," + str(loc[1]) + ";"

    return req[:-1]


def route(locs, extra_args="", ip=DEFAULT_IP, port=DEFAULT_PORT):
    # Building request.
    req = format_request("route", locs, ip, port)

    req += "?alternatives=false&steps=false&overview=full&continue_straight=false"
    req += extra_args

    return requests.get(req).json()


def table(locs, ip=DEFAULT_IP, port=DEFAULT_PORT):
    req = format_request("table", locs, ip, port)

    req += "?annotations=duration,distance"

    return requests.get(req).json()
