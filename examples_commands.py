#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#comm ={"device_name": "hue", 
#       "value": "Kitchen two",
#       "command": "turn_on", 
#       "origin": "app_autolight"}'}
comm = {"device_name":"caja_riego_jardin",
        "value":"jardinera",
        "command":"turn_on",
        "pars":{"tiempo":60},
        "origin":"test" }
message = json.dumps(comm)
r.publish('commands', message)

comm_1 = {"device_name":"caja_riego_jardin",
        "value":"jardinera",
        "command":"turn_off",
        "pars":{},
        "origin":"test" }
message = json.dumps(comm_1)
r.publish('commands', message)

