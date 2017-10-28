import network
import machine
import usocket
import utime

ip_server = '192.168.100.50'
port_server = 8090
last_send = 0
num_ones = 0
last_one = 0

def http_get(url):
    s = usocket.socket()
    s.connect((ip_server, port_server))
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (url, ip_server), 'utf8'))
    s.close()

def send_ring():
    http_get('send_event?event_type=timbre&value=True')
    print("sent rising")
    utime.sleep(3)


signal_bell = machine.Pin(13, machine.Pin.IN)
led = machine.Pin(0, machine.Pin.OUT)
led.off()
utime.sleep(2)
led.on()
send_ring()
#signal.irq(trigger=machine.Pin.IRQ_RISING, handler=detect_rising)
candidate_ring = 0
last_event = 0
total_on = 0
total_off = 0
total_time = 0

while True:
    read_bell = signal_bell.value()
    if(candidate_ring == 0):
        led.on()
        if(read_bell == 1):
            candidate_ring = 1
            last_event = utime.time()
    else:
        diff_time = utime.time() - last_event
        last_event = utime.time()
        if(read_bell == 0):
            led.on()
            total_off = total_off + diff_time
        else:
            led.off()
            total_on = total_on + diff_time
        total_time = total_off + total_on

        if(total_time > 0.75):
            if(total_on > total_off):
                send_ring()
                for i in range(0,3):
                    led.off()
                    utime.sleep(0.5)
                    led.on()
                    utime.sleep(0.2)
            else:
                for i in range(0,3):
                    led.off()
                    utime.sleep(0.1)
                    led.on()
                    utime.sleep(0.1)


            total_time = 0
            total_on = 0
            total_off = 0
            candidate_ring = 0


        

            



