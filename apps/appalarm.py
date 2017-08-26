import json


class Alarmist():
    def __init__(self):
        self.alarms = ['gas_alarm_check', 'temp_alarm_check']
        self.status = 'on'
        self.name = 'app_alarm'
        return

    def gas_alarm_check(self, ev_content,  state):
        #check for gas alarm 
        fire = False
        value = ''
        devices = state['devices']
        if ev_content:
            if(ev_content['event_type']=='gaslpg'):
                #print("Tinmbre")
                #print(ev_content)
                try:
                    if(float(ev_content['value']) > 350):
                        place = devices[ev_content['device_name']].place
                        fire = True
                        value = {'device_name':'alarm',
                            'command':'sound_alarm','value':'gas','origin':ev_content['device_name']}
                except:
                    "Error alarm (parse or place)"
        return fire, value

    def temp_alarm_check(self, ev_content,  state):
        #check for gas alarm 
        fire = False
        value = ''
        devices = state['devices']
        if ev_content:
            if(ev_content['event_type']=='temperature'):
                #print("Tinmbre")
                #print(ev_content)
                if(float(ev_content['value']) > 29):
                    place = devices[ev_content['device_name']].place
                    fire = True
                    value = {'device_name':'alarm',
                            'command':'sound_alarm','value':'temperature','origin':ev_content['device_name']}
        return fire, value

    def activate(self, ev_content, state, r, value):
        commands = []
        for item in value:
            commands.append(json.dumps(item))
        return commands

    def check_event(self, ev_content,  state):
        fire = False
        value = []
        for item in self.alarms:
            fi, val = getattr(self, item)(ev_content, state)
            if fi:
                value.append(val)
                fire = True
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value



