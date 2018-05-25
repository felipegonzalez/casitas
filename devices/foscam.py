import json
import time
import os
import xmltodict
import glob
from shutil import copyfile
import math

class FosCam(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state = {}
        #self.children = init['children']
        self.messager = messager
        self.polling = 10
        self.last_check = time.time()
        self.ip_address = init['ip_address']
        self.port = init['port']
        self.user = init['user']
        self.password = init['password']
        self.place = init['place']
        self.places_movement = init['places_movement']
        self.notify_alarm = False #can be movement, alarm
        self.id_cam = init['id_cam']
        self.path = init['img_path']
        self.dest_path = '/Volumes/mmshared/web_img/' + self.name +'.jpg'
        self.get_address = self.ip_address + ':'+ self.port + '/cgi-bin/CGIProxy.fcgi'
        self.basic_payload = {'usr':self.user,'pwd':self.password}
        #self.state = self.get_state()
        #self.last_on = {}
        #for item in self.children:
        #    self.last_on[self.children[item]] = 0

    def parse(self, message):
        message_p = (message)['data']
        parsed_m = []
        out_dict = xmltodict.parse(message_p)['CGI_Result']
        if('sdFreeSpace' in out_dict.keys()):
            #we assume this condition means a get for state (?)
            self.state = out_dict
            if('motionDetectAlarm' in out_dict.keys()):
                motion = out_dict['motionDetectAlarm'] == '2'
                self.state = out_dict
                #print(self.state)
                parsed_m.append({'device_name':self.name, 'event_type':'motion','value':motion})
        return parsed_m

    def get_state(self):
        pars = self.basic_payload
        pars['cmd'] = 'getDevState'
        new_message = {'device_name':self.name,
                'address':self.get_address, 'pars':pars,
                 'payload':'', 'type':'get'}
        self.messager.publish('http-commands', json.dumps(new_message))
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
    
    def set_motion_detect(self, command, state):
        print("config mov")
        print(command)
        pars = self.basic_payload
        pars['cmd'] = 'setMotionDetectConfig'
        value = command['value']
        if(value=='on'):
            val = 1
        else:
            val = 0
        pars['isEnable'] = val 
        pars['isMovAlarmEnable'] = val
        pars['linkage'] = 12
        pars['snapInterval'] = 2
        pars['sensitivity'] = 3
        pars['triggerInterval'] = 10
        pars['isPirAlarmEnable'] = 1
        for j in range(0,7):
            pars['schedule'+str(j)] = pow(2, 48) - 1
        for j in range(0,10):
            pars['area'+str(j)] = 1023
        new_message = {'device_name':self.name,
            'address':self.get_address, 'pars':pars, 'payload':'',
            'type':'get'}
        self.messager.publish('http-commands', json.dumps(new_message))

    def update(self, global_state):
        if(global_state['timestamp']-self.last_check > self.polling):
            self.get_state()
            self.last_check = time.time()
            if('motionDetectAlarm' in self.state.keys()):
                print('Motion '+self.name+' '+self.state['motionDetectAlarm'])

            if('motionDetectAlarm' in self.state.keys() and self.state['motionDetectAlarm'] == '2'):
                global_state['alarm_cam'] = True
                                ### send movement events
                for place in self.places_movement:
                    virtual_dev = 'virtual-'+place
                    new_message = {'device_name':virtual_dev,
                    'event_type':'motion', 'value':True, 'units':'binary'}
                    self.messager.publish('events', json.dumps(new_message))
                #new_message = {'device_name':'pushover',
                #    'command':'send_message', 'value':'Movimiento en ' + self.name}
                #self.messager.publish('http_commands',
                #a    json.dumps(new_message))
                print(self.path+'/snap/*')

                list_of_files = glob.glob(self.path+'/snap/*') 
                #try:
                latest_file = max(list_of_files, key = os.path.getctime)
                copyfile(latest_file, self.dest_path)
                #except:
                #    print("could not copy file")

                
            if('motionDetectAlarm' in self.state.keys() and self.state['motionDetectAlarm'] != '2'):
                global_state['alarm_cam'] = False
        #     else:
        #         global_state['alarm_cam'] = False
        return