from ultralytics import YOLO
import cv2

# Load model once
model = YOLO("yolov8n.pt")

OBSTACLE_CLASSES = {
    "person",
    "chair",
    "car",
    "truck",
    "bus",
    "motorcycle",
    "bicycle",
    "dog",
    "cat",
    "backpack",
    "suitcase",
    "bench",
    "potted plant",
}

CONFIDENCE_THRESHOLD = 0.5

def detect_obstacles(frame):
    results = model(frame, verbose=False)

    detections = []

    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue
            
            class_id = int(box.cls[0])
            label = model.names[class_id]

            if label not in OBSTACLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1
            area = width * height

            # Rough proximity estimate based on bounding-box area
            if area < 20000:
                proximity = "FAR"
            elif area < 50000:
                proximity = "MEDIUM"
            else:
                proximity = "CLOSE"

            detections.append({
                "label": label,
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2),
                "area": area,
                "proximity": proximity,
            })

    return detections