import time
from enum import Enum
import pigpio
from typing import Optional
from constants import *


class Direction(Enum):
    FORWARD = 1
    BACKWARD = 2

class Motor:

    def __init__(self, in1: int, in2: int, en: int, freq: int = default_freq) -> None:
        # Setting pins
        self.IN1 = in1
        self.IN2 = in2
        self.EN = en
        self.frequency = freq
        self.current_speed = 0
        self.direction: Optional[Direction] = None
        self.stopped: bool = True
        self.pi = pigpio.pi()
        self.pi.set_PWM_range(self.EN, 100)
        # init
        self.setup()
        

    def setup(self):
        self.pi.set_mode(self.IN1, pigpio.OUTPUT)
        self.pi.set_mode(self.IN2, pigpio.OUTPUT)
        self.pi.set_mode(self.EN, pigpio.OUTPUT)
        # Set the PWM frequency (this sets frequency for EN pin)
        self.pi.set_PWM_frequency(self.EN, self.frequency)
        self.pi.set_PWM_dutycycle(self.EN, 0)  # 0 speed

        # Initialize motor in stopped state
        self.pi.write(self.IN1, 0)
        self.pi.write(self.IN2, 0)

       # print(self.IN1, self.IN2, self.EN)

    def set_speed(self, speed=None):
        # Sets percentage speed from 0% - 100%
        if speed is None:
            speed = self.current_speed
        self.current_speed = speed
        self.pi.set_PWM_dutycycle(self.EN, speed)


    def forward(self, speed = None):
        if speed is None:
            speed = self.current_speed
        self.stopped = speed == 0
        self.set_direction(foward=True)
        self.set_speed(speed)

    def set_direction(self, foward):
        if foward:
            self.direction = Direction.FORWARD
            self.pi.write(self.IN1, 1)
            self.pi.write(self.IN2, 0)
        else:
            self.direction = Direction.BACKWARD
            self.pi.write(self.IN1, 0)
            self.pi.write(self.IN2, 1)

    def backward(self, speed = None):
        if speed is None:
            speed = self.current_speed
        self.stopped = False
        self.set_direction(False)
        self.set_speed(speed)

    def stop(self, delay=0.05, step=5):
        self.stopped = True
        """
            Gradually reduce speed to 0 to stop the motor smoothly.

            :param step: Percentage to decrease per iteration.
            :param delay: Time (in seconds) to wait between speed changes.
            """
        while self.current_speed > 0:
            new_speed = max(0, self.current_speed - step)
            self.pi.set_PWM_dutycycle(self.EN, new_speed)
            self.current_speed = new_speed
            time.sleep(delay)

        # Once speed is 0, stop the motor direction (optional)
        print("Motor stopped smoothly.")
        self.pi.write(self.IN1, 0)
        self.pi.write(self.IN2, 0)
        self.pi.set_PWM_dutycycle(self.EN, 0)

    def move(self):
        if self.direction is Direction.FORWARD:
            self.set_direction(True)
            self.set_speed()
        elif self.direction is Direction.BACKWARD:
            self.set_direction(foward=False)
            self.set_speed()
               
