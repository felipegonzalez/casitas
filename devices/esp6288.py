import json
import time

class Esp6288(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.state = {}
        self.messager = messager
        if('polling' in init.keys()):
            self.polling = init['polling']
        else:
            self.polling = 30
        self.last_check = 0


    def parse(self, message):
        # general response 
        parsed_m = []
        message_p = json.loads(message['data'])
        if(isinstance(message_p, dict)):
            if(message_p['type'] == 'status'):
                for elem in message_p['values'].keys():
                    self.state[elem] = message_p['values'][elem]
            if(message_p['type'] == 'event'):
                parsed_m.append(json.loads(message_p['event']))
        return parsed_m

    def update(self, state):
        if(self.polling > 0):
            if(time.time() - self.last_check > self.polling):
                self.last_check = time.time()
                address = self.ip_address + '/status' 
                new_message = json.dumps({'device_name':self.name, 'address':address, 
                        'payload':'', 'pars':'', 'type':'get'})
                #self.messager.publish('http-commands', new_message)
        return

    #generic way of running a command on an esp6288 box
    def _send_get(self, command):
        child = command['value'] #value gives the noun 
        comm = command['command'] # command gives the verb
        pars_get = ''
        # put command and command parameters in one list for get
        if(child in self.children.keys()):
            if('pars' in command.keys()):
                pars_get = {**{'command':comm}, **command['pars']}
            address = self.ip_address + '/' + child #+ '/' + command['command']
            new_message = json.dumps({'device_name':self.name, 'address':address, 
                'payload':'', 'pars':pars_get, 'type':'get'})
            self.messager.publish('http-commands', new_message)
        else:
            print("Child device not found.")
        return 

    # we define these functions which are available to the system:
    def turn_on(self, command, state):
        self._send_get(command)
        state['devices_state'][self.name][command['value']] = 'on'
        return

    def turn_off(self, command, state):
        self._send_get(command)
        state['devices_state'][self.name][command['value']] = 'off'
        return