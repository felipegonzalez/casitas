import json
import time
import datetime

class Timer():
    def __init__(self, name, init, messager):
        self.name = name
        self.polling = 2
        self.last_check = time.time()
        self.place =  init['place']
        self.messager = messager
        #these timers and alarms are commands
        self.timers = []
        self.timestamp = time.time()
        self.timers_fire = []
        self.state = self.timers

    def parse(self, ev_content):
        return

    def add_timer(self, command, state):
        # interval is seconds
        self.timestamp = time.time()
        time_to_fire = self.timestamp + command['interval'] 
        self.timers.append((time_to_fire, command['value']))
        self.state = self.timers
        return 

    #def add_alarm(self, command, state):
    #   self.timestamp = time.time()
   #    self.add_timer(self, command, self.timestamp - time_alarm)

   
    def activate(self, state):
        for i, timer in enumerate(self.timers_fire):
            print("Publishing timer command")
            self.messager.publish('commands', timer[1])
            del self.timers_fire[i]
        return

    def get_pending(self):
        return self.timers

    def update(self, state):
        #self.timestamp = time.time()
        if(time.time() - self.last_check > self.polling):
            #print(self.timers)
            self.timers_fire = []
            #alarms_fire = []
            fire = False
            self.timestamp = time.time()
            for i, timer in enumerate(self.timers):
                if(self.timestamp > timer[0]):
                    self.timers_fire.append(timer)
                    del self.timers[i]
            #check commands
            if(len(self.timers_fire) > 0):
                self.activate(state)
            self.last_check = time.time()
        self.state = self.timers
        return


