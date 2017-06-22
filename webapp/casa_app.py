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

cherrypy.server.socket_host = '0.0.0.0'


class control(object):

    @cherrypy.expose
    def controlcasa(self):
        return open('index_main.html')


    #@cherrypy.expose
    #def autoluz(self):
        #con = lite.connect('/Volumes/mmshared/bdatos/comandos.db')
        #with con:
        #    cur = con.cursor()
        #    commandx = "INSERT INTO pendientes VALUES('auto_luces','0')"
        #    cur.execute(commandx)
        #return 'Auto luces' 



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
    def regar(self, sw):
        mensaje = 'Sistema de goteo' + str(sw)
        if(sw=='1'):
            r.publish('commands', json.dumps({"device_name":"caja_goteo",
                "command":"turn_on", "value":"regar"
                }))
        if(sw=='0'):
            r.publish('commands', json.dumps({'device_name':'caja_goteo',
                'command':'turn_off', 'value':'regar'
                }))  
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
        lugares = ['recamara_principal', 'sala', 'estudiof']
        out = []
        for lugar in lugares:
            temp = r.hget('temperature', lugar).decode('utf-8')
            humd = r.hget('humidity', lugar).decode('utf-8')
            out.append((lugar, 'temperatura', temp))
            out.append((lugar, 'humedad', humd))
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
            'tools.staticdir.dir' : "/Users/felipe/casitas/webapp/img"
        }
}
    webapp = control()
    webapp.info_bas = infoBasica()

    cherrypy.quickstart(webapp, '/', conf)

