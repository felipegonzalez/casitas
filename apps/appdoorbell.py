import json


class DoorBell():
    def __init__(self):
        self.bells = {'patio':'two_tone_doorbell.wav'}
        pass

    def activate(self, ev_content, state, r, value):
        devices = state['devices']
        place = devices[ev_content['device_name']].place
        messages = []
        text = 'Timbre en ' + place
        print(text)
        messages.append(json.dumps({'device_name':'pushover',
            'command':'send_message', 'value':text}))
        messages.append(json.dumps({'device_name':'sonos',
            'command':'play', 'value':self.bells[place],
            'volume':100, 'zone':'Estudio' }))
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
