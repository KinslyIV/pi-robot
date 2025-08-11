import zmq
from server import main

# ===== CONFIGURATION =====

def send_message(message):
    socket.send_json(message)


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    main(send_message)
