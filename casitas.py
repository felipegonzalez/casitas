#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import json
import time
from termcolor import colored
import logdata
import math
import os
import logging
import logging.handlers

from apps.appautolight import AutoLight
from apps.appdoorlight import AppDoorLight
from apps.appdoorbell import DoorBell

#create instances for apps #############
app_doorlight = AppDoorLight(place_lights)
app_autolight = AutoLight(delays)
app_doorbell = DoorBell()

#start logging
format_logging = logging.Formatter(fmt='%(levelname)s|%(asctime)s|%(name)s| %(message)s ', datefmt="%Y-%m-%d %H:%M:%S")
h = logging.handlers.TimedRotatingFileHandler('/Volumes/mmshared/bdatos/log/monitor_casitas/casa_monitor.log', encoding='utf8',
        interval=1, when='midnight', backupCount=4000)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
h.setFormatter(format_logging)
h.setLevel(logging.DEBUG)
root_logger.addHandler(h)
### end loggig handler
print('Creado logging')


# subscribe to events ###############
events = r.pubsub()
events.subscribe('events')
# subscribe to commands
commands = r.pubsub()
commands.subscribe('commands')




#create instances for devices ###############
devices = {}
for dev_name in device_settings.keys():
    type_device = device_settings[dev_name]['device_type']
    init = device_settings[dev_name]
    devices[dev_name] = dev_class[type_device](name=dev_name,init=init, messager = r)
print(devices)

state['devices'] = devices
state['devices_state'] = {}
for dev_name in device_settings.keys():
    state['devices_state'][dev_name] = {}
#print(state['devices_state'])



#subscribe to connections #############
conns = {}
for con in conn_names:
    p = r.pubsub()
    p.subscribe(con)
    conns[con] = p
# check subscriptions are ok 
for con in conn_names:
    a = conns[con].get_message()
    print(a)

#print(state['groups_lights'])
timer_print = time.time()
timer_heartbeat = time.time()

########### main loop ############################################
delta_time = 0
coef = 0.01
initial_time=time.time()
max_time = 0

r.publish('commands', 
    json.dumps({'device_name':'pushover', 
        'command':'send_message',
        'value':'Iniciando sistema.'}))

logging.info('Iniciando sistema')


while True:
    delta_time = time.time() - initial_time
    if(delta_time > max_time):
        max_time = delta_time
    initial_time = time.time()

    state['timestamp'] = time.time()
    for pl in state['motion_value'].keys():
        state['motion_value'][pl] = state['motion_value'][pl]*math.exp(-coef*delta_time)
    #heartbeat
    if(time.time() - timer_heartbeat > 1):
        timer_heartbeat = time.time()
        heartbeat_message = json.dumps({'device_name':'heartbeat', 
            'place':'casa','event_type':'heartbeat','value':time.time()})
        r.publish('events', heartbeat_message)

    ########### Print reports
    if(time.time()-timer_print > 10):
        #print(str(round(1/(time.time() - state['timestamp'])))+' cycles per second' )
        for dev in state['devices']:
            print("")
            #print(dev)
            #print(round(time.time() - state['devices'][dev].last_check, 1))
        for item in state:
            if(item!='devices' and item!='devices_state' and item!='groups_lights'):
                print(item)
                print(colored(state[item], 'magenta'))
        timer_print = time.time()
        print(colored('Alarma: '+str(state['alarm_cam']), 'green'))
        if(state['alarm_cam']):
            pass
            #r.publish('commands', json.dumps({'device_name':'sonos', 'value':'Movimiento cámara', 'command':'say'}))
        print(colored('Delta max :' + str(max_time), 'green'))
        print(colored('Outside: ', 'blue'))
        print(state['devices_state']['estacion_meteo'])
        print(state['motion_value'])
        max_time = 0

        #r.publish('commands', json.dumps({'device_name':'sonos', 'value':'Sistema vivo', 'command':'say'}))
    if(time.time()-timer_print > 3):
       logdata.log(state,r)



    ev_content = None

    # get connection events, and process with corresponding device 
    # system events
    for con_name in conns.keys():
        item = conns[con_name].get_message()
        if (item and (item['type']=='message')):
            #print(item)
            message = json.loads(item['data'])
            #print('Mensaje:')
            #print(message)
            from_device = message['device_name']
            try:
                m_parsed = devices[from_device].parse(message)
                for m in m_parsed:
                    r.publish('events', json.dumps(m))
            except Exception as ex:
                print("Error parsing message")
                print("From device "+ from_device)
                print(ex)
                raise


    # get event and load data
    ev = events.get_message()
    if (ev and (ev['type']=='message')):
        #print(colored(ev , 'blue'))
        ev_content = json.loads(ev['data'])
        logging.info(ev['data'])
        state['devices_state'][ev_content['device_name']][ev_content['event_type']] = ev_content['value']
        place = device_settings[ev_content['device_name']]['place']
        event_type = ev_content['event_type']
        if(event_type != 'none'):
            if(event_type in state.keys()):
                #print(place)
                #print(event_type)
                #print(ev_content['value'])
                state[event_type][place] = ev_content['value']
        
        # update central state depending on events #######
        if(event_type == 'motion'):
            if(ev_content['value']):
                state['motion_value'][place] = 1.0

    # get command and process using device class
    comm = commands.get_message()
    if comm:
        if (comm['type']=='message'):
            print(colored(comm, 'red'))
            logging.info(comm)
            c = json.loads(comm['data'])
            getattr(devices[c['device_name']], c['command'])(c, state)

    # update home state?

    # include app code here ####################################################
    app_messages = []
    appcomms = [] 

    fire = app_doorlight.check(ev_content, state) 
    if(fire):
        appcomms = app_doorlight.activate(ev_content, state, r)
        app_messages = app_messages + appcomms

    fire, value = app_autolight.check(ev_content, state) 
    if(fire):
        appcomms = app_autolight.activate(ev_content, state, r, value)
        app_messages = app_messages + appcomms

    fire, value = app_doorbell.check(ev_content, state) 
    if(fire):
        appcomms = app_doorbell.activate(ev_content, state, r, value)
        app_messages = app_messages + appcomms

    ## timer app
    ####################################################################

    ######## send commands of apps 

    for message in app_messages:
        r.publish('commands', message)

    ######## update devices
    for dev_name in devices.keys():
        devices[dev_name].update(state)
