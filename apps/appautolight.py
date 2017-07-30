import json


class AutoLight():
    def __init__(self, delays):
        self.delays = delays
        self.base_delays = delays
        self.candidates_off = []
        self.last_auto_off = {}
        self.status = 'on'
        self.name = 'app_autolight'

    def activate(self, ev_content, state, r, value):
        devices = state['devices']

        messages = []
        if(value == 'on'):
            place = devices[ev_content['device_name']].place
            ll = state['groups_lights'][place]
            for dd in ll.keys():
                messages.append(json.dumps({'device_name':ll[dd], 
                    'value':dd, 'command':'turn_on', 'origin':self.name}))
        else:       
            for place in self.candidates_off:
                state['last_motion'][place] = state['timestamp']
                ll = state['groups_lights'][place]
                for dd in ll.keys():
                    messages.append(json.dumps({'device_name':ll[dd], 'value':dd, 
                        'command':'turn_off', 'origin':self.name}))
        return messages

    def check_event(self, ev_content,  state):
        fire = False
        value = ''
        devices = state['devices']
        #print ev_content
        if ev_content:
            # turn on if motion event 
            if(ev_content['event_type']=='motion' and ev_content['value']):
                place = devices[ev_content['device_name']].place
                state['last_motion'][place] = state['timestamp']
                try: 
                    if(int(state['photo'][place]) < int(state['min_photo'][place])):
                        fire = True
                        value = 'on'
                except:
                    fire = True
                    value = 'on'
                if(place in self.last_auto_off):
                    if(state['timestamp'] - self.last_auto_off[place] < 5):
                        self.delays[place] = min(self.base_delays[place]*1.5, 60*8)
                    if(state['timestamp'] - self.last_auto_off[place] > 60):
                        self.delays[place] = self.base_delays[place]

            # at heartbeat, check what needs to be turned off
            if(ev_content['event_type']=='heartbeat'):
                self.candidates_off = []
                for place in self.delays.keys():
                    if(state['timestamp'] - state['last_motion'][place] > self.delays[place]):
                        self.candidates_off.append(place)
                        self.last_auto_off[place] = state['timestamp']
                if(len(self.candidates_off) > 0):
                    fire = True
                    value = 'off'

        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value
