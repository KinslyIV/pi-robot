import subprocess

import zmq
from zmq import ZMQError

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
            socket.close()
            process.terminate()
            exit(0)
        except ZMQError as e:
            print("ZMQ Error: ", e)
            socket.close()
            process.terminate()
            exit(0)

if __name__ == "__main__":
    process = subprocess.Popen(["bash", "communication/video_stream.sh"])
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.CONFLATE, 1)
    socket.connect(f"tcp://{SERVER_IP}:5555")  # Laptop is publisher
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    main()