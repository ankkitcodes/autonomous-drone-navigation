import cv2
import numpy as np
from obstacle_detection import detect_obstacles
from navigation import decide_movement
from drone_controller import Drone

def start_camera():

    cap = cv2.VideoCapture(0)
    drone = Drone()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_height, frame_width, _ = frame.shape

        detections = detect_obstacles(frame)

        move = decide_movement(detections, frame_width)

        drone.move(move)
        x, y = drone.get_position()

        # Create simulation canvas
        sim = 255 * np.ones((500, 500, 3), dtype=np.uint8)

        # Draw obstacles
        cv2.rectangle(sim, (200,200), (300,300), (0,255,0), -1)

        # Draw drone
        cv2.circle(sim, (x, y), 10, (0, 0, 255), -1)

        cv2.putText(sim, f"Move: {move}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,0,0),
                    2)

        cv2.imshow("Drone Simulation", sim)

        # Show movement decision
        cv2.putText(frame, f"MOVE: {move}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)

        # Draw detections
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            label = det["label"]
            conf = det["confidence"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0,255,0),
                        2)

        # Draw region lines
        cv2.line(frame, (frame_width//3, 0), (frame_width//3, frame_height), (255,0,0), 2)
        cv2.line(frame, (2*frame_width//3, 0), (2*frame_width//3, frame_height), (255,0,0), 2)

        cv2.imshow("Drone Camera - YOLO", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()