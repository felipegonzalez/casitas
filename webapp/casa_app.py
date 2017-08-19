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
from settings import ip_dict
#from casitas import app_timer

cherrypy.server.socket_host = '0.0.0.0'


class control(object):

    @cherrypy.expose
    def controlcasa(self):
        return open('index_main.html')

    @cherrypy.expose
    def llegada(self):
        return "Veo llegada"

    @cherrypy.expose
    def send_event(self, event_type, value):
        ip_origin = cherrypy.request.remote.ip
        if(ip_origin in ip_dict.keys()):
            device_name = ip_dict[ip_origin]
        else:
            device_name = 'unknown'
        ev = {'device_name':device_name, 'event_type':event_type, 
            'value':value}
        r.publish('events', json.dumps(ev))
        return json.dumps(ev)

    @cherrypy.expose
    def ring(self, lugar):
        print("ring")
        #r.publish('commands', json.dumps({'device_name':'sonos',
        #    'command':'play','value':'store_bell.wav',
        #    'volume':100, 'zone':'Estudio' }))
        r.publish('events', json.dumps({'device_name':'caja_cocina_timbre',
            'event_type':'timbre', 'value':True}))
        return 'Ring!!'    

    @cherrypy.expose
    def location(self):
        print("Location")
        return
        
    @cherrypy.expose
    def autoluz(self):
        message_say =json.dumps({'device_name':'sonos',
            'command':'say', 'value':'Auto luces'
            })
        r.publish('commands', message_say)
        #con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
        #with con:
        #    cur = con.cursor()
        #    commandx = "INSERT INTO pendientes VALUES('auto_luces','0')"
        #    cur.execute(commandx)
        return 'Auto luces' 



    #@cherrypy.expose
    #def alarmas_reset(self):
    #    con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
    #    with con:
    #        cur = con.cursor()
    #        commandx = "INSERT INTO pendientes VALUES('alarmas_reset','0')"
    #        cur.execute(commandx)
    #    return 'Reestableciendo alarmas'


    # @cherrypy.expose
    # def garage(self):
    #     con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
    #     with con:
    #         cur = con.cursor()
    #         commandx = "INSERT INTO pendientes VALUES('abrir_garage','1')"
    #         cur.execute(commandx)
    #     return 'Activando garage'

    # @cherrypy.expose
    # def alarma(self, sw):
    #     con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
    #     with con:
    #         cur = con.cursor()
    #         if(sw=='1'):
    #             commandx = "INSERT INTO pendientes VALUES('activar_alarma','1')"
    #             mensaje = 'Activando alarma'
    #         else:
    #             commandx = "INSERT INTO pendientes VALUES('activar_alarma','0')"
    #             mensaje = 'Desactivando alarma'
    #         cur.execute(commandx)
    #     return mensaje

    # @cherrypy.expose
    # def chapa(self, sw):
    #     con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
    #     with con:
    #         cur = con.cursor()
    #         if(sw=='1'):
    #             commandx = "INSERT INTO pendientes VALUES('chapa','1')"
    #             mensaje ='Cerrar chapa'
    #         if(sw=='0'):
    #             commandx = "INSERT INTO pendientes VALUES('chapa','0')"
    #             mensaje = 'Abrir chapa'
    #         cur.execute(commandx)
    #     return mensaje
    @cherrypy.expose
    def filtro_alberca(self, sw):
        if(sw=='0'):
            r.publish('commands', json.dumps({"device_name":"caja_filtro_alberca",
            "command":"turn_off", "value":"bomba", "origin":"webapp"}))
        if(sw=='1'):
            r.publish('commands', json.dumps({"device_name":"caja_filtro_alberca",
            "command":"turn_on", "value":"bomba", "origin":"webapp"}))
        return 'Bomba alberca'

    @cherrypy.expose
    def garage(self):
        mensaje = 'Activando garage'
        r.publish('commands', json.dumps({"device_name":"caja_garage",
            "command":"send_command", "value":"garage_open", "origin":"webapp"}))
        r.publish('commands', json.dumps({"device_name":"sonos",
                "command":"say", "value":"Puerta de garage activada"})) 
        r.publish('commands', json.dumps({"device_name":"pushover",
                "command":"send_message", "value":"Puerta de garage activada"})) 
        return mensaje

    @cherrypy.expose
    def detecta_movimiento(self, sw):
        mensaje = 'Detector mov ' + str(sw)
        if(sw=='1'):
            r.publish('commands', json.dumps({"device_name":"cam_entrada",
                "command":"set_motion_detect", "value":"on", "origin":"webapp"
                }))
            r.publish('commands', json.dumps({"device_name":"cam_patio",
                "command":"set_motion_detect", "value":"on","origin":"webapp"
                }))
            #app_timer.add_timer((20, json.dumps({"device_name":"caja_goteo",
            #    "command":"turn_off", "value":"regar"})))
        if(sw=='0'):
            print("apagando")
            r.publish('commands', json.dumps({"device_name":"cam_entrada",
                "command":"set_motion_detect", "value":"off", "origin":"webapp"
                }))
            r.publish('commands', json.dumps({"device_name":"cam_patio",
                "command":"set_motion_detect", "value":"off", "origin":"webapp"
                })) 
        return mensaje

    @cherrypy.expose
    def regar(self, sw):
        mensaje = 'Sistema de goteo' + str(sw)
        if(sw=='1'):
            r.publish('commands', json.dumps({"device_name":"caja_goteo",
                "command":"turn_on", "value":"regar", "origin":"webapp"
                }))
            r.publish('commands', json.dumps({"device_name":"sonos",
                "command":"say", "value":"Regando ahora", "origin":"webapp"}))
            message_off =json.dumps({'device_name':'caja_goteo',
                'command':'turn_off', 'value':'regar', "origin":"timer"})
            r.publish('commands', json.dumps({"device_name":"timer_1",
                "command":"add_timer", "interval":60*30, 
                "value":message_off, "origin":"webapp"}))
            #app_timer.add_timer((20, json.dumps({"device_name":"caja_goteo",
            #    "command":"turn_off", "value":"regar"})))
        if(sw=='0'):
            r.publish('commands', json.dumps({'device_name':'caja_goteo',
                'command':'turn_off', 'value':'regar', "origin":"webapp"
                }))
            r.publish('commands', json.dumps({"device_name":"sonos",
                "command":"say", "value":"Riego apagado", "origin":"webapp"}))  
        # con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
        # with con:
        #     cur = con.cursor()
        #     if(sw=='1'):
        #         commandx = "INSERT INTO pendientes VALUES('regar','1')"
        #         mensaje ='Regar patio'
        #     if(sw=='0'):
        #         commandx = "INSERT INTO pendientes VALUES('regar','0')"
        #         mensaje = 'Dejar de regar patio'
        #     cur.execute(commandx)
        return mensaje

