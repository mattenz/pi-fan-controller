#!/usr/bin/env python3

import subprocess
import time

from gpiozero import OutputDevice, PWMOutputDevice


FULL_THRESHOLD = 70  # (degrees Celsius) Fan kicks on at this temperature.
IDLE_THRESHOLD = 50  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 1  # (seconds) How often we check the core temperature.
GPIO_PIN = 18  # Which GPIO pin you're using to control the fan.
FAN_IDLE = 0.3 # Minimum fan speed. Do not set below 0.3.
FAN_FULL = 1.0 # Maximum fan speed. Do not set abole 1.0.


def get_temp():
    """Get the core temperature.
    Run a shell script to get the core temp and parse the output.
    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')


if __name__ == '__main__':
    # Validate the on and off thresholds
    if IDLE_THRESHOLD >= FULL_THRESHOLD:
        raise RuntimeError('IDLE_THRESHOLD must be less than FULL_THRESHOLD')

    if FAN_IDLE >= FAN_FULL:
        raise RuntimeError('FAN_IDLE must be less than FAN_FULL')

    fan = PWMOutputDevice(GPIO_PIN)

    while True:
        temp = get_temp()

        if temp >= FULL_THRESHOLD:
            fan.value = FAN_FULL
            print(f'Set fan to {fan.value:.3f} (Full). Temp is {temp:.2f}')

        elif temp > IDLE_THRESHOLD and temp < FULL_THRESHOLD:
            speed = FAN_IDLE + ((temp - IDLE_THRESHOLD) * ((FAN_FULL - FAN_IDLE) / (FULL_THRESHOLD - IDLE_THRESHOLD)))
            if speed != fan.value:
                fan.value = speed
                print(f'Set fan to {fan.value:.3f}. Temp is {temp:.2f}')

        elif temp < IDLE_THRESHOLD and fan.value != FAN_IDLE:
            fan.value = FAN_IDLE
            print(f'Set fan to {fan.value:.3f} (Idle). Temp is {temp:.2f}')


        time.sleep(SLEEP_INTERVAL)
