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
places = ['sala', 'bano_visitas']


# devices
device_settings = {
        'cajasala':{
        'place':'sala',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf0582'
        },
        'caja_bano_visitas':{
        'place':'bano_visitas',
        'device_type':'xbeebox',
        'addr_long':'0013a20040caaddc',
        'pins':{'dio-1':'motion'}
        },
        'caja_bano_principal':{
        'place':'bano_principal',
        'device_type':'xbeebox',
        'addr_long':'0013a20040c2833b',
        'pins':{'dio-1':'motion'}
        },
        #cajarecamara':{
        #'place':'recamara',
        #'device_type':'xbeebox',
        #'addr_long':'0013a20040c45639',
        #'children':{'luzchica':'D2'} #pin number
        #},
        'hue':{
        'ip_address':'192.168.100.203',
        'place':'home',
        'device_type':'hue',
        'children':{'Living room foot 1':'49', 'Living room foot 2':'50',
        'Downstairs bath 1':'37' ,'Main bath one':'57'},
        },
        'ouralarm':{
        'device_type':'alarm',
        'state':'unarmed'
        }
}
#xbee_dict
xbee_dict = {}
for key in device_settings.keys():
        if(device_settings[key]['device_type'] == 'xbeebox'):
                xbee_dict[device_settings[key]['addr_long']] = key


# device classes
dev_class = {'xbeebox':XbeeBox, 'hue':HueHub, 'alarm':Alarm}


#state definition, initial
state = {'timestamp':0}
state['photo'] = {'sala':0, 'bano_visitas':0, 'bano_principal':0}
state['min_photo'] = {'sala':100, 'bano_visitas':100, 'bano_principal':100}
state['last_motion'] = {'sala':time.time(), 'bano_visitas':time.time(),
        'bano_principal':time.time()}
state['groups_lights'] = { 
                'sala':{'Living room foot 1':'hue', 'Living room foot 2':'hue'},
                'bano_visitas':{'Downstairs bath 1':'hue'},
                'bano_principal':{'Main bath one':'hue'}}
state['lights'] = ['Living room foot 1','Living room foot 2','Downstairs bath 1',
        'Main bath one']

#apps_settings = ['app_motion']