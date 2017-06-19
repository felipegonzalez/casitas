#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
import json
import time
import datetime
from astral import Astral
import pytz
devices_outside = ['virtual-jardin','virtual-patio', 
	'virtual-front_door_hall', 'virtual-escaleras_patio']

a = Astral()
a.solar_depression = 'civil'
city = a['Mexico']
sun = city.sun(date=datetime.datetime.now(), local = True)
longitude = -99.226053
latitude = 18.956165

def OutsidePhoto():

    print('Iniciar ciclo')
    time_last = time.time()
    while True:
        #response = xbee.wait_read_frame(timeout=0.10)
        #message = json.dumps({'type':'xbee', 'source':response['dest_addr_long'], 'content':response})
        if(time.time() - time_last > 10):
        	dt = datetime.datetime.now()
        	dt_local = pytz.timezone('America/Mexico_City').localize(dt)
        	sun = city.sun(date = dt, local = True)

        	print(time.time())
        	value = '1000'
        	if(not sun_up(dt, sun)):
        		value = '0'
        	for dev in devices_outside:
        		r.publish('events', json.dumps({'device_name':dev, 
        			'event_type':'photo', 'value':value}))
       		time_last = time.time()

def sun_up(dt, sun):
	min_dt = pytz.timezone('America/Mexico_City').localize(dt + datetime.timedelta(hours = 1))
	max_dt = pytz.timezone('America/Mexico_City').localize(dt - datetime.timedelta(hours = 1))
	sunup = False
	if(max_dt > sun['dawn'] and min_dt < sun['sunset']):
		sunup = True
	return sunup
if __name__ == "__main__":
    try:
        OutsidePhoto()
    except KeyboardInterrupt:
        pass