import time
from pi_robot import PiBot

my_pibot = PiBot()

my_pibot.move_foward(100)
time.sleep(2)
my_pibot.turn_left()
my_pibot.change_speed(60)
time.sleep(1)
my_pibot.stop(duration=1)
my_pibot.turn_around()
my_pibot.move_backward(30, 3)
my_pibot.turn_right(duration=0.7)
time.sleep(2)
my_pibot.stop()
