import time
from motor import Motor
from constants import *


class PiBot:

    def __init__(self, **kwargs) -> None:

        self.motor_left = Motor(kwargs.get('IN1', IN1), 
                           kwargs.get('IN2', IN2),
                           kwargs.get('EN', EN1),
                           kwargs.get('freq', default_freq))
        
        self.motor_right = Motor(kwargs.get('IN1', IN3), 
                           kwargs.get('IN2', IN4),
                           kwargs.get('EN', EN2),
                           kwargs.get('freq', default_freq))

        self.current_speed = 0

        
    def move_forward(self, speed, duration=None):
        self.current_speed = speed
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self, duration=None):
        self.motor_left.stop()
        self.motor_right.stop()

        if duration:
            time.sleep(duration)
            self.motor_left.move()
            self.motor_right.move()


    def move_backward(self, speed, duration=None):
        self.current_speed = speed
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def change_speed(self, speed):
        self.current_speed = speed
        self.motor_left.set_speed(speed)
        self.motor_right.set_speed(speed)

    def turn_round(self, speed = None, clockwise= True, duration= 3.0):
        if speed is None:
            speed = self.current_speed if self.current_speed != 0 else 70
        if clockwise:
            self.motor_left.forward(speed)
            self.motor_right.backward(speed)
        else:
            self.motor_left.backward(speed)
            self.motor_right.backward(speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def stop_turn_left(self, speed = None, duration = 1):
        if speed is None:
            speed = self.current_speed if self.current_speed != 0 else 70
        duration = duration if duration != 0 else 1
        self.turn_round(speed, clockwise=False, duration=duration)

    def stop_turn_right(self, speed = None, duration = 1):
        if speed is None:
            speed = self.current_speed if self.current_speed != 0 else 70
        duration = duration if duration != 0 else 1
        self.turn_round(speed, clockwise=True, duration=duration)

    def turn_left(self, duration=turn_duration):
        self.motor_left.set_speed(100)
        self.motor_right.set_speed(60)
        time.sleep(duration)
        self.change_speed(self.current_speed)

    def turn_right(self, duration=turn_duration):
        self.motor_left.set_speed(60)
        self.motor_right.set_speed(100)
        time.sleep(duration)
        self.change_speed(self.current_speed)

    def clean(self):
        self.motor_left.cleanup()
        self.motor_right.cleanup()
