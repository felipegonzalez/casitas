#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
import pytz
import requests
import math


url_wunder = 'weatherstation.wunderground.com/weatherstation/updateweatherstation.php'
id_wunder = 'ICUERNAV5' 
#pass_wunder= 'A34-Qg6-272-6Jq'
#pass_wunder = '1b3eda3c'
pass_wunder = "valqui1"
url_1 = url_wunder + 'ID='+id_wunder+'&PASSWORD='+pass_wunder

to_utc_zone = tz.tzutc()

def log(state, r):
    r.hmset('temperature', state['temperature'])
    #print(state['temperature'])
    r.hmset('humidity', state['humidity'])
    r.hmset('motion', state['motion'])
    if(len(state['devices_state']['caja_consumo_electrico']) > 0):
        r.hmset('power usage', state['devices_state']['caja_consumo_electrico'])
    #print(state['devices_state']['caja_goteo'])
    try:
        r.set('riego', state['devices_state']['caja_goteo']['regar'])
    except:
        pass
    #app_state = {}
    #for appname in state['apps']:
    #    app_state[appname] = state['apps'][appname].status
    #r.hmset('apps', app_state)
    # Build appliances states
    dev_json = {}
    app_json = {}
    r.delete('apps')
    for dev_name in state['devices_state']:
        dev_json[dev_name] = json.dumps(state['devices_state'][dev_name])
        #dev_json[dev_name]['ts_log'] = str(datetime.now())
    for app_name in state['apps']:
        app_json[app_name] = json.dumps(state['apps'][app_name].state, default=str)
        #app_json[app_name]['ts_log'] = str(datetime.now())
    print(app_json)
    r.hmset('devices', dev_json)
    r.hmset('apps', app_json)
    if('distancia' in state['devices_state']['caja_cisterna']):
        r.set('Nivel cisterna', state['devices_state']['caja_cisterna']['distancia_filtrada'])

    # wu underground updates
    station_data = state['devices_state']['estacion_meteo']
    if(len(station_data) > 0):
        try:
            pressure = float(state['devices_state']['caja_pasillo_comedor']['pressure'])
            pressure_hg = pressure / 33.863887
            rh = float(station_data['humidity'])
            tc = float(station_data['temperature'])
            gamma = math.log((rh/100)*math.exp((18.678-tc/234.5)*tc/(257.14+tc)))
            dp = 257.14*gamma/(18.678-gamma)
            dewptf = dp*(9.0/5.0) +32.0
            
            date_report = parse(station_data['date']).replace(tzinfo = tz.gettz("America/Mexico_City"))
            #print(date_report)
            #print(date_report.astimezone(pytz.utc))
            date_utc = date_report.astimezone(pytz.utc)
            temp = float(station_data['temperature'])*(9.0/5.0)+32.0
            pars_get = {'ID':id_wunder, 'PASSWORD':pass_wunder,
                'dateutc':'now', 'tempf': temp, 'humidity': float(station_data['humidity']),
                'windspeedmph':float(station_data['wind_speed'])/1.60934, 
                'winddir':float(station_data['wind_direction']),
                'dewptf' : round(dewptf,2) ,'baromin':pressure_hg}
            new_message = json.dumps({'device_name':'logger', 'address':url_wunder, 
                'payload':'', 'pars':pars_get, 'type':'get'})
            r.publish("http-commands", new_message)
        except Exception as ex:
            print("Failed to parse/send weather station data")

    return
