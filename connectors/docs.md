

## Conectores

- xbee_connect
    recibe comandos por canal xbee-command 
        {'mode':'tx', 'dest_addr_long', 'dest_addr': , 'data':}
        {'dest_addr_long': ,mode':'pin', 'command':'D2', parameter:'\x05'}

- Devices: xbeebox, hue


Comandos:

{'device_name':'aab', 'command':'turn_on', 'value':xxxx}

command es una función 
value contiene parámetros para la función turn on , por ejemplo child device


Events:
event_type
value
device_name