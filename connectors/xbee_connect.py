#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from xbee import ZigBee
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
from settings import xbee_dict
import json
import serial
from binascii import unhexlify
from binascii import hexlify


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
        response = xbee.wait_read_frame(timeout = 0.15)
        if(len(response)>0):
            #print(response)
            response['source_addr_long'] = response['source_addr_long'].hex()
            response['source_addr'] = response['source_addr'].hex()
            #if(xbee_dict[response['source_addr_long']]=='caja_estudiot'):
            if(True):
                print(response)
                print(response['source_addr_long'])
                print(xbee_dict[response['source_addr_long']])
            print("")
            if('rf_data' in response.keys()):
                try:
                    response['rf_data'] = response['rf_data'].decode('utf-8')
                    message = json.dumps({'device_type':'xbeebox', 'device_name':xbee_dict[response['source_addr_long']],
                        'source':response['source_addr_long'], 'type':'rf_data',
                        'content':response['rf_data']})
                    r.publish('xbee-events', message)
                    #if(json.loads(message)['device_name']=='cajarecamara'):
                    #    print('\a')
                except:
                    print("Error decoding xbee message")
                    raise
            if('samples' in response.keys()):
                #response['samples'] = response['rf_data'].decode('utf-8')
                message = json.dumps({'device_type':'xbeebox', 'device_name':xbee_dict[response['source_addr_long']],
                    'source':response['source_addr_long'], 'type':'samples',
                    'content':response['samples']})
                r.publish('xbee-events', message)

            

        message = p.get_message()
        if(message and message['type'] == 'message'):
            print(message)
            message_in = json.loads(message['data'].decode('utf-8'))
            print(message_in)
            if message_in:
                dest_addr_long = unhexlify(message_in['addr_long'])
                if message_in['mode'] == 'tx':
                    dest_addr = message_in['source_addr']
                    data = message_in['data']
                    xbee.tx(dest_addr_long=dest_addr_long, dest_addr=dest_addr, data=data)
                        #xbee.tx(dest_addr_long=b'\x00\x13\xa2\x00\x40\xbf\x96\x2c',dest_addr='\x40\xb3', data=b'1')
                if message_in['mode'] == 'pin':
                    command = hexlify(bytes.fromhex(message_in['command']))
                    print(dest_addr_long)
                    print(command)
                    parameter = bytes.fromhex(message_in['parameter'])
                    print(parameter)
                    xbee.remote_at(dest_addr_long= dest_addr_long, command=command, parameter=parameter)


if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass