import time
from pi_robot import PiBot
import RPi.GPIO as GPIO

my_pibot = PiBot()

my_pibot.move_forward(60)
time.sleep(1.5)
my_pibot.turn_right()
my_pibot.change_speed(90)
time.sleep(1.5)
my_pibot.stop(duration=2)
time.sleep(2)
my_pibot.turn_around(70)
my_pibot.move_backward(60, 1)
my_pibot.turn_left(duration=2)
time.sleep(1)
my_pibot.stop()

GPIO.cleanup()
