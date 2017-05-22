#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from xbee import ZigBee
from pubsubsettings import r 
import json

SERIAL_PORT = '/dev/tty.usbserial-AH02VCE9'

def monitor()
    p = r.pubsub()
    p.suscribe('xbee-commands')
    print("Activar xbee coordinator...")
    try:
        serialConnection = serial.Serial( SERIAL_PORT, 9600,timeout=0.15)
        xbee = ZigBee(serialConnection)
        print "Conexión xbee serial...OK"
    except:
        logging.warning('Error serial/xbee')
        print "Error serial/xbee"
    print('Iniciar ciclo')
    while True:
        response = xbee.wait_read_frame(timeout=0.10)
        message = json.dumps({'type':'xbee', 'source':response['dest_addr_long'], 'content':response})
        r.publish('xbee-events', message)

        message = p.get_message()
        message_in = json.loads(message['data'])
        if message_in:
            dest_addr_long = message_in['dest_addr_long']
            if message_in['mode'] == 'tx':
                 dest_addr = message_in['dest_addr']
                 data = message_in['data']
                 xbee.tx(dest_addr_long=dest_addr_long, dest_addr=dest_addr, data=data)
                #xbee.tx(dest_addr_long='\x00\x13\xa2\x00\x40\xbf\x96\x2c',dest_addr='\x40\xb3', data=b'1')
            if message_in['mode'] == 'pin':
                command = message_in['command']
                parameter = message_in['parameter']
            xbee.remote_at(dest_addr_long= dest_addr_long, command=command, parameter=parameter)


if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass