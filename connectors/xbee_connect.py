#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from xbee import ZigBee
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
import json
import serial

SERIAL_PORT = '/dev/tty.usbserial-AH02VCE9'

def monitor():
    p = r.pubsub()
    p.subscribe('xbee-commands')
    print("Activar xbee coordinator...")
    try:
        serialConnection = serial.Serial( SERIAL_PORT, 9600,timeout=0.15)
        xbee = ZigBee(serialConnection)
        print("Conexión xbee serial...OK")
    except:
        e = sys.exc_info()[0]
        print( "Error: %s" % e )
        logging.warning('Error connecting serial/xbee')
        print("Error connecting serial/xbee")
    print('Iniciar ciclo')
    while True:
        response = {}
        response = xbee.wait_read_frame()
        #print(response)
        if(len(response)>0):
            response['source_addr_long'] = response['source_addr_long'].hex()
            response['source_addr'] = response['source_addr'].hex()
            response['rf_data'] = response['rf_data'].decode('utf-8')
            message = json.dumps({'type':'xbee', 
                'source':response['source_addr_long'], 'content':response['rf_data']})
            r.publish('xbee-events', message)

            message = p.get_message()
            if(message and message['type'] == 'message'):
                print(message)
                message_in = json.loads(message['data'])
                print(message_in)
                if message_in:
                    dest_addr_long = message_in['source_addr_long']
                    if message_in['mode'] == 'tx':
                        dest_addr = message_in['source_addr']
                        data = message_in['data']
                        xbee.tx(dest_addr_long=dest_addr_long, dest_addr=dest_addr, data=data)
                        #xbee.tx(dest_addr_long=b'\x00\x13\xa2\x00\x40\xbf\x96\x2c',dest_addr='\x40\xb3', data=b'1')
                    if message_in['mode'] == 'pin':
                        command = message_in['command']
                        parameter = message_in['parameter']
                        xbee.remote_at(dest_addr_long= dest_addr_long, command=command, parameter=parameter)


if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass