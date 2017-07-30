import json
import time

class Esp6288(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.state = {}
        self.messager = messager
        self.polling = 30
        self.last_check = 0


    def parse(self, message):
        parsed_m = []
        return parsed_m

    def update(self, state):
        return
