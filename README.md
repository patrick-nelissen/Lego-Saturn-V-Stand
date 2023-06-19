# Lego-Saturn-V---Stand
Printed rocket engine exhaust flames with Pi Pico W modulated LEDs that function as stand.

![alt text](https://github.com/patrick-nelissen/Lego-Saturn-V---Stand/tree/main/pictures/EngineInDark.jpg?raw-true)

## ABOUT
This microPython application runs on a Raspberry Pi Pico W (RP2040) and modulates LEDs in a set of 3D printed rocket exhaust flames that act as a stand for the Lego Saturn V rocket.
The code consists of a threaded application, which runs a simple webservice on core0, and LED modulation on core1.
LEDs can be switched on and off on the simple webpage that is served up by this webservice.

## SOFTWARE

### main.py
This module is the top-level module that starts both threads on core0 and core1.

### lib/EngineLED.py
This module manages the class for modulating the 5 LEDs via randomized PWM control.

## Hardware

### 3D printing
Relevant 3D printing files are on https://www.printables.com/
1. Pi Pico case: https://www.printables.com/model/226610-raspberry-pi-pico-case
2. Flames, LED holder and Pi Pico Case Wire Feed-through: https://www.printables.com/model/459757-lego-saturn-v-rocket-flames-stand

### Wiring
Wiring as in schematic.pdf

### Miscellaneous

- For wiring I used 30 AWG enameled copper wire to keep the wire as invisible as possible.
- White LEDs (5) because they have a forward voltage drop of 3-4 volts; hence don't need a current limiting resistor when driven by 3.3V PWM.
- For instruction on how to download microPython on the Pi Pico W, see: https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/2
- U2F bootloader available here: https://micropython.org/download/rp2-pico-w/