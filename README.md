# Pi Fan Controller

Raspberry Pi fan controller.

## Description

This repository provides scripts that can be run on the Raspberry Pi that will
monitor the core temperature and start the fan when the temperature reaches
a certain threshold. This fork uses a PWM controller via GPIO pin 18 to increase and decrease the speed, allowing one to set a maximum speed

To use this code, you'll have to install a fan. The full instructions can be
found on our guide: [Control Your Raspberry Pi Fan (and Temperature) with Python](https://howchoo.com/g/ote2mjkzzta/control-raspberry-pi-fan-temperature-python). Only modification to make from the original instructions is to use GPIO pin 18 as this is a PWM pin. Using a ground on the same side makes things easier too
