#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests

DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = "8080"


def table(locs, profile, ip=DEFAULT_IP, port=DEFAULT_PORT):
    url = "http://" + ip + ":" + port + "/ors/v2/matrix/" + profile
    req = requests.post(
        url,
        data=json.dumps({"locations": locs}),
        headers={"Content-type": "application/json"},
    )
    return req.json()
