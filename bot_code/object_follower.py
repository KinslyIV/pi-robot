import time

import zmq
import cv2
from ultralytics import YOLO
from bot_code.constants import (FORWARD, BACKWARD, TURN_RIGHT, TURN_LEFT, CHANGE_SPEED, TURN_ROUND,
                                STOP, STOP_TURN_LEFT, STOP_TURN_RIGHT, ACCELERATE, CLEANUP)

YOLO_MODEL_PATH = "yolo12n.pt"    # or your trained model
TARGET_CLASS = "bottle"               # None = first detected object, or set class name like "person"


# GStreamer pipeline (Raspberry Pi sending H264 to laptop)
GST_PIPELINE = (
    "udpsrc port=5000     ! h264parse ! openh264dec ! videoconvert ! appsink")


def send_command(speed, command : str):
    """Send motor command as JSON to robot."""
    message = {
            "command": command,
            "speed": speed,
            "duration": 0
        }
    socket.send_json(message)
    print("Sent:", message)

# =========================
# YOLO SETUP
# =========================
model = YOLO(YOLO_MODEL_PATH)

def follow_object(frame, detections):

    if len(detections) == 0:
        send_command(1, STOP)  # stop if no object
        return

    # Pick first detection or specific class
    target = None
    for det in detections:
        cls_name = model.names[int(det.cls)]
        # print(f"Detected {cls_name}")
        if TARGET_CLASS is None or cls_name == TARGET_CLASS:
            target = det
            break
    if target is None:
        send_command(1, STOP)
        return

    print("Target Class:", model.names[int(target.cls)])
    # Get bounding box center
    x1, y1, x2, y2 = target.xyxy[0]
    center_x = (x1 + x2) / 2
    frame_center = frame.shape[1] / 2

    # Control: proportional steering
    offset = center_x - frame_center
    offset_norm = offset / frame_center  # -1 (left) to 1 (right)
    approx_dist = (y2 - y1) / frame.shape[0]

    # Dynamic turn threshold (min 0.05, max 0.2)
    turn_threshold = max(0.2, (1 - approx_dist))
    turn_speed = int(60 + 20 * abs(offset_norm))

    # print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
    print(f"height: {y2 - y1}, width: {x2 - x1}")
    print(f"center_x: {center_x} frame_center: {frame_center}")
    print(f"offset_norm: {offset_norm} offset: {offset}")
    print(f"approx_dist: {approx_dist} turn_threshold: {turn_threshold}")
    print(f"turn_speed: {turn_speed}")

    if approx_dist > 0.9:
        # Object too close
        send_command(0, STOP)
    elif abs(offset_norm) < turn_threshold:
        # Go straight
        send_command(70, FORWARD)
    elif offset_norm < 0:
        # Turn left
        send_command(turn_speed, TURN_LEFT)
    else:
        # Turn right
        send_command(turn_speed, TURN_RIGHT)


def main():

    cap = cv2.VideoCapture(GST_PIPELINE, cv2.CAP_GSTREAMER)
    # cap = cv2.VideoCapture("/home/immata/Downloads/my_vid.mp4")
    if not cap.isOpened():
        print("Error: Cannot open GStreamer pipeline.")
        exit(1)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLO inference
            results = model(frame)
            follow_object(frame, results[0].boxes)

            # OPTIONAL: visualize
            annotated = results[0].plot()
            cv2.imshow("Object Follower", annotated)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
                break

    except KeyboardInterrupt:
        message = {
            "command": CLEANUP,
            "speed": 0,
            "duration": 0
        }
        socket.send_json(message)
        print("Ending Communication...")
        socket.close()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    main()
