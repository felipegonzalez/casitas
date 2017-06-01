import json



class AppNoMotionLight():
    def __init__(self):
        self.delays = {'sala':10, 'bano_visitas':10, 'bano_principal':10, 'cocina':10}
        self.candidates = []
        #self.device = device

    def activate(self, ev_content, state, r):
        devices = state['devices']
        messages = []
        print(self.candidates)
        for place in self.candidates:
            state['last_motion'][place] = state['timestamp']
            ll = state['groups_lights'][place]
            for dd in ll.keys():
                messages.append(json.dumps({'device_name':ll[dd], 'value':dd, 'command':'turn_off'}))
        return messages


    def check(self, ev_content,  state):
        fire = False
        devices = state['devices']
        #print ev_content
        self.candidates = []
        for place in self.delays.keys():
            if(state['timestamp'] - state['last_motion'][place] > self.delays[place]):
                self.candidates.append(place)
                fire = True
        return fire


