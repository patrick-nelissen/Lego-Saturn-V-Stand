from machine import Pin, PWM
import utime
import random

# Small class to switch the engine LEDs on and off
# When on, they will randomly pulsate
class EngineLED:

    LEDvalue = 50     # LED brightness initial value (50%)
    LEDspeed = 1      # Change brightness in increments of 1%

    def __init__(self, pin):
        
        self.LED = PWM(Pin(pin)) # Set the pin
        self.LED.freq(1000)      # Set the PWM frequency value

    
    def On(self):
                    
        self.LEDvalue += self.LEDspeed              # Increment or decrement the brigthness
        self.LED.duty_u16(int(self.LEDvalue * 500)) # Set the duty cycle, between 0-50000
        
        if self.LEDvalue >= 100: # Limit to upper level of brightness to 100%
            self.LEDvalue = 100
            self.LEDspeed = -random.randint(0,20)/10 # Decrease brighness at random speed
        elif self.LEDvalue <= 50: # Limit to lower level of brightness to 50%
            self.LEDvalue = 50
            self.LEDspeed = random.randint(0,20)/10  # Increase brighness at random speed
                
                
    def Off(self):
        
        self.LED.duty_u16(0) # Set Dutycycle to 0%