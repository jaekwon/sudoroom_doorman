# SudoRoom Doorman (Access Control)

The Doorman is a 3d printable bot that handles access control.
It uses Ti's MSP-EXP430G2 development board to listen on the UART serial pins for commands from a web server to unlock or lock the door,
by rotating a gear via a stepper motor, controlled by something like an L293DNE dual H-bridge.

1. User accesses a secret web URL
2. Server uses PySerial to send a command to the MSP430
3. MSP430 detects command on the UART Rx pin and runs the stepper motor (via a dual H-bridge)

### Objectives

* Status updates of whether SudoRoom is open or not
* Unlock the inner door via some mechanism

### Project Structure

* msp430/ code for the msp430 on an MSP-EXP430G2 development board. See msp430/doorman/doorman.c for details.
* web/ code for access control webserver running on Tornado (on a raspberry pi)
* models/ model files for the physical device

### TODO

* Model files are not up to date, but more importantly, move away from blender for modeling. (maybe Autodesk Inventor Fusion)
* Add OpenSCAD/MCAD code for the gears
* Change gear ratio to make unlocking work better (stronger, as the key or lock-knob probably requires quite a bit of force to rotate)
* Add a mechanism for detecting end-of-rotation
* Upload electronics schematics and photos
* Move secrets into another file
* Move this project to a SudoRoom account

### Contributors

* Max KleinBottle
* Andrew
* Jae