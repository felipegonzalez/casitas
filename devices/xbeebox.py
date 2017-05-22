import time

class XbeeBox(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.dest_addr_long = init['dest_addr_long']
        self.place = init['place']
        self.state = {}
        self.polling = 60
        self.last_check = 0

        if ('children' in init.keys()):
            self.children = init['children'] #dictionary {'luzchica':'D2', ...}
            for child in self.children.keys():
                # suppose all pins are off
                self.state[child] = 'off'
        else:
            self.children = None

        self.messager = messager


    def parse(self, ev_content):
        #in this case, xbee only has motion sensor
        data = ev_content['data']
        events = []
        for key in data.keys():
            event_type = key
            value = data[key]
            events.append({'device_name':self.name, 'event_type':event_type, 'value':value})
        return events

    def turn_on(self, command, state):
        #data = json.loads(command['data']) should be done before
        if (self.children[command['value']] in state['lights']):
            state['last_motion'][self.place] = state['timestamp']
        new_message = {'dest_addr_long': self.dest_addr_long, 'command':self.children[command['value']], 
                       'parameter':'\x05', 'mode':'pin'}
        self.state[command['value']] = 'on'
        self.messager.publish('xbee-commands', new_message)
        print('Encender xbee')
        return
        
    def turn_off(self, command, state):
        #data = json.loads(command['data']) should be done before
        new_message = {'dest_addr_long': self.dest_addr_long, 'command':self.children[command['value']], 
                       'parameter':'\x04', 'mode':'pin'}
        self.state[command['value']] = 'off'
        self.messager.publish('xbee-commands', new_message)
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