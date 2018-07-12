import json
import time
import datetime
import pytz
tz = pytz.timezone('America/Mexico_City')

class AppIrrigation():
    def __init__(self):
        self.name = 'app_irrigation'
        self.status = 'on'
        self.state = {}
        self.state = [{'device':'caja_riego_jardin', 'child':'jardinera', 
                         'pattern':{'start_time':3, 'duration':140, 'gap':2}},
                        {'device':'caja_riego_jardin', 'child':'pasto', 
                         'pattern':{'start_time':6, 'duration':30, 'gap':1}},
                        #{'device':'caja_riego_jardin', 'child':'pasto', 'start_time':18, 'duration':30, 'gap':1},
                        {'device':'caja_riego_jardin', 'child':'macetas', 
                        'pattern':{'start_time': 5, 'duration':40, 'gap':2}}]
        # start today
        now = datetime.datetime.now(tz)
        for i, val in enumerate(self.state):
            time_start =  now.replace(hour = val['pattern']['start_time'], minute = 0, second = 0)
            time_now = datetime.datetime.now(tz)
            offset = 0
            if(time_start <  now):
                offset = 1
            self.state[i]['next_time'] = time_start + datetime.timedelta(days = offset)
            #if(val['start_time'] > 8):
            #    self.pattern[i]['next_time'] =  now.replace(hour = val['start_time'], minute = 0, second = 0)
            #else:
            #    time_now =  now.replace(hour = val['start_time'], minute = 0, second = 0)
            #    self.pattern[i]['next_time'] = time_now + datetime.timedelta(days = 1)
        #self.state = self.pattern


    def activate(self, ev_content, state, r, value):
        now = datetime.datetime.now(tz)
        i = value
        device_name = self.state[i]['device']
        child = self.state[i]['child']
        duration = self.state[i]['pattern']['duration']
        # plan next
        gap = self.state[i]['pattern']['gap']
        
        mensajes = []
        no_rain = True
        water_available = True
        try:
            water_dist = state['devices_state']['caja_cisterna']['distancia_filtrada']
            water_level = 5.6*(2120.0 - 10*water_dist)
            water_available = water_level > 2000
            if(not water_available):
                text = 'Riego cancelado. Nivel de cisterna bajo.'
                mensajes.append(json.dumps({'device_name':'pushover',
                'command':'send_message', 'value':text, 'origin':self.name}))
        except Exception as ex:
            print("Error parsing water level data")
        try:
            estacion_meteo = state['devices_state']['estacion_meteo']
            lluvia_hoy_cm = estacion_meteo['rain_mm_day']/10
            lluvia_ayer_cm = estacion_meteo['rain_mm_yesterday']/10
            if(lluvia_hoy_cm > 8 or lluvia_ayer_cm > 8):
                no_rain = False
        except Exception as ex:
            print("Error parsing meteo station")
            print(ex)
        if(no_rain and water_available):
            mensajes.append(json.dumps({'device_name':device_name, 'value':child, 
                'command':'turn_on', 'origin':self.name, 
                'pars':{'zona':child, 'tiempo':duration}
                }))
            self.state[i]['last_time'] = self.state[i]['next_time']
        self.state[i]['next_time'] = self.state[i]['next_time'] + datetime.timedelta(days=gap)
        #self.state = self.pattern

        return mensajes



    def check_event(self, ev_content,  state):
        fire = False
        value =''
        if(ev_content):
            if(ev_content['event_type'] == 'heartbeat'):
                now = datetime.datetime.now(tz)
                for i, current_dev in enumerate(self.state):
                    if(current_dev['next_time'] < now):
                        print("Start irrigation")
                        print(self.state[i])
                        fire = True
                        value = i
                        break 
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        if(comm_content):
            if(comm_content["device_name"]=="caja_riego_jardin"):
                if(comm_content['command']=="turn_on"):
                    zona = comm_content["value"]
                    for i, current_dev in enumerate(self.state):
                        if(current_dev["child"] == zona):
                            self.state[i]["last_time"] = datetime.datetime.now(tz)
        return fire, value
