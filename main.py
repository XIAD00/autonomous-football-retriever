# =========================================================
# AUTONOMOUS FOOTBALL RETRIEVER - MAIN CONTROLLER
# Brain of the robot system (Vision + Logic + Embedded)
# =========================================================

import time

# ---------------- MODULES ----------------
from software.vision.detector import BallDetector
from software.logic.mapper import CoordinateMapper
from embedded.serial_link import SerialLink


# ================= SYSTEM CORE =================
class RobotSystem:
    def __init__(self):

        print("[INIT] Starting Autonomous Football Retriever...")

        # Vision (camera + YOLO/OpenCV)
        self.detector = BallDetector()

        # Logic (convert image coords → robot coords)
        self.mapper = CoordinateMapper()

        # Embedded communication (Arduino/Raspberry Pi serial)
        self.robot = SerialLink(port="/dev/ttyUSB0", baudrate=9600)

        self.running = True

        print("[OK] System initialized successfully")


# ================= MAIN LOOP =================
    def run(self):

        print("[RUN] System is now active")

        while self.running:

            # 1. Detect ball from camera
            detection = self.detector.get_ball()

            if detection is not None:

                # 2. Convert vision data to robot coordinates
                x, y = self.mapper.convert(detection)

                # 3. Send command to robot
                self.robot.send(f"{x},{y}")

                print(f"[BALL] Sent position → X:{x} Y:{y}")

            else:
                # No ball detected signal
                self.robot.send("16")
                print("[INFO] No ball detected")

            time.sleep(0.05)  # control loop speed (~20 FPS)


# ================= SAFETY STOP =================
    def stop(self):
        print("[STOP] Shutting down system...")
        self.running = False
        self.robot.close()


# ================= ENTRY POINT =================
if __name__ == "__main__":

    robot = RobotSystem()

    try:
        robot.run()

    except KeyboardInterrupt:
        robot.stop()