import time
from pi_robot import PiBot

my_pibot = PiBot()

my_pibot.move_forward(70)
time.sleep(1)
my_pibot.turn_right()
time.sleep(1)
# my_pibot.change_speed(70) # Testing chqnge speed while moving
# time.sleep(1)
my_pibot.stop(duration=2) # Testing stop with n without duration
time.sleep(2)
# my_pibot.turn_round(80)
my_pibot.move_backward(70)
my_pibot.turn_left() # Testing Turn left while moving
time.sleep(1.5)
my_pibot.stop_turn_left(70)
time.sleep(1.5)
my_pibot.clean()
