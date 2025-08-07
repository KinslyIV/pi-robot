import time
from pi_robot import PiBot

my_pibot = PiBot()

my_pibot.move_forward(200)
time.sleep(1.5)
my_pibot.turn_right()
my_pibot.change_speed(150)
time.sleep(1.5)
my_pibot.stop(duration=2)
time.sleep(2)
my_pibot.turn_around(200)
my_pibot.move_backward(225, 1)
my_pibot.turn_left(duration=2)
time.sleep(1)
my_pibot.stop()
