from machine import Pin, PWM

import network
import socket
import utime, time
import random
import _thread

from EngineLED import EngineLED

# The Pi Pico has 2 cores, core 0 and core 1
# This core, core 0 will run the webservice
def core0_thread():
    
    global EngineOn

    ssid = 'your_ssid'
    password = 'your_password'

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    html = """<!DOCTYPE html>
    <html>
        <head> <title>Saturn V - Engine</title> </head>
        <body> <h1>Saturn V - Engine</h1>
            <p>%s</p>
        </body>
    </html>
    """

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

    # Open socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    # Listen for connections
    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)
            request = str(request)
            engine_on = request.find('/engine/on')
            engine_off = request.find('/engine/off')
            print( 'Engine on = ' + str(engine_on))
            print( 'Engine off = ' + str(engine_off))

            if engine_on == 6:
                print("Engine on")
                stateis = "Engine is ON"
                EngineOn = True
                    
            if engine_off == 6:
                print("Engine off")
                stateis = "Engine is OFF"
                EngineOn = False


            response = html % stateis
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()           


        except OSError as e:
            cl.close()
            print('connection closed')

# The Pi Pico has 2 cores, core 0 and core 1
# This core, core 1 will drive the LEDs and randomly
# change the brightness of each of the 5 engines
def core1_thread():

    Engine1 = EngineLED(9)
    Engine2 = EngineLED(10)
    Engine3 = EngineLED(11)
    Engine4 = EngineLED(12)
    Engine5 = EngineLED(13)

    while True:

        utime.sleep_ms(10)

        if EngineOn == True:
      
            Engine1.On()
            Engine2.On()
            Engine3.On()
            Engine4.On()
            Engine5.On()
            
        else:
            
            Engine1.Off()
            Engine2.Off()
            Engine3.Off()
            Engine4.Off()
            Engine5.Off()

# Global variable to send signals between threads
EngineOn = False

# Start both threads on core 0 and 1
second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()