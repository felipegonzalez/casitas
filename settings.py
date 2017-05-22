#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import time
# pubsub redis settings
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# import device types
from devices.xbeebox import XbeeBox
from devices.hue import HueHub
from devices.alarm import Alarm

# connections
conn_names = ['xbee-events']

# home areas
places = ['sala', 'comedor', 'recamara', 'entrada','patio']


# devices
device_settings = {
        'cajasala':{
        'place':'sala',
        'device_type':'xbeebox',
        'dest_addr_long':'0013a20040bf0582'
        },
        'cajarecamara':{
        'place':'recamara',
        'device_type':'xbeebox',
        'dest_addr_long':'0013a20040c45639',
        'children':{'luzchica':'D2'} #pin number
        },
        'hue':{
        'ip_address':'192.168.0.6',
        'place':'home',
        'device_type':'hue',
        'children':{'sala1':'1', 'sala2':'2','recamara1':'3','patio':'4'},
        },
        'ouralarm':{
        'device_type':'alarm',
        'state':'unarmed'
        }
}

# device classes
dev_class = {'xbeebox':XbeeBox, 'hue':HueHub, 'alarm':Alarm}


#state definition, initial
state = {'timestamp':0}
state['light_levels'] = {'sala':0, 'recamara':0, 'patio':200}
state['min_light_levels'] = {'sala':100, 'recamara':100, 'patio':100}
state['last_motion'] = {'sala':time.time(), 'recamara':time.time()}
state['groups_lights'] = {'recamara':{'recamara1':'hue','luzchica':'cajarecamara'}, 
                'sala':{'sala1':'hue', 'sala2':'hue'}}
state['lights'] = ['sala1','sala2','recamara1','luzchica']

#apps_settings = ['app_motion']