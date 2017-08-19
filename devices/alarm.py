import json
import time

class Alarm(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.place = init['place']
        self.state = {}
        self.messager = messager
        self.polling = 30
        self.last_alarm = 0
        self.last_check = 0


    def parse(self, message):
        # general response 
        parsed_m = []
        #message_p = json.loads(message['data'])
        #if(isinstance(message_p, dict)):
        #    if(message_p['type'] == 'status'):
        #        for elem in message_p['events']:
                    #self.status[elem] = message_p['values'][elem]
        #            parsed_m.append(json.loads(message_p['events'][elem]))
        return parsed_m

    def update(self, state):
        return

    def sound_alarm(self, command, state):
        r = self.messager
        if(time.time() - self.last_alarm > 10):
            self.last_alarm = time.time()
            if(command['value']=='gas'):
                r.publish('commands', json.dumps({'device_name':'pushover', 'command':'send_message',
                    'value':'Alarma de gas'}))
                r.publish('commands', json.dumps({'device_name':'sonos', 'command':'say',
                    'value':'Alarma de gas', 'volume':100}))
            if(command['value']=='temperature'):
                r.publish('commands', json.dumps({'device_name':'pushover', 'command':'send_message',
                    'value':'Alarma de temperatura'}))
                r.publish('commands', json.dumps({'device_name':'sonos', 'command':'say',
                    'value':'Alarma de temperatura'}))          
