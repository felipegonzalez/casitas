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
        zones = {}
        while(len(sonos_list) > 0):
            player = sonos_list.pop()
            zones[player.player_name] = player
            if(player.player_name == self.pref_zone):
                self.sonos = player
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

    def play(self, command, state):
        if('zone' in command.keys()):
            zone = command['zone']
        else:
            zone = self.sonos.player_name
        self._play(command['value'], volume = command['volume'], player_name = zone)
        return

    def say(self, command, state):
        #data = json.loads(command['data'])         
        text = command['value']
        self.prev_state['volume'] = self.sonos.volume
        #try:
        os.system("say -v Paulina '"+text+"' -o "+"/Volumes/mmshared/sonidos/voz.mp4")
        self._play("voz.mp4", volume = 80)        
        
            #sonos.play_uri('x-file-cifs:%s' % '//homeserver/sonidos/voz.mp4')
        #except:
        #    print("Error say!")
        return


   
    def _play(self, file, volume = 100, player_name = None):
        if(player_name is None):
            player = self.sonos
        else:
            player = self.zones[player_name]
        try:
            #sonos = self.zones[0]
            track = player.get_current_track_info()
            playlistPos = int(track['playlist_position'])-1
            trackPos = track['position']
            trackURI = track['uri']

            # This information allows us to resume services like Pandora
            mediaInfo = player.avTransport.GetMediaInfo([('InstanceID', 0)])
            #mediaURI = mediaInfo['CurrentURI']
            #mediaMeta = mediaInfo['CurrentURIMetaData']
            transport_state = player.get_current_transport_info()['current_transport_state']
            volume_before = player.volume
            player.volume = volume
            player.play_uri('x-file-cifs://homeserver/sonidos/' + file)
            duration_txt = self.sonos.get_current_track_info()['duration']
            alertDuration = 60*int(duration_txt.split(':')[1])  +  int(duration_txt.split(':')[2])
            r = self.messager
            # go back to previous values
            com = json.dumps({'device_name':'sonos', 'command':'set_volume',
                'value':volume})
            r.publish('commands', 
                json.dumps({'device_name':'timer_1', 'command':'add_timer',
                'interval':alertDuration + 2, 'value':com}))


   
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