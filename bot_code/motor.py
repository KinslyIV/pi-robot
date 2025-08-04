from enum import Enum
from typing import Optional
import RPi.GPIO as GPIO
from bot_code.constants import *


class Direction(Enum):
    FOWARD = 1
    BACKWARD = 2

class Motor:
    IN1 : int = 0
    IN2 : int = 0
    EN : int = 0
    freq : int = 0
    current_speed : int = 0
    pwm : GPIO.PWM
    stopped : bool
    direction : Direction

    def __init__(self, in1: int, in2: int, en: int, freq: int = default_freq) -> None:
        # Setting pins
        self.IN1 = in1
        self.IN2 = in2
        self.EN = en
        self.frequency = freq

        # init
        self.pwm = GPIO.PWM(self.EN, freq)
        self.pwm.start(0)

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)

    def set_speed(self, speed=current_speed):
        # Sets percentage speed from 0% - 100%
        self.current_speed = speed
        self.pwm.ChangeDutyCycle(speed)

    def foward(self, speed = current_speed):
        self.stopped = speed == 0
        self.set_direction(foward=True)
        self.set_speed(speed)

    def set_direction(self, foward):
        if foward:
            self.direction = Direction.FOWARD
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        else:
            self.direction = Direction.BACKWARD
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)

    def backward(self, speed = current_speed):
        self.stopped = False
        self.set_direction(False)
        self.set_speed(speed)

    def stop(self):
        self.stopped = True
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def move(self):
        if self.direction is Direction.FOWARD:
            self.set_direction(True)
            self.set_speed()
        elif self.direction is Direction.BACKWARD:
            self.set_direction(foward=False)
            self.set_speed()
               
