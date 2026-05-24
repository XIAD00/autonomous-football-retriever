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
        best_ball = None
        best_conf = 0

        for box in results.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0 and conf > 0.5:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if conf > best_conf:
                best_conf = conf
                best_ball = {
                "center": (cx, cy),
                 "frame_size": (w, h),
                 "confidence": conf
                  }

        return best_ball
    
    def stop(self):
        self.cap.stop()