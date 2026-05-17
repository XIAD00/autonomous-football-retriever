import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
import time


class BallDetector:
    def __init__(self, model_path="best.pt", use_pi_camera=False):

        print("[VISION] Loading model...")

        self.model = YOLO(model_path)

        self.cap = VideoStream(usePiCamera=use_pi_camera).start()
        time.sleep(2)

        print("[VISION] Camera ready")

    def get_ball(self):

        frame = self.cap.read()

        if frame is None:
            return None

        results = self.model(frame, verbose=False)[0]

        h, w, _ = frame.shape

        for box in results.boxes:

            cls = int(box.cls[0])

            # class 0 = ball (adjust if needed)
            if cls == 0:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                return {
                    "center": (cx, cy),
                    "frame_size": (w, h)
                }

        return None
