#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis


def log(state, r):
	r.hmset('temperature', state['temperature'])
	print(state['temperature'])
	r.hmset('humidity', state['humidity'])
	return
