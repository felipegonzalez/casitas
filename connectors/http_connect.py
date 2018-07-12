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
    print("------------- ")
    #print(response.content) 
    data = response.content
    ip_addr = str(urlparse(response.url).hostname)
    #print(ip_addr)
    data_decode = data.decode('utf-8')
    if data_decode == '':
        data_decode = json.dumps({})
    try:
        if(ip_addr in ip_dict):
            new_message = json.dumps({"device_name":ip_dict[ip_addr], 
                "ip_addr":ip_addr, "data":data_decode})
            print("Received from " + ip_dict[ip_addr])
            #print(new_message)
            r.publish('http-events', new_message)
        else:
            if(data_decode!="success\n"):
                print("Message of unknown")
                print(data_decode)
                print(response.content)
    except Exception as ex:
        print("Could not parse message.")
        print(ip_addr)
        print(data_decode)
        print(ex)
        raise
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

    session = FuturesSession(max_workers=20)

    while True:
        message = command_sub.get_message()        
        if (message and message['type']=='message'):
            #print(message['data'])
            message_in = json.loads(message['data'])
            device_name = message_in['device_name']
            if message_in['type'] == 'get':
                #print(message_in)
                try:
                    url_initial = 'http://'
                    if(message_in['address'][:4] == "http"):
                        url_initial = ''
                    req =  session.get(url_initial+message_in['address']+'', 
                                    #data = message_in['payload'], 
                                    params = message_in['pars'],
                                    background_callback =process_response,
                                    timeout = 4)
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
                                    background_callback=process_response,
                                    timeout = 2)
                except:
                    print('Error http request put')



if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass