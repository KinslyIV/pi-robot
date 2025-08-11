import json
from bot_code.pi_robot import PiBot
# from bot_code.sim_pibot import SimPiBot
from bot_code.constants import (FORWARD, BACKWARD, TURN_RIGHT, TURN_LEFT, CHANGE_SPEED, TURN_ROUND,
                                STOP, STOP_TURN_LEFT, STOP_TURN_RIGHT, ACCELERATE, CLEANUP)

my_pibot = PiBot()


def exec_command(msg_str):
    msg_json = json.loads(msg_str)
    command = msg_json["command"]
    speed = msg_json["speed"]
    duration = msg_json["duration"]

    if command == FORWARD:
        my_pibot.move_forward(speed, duration)
    elif command == BACKWARD:
        my_pibot.move_backward(speed, duration)
    elif command == TURN_LEFT:
        my_pibot.turn_left(ratio=speed)
    elif command == TURN_RIGHT:
        my_pibot.turn_right(ratio=speed)
    elif command == STOP:
        my_pibot.stop(duration)
    elif command == CHANGE_SPEED:
        my_pibot.change_speed(speed)
    elif command == TURN_ROUND:
        my_pibot.turn_round(speed)
    elif command == STOP_TURN_LEFT:
        my_pibot.stop_turn_left(70)
    elif command == STOP_TURN_RIGHT:
        my_pibot.stop_turn_right(70)
    elif command == ACCELERATE:
        my_pibot.accelerate(duration)
    elif command == CLEANUP:
        my_pibot.clean()
    else:
        print("Unknown command")