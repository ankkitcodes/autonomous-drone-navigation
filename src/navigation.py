def decide_movement(detections, frame_width):

    if not detections:
        return "FORWARD"

    # choose biggest box (closest object)
    largest = max(detections, key=lambda d: (d["bbox"][2]-d["bbox"][0]) * (d["bbox"][3]-d["bbox"][1]))

    x1, y1, x2, y2 = largest["bbox"]
    center = (x1 + x2) // 2

    # Safety distance check
    area = (x2 - x1) * (y2 - y1)
    if area > 50000:
        return "BACKWARD"

    left_zone = frame_width // 3
    right_zone = 2 * frame_width // 3

    if center < left_zone:
        return "RIGHT"
    elif center > right_zone:
        return "LEFT"
    else:
        return "STOP"