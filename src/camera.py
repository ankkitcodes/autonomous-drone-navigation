import cv2
import numpy as np

from obstacle_detection import detect_obstacles
from navigation import decide_movement
from drone_controller import Drone


def start_camera():

    cap = cv2.VideoCapture(0)
    drone = Drone()

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        frame_height, frame_width, _ = frame.shape

        # -----------------------------
        # 1. YOLO obstacle detection
        # -----------------------------
        detections = detect_obstacles(frame)

        # Select the most significant obstacle
        obstacle = None

        if detections:
            obstacle = max(
                detections,
                key=lambda d: d["area"]
            )
        # -----------------------------
        # 2. Navigation decision
        # -----------------------------
        move = decide_movement(
            detections,
            frame_width
        )

        # -----------------------------
        # 3. Move simulated drone
        # -----------------------------
        drone.move(move)

        drone_x, drone_y = drone.get_position()

        # -----------------------------
        # 4. Create simulation canvas
        # -----------------------------
        sim_width = 500
        sim_height = 500

        sim_obstacle = None

        if obstacle:

            x1, y1, x2, y2 = obstacle["bbox"]

            sim_x1 = int(x1 / frame_width * sim_width)
            sim_y1 = int(y1 / frame_height * sim_height)

            sim_x2 = int(x2 / frame_width * sim_width)
            sim_y2 = int(y2 / frame_height * sim_height)

            sim_obstacle = (
                sim_x1,
                sim_y1,
                sim_x2,
                sim_y2
            )
        
        sim = np.ones(
            (500, 500, 3),
            dtype=np.uint8
        ) * 255


        if sim_obstacle:

            x1, y1, x2, y2 = sim_obstacle

            cv2.rectangle(
                sim,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                sim,
                obstacle["label"],
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )
        # Draw drone
        cv2.circle(
            sim,
            (drone_x, drone_y),
            10,
            (0, 0, 255),
            -1
        )

        # Display movement command
        cv2.putText(
            sim,
            f"Move: {move}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2
        )

        cv2.imshow(
            "Drone Simulation",
            sim
        )

        # -----------------------------
        # 5. Display camera + YOLO
        # -----------------------------

        cv2.putText(
            frame,
            f"MOVE: {move}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Draw YOLO detections
        for det in detections:

            x1, y1, x2, y2 = det["bbox"]
            label = det["label"]
            conf = det["confidence"]
            proximity = det["proximity"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{label} {conf:.2f} {proximity}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        # Draw navigation zones
        cv2.line(
            frame,
            (frame_width // 3, 0),
            (frame_width // 3, frame_height),
            (255, 0, 0),
            2
        )

        cv2.line(
            frame,
            (2 * frame_width // 3, 0),
            (2 * frame_width // 3, frame_height),
            (255, 0, 0),
            2
        )

        cv2.imshow(
            "Drone Camera - YOLO",
            frame
        )

        # Quit with Q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()