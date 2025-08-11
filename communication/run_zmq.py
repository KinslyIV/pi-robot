import zmq
from communication.run import exec_command
from bot_code.constants import SERVER_IP

def main():
    while True:
        msg = socket.recv_string()
        print(f"Received a new message: {msg} ")
        exec_command(msg)

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{SERVER_IP}:5555")  # Laptop is publisher
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    main()