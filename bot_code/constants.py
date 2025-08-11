# Motor 1 Pins
IN1 = 17
IN2 = 27
EN1 = 22

# Motor 2 Pins
IN3 = 23
IN4 = 24
EN2 = 25

# Other values
default_freq = 2000
turn_duration = 0.8
turn_speed_delta = 50

MAX_SPEED = 255

# Commands
FORWARD = "forward"
BACKWARD = "backward"
TURN_LEFT = "left"
TURN_RIGHT = "right"
STOP = "stop"
CHANGE_SPEED = "change_speed"
TURN_ROUND = "turn_round"
STOP_TURN_LEFT = "stop_turn_left"
STOP_TURN_RIGHT = "stop_turn_right"
ACCELERATE = "accelerate"
CLEANUP = "cleanup"

# Connection
TOPIC = "pi-robot/command"
BROKER_ADDRESS = "192.168.1.126"
SERVER_IP = "192.168.1.126"

# ===== COMMAND MAP =====
COMMANDS = {
    "1": FORWARD,
    "2": BACKWARD,
    "3": TURN_LEFT,
    "4": TURN_RIGHT,
    "5": STOP,
    "6": CHANGE_SPEED,
    "7": TURN_ROUND,
    "8": STOP_TURN_LEFT,
    "9": STOP_TURN_RIGHT,
    "10": ACCELERATE,
    "11": CLEANUP,
}

