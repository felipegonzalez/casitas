import json
import time
import os
import requests
import xmltodict

class FosCam(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state = {}
        #self.children = init['children']
        self.messager = messager
        self.polling = 5
        self.last_check = time.time()
        self.ip_address = init['ip_address']
        self.port = init['port']
        self.user = init['user']
        self.password = init['password']
        self.get_address = 'http://' + self.ip_address + ':'+ self.port + '/cgi-bin/CGIProxy.fcgi'
        self.basic_payload = {'usr':self.user,'pwd':self.password}
        #self.state = self.get_state()
        #self.last_on = {}
        #for item in self.children:
        #    self.last_on[self.children[item]] = 0

    def parse(self, message):
        parsed_m = ''
        return parsed_m

    def get_state(self):
        pars = self.basic_payload
        pars['cmd'] = 'getDevState'
        new_message = {'device_name':self.name,
                'address':self.get_address, 'params':pars,
                 'payload':'', 'type':'get'}
        self.messager.publish('http-events', json.dumps(new_message))
        #req = requests.get(self.get_address, params = pars, timeout = 0.1)
        #out_dict = xmltodict.parse(req.content)['CGI_Result']
        #print(out_dict)
        return 

    # def get_alarm_state(self):
    #     state_alarm = ''
    #     if(not('motionDetectAlarm' in self.state.keys())):
    #         self.state = self.get_state()
    #         self.last_check = time.time()
    #     state_alarm = self.state['motionDetectAlarm']
    #     return state_alarm
            

    def update(self, global_state):
        # if(global_state['timestamp']-self.last_check > self.polling):
        #     self.state = self.get_state()
        #     if('motionDetectAlarm' in self.state.keys() and self.state['motionDetectAlarm'] == '2'):
        #         global_state['alarm_cam'] = True
        #     else:
        #         global_state['alarm_cam'] = False
        #     self.last_check = time.time()
        return