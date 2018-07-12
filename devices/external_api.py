import json
import time

class ExternalApi(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.state = {}
        self.internal_state = {}
        self.messager = messager
        self.port = init['port']
        if('polling' in init.keys()):
            self.polling = init['polling']
        else:
            self.polling = 30
        self.last_check = 0
        self.children = {}
        if('children' in init):
            self.children = init['children']
        self.requests = init['requests']


    def parse(self, message):
        # general response 
        parsed_m = []
        #print("Mensaje:")
        #print(message)
        #print(message['data'])
        try:
            message_p = json.loads(message['data'])
            print("exgterna")
            print(message_p)
            #print(message_p)
            self.internal_state = message_p
            # update state
            #if('device_name' in message_p.keys()):
            self.state = self.internal_state          
        except Exception as ex:
            print("Error parsing api message "+self.name) 
            print(ex)
        return parsed_m

    def update(self, state):
        state['devices_state'][self.name] = self.state
        if(self.polling > 0):
            if(time.time() - self.last_check > self.polling):
                print("Updating "+self.name)
                self.last_check = time.time()
                address = self.ip_address 
                for elem in self.requests:
                    endpoint = elem[0]
                    parameters = elem[1]
                    new_message = json.dumps({'device_name':self.name, 'address':address + endpoint, 
                        'payload':'', 'pars':parameters, 'type':'get', 'port':self.port})
                print("Requesting for " + self.name)
                self.messager.publish('http-commands', new_message)
        return
