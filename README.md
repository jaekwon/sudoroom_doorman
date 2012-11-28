# Sudoroom Access Control

We want to know whether SudoRoom has people in it or not.

### doorman.py

This script will listen to audio signals from an audio jack, and change state depending on whether it hears a loud squarewave.
The input signal could probably just be a boolean high/low signal (it probably doesn't have to be an audible signal).
In the future, this script will post the status change somewhere where we can all see whether sudoroom is open.

### mspthing

We're using the msp430 chip for all the interacing outside of a traditional computer. Code coming soon...
