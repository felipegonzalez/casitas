import json
import time
import datetime
import pytz


class AppIrrigation():
    def __init__(self, place_lights):
        self.name = 'app_irrigation'

        self.pattern = [{'device':'caja_riego_jardin', 'child':'pasto', 'start_time':17, 'duration':1},
                        {'device':'caja_riego_jardin', 'child':'jardinera', 'start_time':6, 'duration':20},
                        {'device':'caja_riego_jardin', 'child':'macetas', 'start_time': 5, 'duration':20}]
        # start today
        now = datetime.datetime.now()
        for i, val in enumerate(self.pattern):
            self.pattern[i]['next_time'] =  now.replace(hour = elem['start_time'], minute = 0, second = 0)


    def activate(self, ev_content, state, r, value):
        now = datetime.datetime.now()
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
        if(ev_content['event_type'] == 'hearbeat'):
            now = datetime.datetime.now()
            for i, current_patern in self.pattern:
                if(pat['next_time'] < now):
                    fire = True
                    value = i 
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value
