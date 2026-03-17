from ultralytics import YOLO
import cv2

# Load model once
model = YOLO("yolov8n.pt")

def detect_obstacles(frame):
    results = model(frame)

    detections = []

    for result in results:
        boxes = result.boxes

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            label = model.names[cls]

            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": (x1, y1, x2, y2)
            })

    return detections