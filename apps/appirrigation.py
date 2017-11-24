import json
import time
import datetime
import pytz


class AppIrrigation():
    def __init__(self):
        self.name = 'app_irrigation'
        self.status = 'on'
        self.pattern = [{'device':'caja_riego_jardin', 'child':'pasto', 'start_time':3, 'duration':110},
                        {'device':'caja_riego_jardin', 'child':'jardinera', 'start_time':6, 'duration':40},
                        {'device':'caja_riego_jardin', 'child':'macetas', 'start_time': 5, 'duration':30}]
        # start today
        now = datetime.datetime.now()
        for i, val in enumerate(self.pattern):
            if(val['start_time'] > 8):
                self.pattern[i]['next_time'] =  now.replace(hour = val['start_time'], minute = 0, second = 0)
            else:
                time_now =  now.replace(hour = val['start_time'], minute = 0, second = 0)
                self.pattern[i]['next_time'] = time_now + datetime.timedelta(days = 1)


    def activate(self, ev_content, state, r, value):
        now = datetime.datetime.now()
        i = value
        device_name = self.pattern[i]['device']
        child = self.pattern[i]['child']
        duration = self.pattern[i]['duration']
        # plan next
        self.pattern[i]['next_time'] = self.pattern[i]['next_time'] + datetime.timedelta(days=2)
        mensajes = []
        no_rain = True
        if(no_rain):
            mensajes.append(json.dumps({'device_name':device_name, 'value':child, 
                'command':'turn_on', 'origin':self.name, 
                'pars':{'zona':child, 'tiempo':duration}
                }))
        return mensajes



    def check_event(self, ev_content,  state):
        fire = False
        value =''
        if(ev_content):
            if(ev_content['event_type'] == 'heartbeat'):
                now = datetime.datetime.now()
                for i, current_pattern in enumerate(self.pattern):
                    if(current_pattern['next_time'] < now):
                        print("Start irrigation")
                        print(self.pattern[i])
                        fire = True
                        value = i
                        break 
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value
