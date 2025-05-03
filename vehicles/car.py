class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0

    def update(self, city=None):
        if self.index >= len(self.path) - 1:
            return  # Reached destination

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        # Only check the light when starting to move to next segment
        if self.t == 0.0 and city:
            intersection = city.intersections[current_node]
            if not intersection.is_green:
                return  # Stop at red light

        # Move forward toward the next node
        self.t += self.speed * 0.02
        if self.t >= 1.0:
            self.t = 0.0
            self.index += 1  # Proceed to the next segment

        

    def get_position(self, pixel_coords_func):
        if self.index >= len(self.path) - 1:
            return pixel_coords_func(self.path[-1])

        p1 = pixel_coords_func(self.path[self.index])
        p2 = pixel_coords_func(self.path[self.index + 1])

        x = p1[0] + (p2[0] - p1[0]) * self.t
        y = p1[1] + (p2[1] - p1[1]) * self.t
        return (x, y)
