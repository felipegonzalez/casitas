import json


class DoorBell():
    def __init__(self):
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
            'command':'say', 'value':'Alguien está en la puerta del patio',
            'volume':10 }))
        return messages

    def check(self, ev_content,  state):
        fire = False
        value = ''
        devices = state['devices']
        if ev_content:
            if(ev_content['event_type']=='timbre'):
                print("Tinmbre")
                print(ev_content)
            if(ev_content['event_type']=='timbre' and not(ev_content['value'])):
                place = devices[ev_content['device_name']].place
                fire = True
        return fire, value
