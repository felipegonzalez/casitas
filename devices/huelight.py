class HueLight(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.ip_address= init['ip_address']
        self.light_num = init['light_num']
        self.place = init['place']
        self.state = {}
        self.messager = messager
        if('children' in init.keys()):
            self.children = init['children']
        else:
            self.children = None

    def parse(self, message, r):
        parsed_m = ''
        return parsed_m

    def turn_on(self, command, state, r):
        print('Encender hue light')
        return 
        
    def turn_off(self, command, state, r):
        print('Apagar hue light')
        return 
