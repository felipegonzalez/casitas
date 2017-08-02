import network
import machine
import usocket
import utime

ip_server = '192.168.100.50'
port_server = 8090

timeout = 500*2*30

def http_get(url):
    s = usocket.socket()
    try:
        s.connect((ip_server, port_server))
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (url, ip_server), 'utf8'))
    except:
        print('Not able to connect to server')
    s.close()

 
def pulse_wait(trigger, echo):
    trigger.off()
    utime.sleep_us(5)
    # pulse
    trigger.on()
    utime.sleep_us(10)
    trigger.off()
    try:
        pulse_time = machine.time_pulse_us(echo, 1, timeout)
        return pulse_time
    except :
        return 0

def calc_distance_cm(pulse_time):
    return (pulse_time/2)/29.1



trigger = machine.Pin(13, machine.Pin.OUT)
trigger.off()
echo = machine.Pin(12, machine.Pin.IN)
utime.sleep(1)
#send = 0
print('Iniciando ciclo')
while True:
    print('Tomar medición')
    utime.sleep(10)
    elapsed  = pulse_wait(trigger, echo)
    distance_cm = calc_distance_cm(elapsed)
    print('send_event?event_type=distancia&value='+str(distance_cm))
    http_get('send_event?event_type=distancia&value='+str(distance_cm))

    
    



