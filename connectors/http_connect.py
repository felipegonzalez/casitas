import requests
import logging
import logging.handlers
from pubsubsettings import r 
import json





def monitor()
    p = r.pubsub()
    p.suscribe('http-commands')
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
        message_in = json.loads(message['data'])
        if message_in:
            if message_in['get']:
                try:
                    req =  requests.get(message_in['address'], 
                                    data = message_in['payload'], 
                                    timeout = 0.5)
                    r.publish('http-events', req.content)
                except:
                    print('Error http request get')
            if message_in['put']:
                try:
                    req = requests.put(message_in['address'], 
                                    data=message_in['payload'], 
                                    timeout=0.5)
                except:
                    print('Error http request put')



if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        pass