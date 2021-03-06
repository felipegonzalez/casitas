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
from devices.virtual import Virtual
from devices.timer import Timer
from devices.foscam import FosCam
from devices.weather_station import WeatherStation
from devices.pushover_service import PushMessenger
from devices.esp6288 import Esp6288
from devices.general import GeneralDevice
from devices.alarm import Alarm
from devices.external_api import ExternalApi
from devices.solcast_api import SolcastApi
from devices.sonoff import Sonoff
from devices.apple_tv import AppleTV

# device classes
dev_class = {'xbeebox':XbeeBox, 'hue':HueHub, 'alarm':Alarm, 'sonos':Sonos,
    'virtual':Virtual, 'timer':Timer, 'foscam':FosCam , 'meteo':WeatherStation,
    'push_messenger':PushMessenger, 'esp6288':Esp6288, 'general':GeneralDevice,
    'alarm_exe':Alarm, 'external_api':ExternalApi, 'solcast_api':SolcastApi,
    'sonoff':Sonoff, 'apple_tv':AppleTV}

# connections
conn_names = ['xbee-events', 'http-events']

# home areas
places = ['sala', 'bano_visitas', 'bano_principal', 'cocina', 
'hall_entrada', 'recamara_principal', 'pasillo_recamaras',
        'front_door_hall', 'escaleras_patio','patio', 'estudiof','jardin',
        'exterior', 'estudiot' ,'comedor', 'pasillo_comedor','casa',
        'calle_frente', 'cuarto_tv', 'external']

delays = {'sala':120, 'bano_visitas':125, 'bano_principal':130, 'cocina':130,
            'hall_entrada':65, 'recamara_principal':180, 'pasillo_recamaras':30,
            'front_door_hall':60, 'escaleras_patio':60*5, 'patio':60*5,
            'estudiof':120, 'jardin':80,'estudiot':120, 'comedor':120,
            'pasillo_comedor':120, 'cuarto_tv':180}


