#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import json
import time
from termcolor import colored


#import apps
from apps.appmotionlight import AppMotionLight 
from apps.appnomotion import AppNoMotionLight


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
print(state['devices_state'])

#create instances for apps #############
app_motion = AppMotionLight()
app_nomotion = AppNoMotionLight()




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

timer_print = time.time()

########### main loop ############################################

while True:


    if(time.time()-timer_print > 10):
        print(str(round(1/(time.time() - state['timestamp'])))+' cycles per second' )
        print(colored(state, 'green'))
        timer_print = time.time()

    state['timestamp'] = time.time()

    ev_content = None

    # get connection events, and process with corresponding device 
    # system events
    for con_name in conns.keys():
        item = conns[con_name].get_message()
        if (item and (item['type']=='message')):
            print(item)
            message = json.loads(item['data'])
            print(message)
            from_device = message['device_name']
            m_parsed = devices[from_device].parse(message)
            for m in m_parsed:
                r.publish('events', json.dumps(m))

    # get event and load data
    ev = events.get_message()
    if (ev and (ev['type']=='message')):
        print(colored(ev , 'blue'))
        ev_content = json.loads(ev['data'])
        state['devices_state'][ev_content['device_name']][ev_content['event_type']] = ev_content['value']
        #print ev

    # get command and process using device class
    comm = commands.get_message()
    if comm:
        if (comm['type']=='message'):
            print(colored(comm, 'red'))
            c = json.loads(comm['data'])
            getattr(devices[c['device_name']], c['command'])(c, state)

    # update home state?

    # include app code here ####################################################
    app_messages = []
    appcomms = []

    ### motion app
    if (ev and ev_content):
        if (app_motion.check(ev_content, state)):
            print('Activar app luces')
            appcomms = app_motion.activate(ev_content, state, r)
            app_messages = app_messages + appcomms
    
    ## no motion app
    if(app_nomotion.check(ev_content, state)):
        print('Apagar por falta de movimiento')
        appcoms = app_nomotion.activate(ev_content, state, r)
        app_messages = app_messages + appcoms
    ####################################################################

    ######## send commands of apps 

    for message in app_messages:
        r.publish('commands', message)

    ######## update devices
    for dev_name in devices.keys():
        devices[dev_name].update(state)
