import time
from motor import Motor
from bot_code.constants import *


class PiBot:

    motor_right : Motor
    motor_left : Motor
    current_speed : int = 0

    def __init__(self, **kwargs) -> None:

        self.motor_left = Motor(kwargs.get('IN1', IN1), 
                           kwargs.get('IN2', IN2),
                           kwargs.get('EN', EN1),
                           kwargs.get('freq', default_freq))
        
        self.motor_right = Motor(kwargs.get('IN1', IN3), 
                           kwargs.get('IN2', IN4),
                           kwargs.get('EN', EN2),
                           kwargs.get('freq', default_freq))
        
        self.motor_left.setup()
        self.motor_right.setup()
        
    def move_foward(self, speed, duration=None):
        self.current_speed = speed
        self.motor_left.foward(speed)
        self.motor_right.foward(speed)

        if duration:
            time.sleep(duration)

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

    def turn_around(self, speed = current_speed, clockwise= True, duration= 3.0):
        if clockwise:
            self.motor_left.foward(speed)
            self.motor_right.backward(speed)
        else:
            self.motor_left.backward(speed)
            self.motor_right.backward(speed)

        if duration:
            time.sleep(duration)
            self.stop()

    def stop_turn_left(self, speed = current_speed, duration = turn_duration):
        self.turn_around(speed, clockwise=False, duration=duration)

    def stop_turn_right(self, speed = current_speed, duration = turn_duration):
        self.turn_around(speed, clockwise=True, duration=duration)

    def turn_left(self, duration=turn_duration, delta=turn_speed_delta):
        speed_delta = self.current_speed+delta
        self.motor_right.set_speed(speed_delta if speed_delta <= 100 else 100)
        time.sleep(duration)
        self.change_speed(self.current_speed)

    def turn_right(self, duration=turn_duration, delta=turn_speed_delta):
        speed_delta = self.current_speed+delta
        self.motor_left.set_speed(speed_delta if speed_delta <= 100 else 100)
        time.sleep(duration)
        self.change_speed(self.current_speed)
    