import json
import time
import datetime
import pytz
from dateutil.parser import parse
from dateutil import tz
import numpy as np 
from filterpy.kalman import KalmanFilter
to_zone = tz.gettz("America/Mexico_City")

class AppKalman():
    def __init__(self):
        self.name = 'app_kalman'
        self.status = 'on'
        self.filters = {'caja_cisterna':{'distancia':self.initialize_filter(x_inicial=100.)}}
        self.state = {}
        #self.pattern = [{'device':'caja_filtro_alberca', 'child':'bomba', 'start_time':10, 'duration':3, 'gap':1}]
        # start today
        

    def initialize_filter(self, x_inicial):
        filtro = KalmanFilter(dim_x=2, dim_z=1)
        filtro.x = np.array([[x_inicial],[0.]])
        filtro.F = np.array([[1.,1.],[0.,1.]])
        filtro.H = np.array([[1.,0.]])
        filtro.P = np.array([[10000.,0.],[0.,100.]])
        filtro.R = 5.**2
        filtro.Q = np.array([[0.0001,0.],[0.,0.00001]])
        return filtro

    def update_gated(self, kf, z, dt=10.):
        std_x = np.sqrt(kf.P[0,0])
        res = kf.residual_of(z)
        print(res[0][0])
        print(kf.x)
        print(std_x)

        print(z)
        if(abs(res[0][0]) > 3*std_x or z > 300 or z < 0):
            pass
        else:
            kf.Q = np.array([[0.0001, 0.],[0., 0.00001]])*dt/10.
            kf.update(z)
        kf.predict()
        print(kf.x[0][0])
        return kf.x[0][0]

    def activate(self, ev_content, state, r, value):
        now = datetime.datetime.now()
        mensajes = []
        i = value
        device_name = ev_content['device_name']
        variable = ev_content['event_type']
        filtro = self.filters[device_name][variable]
        #print(ev_content['value'])
        z = float(ev_content['value'])
        new_val = self.update_gated(kf = filtro, z = z)
        r.publish('events', json.dumps({'device_name':device_name, 
                            'event_type':'distancia_filtrada',
                            'value':new_val}))
        return mensajes



    def check_event(self, ev_content,  state):
        fire = False
        value =''
        if(ev_content):
            if(ev_content['event_type'] == 'distancia' and ev_content['device_name']=='caja_cisterna'):
                fire = True
                value = 1
        return fire, value

    def check_command(self, comm_content,  state):
        fire = False
        value = ''
        return fire, value