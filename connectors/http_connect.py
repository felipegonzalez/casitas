#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import grequests
from requests_futures.sessions import FuturesSession
from urllib.parse import urlparse
import logging
import logging.handlers
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
from settings import ip_dict

import json


def process_response(session, response):
    #print("Calling process_response")
    #print(response) 
    data = response.content
    ip_addr = str(urlparse(response.url).hostname)
    new_message = json.dumps({'device_name':ip_dict[ip_addr], 
        'ip_addr':ip_addr, 'data':data.decode('utf-8')})
    #print(new_message)
    r.publish('http-events', new_message)
    return

def monitor():
    command_sub = r.pubsub()
    command_sub.subscribe('http-commands')
    #print("Activar x coordinator...")
    #try:
    #    serialConnection = serial.Serial( SERIAL_PORT, 9600,timeout=0.15)
    #    xbee = ZigBee(serialConnection)
    #    print "Conexión xbee serial...OK"
    #except:
    #    logging.warning('Error serial/xbee')
    #    print "Error serial/xbee"
    print('Iniciar ciclo')

    session = FuturesSession(max_workers=10)

    while True:
        message = command_sub.get_message()        
        if (message and message['type']=='message'):
            #print(message['data'])
            message_in = json.loads(message['data'])
            device_name = message_in['device_name']
            if message_in['type'] == 'get':
                try:
                    req =  session.get('http://'+message_in['address']+'', 
                                    #data = message_in['payload'], 
                                    params = message_in['pars'],
                                    background_callback =process_response)
                except Exception as ex:
                    print('Error http request get')
                    print(format(ex))
            if message_in['type']=='put':
                #try:
                #print('http://'+message_in['address'])
                #print(message_in['payload'])
                try:
                    req = session.put('http://'+message_in['address'], 
                                    data=message_in['payload'], 
                                    background_callback=process_response)
                except:
                    print('Error http request put')



if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass