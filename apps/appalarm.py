import json


class Alarmist():
    def __init__(self):
        self.alarms = {'gas_alarm':
                            {'say':'Alarma de gas', 
                             'notify':True},
                        'rain_alarm':
                            {'say':'Alarma de lluvia',
                                'notify':True}} 
        self.status = 'on'
        self.name = 'app_alarm'
        return

    def add_alarm(self, name, alarm_config):
        self.alarms[name] = alarm_config
        return

    def activate(self, ev_content, state, r, value):
        devices = state['devices']
        place = devices[ev_content['device_name']].place
        if(place in self.bells.keys()):
            sound_file = self.bells[place]
        else:
            sound_file = 'store_bell.wav'
        messages = []
        text = 'Timbre en ' + place
        print(text)
        messages.append(json.dumps({'device_name':'pushover',
            'command':'send_message', 'value':text, 'origin':self.name}))
        messages.append(json.dumps({'device_name':'sonos', 'command':'play',
            'value':sound_file,'zone':'Estudio','volume':95}))
        return messages

    def check_event(self, ev_content,  state):
        fire = False
        value = ''
        devices = state['devices']
        if ev_content:
            if(ev_content['event_type']=='timbre'):
                print("Tinmbre")
                print(ev_content)
            if(ev_content['event_type']=='timbre' and (ev_content['value'])):
                place = devices[ev_content['device_name']].place
                fire = True
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value



