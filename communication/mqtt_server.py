import paho.mqtt.client as mqtt
import json
from bot_code.constants import TOPIC
from server import main

# ===== CONFIGURATION =====
BROKER_ADDRESS = "localhost"  # Replace with your Pi's IP or hostname
PORT = 1883


def send_message(message):
    client.publish(TOPIC, json.dumps(message))


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_ADDRESS, PORT, keepalive=300)

    main(send_message)
