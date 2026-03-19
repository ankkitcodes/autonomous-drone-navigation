class Drone:

    def __init__(self):
        self.x = 250
        self.y = 250
        self.speed = 10

    def move(self, direction):

        if direction == "FORWARD":
            self.y -= self.speed

        elif direction == "BACKWARD":
            self.y += self.speed

        elif direction == "LEFT":
            self.x -= self.speed

        elif direction == "RIGHT":
            self.x += self.speed

        elif direction == "STOP":
            pass

        # Keep drone within boundaries
        self.x = max(0, min(500, self.x))
        self.y = max(0, min(500, self.y))

    def get_position(self):
        return self.x, self.y