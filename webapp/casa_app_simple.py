import os, os.path
import random
import string
import json
#import sqlite3 as lite
import HTML
import cherrypy
from cherrypy import tools
import os, sys
sys.path.insert(0,os.path.pardir)
from settings import r 
#from casitas import app_timer

cherrypy.server.socket_host = '0.0.0.0'

house_secret = 'momoycuca'

class control(object):

    @cherrypy.expose
    def remoto(self, secreto=''):
        salida = ''
        if(secreto==house_secret):
            salida = open('index_simple.html')
        return salida

    @cherrypy.expose
    @tools.json_out()
    def micro_weather(self, **kwargs):
        secreto = kwargs.get('secreto', None)
        temps = {}
        humedad = {}
        weath_out ={}
        lugares = ['recamara_principal', 'sala', 'estudiof','cocina',
            'hall_entrada', 'patio', 'exterior', 'pasillo_comedor']
        if(secreto==house_secret):
            for lugar in lugares:
                temps[lugar] = float(r.hget('temperature', lugar).decode('utf-8'))
                humedad[lugar] = float(r.hget('humidity', lugar).decode('utf-8'))
            weath_out['planta baja'] = round((temps['sala'] + temps['estudiof'])/2, 2)
            weath_out['planta alta'] = round(temps['recamara_principal'],2)
            weath_out['exterior'] = round(temps['exterior'],2)
            weath_out['humedad_dentro'] = round((humedad['sala'] + humedad['cocina'] )/2,1)
            weath_out['humedad_fuera'] = humedad['exterior']
            print(weath_out)
        return (weath_out)

    @cherrypy.expose
    @tools.json_out()
    def devices(self, **kwargs):
        secreto = kwargs.get('secreto', None)
        state_appliances = {}
        if(secreto == house_secret):
            state_appliances_b = r.hgetall('devices')
            for dev_name in state_appliances_b.keys():
                if(dev_name != 'solcast'):
                    state_appliances[dev_name] = json.loads(state_appliances_b[dev_name])
        return state_appliances

    @cherrypy.expose
    @tools.json_out()
    def apps(self, **kwargs):
        secreto = kwargs.get('secreto', None)
        state_app = {}
        if(secreto == house_secret):
            state_app_b = r.hgetall('apps')
            for app_name in state_app_b.keys():
                try: 
                    state_app[app_name] = json.loads(state_app_b[app_name])
                except Exception as ex:
                    print(ex)
        return state_app


    @cherrypy.expose
    def garage(self):
        mensaje = 'Activando garage'
        r.publish('commands', json.dumps({"device_name":"caja_garage",
            "command":"activate", "value":"garage", "origin":"webapp"}))
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

