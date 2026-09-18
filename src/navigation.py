def decide_movement(detections, frame_width):

    if not detections:
        return "FORWARD"

    # Select the largest detected obstacle
    obstacle = max(
        detections,
        key=lambda d: d["area"]
    )

    x1, y1, x2, y2 = obstacle["bbox"]

    center_x = (x1 + x2) // 2

    left_boundary = frame_width // 3
    right_boundary = 2 * frame_width // 3

    proximity = obstacle["proximity"]

    # Far obstacle → continue forward
    if proximity == "FAR":
        return "FORWARD"

    # Medium obstacle → begin avoiding
    if proximity == "MEDIUM":

        if center_x < left_boundary:
            return "RIGHT"

        elif center_x > right_boundary:
            return "LEFT"

        else:
            return "STOP"

    # Close obstacle → immediate avoidance
    if proximity == "CLOSE":

        if center_x < left_boundary:
            return "RIGHT"

        elif center_x > right_boundary:
            return "LEFT"

        else:
            return "BACKWARD"

    return "STOP"