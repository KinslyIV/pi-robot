import time
from bot_code.motor import Motor, Direction
from bot_code.constants import *


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
        self.direction = Direction.FORWARD

        
    def move_forward(self, speed, duration=None):
        self.current_speed = speed
        self.direction = Direction.FORWARD
        self.motor_left.forward(speed)
        self.motor_right.forward(speed)

        if duration:
            time.sleep(duration)
            self.stop()


    def stop(self, duration=None):

        while self.motor_left.is_moving() and self.motor_right.is_moving():
            self.motor_left.accelerate(-10)
            self.motor_right.accelerate(-10)
            time.sleep(0.05)

        if duration:
            time.sleep(duration)
            self.motor_left.move()
            self.motor_right.move()
        else:
            self.current_speed = 0


    def move_backward(self, speed, duration=None):
        self.current_speed = speed
        self.direction = Direction.BACKWARD
        self.motor_left.backward(speed)
        self.motor_right.backward(speed)

        if duration:
            time.sleep(duration)
            self.stop()


    def change_speed(self, speed):

    # Gradually change speed for each motor one after another
        motors = [self.motor_left, self.motor_right]
        currents = [motor.current_speed for motor in motors]
        steps = [5 if speed > current else -5 for current in currents]

        while currents[0] != speed or currents[1] != speed:
            for i, motor in enumerate(motors):
                if currents[i] != speed:
                    next_speed = currents[i] + steps[i]
                    if (steps[i] > 0 and next_speed > speed) or (steps[i] < 0 and next_speed < speed):
                        next_speed = speed
                    motor.accelerate(next_speed - currents[i])
                    currents[i] = next_speed

        self.current_speed = speed

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


    def turn_left(self, ratio=65, duration=TURN_DURATION):
        if ratio < 0:
            self.motor_right.reverse_direction()
        self.motor_left.move(abs(ratio))
        self.motor_right.move(TURN_SPEED)
        time.sleep(duration)
        if ratio < 0:
            self.motor_right.reverse_direction()
        self.change_speed(self.current_speed)

    def turn_right(self, ratio=65, duration=TURN_DURATION):
        if ratio < 0:
            self.motor_left.reverse_direction()
        self.motor_right.move(abs(ratio))
        self.motor_left.move(TURN_SPEED)
        # print(f"turning right: left_motor: {self.motor_left.current_speed} duration: {duration} right_motor: {self.motor_right.current_speed}")
        time.sleep(duration)
        if ratio < 0:
            self.motor_left.reverse_direction()
        self.change_speed(self.current_speed)

    def clean(self):
        print("Cleaning up...")
        self.motor_left.cleanup()
        self.motor_right.cleanup()


    def get_speed(self):
        return self.current_speed

    def accelerate(self, delta=10):
        self.motor_left.accelerate(delta)
        self.motor_right.accelerate(delta)
