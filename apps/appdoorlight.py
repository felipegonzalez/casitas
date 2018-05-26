import json


class AppDoorLight():
    def __init__(self, place_lights):
        self.place_lights = place_lights
        self.door_mapping = {'hall_entrada':['Entrance hall','Front door',
        'Patio stairs one', 'Patio stairs two', 'Patio stairs three',
        'Entrance table', 'Caballeriza uno', 'Caballeriza dos'],
        'patio':['Caballeriza uno','Caballeriza dos', 'Patio stairs one',
        'Patio stairs two', 'Patio stairs three', 'Front door']}
        self.status = 'on'
        self.name = "app_doorlight"

    def activate(self, ev_content, state, r, value):
        devices = state['devices']
        place = devices[ev_content['device_name']].place
        #state['last_motion'][place] = state['timestamp']
        #a = self.door_mapping[place]
        to_light = []
        for ll in self.door_mapping[place]:
            current_place = state['place_lights'][ll]
            state['last_motion'][current_place] = state['timestamp']
            if(int(state['photo'][current_place]) < int(state['min_photo'][current_place])):
                to_light.append(ll)

        #ll = state['groups_lights'][place]
        #print(to_light)
        mensajes = []
        for dd in to_light:
            mensajes.append(json.dumps({'device_name':'hue', 'value':dd, 
                'command':'turn_on', 'origin':self.name}))
        return mensajes



    def check_event(self, ev_content,  state):
        fire = False
        devices = state['devices']
        value =''
        #print ev_content
        if ev_content:
            if(ev_content['event_type']=='door' and not(ev_content['value'])):
                place = devices[ev_content['device_name']].place
                places_fire = self.door_mapping[place]
                for ll in places_fire:
                    pl = self.place_lights[ll]
                    if(int(state['photo'][pl]) < int(state['min_photo'][pl])):
                        fire = fire or True
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        #if comm_content:
        #    if(comm_content['value']=='garage_open'):
        #        state['last_motion']['patio'] = state['timestamp']
        #        state['last_motion']['escaleras_patio'] = state['timestamp']
        #        state['last_motion']['hall_entrada'] = state['timestamp']
                #places_fire = self.door_mapping['hall_entrada']
                #for ll in places_fire:
                #    pl = self.place_lights[ll]
                #    if(int(state['photo'][pl]) < int(state['min_photo'][pl])):
                #        fire = fire or True
        return fire, value
