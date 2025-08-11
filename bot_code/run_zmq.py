import subprocess

import zmq
from communication.run import exec_command
from bot_code.constants import SERVER_IP

def main():
    while True:
        try:
            msg = socket.recv_string()
            print(f"Received a new message: {msg} ")
            exec_command(msg)
        except KeyboardInterrupt:
            print("Ending Communication and Streaming")
            process.terminate()
            socket.close()

if __name__ == "__main__":
    process = subprocess.Popen(["bash", "communication/video_stream.sh"])
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{SERVER_IP}:5555")  # Laptop is publisher
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    main()