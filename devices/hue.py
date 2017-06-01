import json
import time

class HueHub(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.place_lights = init['place_lights']
        self.state = {}
        self.children = init['children']
        self.messager = messager
        self.polling = 60
        self.last_check = 0



    def parse(self, message):
        # deal with gets from states
        return parsed_m

    def turn_on(self, command, state):
        #data = json.loads(command['data']) should be done before
        light_no = self.children[command['value']]
        place = self.place_lights[command['value']]
        #if (light_name in state['lights']):
        state['last_motion'][place] = state['timestamp']
        if (state['photo'][place] < state['min_photo'][place]):
            address = self.ip_address + '/api/newdeveloper/lights/' + light_no
            data = json.dumps({'on':True})
            self.state[command['value']] = 'on'
            new_message = {'address':address, 'payload':data, 'type':'put'}
            self.messager.publish('http-commands', json.dumps(new_message))
        #print('Encender hue light')
        return
   
    def turn_off(self, command, state):
        address = self.ip_address + '/api/newdeveloper/lights/' + self.children[command['value']]
        data = json.dumps({'on':False})    
        self.state[command['value']] = 'off'
        new_message = {'address':address, 'payload':data, 'type':'put'}
        self.messager.publish('http-commands', json.dumps(new_message))
        #print('Apagar hue light')
        return 
 
    def update(self, state):
        if(state['timestamp']-self.last_check > self.polling):
            new_message = {'address':self.ip_address, 'payload':'query', 'type':'get'}
            self.messager.publish('http-commands', json.dumps(new_message))
            self.last_check = time.time()
        return