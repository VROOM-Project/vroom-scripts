#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import subprocess


def solve(data):
    str_data = json.dumps(data)
    try:
        result = subprocess.check_output(["vroom", str_data])
    except subprocess.CalledProcessError as e:
        # Some error reported by vroom
        json_error = json.loads(e.output)
        raise OSError(json_error["code"], json_error["error"])

    return json.loads(result)
