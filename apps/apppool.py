import json
import time
import datetime
import pytz
from dateutil.parser import parse
from dateutil import tz

to_zone = tz.gettz("America/Mexico_City")

class AppPool():
    def __init__(self):
        self.name = 'app_pool'
        self.status = 'on'
        self.pattern = [{'device':'caja_filtro_alberca', 'child':'bomba', 'start_time':10, 'duration':3, 'gap':1}]
        # start today
        now = datetime.datetime.now()
        for i, val in enumerate(self.pattern):
            time_start =  now.replace(hour = val['start_time'], minute = 0, second = 0)
            time_now = datetime.datetime.now()
            offset = 0
            if(time_start <  now):
                offset = 1
            self.pattern[i]['next_time'] = time_start + datetime.timedelta(days = offset)
        self.state = self.pattern


    def reset_timer(self, i):
        pat = self.pattern[i]['start_time']
        now = datetime.datetime.now()
        time_start =  now.replace(hour = pat, minute = 0, second = 0)
        self.pattern[i]['next_time'] = time_start + datetime.timedelta(days = 1)
        self.state = self.pattern
        return 


    def activate(self, ev_content, state, r, value):
        now = datetime.datetime.now()
        i = value
        device_name = self.pattern[i]['device']
        duration = self.pattern[i]['duration']
        gap = self.pattern[i]['gap']
        # plan next
        mensajes = []
        # check radiation
        time_now = datetime.datetime.now()
        radiation_data = state['devices']['solcast'].state
        #radiation_data = get_radiation(time_now, state)

        if(radiation_data['best_index']==0):
            r.publish('commands', json.dumps({"device_name":"caja_filtro_alberca",
                "command":"turn_on", "value":"bomba", "origin":self.name}))
            mensaje_off = json.dumps({"device_name":"caja_filtro_alberca",
            "command":"turn_off", "value":"bomba", "origin":self.name})
            r.publish('commands', json.dumps({"device_name":"timer_1",
                "command":"add_timer", "interval":60*60*float(duration), 
                "value":mensaje_off, "origin":self.name}))
            self.reset_timer(i)
        else:
            self.pattern[i]['next_time'] = time_now + datetime.timedelta(minutes=30)

        self.state = self.pattern
        return mensajes



    def check_event(self, ev_content,  state):
        fire = False
        value =''
        if(ev_content):
            if(ev_content['event_type'] == 'heartbeat'):
                now = datetime.datetime.now()
                for i, current_pattern in enumerate(self.pattern):
                    if(current_pattern['next_time'] < now):
                        print("Check pool start")
                        print(self.pattern[i])
                        fire = True
                        value = i
                        break 
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value