# devices
device_settings = {
        'virtual-jardin':{
        'place':'jardin',
        'device_type':'virtual'
        },
        'virtual-patio':{
        'place':'patio',
        'device_type':'virtual'
        },
        'virtual-front_door_hall':{
        'place':'front_door_hall',
        'device_type':'virtual'
        },
        'virtual-hall_entrada':{
        'place':'front_door_hall',
        'device_type':'virtual'
        },
        'virtual-escaleras_patio':{
        'place':'escaleras_patio',
        'device_type':'virtual'
        },
        'virtual-bano_visitas':{
        'place':'bano_visitas',
        'device_type':'virtual'
        },
        'virtual-pasillo_recamaras':{
        'place':'pasillo_recamaras',
        'device_type':'virtual'
        },
        'cajasala':{
        'place':'sala',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf0582'
        },
        'cajacocina':{
        'place':'cocina',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf06bd',
        'txcommands':{'strip_cocina':{'turn_on':'1', 'turn_off':'0'}}
        #'txcommands':{'turn_on':'1', 'turn_off':'0'}
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
        'caja_estudiof':{
        'place':'estudiof',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf06d4'
        },
        'caja_consumo_electrico':{
        'place':'casa',
        'device_type':'xbeebox',
        'addr_long':'0013a20040c4605b'
        },
        'caja_estudiot':{
        'place':'estudiot',
        'device_type':'xbeebox',
        'addr_long':'0013a20040be4592'
        },
        'caja_pasillo_comedor':{
        'place':'pasillo_comedor',
        'device_type':'xbeebox',
        'addr_long':'0013a20040c4190d'
        },
        'caja_goteo':{
        'place':'patio',
        'device_type':'xbeebox',
        'addr_long':'0013a20040caadda',
        'children':{'regar':'D2'}
        },
        'caja_terraza':{
        'place':'jardin',
        'device_type':'xbeebox',
        'addr_long':'0013a20040caacd7',
        'txcommands':{'strip_terraza':{'turn_on':'1', 'turn_off':'0'}}
        },
        'caja_garage':{
        'place':'patio',
        'device_type':'xbeebox',
        'addr_long':'0013a20040c059bc',
        'txcommands':{'garage':{'activate':'g'}},
        },
        'caja_comedor':{
        'place':'comedor',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bf962c'
        },
        'caja_filtro_alberca':{
        'place':'patio',
        'device_type':'xbeebox',
        'addr_long':'0013a20040bef862',
        'children':{'bomba':'D2'}
        },
        #cajarecamara':{
        #'place':'recamara',
        #'device_type':'xbeebox',
        #'addr_long':'0013a20040c45639',
        #'children':{'luzchica':'D2'} #pin number
        #},
        'sonos':{
        'place':'home',
        'device_type':'sonos',
        'children':{'1':'Sala de estar', '2':'Estudio'}
        },
        'timer_1':{
        'device_type':'timer',
        'place':'casa',
        },
        'apple_tv_1':{
            'device_type':'apple_tv',
            'ip_address':'192.168.100.206',
            'login_id':'00000000-103f-73f9-0dfa-3907df3f43d8',
            'port':3689,
            'place':'cuarto_tv',
            'name':'Entertainment Room'
        },
        'cam_entrada':{
        'device_type':'foscam',
        'place':'hall_entrada',
        'places_movement': [],
        'ip_address':'192.168.100.220',
        'port':'88',
        'user':'felipe',
        'password':'valqui1',
        'id_cam':'FI9821P_C4D6554064C4',
        'img_path':'/Users/felipe/Volumes/mmshared/foscam_camds/FI9821P_C4D6554064C4',
        'dest_path':'/Volumes/mmshared/imagenes/img_mov_entrada.jpg' 
        },
        'cam_patio':{
        'device_type':'foscam',
        'place':'patio',
        'places_movement': ['patio', 'escaleras_patio', 'hall_entrada', 'front_door_hall'],
        'ip_address':'192.168.100.221',
        'port':'88',
        'user':'felipe',
        'password':'valqui1',
        'id_cam':'AMBIENTCAMHD_00626E564319',
        'img_path':'/Volumes/mmshared/foscam_cams/AMBIENTCAMHD_00626E564319',
        'dest_path':'/Volumes/mmshared/imagenes/img_mov_patio.jpg' 
        },
        'estacion_meteo':{
        'device_type':'meteo',
        'place':'exterior',
        'ip_address':'estacionyun.local'
        },
        'heartbeat':{
        'device_type':'virtual',
        'place':'casa'
        },
        'pushover':{
        'device_type':'push_messenger',
        'place':'casa'
        },
        'caja_cocina_timbre':{
        'device_type':'esp6288',
        'ip_address':'192.168.100.152',
        'place':'calle_frente',
        'polling':0
        },
        'solcast':{
        'device_type':'solcast_api',
        'ip_address':'api.solcast.com.au',
        'requests':[  # [endpoint, parameters]
            ['/radiation/forecasts',
            {'longitude':-99.226185, 'latitude':18.956130, 'api_key':'Gfeq_t9Crr0DgbfqN-TdKXd0fA6bW5ef', 'format':'json'}]
            ],
        'place':'external',
        'polling':60*60,
        'port':80
        },
        'gas_meter':{
        'device_type':'external_api',
        'ip_address':'raspicam.local',
        'requests':[
            ['/get_reading', {}]
        ],
        'place':'cocina',
        'polling':300,
        'port':80
        },
        'caja_riego_jardin':{
            'device_type':'esp6288',
            'ip_address':'192.168.100.154',
            'place':'jardin',
            'children':{'jardinera':'1','pasto':'2', 'macetas':'3'},
            'polling':30
        },
        'caja_hongos':{
            'device_type':'esp6288',
            'ip_address':'192.168.100.155',
            'place':'patio',
            'children':{'ventilador':'1', 'environment':'2'},
            'polling':10
        },
        'caja_tv':{
            'device_type':'esp6288',
            'ip_address':'192.168.100.157',
            'place':'cuarto_tv',
            'children':{'switch':'1'},
            'polling':10
        },
        'sonoff_washing':{
            'device_type':'sonoff',
            'ip_address':'192.168.100.161',
            'place':'cocina',
            'children':{'luz_lavado':'1'},
            'polling':10
        },
        'sonoff_garage':{
            'device_type':'sonoff',
            'ip_address':'192.168.100.160',
            'place':'patio',
            'children':{'luzgarage':'1'},
            'polling':10
        },
        'caja_cisterna':{
        'device_type':'esp6288',
        'ip_address':'192.168.100.153',
        'place':'patio',
        'polling':0
        },
        'homeserver':{
        'device_type':'general',
        'ip_address':'192.168.100.50',
        'place':'unknown'
        },
        'alarm':{
        'device_type':'alarm_exe',
        'place':'casa'
        }
}

place_lights = { 'Living room foot 1':'sala', 
                'Living room foot 2':'sala',
                'Hue bloom 1':'comedor',
                'Living room wall':'sala',
                'Downstairs bath':'bano_visitas',
                'Main bath one':'bano_principal',
                'Main bath two':'bano_principal',
                'Main bath three':'bano_principal',
                 'Kitchen one':'cocina',
                 'Kitchen two':'cocina',
                 'TV room':'cuarto_tv',
                 'Entrance hall':'hall_entrada',
                 'Entrance table':'hall_entrada',
                 'Bedroom one':'recamara_principal',
                 'Bedroom two':'recamara_principal',
                 'Bedroom hall':'pasillo_recamaras',
                 'Stairs':'pasillo_recamaras',
                 'Front door':'front_door_hall',
                 'Patio stairs one':'escaleras_patio',
                 'Patio stairs two':'escaleras_patio',
                 'Patio stairs three':'escaleras_patio',
                 'Felipe Study':'estudiof',
                 'Study Tere':'estudiot',
                 'Dining room':'comedor',
                 'Dining hall 1':'pasillo_comedor',
                 'Dining hall 2':'pasillo_comedor',
                 'Caballeriza uno':'patio',
                 'Caballeriza dos':'patio',
                 'Backyard':'jardin'}

device_settings['hue'] = {
        'ip_address':'192.168.100.203',
        'place':'casa',
        'device_type':'hue',
        'children':{'Living room foot 1':'49', 'Living room foot 2':'50',
        'Patio stairs three':'37' ,'Main bath one':'57' ,
        'Main bath two':'56', 'Kitchen one':'42',
        'TV room':'47',
        'Kitchen two':'44' ,'Entrance hall':'39', 'Bedroom one':'45', 
        'Bedroom two':'46', 'Bedroom hall':'54', 'Front door':'51',
        'Patio stairs one':'52', 'Patio stairs two':'53', 
        'Patio stairs three':'37',
        'Entrance table':'48','Felipe Study':'36', 'Study Tere':'43',
        'Dining room':'38', 'Hue bloom 1':'58' ,'Dining hall 1':'41',
        'Dining hall 2':'40', 'Living room wall':'60',
        'Downstairs bath':'59' ,'Stairs':'61', 'Dining hall 1':'41',
        'Dining hall 2':'40', 'Caballeriza uno':'62','Caballeriza dos':'63',
        'Backyard':'55', 'Main bath three':'1'},
        'place_lights':place_lights
        }
#xbee_dict
xbee_dict = {}
for key in device_settings.keys():
        if(device_settings[key]['device_type'] == 'xbeebox'):
                xbee_dict[device_settings[key]['addr_long']] = key
ip_dict = {}
for key in device_settings.keys():
        if('ip_address' in device_settings[key].keys()):
                ip_dict[device_settings[key]['ip_address']] = key

print('Ip devices ***********')
print(ip_dict)


#state definition, initial
state = {'timestamp':time.time()}
state['photo'] = {}
state['temperature'] = {}
state['humidity'] = {}
state['min_photo'] = {}
state['last_motion'] = {}
state['motion_value'] = {}
state['motion'] = {}
for place in places :
        state['photo'][place] = 0
        state['min_photo'][place] = 300
        state['last_motion'][place] =  0
        state['humidity'][place] = 0
        state['temperature'][place] = 0.0
        state['motion'][place] = False
        state['motion_value'][place] = 0
#state['min_photo']['estudiot'] = 1000
state['min_photo']['pasillo_comedor'] = 70
state['min_photo']['estudiot'] = 360
state['min_photo']['cuarto_tv'] = 150
state['min_photo']['cocina'] = 150

state['groups_lights'] = {}
for place in places:
        place_dict = {}
        for elem in place_lights.keys():
                if place_lights[elem] == place:
                        place_dict[elem] = 'hue'
        state['groups_lights'][place] = place_dict

## Luces que no son de hue
place_lights['strip_cocina'] = 'cocina'
place_lights['strip_terraza'] = 'jardin'
#place_lights['lampara'] = 'cuarto_tv'
place_lights['luzgarage'] = 'patio'
place_lights['luz_lavado'] = 'cocina'

state['groups_lights']['cocina']['strip_cocina'] = 'cajacocina'
state['groups_lights']['jardin']['strip_terraza'] = 'caja_terraza'
#state['groups_lights']['cuarto_tv']['lampara'] = 'caja_tv'
state['groups_lights']['cocina']['luz_lavado'] = 'sonoff_washing'
state['groups_lights']['patio']['luzgarage'] = 'sonoff_garage'

print(place_lights)
print(state['groups_lights'])
#print(" ")
#print("Groups lights")
#print(state['groups_lights'])
#print(" ")
#state['groups_lights'] = { 
#                'sala':{'Living room foot 1':'hue', 'Living room foot 2':'hue'},
#                'bano_visitas':{'Downstairs bath 1':'hue'},
#                'bano_principal':{'Main bath one':'hue'}}


state['lights'] = place_lights.keys()
state['place_lights'] = place_lights
state['alarm_cam'] = True
#print(state['lights'])
#apps_settings = ['app_motion']