#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis


def log(state, r):
	r.hmset('temperature', state['temperature'])
	print(state['temperature'])
	r.hmset('humidity', state['humidity'])
	r.hmset('motion', state['motion'])
	if(len(state['devices_state']['caja_consumo_electrico']) > 0):
		r.hmset('power usage', state['devices_state']['caja_consumo_electrico'])
	print(state['devices_state']['caja_goteo'])
	try:
		r.set('riego', state['devices_state']['caja_goteo']['regar'])
	except:
		pass
	app_state = {}
	for appname in state['apps']:
		app_state[appname] = state['apps'][appname].status
	r.hmset('apps', app_state)
	# Build appliances states
	dev_json = {}
	for dev_name in state['devices_state']:
		dev_json[dev_name] = json.dumps(state['devices_state'][dev_name])
	r.hmset('devices', dev_json)
	if('distancia' in state['devices_state']['caja_cisterna']):
		r.set('Nivel cisterna', state['devices_state']['caja_cisterna']['distancia'])
	return
