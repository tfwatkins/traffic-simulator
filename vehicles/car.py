# vehicles/car.py

import pygame
from math import sqrt

CELL_SIZE = 100
CAR_WIDTH = 10
CAR_LENGTH = 20
AVOID_RADIUS = 30  # adjust as needed

class Car:
    def __init__(self, path, speed=2):
        self.path = path
        self.speed = speed
        self.index = 0
        self.t = 0.0
        self.is_done = False  # <-- flag used to exclude parked cars from blocking

    def update(self, city=None, cars=None, pixel_coords_func=None, quadtree=None):
        if self.index >= len(self.path) - 1:
            self.is_done = True
            return  # Reached destination

        current_node = self.path[self.index]
        next_node = self.path[self.index + 1]

        if self.t == 0.0 and city:
            intersection = city.intersections[current_node]
            if intersection.has_light and not intersection.is_green:
                return  # Stop at red light

        # Check quadtree for blockage ahead
        if quadtree and self._is_blocked(quadtree, current_node, next_node, pixel_coords_func):
            return

        # Move forward
        self.t += self.speed * 0.02
        if self.t >= 1.0:
            self.t = 0.0
            self.index += 1

    def _is_blocked(self, quadtree, current_node, next_node, pixel_coords_func):
        x1, y1 = pixel_coords_func(current_node)
        x2, y2 = pixel_coords_func(next_node)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        neighbors = quadtree.query_range((mid_x, mid_y, AVOID_RADIUS, AVOID_RADIUS))
        for car in neighbors:
            if car is not self and not car.is_done:
                cx, cy = car.get_position(pixel_coords_func)
                if sqrt((cx - mid_x)**2 + (cy - mid_y)**2) < AVOID_RADIUS:
                    return True
        return False

    def get_position(self, pixel_coords_func):
        if self.index >= len(self.path) - 1:
            return pixel_coords_func(self.path[-1])

        p1 = pixel_coords_func(self.path[self.index])
        p2 = pixel_coords_func(self.path[self.index + 1])

        x = p1[0] + (p2[0] - p1[0]) * self.t
        y = p1[1] + (p2[1] - p1[1]) * self.t
        return (x, y)
