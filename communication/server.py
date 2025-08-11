from bot_code.constants import COMMANDS
from typing import Callable

def get_input(prompt, default=0.0, cast_func: type =str):
    value = input(prompt)
    if value.strip() == "":
        return default
    try:
        return cast_func(value)
    except ValueError:
        print(f"Invalid input, using default: {default}")
        return default


def main(send_message_func : Callable):
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
            send_message_func(message)
            print(f"Published: {message}")
        except Exception as e:
            print(f"Failed to send command: {e}")