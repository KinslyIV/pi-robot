from communication.run import exec_command
from constants import *
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Received a new message on {msg.topic}: "
          f"{msg.payload.decode()}")

    if msg.topic == TOPIC:
        msg_str = msg.payload.decode()
        exec_command(msg_str)


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_ADDRESS, 1883, 300)  # Replace with your computer’s IP

    client.subscribe(TOPIC)
    client.on_message = on_message

    client.loop_forever()
