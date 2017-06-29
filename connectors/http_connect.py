#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import grequests
from requests_futures.sessions import FuturesSession
import logging
import logging.handlers
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
import json


def process_response(session, response):
    print("Calling process_response")
    print(response) 
    r.publish('http-events', response.content)


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
        #response = xbee.wait_read_frame(timeout=0.10)
        #message = json.dumps({'type':'xbee', 'source':response['dest_addr_long'], 'content':response})

        message = command_sub.get_message()        
        if (message and message['type']=='message'):
            print(message['data'])
            message_in = json.loads(message['data'])
            if message_in['type'] == 'get':
                try:
                    req =  session.get('http://'+message_in['address']+'', 
                                    data = message_in['payload'], 
                                    background_callback =process_response)
                except:
                    print('Error http request get')
            if message_in['type']=='put':
                #try:
                print('http://'+message_in['address'])
                print(message_in['payload'])
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