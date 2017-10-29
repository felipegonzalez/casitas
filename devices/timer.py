import json
import time
import datetime
from ast import literal_eval as make_tuple

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
        #get timers from redis
        current_timers = self.messager.hgetall('timers ' + self.name)
        print(current_timers)
        for k in current_timers.keys():
            timer_str = current_timers[k].decode('utf-8')
            timer_tuple = make_tuple(timer_str)
            new_tuple = (timer_tuple[0], json.loads(timer_tuple[1]))
            self.timers.append(new_tuple)
        self.state = self.timers
        print(self.state)

    def parse(self, ev_content):
        return

    def add_timer(self, command, state):
        # interval is seconds
        self.timestamp = time.time()
        time_to_fire = self.timestamp + command['interval'] 
        self.timers.append((time_to_fire, command['value']))
        # save in redis
        self.messager.hset('timers '+self.name, time_to_fire, (time_to_fire, command['value']))
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
                    self.messager.hdel('timers '+self.name, timer[0])
            #check commands
            if(len(self.timers_fire) > 0):
                self.activate(state)
            self.last_check = time.time()
            self.state = self.timers
            state['devices_state'][self.name] = self.state
        return


