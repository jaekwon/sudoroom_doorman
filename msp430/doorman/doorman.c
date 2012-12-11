/**

  (see https://github.com/jaekwon/sudoroom_doorman)

  This code listens for serial input from the Rx line (UART pin 1.2) using software UART,
  and when it detects a character 'c' it turns the stepper motor one way,
  and when it detects a character 'o' it turns the stepper motor another way.
 
  Instructions for uploading:

  0. install the mspgcc toolchain
  1. connect the msp430 launchpad (MSP-EXP430G2)
  2. make upload

  Known issues:

  * it doesn't know when to stop rotating, as it has no sensory input, resulting in loud (but harmless) noise.
  * Ubuntu has all kinds of issues with establishing a USB<->serial connection for firmware uploading and such.

  Future work:

  * add code (and hardware) to detect when the door is open(ed) and communicate on the Tx pin.
  * add code (and hardware) to make a sound to alert people that the door will unlock.

 */ 

#include <watchdog.h>
#include <clock.h>
#include <pins.h>
#include <delay.h>

// from examples/serial.c
#define SERIAL_RX_BUFSIZE 32
#include "lib/serial_tx.c"
#include "lib/serial_rx.c"

#define LED2 1.6

// pin 1.2 UART (serial) Rx for listening
// pin 1.3 Motor Coil 1 Direction A
// pin 1.4 Motor Coil 1 Direction B
// pin 1.5 Motor Coil 1 Enable
// pin 1.6 Reserved for LED2 debugging
// pin 2.0 Motor Coil 2 Direction A
// pin 2.1 Motor Coil 2 Direction B
// pin 2.2 Motor Coil 2 Enable

#define DELAY 0x08ff
#define ROTATE_AMOUNT 65

void flash(void);
void pause(void);
/**
  Code for debugging, when serial isn't working.
  debug_char() will flash the bits of the char argument,
  starting from the least significant bit.
 */
void debug_char(unsigned char c) {
  unsigned int c2 = (unsigned int) c;
  for (int i=0; i<8; i++) {
    if (c2 & 0x01) { // twice for 1
      flash();
      flash();
    } else {         // once for 0
      flash();
    }
    pause();
    c2 = c2 >> 1;
  }
}
void flash(void) {
  unsigned int i;
  pin_toggle(LED2);
  for (i=0; i<20; i++) { delay(DELAY); }
  pin_toggle(LED2);
  for (i=0; i<20; i++) { delay(DELAY); }
}
void pause(void) {
  unsigned int i;
  for (i=0; i<40; i++) { delay(DELAY); }
}
/* end debugging code */

int
main(void)
{
	watchdog_off();
	clock_init_1MHz();

	port1_direction = 0xFC; // 1111 1011 --> p1.2 is Rx
  port2_direction = 0xFF; // 1111 1111
  port1_output   &= 0x00; // turn off motors or it'll heat up!
  port2_output   &= 0x00; // turn off motors or it'll heat up!

  delay(0xffff); // wait for initialization or something

	/* initialize serial clock, tx and rx parts */
	serial_init_clock();
	serial_init_tx();
	serial_init_rx();

	/* enable interrupts */
	__eint();

	while (1) {
	  unsigned int i;
    unsigned char c;

    c = serial_getchar();
    //debug_char(c);

    if (c == 'o') { // open
      flash();
      for (i=0; i<ROTATE_AMOUNT; i++) {
        port1_output = 0x20; // 0010 0000
        port2_output = 0x05; // 0000 0101
        delay(DELAY);
        port1_output = 0x28; // 0010 1000
        port2_output = 0x04; // 0000 0100
        delay(DELAY);
        port1_output = 0x20; // 0010 0000
        port2_output = 0x06; // 0000 0110
        delay(DELAY);
        port1_output = 0x30; // 0011 0000
        port2_output = 0x04; // 0000 0100
        delay(DELAY);
      }
      port1_output &= 0x00; // turn off motors!
      port2_output &= 0x00; // turn off motors!
    }

    else if (c == 'c') { // close
      flash();
      flash();
      for (i=0; i<ROTATE_AMOUNT; i++) {
        port1_output = 0x30; // 0011 0000
        port2_output = 0x04; // 0000 0100
        delay(DELAY);
        port1_output = 0x20; // 0010 0000
        port2_output = 0x06; // 0000 0110
        delay(DELAY);
        port1_output = 0x28; // 0010 1000
        port2_output = 0x04; // 0000 0100
        delay(DELAY);
        port1_output = 0x20; // 0010 0000
        port2_output = 0x05; // 0000 0101
        delay(DELAY);
      }
      port1_output &= 0x00; // turn off motors!
      port2_output &= 0x00; // turn off motors!
    }

	}
}
