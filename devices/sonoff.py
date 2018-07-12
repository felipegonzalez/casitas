import json
import time

class Sonoff(object):

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
        self.children = {}
        if('children' in init):
            self.children = init['children']


    def parse(self, message):
        # general response 
        parsed_m = []
        #print("Mensaje:")
        #print(message)
        #print(message['data'])
        try:
            message_p = json.loads(message['data'])
       
            #print(message_p)
            if(isinstance(message_p, dict)):
                for key in message_p.keys():
                    if(key == "POWER"):
                        if(message_p[key] == "ON"):
                            self.state["status"] = 1
                        else:
                            self.state["status"] = 0
        except Exception as ex:
            print("Error parsing message sonoff: " + message['data']) 
            print(ex)
        return parsed_m

    def update(self, state):
        state['devices_state'][self.name] = self.state
        if(self.polling > 0):
            if(time.time() - self.last_check > self.polling):
                #print("Updating")
                self.last_check = time.time()
                address = self.ip_address + '/cm?cmnd=Power' 
                new_message = json.dumps({'device_name':self.name, 'address':address, 
                        'payload':'', 'pars':'', 'type':'get'})
                self.messager.publish('http-commands', new_message)
        return

    #generic way of running a command 
    ## TODO: update for sonoff ################
    def _send_get(self, command):

        child = command['value'] #value gives the noun 
        comm = command['command'] # command gives the verb
        pars_get = ''
        # put command and command parameters in one list for get
        if(child in self.children.keys()):
            if(comm == "turn_on"):
                address = self.ip_address + '/cm?cmnd=Power' + self.children[child]+'%20On'
            else:
                address = self.ip_address + '/cm?cmnd=Power' + self.children[child]+'%20Off'

            new_message = json.dumps({'device_name':self.name, 'address':address, 
                'payload':'', 'pars':pars_get, 'type':'get'})
            self.messager.publish('http-commands', new_message)
        else:
            print("Child device not found.")
        return 

    # we define these functions which are available to the system:
    def turn_on(self, command, state):
        self._send_get(command)
        return

    def turn_off(self, command, state):
        self._send_get(command)
        return