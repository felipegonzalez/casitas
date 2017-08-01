import json
import time

class GeneralDevice(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.state = {}
        self.messager = messager
        self.polling = 30
        self.last_check = 0


    def parse(self, message):
        # general response 
        parsed_m = []
        #message_p = json.loads(message['data'])
        #if(isinstance(message_p, dict)):
        #    if(message_p['type'] == 'status'):
        #        for elem in message_p['events']:
                    #self.status[elem] = message_p['values'][elem]
        #            parsed_m.append(json.loads(message_p['events'][elem]))
        return parsed_m

    def update(self, state):
        return

    # #generic way of running a command on an esp6288 box
    # def _send_get(self, command):
    #     subdevice = command['value']
    #     address = self.ip_address + '/' + subdevice + '/' + command['command']
    #     new_message = json.dumps({'device_name':self.name, 'address':address, 
    #         'payload':'', 'type':'get'})
    #     self.messager.publish('http-commands', new_message)
    #     return 

    # # we define these functions which are available to the system:
    # def turn_on(self, command, state):
    #     self._send_get(command)
    #     return

    # def turn_off(self, command, state):
    #     self._send_get(command)
    #     return