# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import network

#import gc
#import webrepl
#webrepl.start()
#gc.collect()

#
esp.osdebug(None)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    print('connecting to network...')
    sta_if.active(True)
    sta_if.ifconfig(('192.168.100.153', '255.255.255.0','192.168.100.1','8.8.8.8'))
    sta_if.connect('COM-818', 'valquiria')
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())

do_connect()
