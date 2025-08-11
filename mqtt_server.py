import paho.mqtt.client as mqtt
import json

# ===== CONFIGURATION =====
BROKER_ADDRESS = "localhost"  # Replace with your Pi's IP or hostname
PORT = 1883
TOPIC = "robot/command"

# ===== COMMAND MAP =====
COMMANDS = {
    "1": "forward",
    "2": "backward",
    "3": "left",
    "4": "right",
    "5": "stop",
    "6": "change_speed",
    "7": "turn_round",
    "8": "stop_turn_left",
    "9": "stop_turn_right",
    "10": "accelerate",
    "11": "cleanup",
}


def get_input(prompt, default=None, cast_func=str):
    value = input(prompt)
    if value.strip() == "":
        return default
    try:
        return cast_func(value)
    except ValueError:
        print(f"Invalid input, using default: {default}")
        return default

def main():
    while True:
        print("Choose a command:")
        for num, cmd in COMMANDS.items():
            print(f"{num}. {cmd.capitalize()}")

        choice = input("> ").strip()
        if choice not in COMMANDS:
            print("Invalid choice.")
            return

        command = COMMANDS[choice]
        speed = get_input("Enter speed/ratio(for turn) (0-100) [default: 50]: ", default=60, cast_func=int)
        duration = get_input("Enter duration/delta(for acc) in seconds [default: 1.5]: ", default=1.5, cast_func=float)

        message = {
            "command": command,
            "speed": speed,
            "duration": duration
        }

        # Publish

        try:
            client.publish(TOPIC, json.dumps(message))
            print(f"Published: {message}")
            client.disconnect()
        except Exception as e:
            print(f"Failed to send command: {e}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, PORT, keepalive=300)

    main()
