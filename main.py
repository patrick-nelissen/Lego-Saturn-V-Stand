from machine import Pin, PWM

import network
import socket
import utime, time
import random
import _thread

from EngineLED import EngineLED

def webpage():
    html = f"""
            <!DOCTYPE html>
            <html>          
            <body>
            <form action="./on">
            <input type="submit" value="Engine On"/>
            </form>
            </form>
            <form action="./off">
            <input type="submit" value="Engine Off" />
            </form>
            </body>
            </html>
            """

    return html
 
def serve(connection):

    global EngineOn

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        print(request)
        
        if request == '/on?':
            EngineOn = True
        elif request == '/off?':
            EngineOn = False      
  
        html=webpage()
        client.send(html)
        client.close()
 
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return(connection)

# The Pi Pico has 2 cores, core 0 and core 1
# This core, core 0 will run the webservice
def core0_thread():
    
    global EngineOn

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("your_SSID","your_PASSWORD")
         
    # Wait for connect or fail
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)
     
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')
    else:
        print('connected')
        ip=wlan.ifconfig()[0]
        print('IP: ', ip)
        
    try:
        if ip is not None:
            connection=open_socket(ip)
            serve(connection)
    except KeyboardInterrupt:
        machine.reset()
        

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