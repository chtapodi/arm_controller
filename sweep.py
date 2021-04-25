import time
import pigpio

import argparse
import sys
import readchar

# GPIO number. On a rapsberry pi 1, the hardware PWM pin is
# GPIO 18
SERVO_PIN = 17

# Delay in seconds to wait after sending an angle to the servo
# motor
DELAY     = 0.02

# Minimum angle (usually 0)
MIN_ANGLE = 0

# Maximum angle
MAX_ANGLE = 180

# Minimum duty cycle, in milliseconds
MIN_DUTYCYCLE = 500

# Maximum duty cycle, in milliseconds
MAX_DUTYCYCLE = 2500

def remap(v, oMin, oMax, nMin, nMax):
    """
    Take a number v, that's within the range oMin and oMax
    Figure out what that number would actually be if the range
    is nMin and nMax
    """
    return (((v - oMin) * (nMax - nMin)) / (oMax - oMin)) + nMin

def set_angle(pi, angle):
    """
    Sets the angle on the motor. A max range of 0 to 180 degrees
    o
    """
    if angle < MIN_ANGLE:
        angle = 0
    elif angle > MAX_ANGLE:
        angle = 175
    print(angle)
    pulse = remap(angle, MIN_ANGLE, MAX_ANGLE, MIN_DUTYCYCLE, MAX_DUTYCYCLE)
    pi.set_servo_pulsewidth(SERVO_PIN, pulse)
    time.sleep(DELAY)


pi = pigpio.pi()
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)
time.sleep(2)

try:
    while True:
        for pos in range(0, 180):
            pulse = set_angle(pi, pos)

        for pos in range(180, 0, -1):
            pulse = set_angle(pi, pos)
except Exception as e:
    pi.stop()
