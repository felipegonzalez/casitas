from settings import r
import time
import random
import json


for i in range(100): 
    if random.random() > 0.1:
        mensaje = json.dumps({'device_name':'cajasala', 'data':{'temperature':25*(0.5 + random.random()/2), 'door':'closed' }})
        r.publish('xbee-events', mensaje)
        print mensaje
    else:
        mensaje = json.dumps({'device_name':'cajarecamara', 'data':{'motion':'on'}})
        r.publish('xbee-events', mensaje)        
        print mensaje
    time.sleep(1)
    #maybe send command to turn light
    if random.random() > 0.8:
        mensaje = json.dumps({'device_name':'cajarecamara', 'value':'luzchica', 'command':'turn_on'})
        r.publish('commands', mensaje)
        print mensaje
        time.sleep(1)
    if random.random() > 0.8:
        mensaje = json.dumps({'device_name':'hue', 'value':'sala1', 'command':'turn_on'})
        r.publish('commands', mensaje)
        print mensaje
        time.sleep(1)
    time.sleep(5)
