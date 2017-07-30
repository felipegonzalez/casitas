import time
import json

class XbeeBox(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.addr_long = init['addr_long']
        self.place = init['place']
        self.state = {}
        self.polling = 60
        self.last_check = time.time()
        if('pins' in init):
            self.pins = init['pins']
        else:
            self.pins = {}
        if('txcommands' in init):
            self.txcommands = init['txcommands']

        if ('children' in init.keys()):
            self.children = init['children'] #dictionary {'luzchica':'D2', ...}
            for child in self.children.keys():
                # suppose all pins are off
                self.state[child] = 'off'
        else:
            self.children = None

        self.messager = messager


    def parse(self, ev_content):
        self.last_check = time.time()
        events = []
        try:
            if(ev_content['type']=='rf_data'):
                data = ev_content['content'].split('\r\n')
                #print(data)
                for elem in data:
                    try:
                        if(len(elem) > 0):
                            ev_split = elem.split(',')
                            event_type = ev_split[0]
                            value = ev_split[3]
                            internal_id = ev_split[2]
                            units = ev_split[1]
                            if(event_type=='pir'):
                                event_type ='motion'
                                value = int(value)==1
                                #if(value):
                                #    print("motion reg***********")
                            events.append({'device_name':self.name, 
                                'event_type':event_type, 'value':value,
                                'internal_id':internal_id, 'units':units})
                    except:
                        print("Error parsing element")
                        print(elem)
            if(ev_content['type']=='samples'):
                for elem in ev_content['content']:
                    for k in elem.keys():
                        event_type = self.pins[k]
                        value = elem[k]
                        events.append({'device_name':self.name,
                         'event_type':event_type, 'value':value})
        except:
            print("Error parsing xbee message")
            print(data)
            raise
        return events

    def send_command(self, command, state):
        new_message = {'addr_long': self.addr_long, 'mode':'tx',
            'data':self.txcommands[command['value']]}
        self.messager.publish('xbee-commands', json.dumps(new_message))
        return

    def turn_on(self, command, state):
        #command = json.loads(command['data']) should be done before
        #if (self.children[command['value']] in state['lights']):
        #    state['last_motion'][self.place] = state['timestamp']
        new_message = {"addr_long": self.addr_long, "command":self.children[command['value']], 
                       "parameter":"05", "mode":"pin"}
        self.state[command['value']] = 'on'
        self.messager.publish('xbee-commands', json.dumps(new_message))
        print('Encender xbee')
        return
        
    def turn_off(self, command, state):
        #command = json.loads(command['data']) should be done before
        new_message = {"addr_long": self.addr_long, "command":self.children[command['value']], 
                       "parameter":"04", "mode":"pin"}
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