import cv2
from obstacle_detection import detect_obstacles
from navigation import decide_movement

def start_camera():

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_height, frame_width, _ = frame.shape

        detections = detect_obstacles(frame)

        move = decide_movement(detections, frame_width)

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