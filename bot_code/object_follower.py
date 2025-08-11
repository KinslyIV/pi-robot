import zmq
import cv2
from ultralytics import YOLO
from bot_code.constants import (FORWARD, BACKWARD, TURN_RIGHT, TURN_LEFT, CHANGE_SPEED, TURN_ROUND,
                                STOP, STOP_TURN_LEFT, STOP_TURN_RIGHT, ACCELERATE, CLEANUP)

YOLO_MODEL_PATH = "yolov10n.pt"    # or your trained model
TARGET_CLASS = "bottle"               # None = first detected object, or set class name like "person"


# GStreamer pipeline (Raspberry Pi sending H264 to laptop)
GST_PIPELINE = "udpsrc port=5000     ! h264parse ! openh264dec ! videoconvert ! autovideosink sync=false"


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
        send_command(0, 0)  # stop if no object
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
        send_command(0, STOP)
        return

    # Get bounding box center
    x1, y1, x2, y2 = target.xyxy[0]
    center_x = (x1 + x2) / 2
    frame_center = frame.shape[1] / 2

    # Control: proportional steering
    offset = center_x - frame_center
    offset_norm = offset / frame_center  # -1 (left) to 1 (right)

    if abs(offset_norm) < 0.1:
        # Go straight
        send_command(70, FORWARD)
    elif offset_norm < 0:
        # Turn left
        send_command(70, TURN_LEFT)
    else:
        # Turn right
        send_command(70, TURN_RIGHT)


def main():

    cap = cv2.VideoCapture(GST_PIPELINE, cv2.CAP_GSTREAMER)
    # cap = cv2.VideoCapture("/home/immata/Downloads/my_vid.mp4")
    if not cap.isOpened():
        print("Error: Cannot open GStreamer pipeline.")
        return

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

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    main()
