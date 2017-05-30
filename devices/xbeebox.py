import time
import json

class XbeeBox(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.addr_long = init['addr_long']
        self.place = init['place']
        self.state = {}
        self.polling = 60
        self.last_check = 0
        if('pins' in init):
            self.pins = init['pins']
        else:
            self.pins = {}

        if ('children' in init.keys()):
            self.children = init['children'] #dictionary {'luzchica':'D2', ...}
            for child in self.children.keys():
                # suppose all pins are off
                self.state[child] = 'off'
        else:
            self.children = None

        self.messager = messager


    def parse(self, ev_content):
        events = []
        if(ev_content['type']=='rf_data'):
            data = ev_content['content'].split('\r\n')
            #print(data)
            for elem in data:
                if(len(elem) > 0):
                    ev_split = elem.split(',')
                    event_type = ev_split[0]
                    value = ev_split[3]
                    if(event_type=='pir'):
                        event_type ='motion'
                    events.append({'device_name':self.name, 'event_type':event_type, 'value':value})
        if(ev_content['type']=='samples'):
            for elem in ev_content['content']:
                for k in elem.keys():
                    event_type = self.pins[k]
                    value = elem[k]
                    events.append({'device_name':self.name, 'event_type':event_type, 'value':value})
        return events

    def turn_on(self, command, state):
        #data = json.loads(command['data']) should be done before
        if (self.children[command['value']] in state['lights']):
            state['last_motion'][self.place] = state['timestamp']
        new_message = {'addr_long': self.addr_long, 'command':self.children[command['value']], 
                       'parameter':'05', 'mode':'pin'}
        self.state[command['value']] = 'on'
        self.messager.publish('xbee-commands', new_message)
        print('Encender xbee')
        return
        
    def turn_off(self, command, state):
        #data = json.loads(command['data']) should be done before
        new_message = {'addr_long': self.addr_long, 'command':self.children[command['value']], 
                       'parameter':'04', 'mode':'pin'}
        self.state[command['value']] = 'off'
        self.messager.publish('xbee-commands', json.dumps(new_message))
        print('Apagar xbee')
        return 

    def press(self, m, state):
        # use threading to implement press on for a while without blocking main loop
        # or define timers to go with update?
        return

    def update(self, state):
        if(state['timestamp']-self.last_check > self.polling):
            # code here to update if necessary
            self.last_check = time.time()
        return