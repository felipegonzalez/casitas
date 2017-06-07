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
from devices.sonos import Sonos
# connections
conn_names = ['xbee-events']

# home areas
places = ['sala', 'bano_visitas', 'bano_principal', 'cocina', 
'hall_entrada', 'recamara_principal', 'pasillo_recamaras',
        'front_door_hall', 'escaleras_patio','patio']

delays = {'sala':60, 'bano_visitas':60, 'bano_principal':60, 'cocina':60,
            'hall_entrada':30, 'recamara_principal':120, 'pasillo_recamaras':20,
            'front_door_hall':60, 'escaleras_patio':60, 'patio':60}

place_lights = { 'Living room foot 1':'sala', 
                'Living room foot 2':'sala',
                'Downstairs bath 1':'bano_visitas',
                'Main bath one':'bano_principal',
                 'Kitchen one':'cocina',
                 'Kitchen two':'cocina',
                 'Entrance hall':'hall_entrada',
                 'Entrance table':'hall_entrada',
                 'Bedroom one':'recamara_principal',
                 'Bedroom two':'recamara_principal',
                 'Bedroom hall':'pasillo_recamaras',
                 'Front door':'front_door_hall',
                 'Patio stairs one':'escaleras_patio',
                 'Patio stairs two':'escaleras_patio'}
# devices
device_settings = {
        'cajasala':{
        'place':'sala',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf0582'
        },
        'cajacocina':{
        'place':'cocina',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf06bd'
        },
        'cajarecamara':{
        'place':'recamara_principal',
        'device_type':'xbeebox',
        'addr_long':'0013a20040c45639'
        },
        'caja_pasillo_recamaras':{
        'place':'pasillo_recamaras',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf05de',
        'pins':{'dio-4':'motion'}
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
        'caja_puerta':{
        'place':'hall_entrada',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bef84d',
        'pins':{'dio-1':'motion', 'dio-2':'door', 'adc-3':'photo', 'dio-0':'none',
        'dio-12':'none', 'dio-4':'none'}
        },
        'caja_goteo':{
        'place':'patio',
        'device_type':'xbeebox',
        'addr_long':'0013a20040caadda',
        'pins':{'D2':'regar'}
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
        'Downstairs bath 1':'37' ,'Main bath one':'57' ,'Kitchen one':'42',
        'Kitchen two':'44' ,'Entrance hall':'39', 'Bedroom one':'45', 
        'Bedroom two':'46', 'Bedroom hall':'54', 'Front door':'51',
        'Patio stairs one':'52', 'Patio stairs two':'53', 'Entrance table':'48'},
        'place_lights':place_lights
        },
        'sonos':{
        'place':'home',
        'device_type':'sonos',
        'children':{'Estudio':1, 'Sala de estar':2}
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
dev_class = {'xbeebox':XbeeBox, 'hue':HueHub, 'alarm':Alarm, 'sonos':Sonos}


#state definition, initial
state = {'timestamp':time.time()}
state['photo'] = {}
state['temperature'] = {}
state['humidity'] = {}
state['min_photo'] = {}
state['last_motion'] = {}
state['motion'] = {}
for place in places :
        state['photo'][place] = 0
        state['min_photo'][place] = 200
        state['last_motion'][place] =  0
        state['humidity'][place] = 50
        state['temperature'][place] = 20.0
        state['motion'][place] = False

state['groups_lights'] = {}
for place in places:
        place_dict = {}
        for elem in place_lights.keys():
                if place_lights[elem] == place:
                        place_dict[elem] = 'hue'
        state['groups_lights'][place] = place_dict
print(" ")
print("Groups lights")
print(state['groups_lights'])
print(" ")
#state['groups_lights'] = { 
#                'sala':{'Living room foot 1':'hue', 'Living room foot 2':'hue'},
#                'bano_visitas':{'Downstairs bath 1':'hue'},
#                'bano_principal':{'Main bath one':'hue'}}


state['lights'] = place_lights.keys()
state['place_lights'] = place_lights
print(state['lights'])
#apps_settings = ['app_motion']