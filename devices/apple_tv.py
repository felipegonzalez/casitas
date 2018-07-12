import json
import time
import pyatv
import asyncio

class AppleTV(object):

    def __init__(self, name, init, messager):
        self.ip_address= init['ip_address']
        self.name = name
        self.place = init['place']
        self.appletv_name = init['name']
        self.login_id = init['login_id']
        self.port = init['port']
        self.state = {}
        self.details = pyatv.AppleTVDevice(self.name, self.ip_address, self.login_id)
        self.messager = messager
        if('polling' in init.keys()):
            self.polling = init['polling']
        else:
            self.polling = 30
        self.last_check = 0
        self.children = {}
        if('children' in init):
            self.children = init['children']
        self.delay = 240
        self.last_off = 0



    def parse(self, message):
        # general response 
        parsed_m = []
        #print("Mensaje:")
        #print(message)
        #print(message['data'])
        try:
            message_p = json.loads(message['data'])
            #print(message_p)
        except Exception as ex:
            print("Error parsing message appletv: " + message['data']) 
            print(ex)
        return parsed_m


    @asyncio.coroutine
    def get_playing(self, loop, details):
        atv = pyatv.connect_to_apple_tv(details, loop)
        try:
            playing = yield from atv.metadata.playing()
            self.state['play_state'] = playing.play_state
            self.state['title'] = playing.title
            self.state['status'] = "connected"
            print('Currently playing:')
            print(playing)
        except Exception as ex:
            self.state["status"] = "disconnected"
            print("Error")
            print(ex)
            yield from atv.logout()

    @asyncio.coroutine
    def stop_tv(self, loop, details):
        atv = pyatv.connect_to_apple_tv(details, loop)
        rc = atv.remote_control
        try:
            yield from rc.stop()
        except Exception as ex:            
            print("Error")
            print(ex)

    @asyncio.coroutine
    def play(self, loop, details):
        atv = pyatv.connect_to_apple_tv(details, loop)
        rc = atv.remote_control
        try:
            yield from rc.play()
        except Exception as ex:            
            print("Error")
            print(ex)

    @asyncio.coroutine
    def start_tv(self, loop, details):
        atv = pyatv.connect_to_apple_tv(details, loop)
        rc = atv.remote_control
        try:
            yield from rc.menu()
        except Exception as ex:            
            print("Error")
            print(ex)

    def update(self, state):
        if(self.polling > 0):
            if(time.time() - self.last_check > self.polling):
                self.last_check = time.time()
                state['loop'].run_until_complete(self.get_playing(state['loop'], self.details))
                state['devices_state'][self.name] = self.state
                if(state["timestamp"] - state["last_motion"][self.place] > self.delay):
                    if(self.state["play_state"]==4):
                        self.turn_off(command = "", state = state)
                        self.last_off = time.time()
            if((time.time() - self.last_off) < 10 and (time.time() - state["last_motion"][self.place]) < 20):
                state['loop'].run_until_complete(self.play(state['loop'], self.details))
        return


    # we define these functions which are available to the system:
    def turn_on(self, command, state):
        print("Turn apple tv on")
        if(self.state['play_state']!=4):
            state['loop'].run_until_complete(self.start_tv(state['loop'], self.details))
        return

    def turn_off(self, command, state):
        print("***************** Stopping tv.")
        state['loop'].run_until_complete(self.stop_tv(state['loop'], self.details))
        return