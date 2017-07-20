import json
import time
from soco import SoCo
import soco
import os

class Sonos(object):

    def __init__(self, name, init, messager):
        self.name = name
        self.pref_zone = init['children']['1']
        sonos_list = soco.discover()
        zones = []
        while(len(sonos_list) > 0):
            player = sonos_list.pop()
            zones.append(player)
            if(player.player_name == self.pref_zone):
                self.sonos = player

        print(zones[0].player_name)
        print(zones[1].player_name)
        self.zones = zones

        self.state = {}

        self.prev_state = {'volume':self.sonos.volume}
        #self.children = init['children']
        self.messager = messager
        self.polling = 60
        self.last_check = time.time()
        #self.last_on = {}
        #for item in self.children:
        #    self.last_on[self.children[item]] = 0



    def parse(self, message):
        # deal with gets from states
        parsed_m = ''
        return parsed_m

    def set_volume(self, command, state):
        try:
            self.sonos.volume = command['value']
        except:
            print('Error setting sonos volume')
        return


    def say(self, command, state):
        #data = json.loads(command['data']) 
        state_s = {}
        
        text = command['value']
        self.prev_state['volume'] = self.sonos.volume
        #try:
        self.sonos.volume = 80
        os.system("say -v Paulina '"+text+"' -o "+"/Volumes/mmshared/sonidos/voz.mp4")
        state_s = self.play("voz.mp4")
        duration_txt = self.sonos.get_current_track_info()['duration']
        alertDuration = 60*int(duration_txt.split(':')[1])  +  int(duration_txt.split(':')[2])
        r = self.messager
        com = json.dumps({'device_name':'sonos', 'command':'set_volume',
            'value':self.prev_state['volume']})
        r.publish('commands', 
            json.dumps({'device_name':'timer_1', 'command':'add_timer',
                'interval':alertDuration + 2, 'value':com}))
            #sonos.play_uri('x-file-cifs:%s' % '//homeserver/sonidos/voz.mp4')
        #except:
        #    print("Error say!")
        return
   
    def play(self, file):
        try:
            #sonos = self.zones[0]

            track = self.sonos.get_current_track_info()
            playlistPos = int(track['playlist_position'])-1
            trackPos = track['position']
            trackURI = track['uri']

            # This information allows us to resume services like Pandora
            mediaInfo = self.sonos.avTransport.GetMediaInfo([('InstanceID', 0)])
            #mediaURI = mediaInfo['CurrentURI']
            #mediaMeta = mediaInfo['CurrentURIMetaData']
            transport_state = self.sonos.get_current_transport_info()['current_transport_state']
            volumen = self.sonos.volume
            self.sonos.play_uri('x-file-cifs://homeserver/sonidos/' + file)
            duration_txt = self.sonos.get_current_track_info()['duration']
            #alertDuration = 60*int(duration_txt.split(':')[2]) + 
            #sleepTime=2
            #time.sleep(sleepTime)
            #if len(zp.get_queue()) > 0 and playlistPos > 0:
        #    print 'Resume queue from %d: %s - %s' % (playlistPos, track['artist'], track['title'])
        #    sonos.play_from_queue(playlistPos)
        #    sonos.seek(trackPos)
        #else:
        #    print 'Resuming %s' % mediaURI
        #    sonos.play_uri(mediaURI, mediaMeta)
        #tiempo = time.time()
        #estado_salida = {'track':track, 'mediaInfo':mediaInfo, 
        #                'alertDuration':alertDuration, 'tiempo_inicio':tiempo,
        #                'state':transport_state, 'volumen':volumen}
        #print estado_salida

        except ValueError:
            print("Error sonos")
        return 
 
    def update(self, state):
        if(state['timestamp']-self.last_check > self.polling):
            pass
            self.last_check = time.time()
        return