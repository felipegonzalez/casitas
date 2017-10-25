import json
import time
import os
from pushover import Client



class PushMessenger(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state = {}
        # for push notifications
        self.pb_key = os.environ.get('PB_TOKEN')
        self.pb_api_key = os.environ.get('PB_API_TOKEN')
        self.client = Client(self.pb_key, api_token = self.pb_api_key)

        #self.client.send_message("Iniciando sistema", title="Notificación")
        #self.children = init['children']
        self.messager = messager
        self.polling = 120
        self.last_check = 0
        self.place = init['place']


    def parse(self, message):
        parsed_m = []
        return parsed_m

    def send_message(self, command, state):
        try:
            self.client.send_message(command['value'], title="Notificación")
        except:
            print("Pushover no disponible")

        return 

    def update(self, global_state):
        if(global_state['timestamp']-self.last_check > self.polling):
            pass
            self.last_check = time.time()
        return