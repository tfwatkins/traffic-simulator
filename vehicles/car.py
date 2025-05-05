# vehicles/car.py

import pygame

CELL_SIZE = 100
CAR_WIDTH = 10
CAR_LENGTH = 20
CAR_COLOR = (255, 100, 100)
GAP_DISTANCE = 25  # Pixels between cars

class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0
        self.stopped = False

    def update(self, city=None, cars=None, pixel_coords_func=None):
        if self.index >= len(self.path) - 1:
            return  # Reached destination

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        # Stop at red light
        if self.t == 0.0 and city:
            intersection = city.intersections[current_node]
            if not intersection.is_green:
                self.stopped = True
                return
            else:
                self.stopped = False

        # Check distance to car ahead
        if cars and pixel_coords_func:
            my_pos = self.get_position(pixel_coords_func)
            for other in cars:
                if other is self or other.index < self.index:
                    continue
                other_pos = other.get_position(pixel_coords_func)
                dist = ((my_pos[0] - other_pos[0]) ** 2 + (my_pos[1] - other_pos[1]) ** 2) ** 0.5
                if dist < GAP_DISTANCE:
                    self.stopped = True
                    return
        self.stopped = False

        # Move forward
        self.t += self.speed * 0.02
        if self.t >= 1.0:
            self.t = 0.0
            self.index += 1

    def get_position(self, pixel_coords_func):
        if self.index >= len(self.path) - 1:
            return pixel_coords_func(self.path[-1])

        p1 = pixel_coords_func(self.path[self.index])
        p2 = pixel_coords_func(self.path[self.index + 1])

        x = p1[0] + (p2[0] - p1[0]) * self.t
        y = p1[1] + (p2[1] - p1[1]) * self.t
        return (x, y)
