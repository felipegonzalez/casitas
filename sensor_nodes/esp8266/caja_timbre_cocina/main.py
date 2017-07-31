import network
import machine
import usocket
import utime

ip_server = '192.168.100.50'
port_server = 8090

def http_get(url):
    s = usocket.socket()
    s.connect((ip_server, port_server))
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (url, ip_server), 'utf8'))
    s.close()

def send_rising(p):
    global send 
    send = 1
 


signal = machine.Pin(13, machine.Pin.IN)
led = machine.Pin(0, machine.Pin.OUT)
led.off()
utime.sleep(1)
led.on()
signal.irq(trigger=machine.Pin.IRQ_RISING, handler=send_rising)
send = 0
while True:
    utime.sleep(3)
    led.on()

    if(send==1):
        http_get('ring?lugar=patio')
        print("sent rising")
        led.off()
        send = 0



