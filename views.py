#!/usr/bin/env python
#
# Copyright 2018 Confuture
#
import json

def ApiVerson(connection):
    data = {'version':'one','author':'confuture'}
    json_data = json.dumps(data)
    return json_data