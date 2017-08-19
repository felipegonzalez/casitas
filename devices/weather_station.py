import json
import time
import os
import dateparser



class WeatherStation(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state = {}
        #self.children = init['children']
        self.messager = messager
        self.polling = 120
        self.last_check = 0
        self.ip_address = init['ip_address']
        self.place = init['place']
        self.get_address =  'estacionyun.local' + '/arduino/weather/0'
        try:
            prev_state = json.loads(messager.hget('devices', 'estacion_meteo'))
            self.state = prev_state
        except:
            self.state["rain_mm_yesterday"] = -1.0
        #self.state = self.get_state()
        #self.last_on = {}
        #for item in self.children:
        #    self.last_on[self.children[item]] = 0

    def parse(self, message):
        #print(message['data'])
        message_p_strip = (message['data'].rstrip().replace("'", '"'))
        #print(message_p_strip)
        message_load = json.loads(message_p_strip)
        parsed_m = []
        if('date' in self.state.keys()):
            state_day = dateparser.parse(self.state['date']).weekday()
            message_day = dateparser.parse(message_load['date']).weekday()

            if(state_day != message_day):
                self.state['rain_mm_yesterday'] = self.state['rain_mm_day']
        for elem in message_load:
            self.state[elem] = message_load[elem]
        for k in self.state.keys():
            parsed_m.append({'device_name':self.name, 'event_type':k, 
                    'value':self.state[k]})

        #print(out_dict)
        #parsed_m = [{'device_name':self.name, 'event_type':'motion','value':motion}]
        return parsed_m

    def get_state(self):
        new_message = {'device_name':self.name,
                'address':self.get_address, 'pars':'',
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
            

    def update(self, global_state):
        if(global_state['timestamp']-self.last_check > self.polling):
            self.get_state()
        #     if('motionDetectAlarm' in self.state.keys() and self.state['motionDetectAlarm'] == '2'):
        #         global_state['alarm_cam'] = True
        #     if('motionDetectAlarm' in self.state.keys() and self.state['motionDetectAlarm'] != '2'):
        #         global_state['alarm_cam'] = False
        # #     else:
        # #         global_state['alarm_cam'] = False
            self.last_check = time.time()
        return