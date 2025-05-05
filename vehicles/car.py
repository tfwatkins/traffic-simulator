import pygame
from math import hypot

CAR_WIDTH = 10
CAR_LENGTH = 20

class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0

    def update(self, city=None, cars=None, pixel_coords_func=None):
        if self.index >= len(self.path) - 1:
            return  # Reached destination

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        # Check light (only at segment start)
        if self.t == 0.0 and city:
            intersection = city.intersections[current_node]
            if intersection.has_light and not intersection.is_green:
                return  # Red light

        # Queuing: Check car ahead
        if cars and pixel_coords_func:
            my_pos = self.get_position(pixel_coords_func)
            next_pos = pixel_coords_func(next_node)
            dir_x = next_pos[0] - my_pos[0]
            dir_y = next_pos[1] - my_pos[1]

            axis = 'x' if abs(dir_x) > abs(dir_y) else 'y'
            gap = CAR_LENGTH + 5

            for other in cars:
                if other is self:
                    continue
                other_pos = other.get_position(pixel_coords_func)

                if axis == 'x' and abs(my_pos[1] - other_pos[1]) < CAR_WIDTH:
                    if 0 < other_pos[0] - my_pos[0] < gap:
                        return
                elif axis == 'y' and abs(my_pos[0] - other_pos[0]) < CAR_WIDTH:
                    if 0 < other_pos[1] - my_pos[1] < gap:
                        return

        # Move forward toward the next node
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
