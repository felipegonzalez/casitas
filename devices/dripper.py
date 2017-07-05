import json
import time
import os



class Dripper(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state = {}
        #self.children = init['children']
        self.messager = messager
        self.polling = 120
        self.last_check = time.time()
        self.dripper_device = init['dripper_device']
        self.day_spacing = 2
        self.water_delivered = 0
        #self.place = init['place']
        #self.get_address =  'estacionyun.local' + '/arduino/weather/0'
        #self.state = self.get_state()
        #self.last_on = {}
        #for item in self.children:
        #    self.last_on[self.children[item]] = 0

    def parse(self, message):
        #print(message['data'])
        #message_p_strip = (message['data'].rstrip().replace("'", '"'))
        #print(message_p_strip)
        #message_load = json.loads(message_p_strip)
        #self.state = message_load
        parsed_m = []
        #for k in message_load.keys():
        #    parsed_m.append({'device_name':self.name, 'event_type':k, 
        #        'value':message_load[k]})
        #print(out_dict)
        #parsed_m = [{'device_name':self.name, 'event_type':'motion','value':motion}]
        return parsed_m

    def calculate_water()
        new_message = {'device_name':self.name,
                'address':self.get_address, 'pars':'',
                 'payload':'', 'type':'get'}
        self.messager.publish('http-commands', json.dumps(new_message))
        #req = requests.get(self.get_address, params = pars, timeout = 0.1)
        #out_dict = xmltodict.parse(req.content)['CGI_Result']
        #print(out_dict)
        return 


            

    def update(self, global_state):
        if(global_state['timestamp']-self.last_check > self.polling):
            self.last_check = time.time()
        return