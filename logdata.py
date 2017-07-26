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
	r.set('riego', state['devices']['caja_goteo'].state['regar'])
	app_state = {}
	for appname in state['apps']:
		app_state[appname] = state['apps'][appname].status
	r.hmset('apps', app_state)
	return
