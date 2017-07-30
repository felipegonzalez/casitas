import os, os.path
import random
import string
import json
#import sqlite3 as lite
import HTML
import cherrypy
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
#from casitas import app_timer

cherrypy.server.socket_host = '0.0.0.0'


class control(object):

    @cherrypy.expose
    def remoto(self, secreto=''):
        salida = ''
        if(secreto=='momoycuca'):
            salida = open('index_simple.html')
        return salida



    @cherrypy.expose
    def garage(self):
        mensaje = 'Activando garage'
        r.publish('commands', json.dumps({"device_name":"caja_garage",
            "command":"send_command", "value":"garage_open"}))
        r.publish('commands', json.dumps({"device_name":"sonos",
                "command":"say", "value":"Puerta de garage activada"})) 
        r.publish('commands', json.dumps({"device_name":"pushover",
                "command":"send_message", "value":"Puerta de garage activada"})) 
        return mensaje


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port':8091})
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },

         '/dist/css/bootstrap.min.css': {
		'tools.staticfile.on' : True,
		'tools.staticfile.filename' : "/Users/felipe/casitas/webapp/dist/css/bootstrap.min.css"
        },
        '/dist/jquery/jquery-2.0.3.min.js': {
        'tools.staticfile.on' : True,
        'tools.staticfile.filename' : "/Users/felipe/casitas/webapp/dist/jquery/jquery-2.0.3.min.js"
        },
        '/dist/app.js':{
            'tools.staticfile.on' : True,
            'tools.staticfile.filename' : "/Users/felipe/casitas/webapp/dist/app.js"
        },
        '/img':{
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : "/Volumes/mmshared/web_img"
        }
}
    webapp = control()

    cherrypy.quickstart(webapp, '/', conf)