class infoBasica(object):
    exposed = True
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, resp=''):
        lugares = ['recamara_principal', 'sala', 'estudiof','cocina',
            'hall_entrada', 'patio', 'exterior']
        apps_mon = ['app_doorlight', 'app_autolight', 'app_doorbell']
        out = []
        for lugar in lugares:
            temp = r.hget('temperature', lugar).decode('utf-8')
            if(float(temp) != 0):
                out.append((lugar, 'Temperatura', temp))
        #for lugar in lugares:
        #    temp = r.hget('temperature', lugar).decode('utf-8')
        #    if(float(temp) != 0):
        #        out.append((lugar, 'Temperatura', temp))
        for lugar in lugares:
            humd = r.hget('humidity', lugar).decode('utf-8')
            if(float(humd) != 0):
                out.append((lugar, 'Humedad', humd))
        for lugar in lugares:
            motion = r.hget('motion', lugar).decode('utf-8')
            if(motion=='True'):
                out.append((lugar, 'Movimiento', motion))
        kw = r.hget('power usage', 'ct kW').decode('utf-8')
        out.append(('casa', 'Consumo (kW)', kw))
        amps = r.hget('power usage', 'ct A').decode('utf-8')
        out.append(('casa', 'Consumo (A)', kw))
            
        riego = r.get('riego').decode('utf8')
        out.append(('patio', 'Riego por goteo', riego))
        try:
            dist = r.get('Nivel cisterna').decode('utf8')
            out.append(('cisterna', 'Nivel', dist))
        except:
            pass
        for appname in apps_mon:
            app_status = r.hget('apps', appname).decode('utf-8')
            out.append(('app', appname, app_status))


        # con2 = lite.connect('/Volumes/mmshared/bdatos/ultimas.db')
        # with con2:
        #     cur = con2.cursor()
        #     commandx = "SELECT timestamp, medicion, valor from Status WHERE lugar = 'global' ORDER BY medicion" # OR (lugar='tv' AND medicion='temperature') "
        #     #commandx = "SELECT timestamp,medicion,valor,lugar from Status  ORDER BY lugar, medicion "
        #     res = cur.execute(commandx)
        tabla = HTML.table(out).split('\n')
        tabla2 = " ".join(tabla[1:(len(tabla)-1)])
        tabla3 =  "<table class='table table-striped lead'>"+tabla2+"</table>"
        # con2.close()
        # return tabla3
        return tabla3











# class lucesCocina(object):
#      exposed = True
#      @cherrypy.tools.accept(media='text/plain')
#      def POST(self, resp=''):
#         con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
#         with con:
#             cur = con.cursor()
#             commandx = "INSERT INTO pendientes VALUES('luces_cocina','1')"
#             cur.execute(commandx)
#         return 'Apagando luces' 


# class apagarCocina(object):
#      exposed = True
#      @cherrypy.tools.accept(media='text/plain')
#      def POST(self, resp=''):
#         con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
#         with con:
#             cur = con.cursor()
#             commandx = "INSERT INTO pendientes VALUES('luces_cocina','0')"
#             cur.execute(commandx)
#         return 'Apagando luces' 




if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port':8090})
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath(os.getcwd())
         },
         '/info_bas': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
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
    webapp.info_bas = infoBasica()

    cherrypy.quickstart(webapp, '/', conf)

