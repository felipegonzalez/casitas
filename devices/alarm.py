import time

class Alarm(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.state =  init['state'] #armed, unarmed
        self.messager =  messager
        self.polling = 10000
        self.last_check = 0


    
    def parse(self, m):
        parsed_m = {'device':m['device'], 'event_type':'fired', 'value':'on'}
        return parsed_m

    def arm(self, command, state):
        self.state = 'armed'
        return
        
    def unarm(self, command, state):
        self.state = 'unarmed'
        return

    def fire(self, command, state):
        self.state = 'unarmed'
        print("Alarm!!!")
        return


    def update(self, state):
        if(state['timestamp']-self.last_check > self.polling):
            self.last_check = time.time()
        return