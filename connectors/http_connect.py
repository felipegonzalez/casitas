#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import logging
import logging.handlers
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
import json





def monitor():
    p = r.pubsub()
    p.subscribe('http-commands')
    #print("Activar x coordinator...")
    #try:
    #    serialConnection = serial.Serial( SERIAL_PORT, 9600,timeout=0.15)
    #    xbee = ZigBee(serialConnection)
    #    print "Conexión xbee serial...OK"
    #except:
    #    logging.warning('Error serial/xbee')
    #    print "Error serial/xbee"
    print('Iniciar ciclo')
    while True:
        #response = xbee.wait_read_frame(timeout=0.10)
        #message = json.dumps({'type':'xbee', 'source':response['dest_addr_long'], 'content':response})

        message = p.get_message()        
        if (message and message['type']=='message'):
            print(message['data'])
            message_in = json.loads(message['data'])
            if message_in['type'] == 'get':
                try:
                    req =  requests.get('http://'+message_in['address']+'/state', 
                                    data = message_in['payload'], 
                                    timeout = 0.2)
                    r.publish('http-events', req.content)
                except:
                    print('Error http request get')
            if message_in['type']=='put':
                #try:
                print('http://'+message_in['address']+'/state')
                print(message_in['payload'])
                try:
                    req = requests.put('http://'+message_in['address']+'/state', 
                                    data=message_in['payload'], 
                                    timeout=1)
                except:
                    print('Error http request put')



if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass