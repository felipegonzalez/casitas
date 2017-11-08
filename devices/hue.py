import json
import time

class HueHub(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.place_lights = init['place_lights']
        self.state = {}
        self.bri = {}
        self.reachable = {}
        self.children = init['children']
        self.light_names = {}
        for k in self.children.keys() :
            self.light_names[self.children[k]] = k
        for k in self.children.keys():
            self.state[k] = ''
            self.bri[k] = 254
            self.reachable[k] = False
        print(self.light_names)
        print(self.state)
        self.messager = messager
        self.polling = 30
        self.last_check = 0
        self.last_on = {}
        for item in self.children:
            self.last_on[self.children[item]] = 0



    def parse(self, message):
        # deal with gets from states
        message_p = json.loads(message['data'])
        parsed_m = []
        #print("Parse lights")
        #print(message_p)
        if(isinstance(message_p, dict)):
            for light_no in message_p.keys():
                if(light_no in self.light_names.keys()):
                    #print(self.light_names[light_no])
                    #print(message_p[light_no]['state']['bri'])
                    self.bri[self.light_names[light_no]] = message_p[light_no]['state']['bri']
                    self.reachable[self.light_names[light_no]] = message_p[light_no]['state']['reachable']

                    if(message_p[light_no]['state']['on']):
                        self.state[self.light_names[light_no]] = 'on'
                    else:
                        self.state[self.light_names[light_no]] = 'off'
            print(self.state)
            print(self.bri)
        return parsed_m

    def turn_on(self, command, state):
        #data = json.loads(command['data']) should be done before
        light_no = self.children[command['value']]
        place = self.place_lights[command['value']]
        #if (light_name in state['lights']):
        #state['last_motion'][place] = state['timestamp']
        #if (int(state['photo'][place]) < state['min_photo'][place] and 
        #if (time.time() - self.last_on[light_no] > 1):
        state['devices_state'][self.name][command['value']] = 'on'

        if('brightness' in command.keys()):
            bri = command['brightness']
        else:
            #bri = self.bri[command['value']]
            bri = self.bri[self.light_names[light_no]]  # use previous brightness
            #bri = 254
        if(self.state[command['value']]=='off' or self.state[command['value']]==''):
            address = self.ip_address + '/api/newdeveloper/lights/' + light_no + '/state'
            data = json.dumps({'on':True, 'bri':bri})
            self.state[command['value']] = 'on'
            new_message = {'device_name':self.name, 'address':address, 'payload':data, 'type':'put'}
            self.messager.publish('http-commands', json.dumps(new_message))
            self.last_on[light_no] = time.time()
        #print('Encender hue light')
        return
   
    def turn_off(self, command, state):
        state['devices_state'][self.name][command['value']] = 'off'

        if(self.state[command['value']]=='on'):
            address = self.ip_address + '/api/newdeveloper/lights/' + self.children[command['value']] + '/state'
            data = json.dumps({'on':False})    
            self.state[command['value']] = 'off'
            print(self.state)
            new_message = {'device_name':self.name, 'address':address, 'payload':data, 'type':'put'}
            self.messager.publish('http-commands', json.dumps(new_message))
        #print('Apagar hue light')
        return 
 
    def update(self, state):
        if(state['timestamp']-self.last_check > self.polling):
            new_message = {'device_name':self.name,
                'address':self.ip_address+'/api/newdeveloper/lights/',
                'pars':'',
                'payload':'', 'type':'get'}
            self.messager.publish('http-commands', json.dumps(new_message))
            self.last_check = time.time()
        return