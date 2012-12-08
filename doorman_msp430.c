/*
 * This script is a sample driver for the msp430 for Doorman
 * 1. connect the msp430
 * 2. make upload
 */

#include <watchdog.h>
#include <clock.h>
#include <pins.h>
#include <delay.h>

// pin 1.0 Motor 1 Direction A
// pin 1.1 Motor 1 Direction B
// pin 1.2 Motor 1 Enable
// pin 1.3 Motor 2 Direction A
// pin 1.4 Motor 2 Direction B
// pin 1.5 Motor 2 Enable

int
main(void)
{
	watchdog_off();
	clock_init_1MHz();

	port1_direction = 0xFF;
	//port1_output = 0xFF;

  delay(0xffff);

  unsigned int delay_ = 0x08ff;

	while (1) {
	  unsigned int i;

    delay(0xffff);
    delay(0xffff);
    delay(0xffff);
    delay(0xffff);

    // lock
    for (i=0; i<60; i++) {
      port1_output = 0x25; // 0010 0101
      delay(delay_);
      port1_output = 0x2C; // 0010 1100
      delay(delay_);
      port1_output = 0x26; // 0010 0110
      delay(delay_);
      port1_output = 0x34; // 0011 0100
      delay(delay_);
    }

    delay(0xffff);
    delay(0xffff);
    delay(0xffff);
    delay(0xffff);

    // unlock
    for (i=0; i<68; i++) {
      port1_output = 0x34; // 0011 0100
      delay(delay_);
      port1_output = 0x26; // 0010 0110
      delay(delay_);
      port1_output = 0x2C; // 0010 1100
      delay(delay_);
      port1_output = 0x25; // 0010 0101
      delay(delay_);
    }

	}
}
