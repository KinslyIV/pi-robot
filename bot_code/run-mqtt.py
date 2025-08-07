import json

from pi_robot import PiBot
from constants import *
import paho.mqtt.client as mqtt

my_pibot = PiBot()

def on_message(client, userdata, msg):
    print(f"Received a new message on {msg.topic}: "
          f"{msg.payload.decode()}")

    if msg.topic == "my_pibot/command":
        msg_str = msg.payload.decode()
        msg_json = json.loads(msg_str)
        command = msg_json["command"]
        speed = msg_json["speed"]
        duration = msg_json["duration"]

        if command == FORWARD:
            my_pibot.move_forward(speed, duration)
        elif command == BACKWARD:
            my_pibot.move_backward(speed, duration)
        elif command == TURN_LEFT:
            my_pibot.turn_left(speed)
        elif command == TURN_RIGHT:
            my_pibot.turn_right(speed)
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


client = mqtt.Client()
client.connect("100.87.65.22", 1883, 300)  # Replace with your computer’s IP

client.subscribe("robot/command")
client.on_message = on_message

client.loop_forever()