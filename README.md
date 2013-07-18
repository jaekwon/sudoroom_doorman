[Sudo Room](https://sudoroom.org/) is a hackerspace in downtown Oakland. We try to let people open our doors automatically without physical keys, and this is part of how we do it.

### SETUP

We have two doors - the first door enters our building from the outside, and is controlled by the software under `outer_door/`

The second door enters Sudo Room from the hallway. This has several components:

- A Raspbery Pi running a tornado web server - it has a password-protected user interface and its code is in `inner_door/`
- The server sends commands over RasPi's UART Rx serial pin using PySerial
- The pin is wired to a Texas Instruments MSP-EXP430G2 development board, running code you can find under `msp430/` (especially at `msp430/doorman/doorman.c`)
- The MSP430 runs a stepper motor, controlled by something like an L293DNE dual H-bridge
- The motor rotates 3D-printed gears in a 3D-printed house, which turn a physical key in the lock. The models for these are in `models/`

### TODO

* Model files are not up to date, but more importantly, move away from blender for modeling. (maybe Autodesk Inventor Fusion)
* Add OpenSCAD/MCAD code for the gears
* Change gear ratio to make unlocking work better (stronger, as the key or lock-knob probably requires quite a bit of force to rotate)
* Add a mechanism for detecting end-of-rotation
* Upload electronics schematics and photos
