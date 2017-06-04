import json


class AppDoorLight():
    def __init__(self):
        pass
        self.door_mapping = {'hall_entrada':['Entrance hall','Front door',
        'Patio stairs one', 'Patio stairs two']}
        #self.device = device

    def activate(self, ev_content, state, r):
        devices = state['devices']
        place = devices[ev_content['device_name']].place
        state['last_motion'][place] = state['timestamp']
        ll = self.door_mapping[place]
        #ll = state['groups_lights'][place]
        mensajes = []
        for dd in ll:
            mensajes.append(json.dumps({'device_name':'hue', 'value':dd, 'command':'turn_on'}))
        return mensajes



    def check(self, ev_content,  state):
        fire = False
        devices = state['devices']
        #print ev_content

        if ev_content:
            if(ev_content['event_type']=='door' and not(ev_content['value'])):
                place = devices[ev_content['device_name']].place
                #if(int(state['photo'][place]) < int(state['min_photo'][place])):
                fire = True
        return fire


